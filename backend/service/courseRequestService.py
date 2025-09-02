"""
Service Layer for Course Request Management
Business logic for handling course change requests
"""

from backend.dal.courseRequest import CourseRequest
from backend.dal.course import Course

class CourseRequestService:
    def __init__(self, db):
        self.db = db
        self.course_request = CourseRequest(self.db)
        self.course = Course(self.db)
    
    def submit_request(self, faculty_id, course_id, request_type, details):
        """Submit a new course change request"""
        conn = self.db.get_db_connection()
        cursor = conn.cursor()
        
        try:
            # Validate that faculty member teaches this course
            faculty_course_query = """
            SELECT course_id FROM Course 
            WHERE course_id = %s AND facultyMem_Id = %s
            """
            cursor.execute(faculty_course_query, (course_id, faculty_id))
            if not cursor.fetchone():
                return {"status": "Error", "message": "You are not authorized to make requests for this course"}
            
            # Validate request type
            valid_types = ["UpdateDescription", "AddPrerequisite", "ChangeCapacity"]
            if request_type not in valid_types:
                return {"status": "Error", "message": "Invalid request type"}
            
            # Additional validation based on request type
            if request_type == "ChangeCapacity":
                try:
                    capacity = int(details)
                    if capacity <= 0:
                        return {"status": "Error", "message": "Capacity must be a positive number"}
                except ValueError:
                    return {"status": "Error", "message": "Capacity must be a valid number"}
            
            elif request_type == "AddPrerequisite":
                try:
                    prereq_course_id = int(details)
                    # Check if prerequisite course exists
                    course_check_query = "SELECT course_id FROM Course WHERE course_id = %s"
                    cursor.execute(course_check_query, (prereq_course_id,))
                    if not cursor.fetchone():
                        return {"status": "Error", "message": "Prerequisite course does not exist"}
                    
                    # Check for circular dependencies
                    if prereq_course_id == course_id:
                        return {"status": "Error", "message": "Course cannot be a prerequisite of itself"}
                    
                except ValueError:
                    return {"status": "Error", "message": "Prerequisite course ID must be a valid number"}
            
            elif request_type == "UpdateDescription":
                if not details or len(details.strip()) == 0:
                    return {"status": "Error", "message": "Description cannot be empty"}
                if len(details) > 1000:  # Reasonable limit for description
                    return {"status": "Error", "message": "Description is too long (maximum 1000 characters)"}
            
            # Create the request
            result = self.course_request.create_request(cursor, conn, faculty_id, course_id, request_type, details)
            return result
            
        except Exception as e:
            conn.rollback()
            return {"status": "Error", "message": str(e)}
        finally:
            cursor.close()
            conn.close()
    
    def get_pending_requests(self):
        """Get all pending requests for admin review"""
        conn = self.db.get_db_connection()
        cursor = conn.cursor()
        
        try:
            requests = self.course_request.get_pending_requests(cursor)
            return {"status": "Success", "requests": requests}
        except Exception as e:
            return {"status": "Error", "message": str(e)}
        finally:
            cursor.close()
            conn.close()
    
    def get_faculty_requests(self, faculty_id):
        """Get all requests submitted by a faculty member"""
        conn = self.db.get_db_connection()
        cursor = conn.cursor()
        
        try:
            requests = self.course_request.get_faculty_requests(cursor, faculty_id)
            return {"status": "Success", "requests": requests}
        except Exception as e:
            return {"status": "Error", "message": str(e)}
        finally:
            cursor.close()
            conn.close()
    
    def approve_request(self, request_id, admin_id):
        """Approve a course request"""
        conn = self.db.get_db_connection()
        cursor = conn.cursor()
        
        try:
            result = self.course_request.approve_request(cursor, conn, request_id, admin_id)
            return result
        except Exception as e:
            conn.rollback()
            return {"status": "Error", "message": str(e)}
        finally:
            cursor.close()
            conn.close()
    
    def reject_request(self, request_id, admin_id):
        """Reject a course request"""
        conn = self.db.get_db_connection()
        cursor = conn.cursor()
        
        try:
            result = self.course_request.reject_request(cursor, conn, request_id, admin_id)
            return result
        except Exception as e:
            conn.rollback()
            return {"status": "Error", "message": str(e)}
        finally:
            cursor.close()
            conn.close()
    
    def get_request_details(self, request_id):
        """Get details of a specific request"""
        conn = self.db.get_db_connection()
        cursor = conn.cursor()
        
        try:
            request_data = self.course_request.get_request_by_id(cursor, request_id)
            if request_data:
                return {"status": "Success", "request": request_data}
            else:
                return {"status": "Error", "message": "Request not found"}
        except Exception as e:
            return {"status": "Error", "message": str(e)}
        finally:
            cursor.close()
            conn.close()
    
    def get_faculty_courses(self, faculty_id):
        """Get all courses taught by a faculty member for request form"""
        conn = self.db.get_db_connection()
        cursor = conn.cursor()
        
        try:
            query = """
            SELECT course_id, courseName, description, capacity
            FROM Course 
            WHERE facultyMem_Id = %s
            ORDER BY courseName
            """
            cursor.execute(query, (faculty_id,))
            courses = cursor.fetchall()
            return {"status": "Success", "courses": courses}
        except Exception as e:
            return {"status": "Error", "message": str(e)}
        finally:
            cursor.close()
            conn.close()
    
    def get_all_courses_for_prerequisite(self):
        """Get all courses that can be used as prerequisites"""
        conn = self.db.get_db_connection()
        cursor = conn.cursor()
        
        try:
            query = """
            SELECT course_id, courseName
            FROM Course 
            ORDER BY courseName
            """
            cursor.execute(query)
            courses = cursor.fetchall()
            return {"status": "Success", "courses": courses}
        except Exception as e:
            return {"status": "Error", "message": str(e)}
        finally:
            cursor.close()
            conn.close()
