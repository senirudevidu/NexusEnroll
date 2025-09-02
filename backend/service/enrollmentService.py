from backend.dal.enrollment import Enrollment
from backend.dal.course import Course
from backend.dal.user import Student
from backend.service.notificationService import NotificationManager
from datetime import datetime, time

class EnrollmentService:
    def __init__(self, db):
        self.db = db
        self.enrollment = Enrollment(self.db)
        self.course = Course(self.db)
        self.student = Student(self.db)
        # Initialize notification system using Observer pattern
        self.notification_manager = NotificationManager(self.db)

    def enroll_student_in_course(self, student_id, course_id):
        """Main enrollment method with all validation checks"""
        conn = self.db.get_db_connection()
        cursor = conn.cursor()

        try:
            # Step 1: Check if student is already enrolled in this course
            if self.enrollment.check_existing_enrollment(cursor, student_id, course_id):
                error_msg = "Student is already enrolled in this course"
                # Get course name for notification
                course_data = self.course.getCourseById(cursor, course_id)
                course_name = course_data[1] if course_data else "Unknown Course"
                self.notification_manager.notify_enrollment_failed(student_id, course_id, course_name, error_msg)
                return {"status": "Error", "message": error_msg}

            # Step 2: Check course capacity
            course_data = self.course.getCourseById(cursor, course_id)
            if not course_data:
                error_msg = "Course not found"
                self.notification_manager.notify_system_error("Course Lookup", error_msg, "Enrollment Service")
                return {"status": "Error", "message": error_msg}
            
            # course_data format: (course_id, courseName, description, capacity, availableSeats, credits, degree_ID, dept_Id, preReqYear, allowedDeptID, facultyMem_Id, addedBy)
            course_name = course_data[1]
            available_seats = course_data[4]
            if available_seats <= 0:
                error_msg = "Course is full. No available seats."
                self.notification_manager.notify_enrollment_failed(student_id, course_id, course_name, error_msg)
                return {"status": "Error", "message": error_msg}

            # Step 3: Check prerequisites (year requirement)
            prerequisite_year = course_data[8]
            student_year = self._get_student_year(cursor, student_id)
            
            if student_year < prerequisite_year:
                error_msg = f"Student must be in year {prerequisite_year} or higher to enroll in this course"
                self.notification_manager.notify_enrollment_failed(student_id, course_id, course_name, error_msg)
                return {"status": "Error", "message": error_msg}

            # Step 4: Check for time conflicts
            time_conflict = self._check_time_conflicts(cursor, student_id, course_id)
            if time_conflict:
                error_msg = f"Time conflict detected with course: {time_conflict}"
                self.notification_manager.notify_enrollment_failed(student_id, course_id, course_name, error_msg)
                return {"status": "Error", "message": error_msg}

            # Step 5: All validations passed, proceed with enrollment
            enrollment_result = self.enrollment.enroll_student(cursor, conn, student_id, course_id)
            
            if enrollment_result["status"] == "Success":
                # Update course capacity
                self.enrollment.update_course_capacity(cursor, conn, course_id, increment=False)
                
                # Trigger notification using Observer pattern
                course_name = course_data[1]  # courseName from course_data
                self.notification_manager.notify_enrollment_successful(student_id, course_id, course_name)
                
                # Check for capacity warnings
                if course_data[4] <= 3:  # If available seats <= 3
                    self.notification_manager.notify_capacity_warning(
                        course_id, course_name, course_data[4] - 1, course_data[3]
                    )
            else:
                # Notify about enrollment failure
                course_name = course_data[1]
                self.notification_manager.notify_enrollment_failed(
                    student_id, course_id, course_name, enrollment_result.get("message", "Unknown error")
                )
                
            return enrollment_result

        except Exception as e:
            conn.rollback()
            # Notify about system error
            self.notification_manager.notify_system_error(
                "Enrollment Exception", 
                str(e), 
                "Enrollment Service - enroll_student_in_course"
            )
            return {"status": "Error", "message": str(e)}
        finally:
            cursor.close()
            conn.close()

    def drop_student_from_course(self, enrollment_id):
        """Drop a student from a course"""
        conn = self.db.get_db_connection()
        cursor = conn.cursor()

        try:
            # Get enrollment details before dropping
            enrollment_data = self.enrollment.get_enrollment_by_id(cursor, enrollment_id)
            if not enrollment_data:
                return {"status": "Error", "message": "Enrollment not found"}

            course_id = enrollment_data[2]
            student_id = enrollment_data[1]
            course_name = enrollment_data[3]  # courseName from enrollment_data
            
            # Drop the enrollment
            drop_result = self.enrollment.drop_enrollment(cursor, conn, enrollment_id)
            
            if drop_result["status"] == "Success":
                # Update course capacity (increase available seats)
                self.enrollment.update_course_capacity(cursor, conn, course_id, increment=True)
                
                # Trigger notification using Observer pattern
                self.notification_manager.notify_course_dropped(student_id, course_id, course_name)
                
            return drop_result

        except Exception as e:
            conn.rollback()
            return {"status": "Error", "message": str(e)}
        finally:
            cursor.close()
            conn.close()

    def get_student_enrollments(self, student_id):
        """Get all active enrollments for a student"""
        conn = self.db.get_db_connection()
        cursor = conn.cursor()

        try:
            enrollments = self.enrollment.get_student_enrollments(cursor, student_id)
            return {"status": "Success", "data": enrollments}
        except Exception as e:
            return {"status": "Error", "message": str(e)}
        finally:
            cursor.close()
            conn.close()

    def get_enrollment_statistics(self, course_id=None):
        """Get enrollment statistics"""
        conn = self.db.get_db_connection()
        cursor = conn.cursor()

        try:
            statistics = self.enrollment.get_enrollment_statistics(cursor, course_id)
            return {"status": "Success", "data": statistics}
        except Exception as e:
            return {"status": "Error", "message": str(e)}
        finally:
            cursor.close()
            conn.close()

    def _get_student_year(self, cursor, student_id):
        """Get student's current year of study"""
        query = "SELECT YearOfStudy FROM Student WHERE student_Id = %s"
        cursor.execute(query, (student_id,))
        result = cursor.fetchone()
        return result[0] if result else 1

    def _check_time_conflicts(self, cursor, student_id, new_course_id):
        """Check for time conflicts with student's current schedule"""
        # Get student's current schedule
        current_schedule = self.enrollment.get_student_current_schedule(cursor, student_id)
        
        # Get schedule for the new course
        new_course_schedule = self.enrollment.get_course_schedule(cursor, new_course_id)
        
        # If no schedule data available (CourseSchedule table might not exist), skip time conflict check
        if not new_course_schedule or not current_schedule:
            return None
        
        # Check for conflicts
        for new_class in new_course_schedule:
            new_day, new_start, new_end = new_class
            
            for current_class in current_schedule:
                current_course_id, current_course_name, current_day, current_start, current_end = current_class
                
                # Check if same day
                if new_day == current_day:
                    # Check if times overlap
                    if self._times_overlap(new_start, new_end, current_start, current_end):
                        return current_course_name
        
        return None

    def _times_overlap(self, start1, end1, start2, end2):
        """Check if two time periods overlap"""
        # Convert to datetime objects for comparison if they're time objects
        if isinstance(start1, time):
            start1 = datetime.combine(datetime.today(), start1)
            end1 = datetime.combine(datetime.today(), end1)
        if isinstance(start2, time):
            start2 = datetime.combine(datetime.today(), start2)
            end2 = datetime.combine(datetime.today(), end2)
        
        # Check for overlap: (start1 < end2) and (end1 > start2)
        return start1 < end2 and end1 > start2

    def validate_enrollment_requirements(self, student_id, course_id):
        """Validate all enrollment requirements without actually enrolling"""
        conn = self.db.get_db_connection()
        cursor = conn.cursor()

        try:
            validation_results = {
                "can_enroll": True,
                "issues": []
            }

            # Check if already enrolled
            if self.enrollment.check_existing_enrollment(cursor, student_id, course_id):
                validation_results["can_enroll"] = False
                validation_results["issues"].append("Already enrolled in this course")

            # Check course capacity
            course_data = self.course.getCourseById(cursor, course_id)
            if not course_data:
                validation_results["can_enroll"] = False
                validation_results["issues"].append("Course not found")
                return validation_results
            
            available_seats = course_data[4]
            if available_seats <= 0:
                validation_results["can_enroll"] = False
                validation_results["issues"].append("Course is full")

            # Check prerequisites
            prerequisite_year = course_data[8]
            student_year = self._get_student_year(cursor, student_id)
            
            if student_year < prerequisite_year:
                validation_results["can_enroll"] = False
                validation_results["issues"].append(f"Must be in year {prerequisite_year} or higher")

            # Check time conflicts
            time_conflict = self._check_time_conflicts(cursor, student_id, course_id)
            if time_conflict:
                validation_results["can_enroll"] = False
                validation_results["issues"].append(f"Time conflict with {time_conflict}")

            return validation_results

        except Exception as e:
            return {"can_enroll": False, "issues": [str(e)]}
        finally:
            cursor.close()
            conn.close()

    def get_student_schedule_summary(self, student_id):
        """Get a summary of student's current schedule"""
        conn = self.db.get_db_connection()
        cursor = conn.cursor()

        try:
            # Get enrollments with schedule information
            query = """
            SELECT c.courseName, c.credits, 
                   CONCAT(u.firstName, ' ', u.lastName) as instructor_name,
                   dept.deptName,
                   cs.day, cs.startTime, cs.endTime
            FROM Enrollment e
            JOIN Course c ON e.course_id = c.course_id
            JOIN Users u ON c.facultyMem_Id = u.user_id
            JOIN Department dept ON c.dept_Id = dept.dept_Id
            LEFT JOIN CourseSchedule cs ON c.course_id = cs.course_id
            WHERE e.student_id = %s AND e.enrollmentStatus = 'Active'
            ORDER BY cs.day, cs.startTime
            """
            cursor.execute(query, (student_id,))
            schedule = cursor.fetchall()
            
            # Calculate total credits
            total_credits = sum([course[1] for course in schedule if course[1]])
            
            return {
                "status": "Success", 
                "schedule": schedule,
                "total_credits": total_credits,
                "course_count": len(set([course[0] for course in schedule]))
            }
            
        except Exception as e:
            return {"status": "Error", "message": str(e)}
        finally:
            cursor.close()
            conn.close()

    def get_notification_statistics(self):
        """Get notification system statistics"""
        try:
            return self.notification_manager.get_notification_statistics()
        except Exception as e:
            return {
                "status": "Error", 
                "message": f"Failed to get notification statistics: {str(e)}"
            }
    
    def demo_notification_system(self):
        """Run a demonstration of the notification system"""
        try:
            self.notification_manager.demo_notification_system()
            return {"status": "Success", "message": "Notification demo completed"}
        except Exception as e:
            return {
                "status": "Error", 
                "message": f"Failed to run notification demo: {str(e)}"
            }
    
    def manage_notification_observers(self, action, observer_type=None):
        """Manage notification observers (attach/detach)"""
        try:
            if action == "detach" and observer_type:
                self.notification_manager.detach_observer(observer_type)
                return {"status": "Success", "message": f"{observer_type} observer detached"}
            elif action == "attach" and observer_type:
                self.notification_manager.attach_observer(observer_type)
                return {"status": "Success", "message": f"{observer_type} observer attached"}
            elif action == "attach_all":
                self.notification_manager.attach_all_observers()
                return {"status": "Success", "message": "All observers attached"}
            else:
                return {"status": "Error", "message": "Invalid action or missing observer_type"}
        except Exception as e:
            return {
                "status": "Error", 
                "message": f"Failed to manage observers: {str(e)}"
            }
