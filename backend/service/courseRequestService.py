from backend.dal.courseRequest import CourseRequest

class CourseRequestService:
    def __init__(self, db):
        self.course_request_dal = CourseRequest(db)
        self.db = db
    
    def create_request(self, faculty_id, course_id, request_type, details):
        """Create a new course change request"""
        try:
            conn = self.db.get_connection()
            cursor = conn.cursor()
            
            result = self.course_request_dal.create_request(
                cursor, conn, faculty_id, course_id, request_type, details
            )
            
            cursor.close()
            conn.close()
            return result
            
        except Exception as e:
            if cursor:
                cursor.close()
            if conn:
                conn.close()
            return {"status": "Error", "message": str(e)}
    
    def get_pending_requests(self):
        """Get all pending course requests for admin review"""
        try:
            conn = self.db.get_connection()
            cursor = conn.cursor()
            
            requests = self.course_request_dal.get_pending_requests(cursor)
            
            cursor.close()
            conn.close()
            return {"status": "Success", "data": requests}
            
        except Exception as e:
            if cursor:
                cursor.close()
            if conn:
                conn.close()
            return {"status": "Error", "message": str(e)}
    
    def get_all_requests(self):
        """Get all course requests with optional status filter"""
        try:
            conn = self.db.get_connection()
            cursor = conn.cursor()
            
            requests = self.course_request_dal.get_all_requests(cursor)
            
            cursor.close()
            conn.close()
            return {"status": "Success", "data": requests}
            
        except Exception as e:
            if cursor:
                cursor.close()
            if conn:
                conn.close()
            return {"status": "Error", "message": str(e)}
    
    def get_faculty_requests(self, faculty_id):
        """Get course requests for a specific faculty member"""
        try:
            conn = self.db.get_connection()
            cursor = conn.cursor()
            
            requests = self.course_request_dal.get_faculty_requests(cursor, faculty_id)
            
            cursor.close()
            conn.close()
            return {"status": "Success", "data": requests}
            
        except Exception as e:
            if cursor:
                cursor.close()
            if conn:
                conn.close()
            return {"status": "Error", "message": str(e)}
    
    def approve_request(self, request_id, admin_id):
        """Approve a course request"""
        try:
            conn = self.db.get_connection()
            cursor = conn.cursor()
            
            result = self.course_request_dal.approve_request(cursor, conn, request_id, admin_id)
            
            cursor.close()
            conn.close()
            return result
            
        except Exception as e:
            if cursor:
                cursor.close()
            if conn:
                conn.close()
            return {"status": "Error", "message": str(e)}
    
    def reject_request(self, request_id, admin_id):
        """Reject a course request"""
        try:
            conn = self.db.get_connection()
            cursor = conn.cursor()
            
            result = self.course_request_dal.reject_request(cursor, conn, request_id, admin_id)
            
            cursor.close()
            conn.close()
            return result
            
        except Exception as e:
            if cursor:
                cursor.close()
            if conn:
                conn.close()
            return {"status": "Error", "message": str(e)}
    
    def get_request_stats(self):
        """Get statistics about course requests"""
        try:
            conn = self.db.get_connection()
            cursor = conn.cursor()
            
            stats = self.course_request_dal.get_request_stats(cursor)
            
            cursor.close()
            conn.close()
            return {"status": "Success", "data": stats}
            
        except Exception as e:
            if cursor:
                cursor.close()
            if conn:
                conn.close()
            return {"status": "Error", "message": str(e)}
