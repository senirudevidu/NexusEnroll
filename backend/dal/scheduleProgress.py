class ScheduleProgress:
    def __init__(self, db):
        self.db = db

    # ============ SCHEDULE MANAGEMENT METHODS ============
    
    def get_student_schedule(self, cursor, student_id, semester_id=None):
        """Get student's schedule for a specific semester or current semester"""
        if semester_id:
            query = """
            SELECT 
                c.course_id,
                c.courseName,
                CONCAT(u.firstName, ' ', u.lastName) as instructor_name,
                cs.day,
                cs.startTime,
                cs.endTime,
                cs.location,
                sem.semester_name,
                sem.academic_year,
                c.credits,
                e.marks,
                e.markStatus
            FROM Enrollment e
            JOIN Course c ON e.course_id = c.course_id
            JOIN Users u ON c.facultyMem_Id = u.user_id
            LEFT JOIN CourseSchedule cs ON c.course_id = cs.course_id
            JOIN AcademicSemester sem ON e.semester_id = sem.semester_id
            WHERE e.student_id = %s AND e.semester_id = %s AND e.enrollmentStatus = 'Active'
            ORDER BY cs.day, cs.startTime
            """
            cursor.execute(query, (student_id, semester_id))
        else:
            # Get current semester schedule
            query = """
            SELECT 
                c.course_id,
                c.courseName,
                CONCAT(u.firstName, ' ', u.lastName) as instructor_name,
                cs.day,
                cs.startTime,
                cs.endTime,
                cs.location,
                sem.semester_name,
                sem.academic_year,
                c.credits,
                e.marks,
                e.markStatus
            FROM Enrollment e
            JOIN Course c ON e.course_id = c.course_id
            JOIN Users u ON c.facultyMem_Id = u.user_id
            LEFT JOIN CourseSchedule cs ON c.course_id = cs.course_id
            LEFT JOIN AcademicSemester sem ON e.semester_id = sem.semester_id
            WHERE e.student_id = %s AND e.enrollmentStatus = 'Active' 
            AND (sem.is_current = TRUE OR e.semester_id IS NULL)
            ORDER BY cs.day, cs.startTime
            """
            cursor.execute(query, (student_id,))
        
        schedule = cursor.fetchall()
        return schedule

    def get_available_semesters(self, cursor, student_id):
        """Get all semesters where student has enrollments"""
        query = """
        SELECT DISTINCT 
            sem.semester_id,
            sem.semester_name,
            sem.academic_year,
            sem.is_current,
            COUNT(e.enrollment_id) as course_count
        FROM AcademicSemester sem
        LEFT JOIN Enrollment e ON sem.semester_id = e.semester_id AND e.student_id = %s AND e.enrollmentStatus = 'Active'
        WHERE e.enrollment_id IS NOT NULL OR sem.is_current = TRUE
        GROUP BY sem.semester_id, sem.semester_name, sem.academic_year, sem.is_current
        ORDER BY sem.academic_year DESC, sem.semester_name DESC
        """
        cursor.execute(query, (student_id,))
        semesters = cursor.fetchall()
        return semesters

    def get_current_semester(self, cursor):
        """Get the current active semester"""
        query = """
        SELECT semester_id, semester_name, academic_year, start_date, end_date
        FROM AcademicSemester 
        WHERE is_current = TRUE
        LIMIT 1
        """
        cursor.execute(query)
        semester = cursor.fetchone()
        return semester

    # ============ ACADEMIC PROGRESS METHODS ============
    
    def get_student_progress(self, cursor, student_id):
        """Get comprehensive academic progress for a student"""
        query = """
        SELECT 
            student_Id,
            student_name,
            degree_name,
            degree_ID,
            YearOfStudy,
            completed_courses,
            completed_credits,
            COALESCE(gpa, 0.0) as gpa,
            current_courses,
            current_credits,
            total_degree_credits,
            COALESCE(progress_percentage, 0.0) as progress_percentage
        FROM StudentProgressView
        WHERE student_Id = %s
        """
        cursor.execute(query, (student_id,))
        progress = cursor.fetchone()
        return progress

    def get_completed_courses(self, cursor, student_id):
        """Get all completed courses with grades and semesters"""
        query = """
        SELECT 
            c.course_id,
            c.courseName,
            c.description,
            c.credits,
            e.marks,
            e.markStatus,
            sem.semester_name,
            sem.academic_year,
            CONCAT(u.firstName, ' ', u.lastName) as instructor_name,
            d.deptName as department
        FROM Enrollment e
        JOIN Course c ON e.course_id = c.course_id
        JOIN Users u ON c.facultyMem_Id = u.user_id
        JOIN Department d ON c.dept_Id = d.dept_Id
        LEFT JOIN AcademicSemester sem ON e.semester_id = sem.semester_id
        WHERE e.student_id = %s AND e.markStatus = 'Completed' AND e.enrollmentStatus = 'Active'
        ORDER BY sem.academic_year DESC, sem.semester_name DESC, c.courseName
        """
        cursor.execute(query, (student_id,))
        completed_courses = cursor.fetchall()
        return completed_courses

    def get_pending_requirements(self, cursor, student_id):
        """Get remaining courses required for student's degree"""
        query = """
        SELECT 
            course_id,
            courseName,
            description,
            credits,
            requirement_type,
            year_requirement,
            is_core_requirement
        FROM PendingRequirementsView
        WHERE student_Id = %s
        ORDER BY is_core_requirement DESC, year_requirement ASC, courseName
        """
        cursor.execute(query, (student_id,))
        pending_requirements = cursor.fetchall()
        return pending_requirements

    def get_degree_requirements(self, cursor, degree_id):
        """Get all requirements for a specific degree"""
        query = """
        SELECT 
            dr.requirement_id,
            c.course_id,
            c.courseName,
            c.description,
            c.credits,
            dr.is_core_requirement,
            dr.year_requirement,
            CASE 
                WHEN dr.is_core_requirement = TRUE THEN 'Core Requirement'
                ELSE 'Elective Option'
            END as requirement_type
        FROM DegreeRequirements dr
        JOIN Course c ON dr.course_id = c.course_id
        WHERE dr.degree_id = %s
        ORDER BY dr.is_core_requirement DESC, dr.year_requirement ASC, c.courseName
        """
        cursor.execute(query, (degree_id,))
        requirements = cursor.fetchall()
        return requirements

    # ============ ACADEMIC CALENDAR METHODS ============
    
    def get_weekly_schedule_grid(self, cursor, student_id, semester_id=None):
        """Get student's schedule formatted for weekly calendar grid"""
        schedule_data = self.get_student_schedule(cursor, student_id, semester_id)
        
        # Format schedule into daily grid
        weekly_schedule = {
            'Monday': [],
            'Tuesday': [],
            'Wednesday': [],
            'Thursday': [],
            'Friday': [],
            'Saturday': [],
            'Sunday': []
        }
        
        for course in schedule_data:
            if course[3]:  # if day is not null
                day = course[3]
                course_info = {
                    'course_id': course[0],
                    'courseName': course[1],
                    'instructor': course[2],
                    'startTime': str(course[4]) if course[4] else None,
                    'endTime': str(course[5]) if course[5] else None,
                    'location': course[6],
                    'credits': course[9],
                    'markStatus': course[11]
                }
                
                if day in weekly_schedule:
                    weekly_schedule[day].append(course_info)
        
        # Sort each day's courses by start time
        for day in weekly_schedule:
            weekly_schedule[day].sort(key=lambda x: x['startTime'] if x['startTime'] else '00:00:00')
        
        return weekly_schedule

    # ============ STATISTICS AND ANALYTICS ============
    
    def get_student_semester_statistics(self, cursor, student_id):
        """Get statistics for all semesters a student has been enrolled"""
        query = """
        SELECT 
            sem.semester_name,
            sem.academic_year,
            COUNT(e.enrollment_id) as total_courses,
            SUM(c.credits) as total_credits,
            AVG(CASE WHEN e.marks IS NOT NULL THEN e.marks END) as semester_gpa,
            COUNT(CASE WHEN e.markStatus = 'Completed' THEN 1 END) as completed_courses,
            COUNT(CASE WHEN e.markStatus = 'In Progress' THEN 1 END) as in_progress_courses
        FROM AcademicSemester sem
        JOIN Enrollment e ON sem.semester_id = e.semester_id
        JOIN Course c ON e.course_id = c.course_id
        WHERE e.student_id = %s AND e.enrollmentStatus = 'Active'
        GROUP BY sem.semester_id, sem.semester_name, sem.academic_year
        ORDER BY sem.academic_year DESC, sem.semester_name DESC
        """
        cursor.execute(query, (student_id,))
        statistics = cursor.fetchall()
        return statistics

    def get_grade_distribution(self, cursor, student_id):
        """Get grade distribution for completed courses"""
        query = """
        SELECT 
            CASE 
                WHEN e.marks >= 90 THEN 'A'
                WHEN e.marks >= 80 THEN 'B'
                WHEN e.marks >= 70 THEN 'C'
                WHEN e.marks >= 60 THEN 'D'
                WHEN e.marks < 60 THEN 'F'
                ELSE 'Not Graded'
            END as grade,
            COUNT(*) as count
        FROM Enrollment e
        WHERE e.student_id = %s AND e.markStatus = 'Completed' AND e.enrollmentStatus = 'Active'
        GROUP BY 
            CASE 
                WHEN e.marks >= 90 THEN 'A'
                WHEN e.marks >= 80 THEN 'B'
                WHEN e.marks >= 70 THEN 'C'
                WHEN e.marks >= 60 THEN 'D'
                WHEN e.marks < 60 THEN 'F'
                ELSE 'Not Graded'
            END
        ORDER BY grade
        """
        cursor.execute(query, (student_id,))
        grade_distribution = cursor.fetchall()
        return grade_distribution

    # ============ SEMESTER MANAGEMENT ============
    
    def create_academic_semester(self, cursor, conn, semester_name, start_date, end_date, academic_year):
        """Create a new academic semester"""
        try:
            query = """
            INSERT INTO AcademicSemester (semester_name, start_date, end_date, academic_year, is_current)
            VALUES (%s, %s, %s, %s, FALSE)
            """
            cursor.execute(query, (semester_name, start_date, end_date, academic_year))
            conn.commit()
            return {"status": "Success", "message": "Academic semester created successfully"}
        except Exception as e:
            conn.rollback()
            return {"status": "Error", "message": str(e)}

    def set_current_semester(self, cursor, conn, semester_id):
        """Set a semester as the current active semester"""
        try:
            # First, unset all current semesters
            cursor.execute("UPDATE AcademicSemester SET is_current = FALSE")
            
            # Then set the specified semester as current
            cursor.execute("UPDATE AcademicSemester SET is_current = TRUE WHERE semester_id = %s", (semester_id,))
            
            conn.commit()
            return {"status": "Success", "message": "Current semester updated successfully"}
        except Exception as e:
            conn.rollback()
            return {"status": "Error", "message": str(e)}
