"""
Data Access Layer for Course Request Management
Handles database operations for course change requests
"""

class CourseRequest:
    def __init__(self, db):
        self.db = db
    
    def create_request(self, cursor, conn, faculty_id, course_id, request_type, details):
        """Create a new course change request"""
        query = """
        INSERT INTO CourseRequest (facultyMem_Id, course_id, requestType, details, status)
        VALUES (%s, %s, %s, %s, 'Pending')
        """
        cursor.execute(query, (faculty_id, course_id, request_type, details))
        conn.commit()
        request_id = cursor.lastrowid
        return {"status": "Success", "message": "Course request submitted successfully", "request_id": request_id}
    
    def get_pending_requests(self, cursor):
        """Get all pending course requests for admin review"""
        query = """
        SELECT cr.request_id, cr.facultyMem_Id, cr.course_id, cr.requestType, 
               cr.details, cr.requestDate, cr.status,
               u.firstName, u.lastName, c.courseName
        FROM CourseRequest cr
        JOIN Users u ON cr.facultyMem_Id = u.user_id
        JOIN Course c ON cr.course_id = c.course_id
        WHERE cr.status = 'Pending'
        ORDER BY cr.requestDate ASC
        """
        cursor.execute(query)
        return cursor.fetchall()
    
    def get_faculty_requests(self, cursor, faculty_id):
        """Get all requests submitted by a specific faculty member"""
        query = """
        SELECT cr.request_id, cr.course_id, cr.requestType, cr.details, 
               cr.requestDate, cr.status, cr.decisionDate,
               c.courseName, a.firstName as admin_firstName, a.lastName as admin_lastName
        FROM CourseRequest cr
        JOIN Course c ON cr.course_id = c.course_id
        LEFT JOIN Users a ON cr.approvedBy = a.user_id
        WHERE cr.facultyMem_Id = %s
        ORDER BY cr.requestDate DESC
        """
        cursor.execute(query, (faculty_id,))
        return cursor.fetchall()
    
    def approve_request(self, cursor, conn, request_id, admin_id):
        """Approve a course request and apply changes"""
        # First get the request details
        query = """
        SELECT facultyMem_Id, course_id, requestType, details
        FROM CourseRequest 
        WHERE request_id = %s AND status = 'Pending'
        """
        cursor.execute(query, (request_id,))
        request_data = cursor.fetchone()
        
        if not request_data:
            return {"status": "Error", "message": "Request not found or already processed"}
        
        faculty_id, course_id, request_type, details = request_data
        
        try:
            # Apply the requested change
            if request_type == "UpdateDescription":
                course_query = "UPDATE Course SET description = %s WHERE course_id = %s"
                cursor.execute(course_query, (details, course_id))
            
            elif request_type == "ChangeCapacity":
                try:
                    new_capacity = int(details)
                    # Get current enrollment count
                    enrollment_query = """
                    SELECT COUNT(*) as enrolled 
                    FROM Enrollment 
                    WHERE course_id = %s AND enrollmentStatus = 'Active'
                    """
                    cursor.execute(enrollment_query, (course_id,))
                    enrolled_count = cursor.fetchone()[0]
                    
                    if new_capacity < enrolled_count:
                        return {"status": "Error", "message": f"Cannot reduce capacity below current enrollment ({enrolled_count} students)"}
                    
                    # Update capacity and available seats
                    available_seats = new_capacity - enrolled_count
                    capacity_query = """
                    UPDATE Course 
                    SET capacity = %s, availableSeats = %s 
                    WHERE course_id = %s
                    """
                    cursor.execute(capacity_query, (new_capacity, available_seats, course_id))
                except ValueError:
                    return {"status": "Error", "message": "Invalid capacity value"}
            
            elif request_type == "AddPrerequisite":
                # Check if prerequisite already exists
                prereq_check = """
                SELECT COUNT(*) FROM Prerequisite 
                WHERE course_id = %s AND prerequisite_course_id = %s
                """
                try:
                    prereq_course_id = int(details)
                    cursor.execute(prereq_check, (course_id, prereq_course_id))
                    if cursor.fetchone()[0] > 0:
                        return {"status": "Error", "message": "Prerequisite already exists"}
                    
                    # Add prerequisite
                    prereq_query = """
                    INSERT INTO Prerequisite (course_id, prerequisite_course_id)
                    VALUES (%s, %s)
                    """
                    cursor.execute(prereq_query, (course_id, prereq_course_id))
                except ValueError:
                    return {"status": "Error", "message": "Invalid prerequisite course ID"}
            
            # Update request status
            update_query = """
            UPDATE CourseRequest 
            SET status = 'Approved', decisionDate = CURRENT_TIMESTAMP, approvedBy = %s
            WHERE request_id = %s
            """
            cursor.execute(update_query, (admin_id, request_id))
            conn.commit()
            
            return {"status": "Success", "message": "Request approved and changes applied"}
            
        except Exception as e:
            conn.rollback()
            return {"status": "Error", "message": f"Error applying changes: {str(e)}"}
    
    def reject_request(self, cursor, conn, request_id, admin_id):
        """Reject a course request"""
        # Check if request exists and is pending
        check_query = """
        SELECT request_id FROM CourseRequest 
        WHERE request_id = %s AND status = 'Pending'
        """
        cursor.execute(check_query, (request_id,))
        if not cursor.fetchone():
            return {"status": "Error", "message": "Request not found or already processed"}
        
        # Update request status
        update_query = """
        UPDATE CourseRequest 
        SET status = 'Rejected', decisionDate = CURRENT_TIMESTAMP, approvedBy = %s
        WHERE request_id = %s
        """
        cursor.execute(update_query, (admin_id, request_id))
        conn.commit()
        
        return {"status": "Success", "message": "Request rejected"}
    
    def get_request_by_id(self, cursor, request_id):
        """Get a specific request by ID"""
        query = """
        SELECT cr.request_id, cr.facultyMem_Id, cr.course_id, cr.requestType, 
               cr.details, cr.requestDate, cr.status, cr.decisionDate,
               u.firstName, u.lastName, c.courseName,
               a.firstName as admin_firstName, a.lastName as admin_lastName
        FROM CourseRequest cr
        JOIN Users u ON cr.facultyMem_Id = u.user_id
        JOIN Course c ON cr.course_id = c.course_id
        LEFT JOIN Users a ON cr.approvedBy = a.user_id
        WHERE cr.request_id = %s
        """
        cursor.execute(query, (request_id,))
        return cursor.fetchone()
