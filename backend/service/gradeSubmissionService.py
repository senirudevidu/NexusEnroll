from backend.dal.gradeSubmission import GradeSubmission
from backend.dal.course import Course
from datetime import datetime


class GradeSubmissionService:
    def __init__(self, db):
        self.db = db
        self.grade_submission = GradeSubmission(self.db)
        self.course = Course(self.db)

    def get_course_for_grading(self, faculty_id, course_id):
        """Get course enrollments for grade submission"""
        conn = self.db.get_db_connection()
        cursor = conn.cursor()

        try:
            result = self.grade_submission.get_course_enrollments_for_grading(cursor, faculty_id, course_id)
            return result
        except Exception as e:
            return {"status": "Error", "message": str(e)}
        finally:
            cursor.close()
            conn.close()

    def submit_batch_grades(self, faculty_id, course_id, grade_submissions):
        """Submit multiple grades at once with individual validation"""
        conn = self.db.get_db_connection()
        cursor = conn.cursor()

        try:
            # First verify course access
            verification_result = self.grade_submission.get_course_enrollments_for_grading(cursor, faculty_id, course_id)
            if verification_result["status"] == "Error":
                return verification_result

            # Process batch submission
            result = self.grade_submission.batch_submit_grades(cursor, conn, grade_submissions)
            
            # Add course information to result
            result["course_id"] = course_id
            result["course_name"] = verification_result["course_info"]["course_name"]
            result["instructor"] = verification_result["course_info"]["instructor"]
            result["timestamp"] = datetime.now().isoformat()
            
            return result

        except Exception as e:
            conn.rollback()
            return {"status": "Error", "message": str(e)}
        finally:
            cursor.close()
            conn.close()

    def update_single_grade(self, faculty_id, enrollment_id, new_grade):
        """Update a single pending grade"""
        conn = self.db.get_db_connection()
        cursor = conn.cursor()

        try:
            # Verify faculty has access to this enrollment
            access_query = """
            SELECT e.enrollment_id, c.course_id, c.courseName
            FROM Enrollment e
            JOIN Course c ON e.course_id = c.course_id
            WHERE e.enrollment_id = %s AND c.facultyMem_Id = %s AND e.enrollmentStatus = 'Active'
            """
            cursor.execute(access_query, (enrollment_id, faculty_id))
            access_check = cursor.fetchone()
            
            if not access_check:
                return {"status": "Error", "message": "Enrollment not found or access denied"}

            # Update the grade
            result = self.grade_submission.update_pending_grade(cursor, conn, enrollment_id, new_grade)
            
            if result["status"] == "Success":
                result["course_id"] = access_check[1]
                result["course_name"] = access_check[2]
                result["enrollment_id"] = enrollment_id
                result["updated_grade"] = new_grade
                result["timestamp"] = datetime.now().isoformat()

            return result

        except Exception as e:
            conn.rollback()
            return {"status": "Error", "message": str(e)}
        finally:
            cursor.close()
            conn.close()

    def finalize_all_grades(self, faculty_id, course_id):
        """Finalize all pending grades for a course"""
        conn = self.db.get_db_connection()
        cursor = conn.cursor()

        try:
            result = self.grade_submission.finalize_course_grades(cursor, conn, faculty_id, course_id)
            
            if result["status"] == "Success":
                result["course_id"] = course_id
                result["timestamp"] = datetime.now().isoformat()
                
                # Log the finalization for audit purposes
                self._log_grade_finalization(cursor, conn, faculty_id, course_id, result["finalized_count"])

            return result

        except Exception as e:
            conn.rollback()
            return {"status": "Error", "message": str(e)}
        finally:
            cursor.close()
            conn.close()

    def get_grading_summary(self, faculty_id, course_id):
        """Get detailed summary of grade submission status"""
        conn = self.db.get_db_connection()
        cursor = conn.cursor()

        try:
            result = self.grade_submission.get_grade_submission_summary(cursor, faculty_id, course_id)
            
            if result["status"] == "Success":
                # Add additional useful information
                summary = result["summary"]
                
                # Calculate completion percentage
                total_students = summary["total_students"]
                pending_count = summary["status_breakdown"].get("Pending", 0)
                submitted_count = summary["status_breakdown"].get("Submitted", 0)
                in_progress_count = summary["status_breakdown"].get("In Progress", 0)
                
                summary["completion_stats"] = {
                    "total_students": total_students,
                    "pending_grades": pending_count,
                    "submitted_grades": submitted_count,
                    "ungraded": in_progress_count,
                    "completion_percentage": round((submitted_count / total_students * 100), 2) if total_students > 0 else 0,
                    "pending_percentage": round((pending_count / total_students * 100), 2) if total_students > 0 else 0
                }
                
                # Group grade details by status for easier frontend handling
                summary["students_by_status"] = {
                    "pending": [],
                    "submitted": [],
                    "in_progress": []
                }
                
                for student in summary["grade_details"]:
                    student_info = {
                        "enrollment_id": student[0],
                        "student_id": student[1],
                        "name": f"{student[2]} {student[3]}",
                        "grade": student[4],
                        "mark_status": student[5],
                        "last_updated": student[6].isoformat() if student[6] else None
                    }
                    
                    if student[5] == "Pending":
                        summary["students_by_status"]["pending"].append(student_info)
                    elif student[5] == "Submitted":
                        summary["students_by_status"]["submitted"].append(student_info)
                    else:
                        summary["students_by_status"]["in_progress"].append(student_info)

            return result

        except Exception as e:
            return {"status": "Error", "message": str(e)}
        finally:
            cursor.close()
            conn.close()

    def validate_grade_format(self, grade):
        """Validate grade format without database interaction"""
        return self.grade_submission.validate_grade(grade)

    def get_faculty_courses_with_grading_status(self, faculty_id):
        """Get faculty courses with grading status information"""
        conn = self.db.get_db_connection()
        cursor = conn.cursor()

        try:
            # Get faculty courses with grading statistics
            query = """
            SELECT 
                c.course_id,
                c.courseName,
                c.description,
                COUNT(e.enrollment_id) as total_students,
                SUM(CASE WHEN e.markStatus = 'Pending' THEN 1 ELSE 0 END) as pending_grades,
                SUM(CASE WHEN e.markStatus = 'Submitted' THEN 1 ELSE 0 END) as submitted_grades,
                SUM(CASE WHEN e.markStatus = 'In Progress' THEN 1 ELSE 0 END) as ungraded
            FROM Course c
            LEFT JOIN Enrollment e ON c.course_id = e.course_id AND e.enrollmentStatus = 'Active'
            WHERE c.facultyMem_Id = %s
            GROUP BY c.course_id, c.courseName, c.description
            ORDER BY c.courseName
            """
            cursor.execute(query, (faculty_id,))
            courses = cursor.fetchall()
            
            # Format the results
            formatted_courses = []
            for course in courses:
                course_data = {
                    "course_id": course[0],
                    "course_name": course[1],
                    "description": course[2],
                    "total_students": course[3] or 0,
                    "pending_grades": course[4] or 0,
                    "submitted_grades": course[5] or 0,
                    "ungraded": course[6] or 0,
                    "completion_percentage": round((course[5] or 0) / (course[3] or 1) * 100, 2) if course[3] and course[3] > 0 else 0
                }
                formatted_courses.append(course_data)
            
            return {"status": "Success", "courses": formatted_courses}

        except Exception as e:
            return {"status": "Error", "message": str(e)}
        finally:
            cursor.close()
            conn.close()

    def _log_grade_finalization(self, cursor, conn, faculty_id, course_id, count):
        """Log grade finalization for audit purposes (optional)"""
        try:
            # This could be expanded to create an audit log table
            log_query = """
            INSERT INTO GradeAuditLog (faculty_id, course_id, action, grade_count, timestamp)
            VALUES (%s, %s, 'FINALIZE_GRADES', %s, CURRENT_TIMESTAMP)
            """
            # Only execute if audit table exists
            # cursor.execute(log_query, (faculty_id, course_id, count))
            pass
        except:
            # Ignore audit logging errors
            pass
