class GradeSubmission:
    def __init__(self, db):
        self.db = db

    def get_course_enrollments_for_grading(self, cursor, faculty_id, course_id):
        """Get all active enrollments for a course for grade submission"""
        # First verify that the faculty member teaches this course
        verification_query = """
        SELECT c.course_id, c.courseName, 
               CONCAT(u.firstName, ' ', u.lastName) as instructor_name
        FROM Course c
        JOIN Users u ON c.facultyMem_Id = u.user_id
        WHERE c.course_id = %s AND c.facultyMem_Id = %s
        """
        cursor.execute(verification_query, (course_id, faculty_id))
        course_info = cursor.fetchone()
        
        if not course_info:
            return {"status": "Error", "message": "Course not found or access denied"}
        
        # Get enrolled students for grading
        grades_query = """
        SELECT 
            e.enrollment_id,
            e.student_id,
            u.firstName,
            u.lastName,
            u.email,
            e.markStatus,
            e.marks,
            e.lastUpdated
        FROM Enrollment e
        JOIN Student s ON e.student_id = s.student_Id
        JOIN Users u ON s.student_Id = u.user_id
        WHERE e.course_id = %s AND e.enrollmentStatus = 'Active'
        ORDER BY u.lastName, u.firstName
        """
        cursor.execute(grades_query, (course_id,))
        students = cursor.fetchall()
        
        return {
            "status": "Success",
            "course_info": {
                "course_id": course_info[0],
                "course_name": course_info[1],
                "instructor": course_info[2]
            },
            "students": students
        }

    def validate_grade(self, grade_value):
        """Validate grade format and value"""
        if grade_value is None or grade_value == "":
            return {"valid": False, "message": "Grade cannot be empty"}
        
        # Convert to string for validation
        grade_str = str(grade_value).strip().upper()
        
        # Check for letter grades
        if grade_str in ['A', 'B', 'C', 'D', 'F']:
            return {"valid": True, "normalized_grade": grade_str}
        
        # Check for numeric grades (0-100)
        try:
            numeric_grade = float(grade_str)
            if 0 <= numeric_grade <= 100:
                return {"valid": True, "normalized_grade": str(numeric_grade)}
            else:
                return {"valid": False, "message": "Numeric grade must be between 0 and 100"}
        except ValueError:
            return {"valid": False, "message": "Invalid grade format. Use A-F or 0-100"}

    def submit_single_grade(self, cursor, conn, enrollment_id, grade, mark_status="Pending"):
        """Submit a single grade with validation"""
        try:
            # Validate the grade
            validation = self.validate_grade(grade)
            if not validation["valid"]:
                return {"status": "Error", "message": validation["message"]}
            
            # Check if enrollment exists and is active
            check_query = """
            SELECT enrollment_id, markStatus FROM Enrollment 
            WHERE enrollment_id = %s AND enrollmentStatus = 'Active'
            """
            cursor.execute(check_query, (enrollment_id,))
            enrollment = cursor.fetchone()
            
            if not enrollment:
                return {"status": "Error", "message": "Enrollment not found or inactive"}
            
            # Check if already submitted (not pending)
            current_mark_status = enrollment[1]
            if current_mark_status == "Submitted":
                return {"status": "Error", "message": "Grade already submitted and locked"}
            
            # Update the grade
            update_query = """
            UPDATE Enrollment 
            SET marks = %s, markStatus = %s, lastUpdated = CURRENT_TIMESTAMP 
            WHERE enrollment_id = %s
            """
            cursor.execute(update_query, (validation["normalized_grade"], mark_status, enrollment_id))
            
            return {"status": "Success", "message": "Grade updated successfully"}
            
        except Exception as e:
            return {"status": "Error", "message": str(e)}

    def batch_submit_grades(self, cursor, conn, grade_submissions):
        """Submit multiple grades in batch with individual validation"""
        results = []
        successful_submissions = []
        
        for submission in grade_submissions:
            enrollment_id = submission.get("enrollment_id")
            grade = submission.get("grade")
            
            if not enrollment_id:
                results.append({
                    "enrollment_id": enrollment_id,
                    "status": "Error",
                    "message": "Missing enrollment_id"
                })
                continue
            
            # Submit individual grade
            result = self.submit_single_grade(cursor, conn, enrollment_id, grade, "Pending")
            result["enrollment_id"] = enrollment_id
            results.append(result)
            
            if result["status"] == "Success":
                successful_submissions.append(enrollment_id)
        
        # Commit only if at least one grade was successfully processed
        if successful_submissions:
            conn.commit()
        
        return {
            "status": "Completed" if successful_submissions else "Error",
            "total_submitted": len(grade_submissions),
            "successful": len(successful_submissions),
            "failed": len(grade_submissions) - len(successful_submissions),
            "results": results
        }

    def update_pending_grade(self, cursor, conn, enrollment_id, new_grade):
        """Update a pending grade"""
        try:
            # Validate the new grade
            validation = self.validate_grade(new_grade)
            if not validation["valid"]:
                return {"status": "Error", "message": validation["message"]}
            
            # Check if enrollment exists and is pending
            check_query = """
            SELECT enrollment_id, markStatus FROM Enrollment 
            WHERE enrollment_id = %s AND enrollmentStatus = 'Active'
            """
            cursor.execute(check_query, (enrollment_id,))
            enrollment = cursor.fetchone()
            
            if not enrollment:
                return {"status": "Error", "message": "Enrollment not found or inactive"}
            
            current_mark_status = enrollment[1]
            if current_mark_status == "Submitted":
                return {"status": "Error", "message": "Cannot update submitted grade"}
            
            # Update the grade
            update_query = """
            UPDATE Enrollment 
            SET marks = %s, lastUpdated = CURRENT_TIMESTAMP 
            WHERE enrollment_id = %s AND markStatus = 'Pending'
            """
            cursor.execute(update_query, (validation["normalized_grade"], enrollment_id))
            
            if cursor.rowcount == 0:
                return {"status": "Error", "message": "No pending grade found to update"}
            
            conn.commit()
            return {"status": "Success", "message": "Grade updated successfully"}
            
        except Exception as e:
            conn.rollback()
            return {"status": "Error", "message": str(e)}

    def finalize_course_grades(self, cursor, conn, faculty_id, course_id):
        """Finalize all pending grades for a course (change status from Pending to Submitted)"""
        try:
            # First verify that the faculty member teaches this course
            verification_query = """
            SELECT c.course_id FROM Course c
            WHERE c.course_id = %s AND c.facultyMem_Id = %s
            """
            cursor.execute(verification_query, (course_id, faculty_id))
            if not cursor.fetchone():
                return {"status": "Error", "message": "Course not found or access denied"}
            
            # Get pending grades count
            count_query = """
            SELECT COUNT(*) FROM Enrollment 
            WHERE course_id = %s AND markStatus = 'Pending' AND enrollmentStatus = 'Active'
            """
            cursor.execute(count_query, (course_id,))
            pending_count = cursor.fetchone()[0]
            
            if pending_count == 0:
                return {"status": "Error", "message": "No pending grades found to finalize"}
            
            # Update all pending grades to submitted
            finalize_query = """
            UPDATE Enrollment 
            SET markStatus = 'Submitted', lastUpdated = CURRENT_TIMESTAMP 
            WHERE course_id = %s AND markStatus = 'Pending' AND enrollmentStatus = 'Active'
            """
            cursor.execute(finalize_query, (course_id,))
            
            finalized_count = cursor.rowcount
            conn.commit()
            
            return {
                "status": "Success", 
                "message": f"Finalized {finalized_count} grade(s)",
                "finalized_count": finalized_count
            }
            
        except Exception as e:
            conn.rollback()
            return {"status": "Error", "message": str(e)}

    def get_grade_submission_summary(self, cursor, faculty_id, course_id):
        """Get summary of grade submission status for a course"""
        try:
            # Verify course access
            verification_query = """
            SELECT c.course_id, c.courseName FROM Course c
            WHERE c.course_id = %s AND c.facultyMem_Id = %s
            """
            cursor.execute(verification_query, (course_id, faculty_id))
            course_info = cursor.fetchone()
            
            if not course_info:
                return {"status": "Error", "message": "Course not found or access denied"}
            
            # Get grade submission statistics
            summary_query = """
            SELECT 
                markStatus,
                COUNT(*) as count
            FROM Enrollment 
            WHERE course_id = %s AND enrollmentStatus = 'Active'
            GROUP BY markStatus
            """
            cursor.execute(summary_query, (course_id,))
            status_counts = cursor.fetchall()
            
            # Get detailed breakdown
            detail_query = """
            SELECT 
                e.enrollment_id,
                e.student_id,
                u.firstName,
                u.lastName,
                e.marks,
                e.markStatus,
                e.lastUpdated
            FROM Enrollment e
            JOIN Student s ON e.student_id = s.student_Id
            JOIN Users u ON s.student_Id = u.user_id
            WHERE e.course_id = %s AND e.enrollmentStatus = 'Active'
            ORDER BY e.markStatus, u.lastName, u.firstName
            """
            cursor.execute(detail_query, (course_id,))
            grade_details = cursor.fetchall()
            
            # Format summary
            summary = {
                "course_id": course_info[0],
                "course_name": course_info[1],
                "total_students": sum([count[1] for count in status_counts]),
                "status_breakdown": {status[0]: status[1] for status in status_counts},
                "grade_details": grade_details
            }
            
            return {"status": "Success", "summary": summary}
            
        except Exception as e:
            return {"status": "Error", "message": str(e)}
