class Enrollment:
    def __init__(self, db):
        self.db = db

    def enroll_student(self, cursor, conn, student_id, course_id):
        """Enroll a student in a course"""
        query = """
        INSERT INTO Enrollment (student_id, course_id, markStatus, enrollmentStatus)
        VALUES (%s, %s, 'In Progress', 'Active')
        """
        cursor.execute(query, (student_id, course_id))
        conn.commit()
        return {"status": "Success", "message": "Student enrolled successfully"}

    def drop_enrollment(self, cursor, conn, enrollment_id):
        """Drop/cancel an enrollment"""
        # First check if enrollment exists and is active
        check_query = "SELECT enrollment_id FROM Enrollment WHERE enrollment_id = %s AND enrollmentStatus = 'Active'"
        cursor.execute(check_query, (enrollment_id,))
        if not cursor.fetchone():
            return {"status": "Error", "message": "Active enrollment not found"}
        
        # Update enrollment status to 'Dropped'
        update_query = "UPDATE Enrollment SET enrollmentStatus = 'Dropped' WHERE enrollment_id = %s"
        cursor.execute(update_query, (enrollment_id,))
        conn.commit()
        return {"status": "Success", "message": "Course dropped successfully"}

    def get_student_enrollments(self, cursor, student_id):
        """Get all active enrollments for a student"""
        query = """
        SELECT e.enrollment_id, e.student_id, e.course_id, c.courseName, c.description,
               c.credits, c.capacity, c.availableSeats, 
               CONCAT(u.firstName, ' ', u.lastName) as instructor_name,
               dept.deptName, e.markStatus, e.marks, e.lastUpdated, e.enrollmentStatus
        FROM Enrollment e
        JOIN Course c ON e.course_id = c.course_id
        JOIN Users u ON c.facultyMem_Id = u.user_id
        JOIN Department dept ON c.dept_Id = dept.dept_Id
        WHERE e.student_id = %s AND e.enrollmentStatus = 'Active'
        ORDER BY c.courseName
        """
        cursor.execute(query, (student_id,))
        enrollments = cursor.fetchall()
        return enrollments

    def get_enrollment_by_id(self, cursor, enrollment_id):
        """Get specific enrollment details"""
        query = """
        SELECT e.enrollment_id, e.student_id, e.course_id, c.courseName,
               e.markStatus, e.marks, e.enrollmentStatus, e.lastUpdated
        FROM Enrollment e
        JOIN Course c ON e.course_id = c.course_id
        WHERE e.enrollment_id = %s
        """
        cursor.execute(query, (enrollment_id,))
        enrollment = cursor.fetchone()
        return enrollment

    def check_existing_enrollment(self, cursor, student_id, course_id):
        """Check if student is already enrolled in the course"""
        query = """
        SELECT enrollment_id FROM Enrollment 
        WHERE student_id = %s AND course_id = %s AND enrollmentStatus = 'Active'
        """
        cursor.execute(query, (student_id, course_id))
        result = cursor.fetchone()
        return result is not None

    def get_student_completed_courses(self, cursor, student_id):
        """Get all completed courses for a student"""
        query = """
        SELECT c.course_id, c.courseName, c.preReqYear
        FROM Enrollment e
        JOIN Course c ON e.course_id = c.course_id
        WHERE e.student_id = %s AND e.markStatus = 'Completed'
        """
        cursor.execute(query, (student_id,))
        completed_courses = cursor.fetchall()
        return completed_courses

    def get_student_current_schedule(self, cursor, student_id):
        """Get student's current class schedule to check for time conflicts"""
        query = """
        SELECT c.course_id, c.courseName, cs.day, cs.startTime, cs.endTime
        FROM Enrollment e
        JOIN Course c ON e.course_id = c.course_id
        LEFT JOIN CourseSchedule cs ON c.course_id = cs.course_id
        WHERE e.student_id = %s AND e.enrollmentStatus = 'Active'
        """
        cursor.execute(query, (student_id,))
        schedule = cursor.fetchall()
        return schedule

    def update_course_capacity(self, cursor, conn, course_id, increment=False):
        """Update course available seats when student enrolls or drops"""
        if increment:
            # Student dropped, increase available seats
            query = "UPDATE Course SET availableSeats = availableSeats + 1 WHERE course_id = %s"
        else:
            # Student enrolled, decrease available seats
            query = "UPDATE Course SET availableSeats = availableSeats - 1 WHERE course_id = %s"
        
        cursor.execute(query, (course_id,))
        conn.commit()

    def get_course_schedule(self, cursor, course_id):
        """Get schedule for a specific course"""
        query = """
        SELECT day, startTime, endTime
        FROM CourseSchedule 
        WHERE course_id = %s
        """
        cursor.execute(query, (course_id,))
        schedule = cursor.fetchall()
        return schedule

    def get_enrollment_statistics(self, cursor, course_id=None):
        """Get enrollment statistics for courses"""
        if course_id:
            query = """
            SELECT c.course_id, c.courseName, c.capacity, c.availableSeats,
                   (c.capacity - c.availableSeats) as enrolled_count,
                   ROUND(((c.capacity - c.availableSeats) / c.capacity) * 100, 2) as enrollment_percentage
            FROM Course c
            WHERE c.course_id = %s
            """
            cursor.execute(query, (course_id,))
        else:
            query = """
            SELECT c.course_id, c.courseName, c.capacity, c.availableSeats,
                   (c.capacity - c.availableSeats) as enrolled_count,
                   ROUND(((c.capacity - c.availableSeats) / c.capacity) * 100, 2) as enrollment_percentage
            FROM Course c
            ORDER BY c.courseName
            """
            cursor.execute(query)
        
        statistics = cursor.fetchall()
        return statistics
