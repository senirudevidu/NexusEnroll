from backend.dal.scheduleProgress import ScheduleProgress
from backend.dal.dbconfig import dbconfig

class ScheduleProgressService:
    def __init__(self):
        self.db = dbconfig()
        self.schedule_progress_dal = ScheduleProgress(self.db)

    # ============ SCHEDULE MANAGEMENT SERVICES ============
    
    def get_student_schedule(self, student_id, semester_id=None):
        """Get student's schedule with error handling and data formatting"""
        try:
            conn = self.db.get_db_connection()
            cursor = conn.cursor()
            
            schedule_data = self.schedule_progress_dal.get_student_schedule(cursor, student_id, semester_id)
            
            if not schedule_data:
                return {
                    "status": "Success",
                    "message": "No schedule found for the specified semester",
                    "data": [],
                    "weekly_grid": self._empty_weekly_grid()
                }
            
            # Get weekly grid format
            weekly_grid = self.schedule_progress_dal.get_weekly_schedule_grid(cursor, student_id, semester_id)
            
            # Format schedule data for API response
            formatted_schedule = []
            for course in schedule_data:
                formatted_course = {
                    'course_id': course[0],
                    'courseName': course[1],
                    'instructor': course[2],
                    'day': course[3],
                    'startTime': str(course[4]) if course[4] else None,
                    'endTime': str(course[5]) if course[5] else None,
                    'location': course[6] or 'TBA',
                    'semester': course[7],
                    'academic_year': course[8],
                    'credits': course[9],
                    'marks': float(course[10]) if course[10] else None,
                    'markStatus': course[11]
                }
                formatted_schedule.append(formatted_course)
            
            return {
                "status": "Success",
                "message": "Schedule retrieved successfully",
                "data": formatted_schedule,
                "weekly_grid": weekly_grid
            }
            
        except Exception as e:
            return {
                "status": "Error",
                "message": f"Failed to retrieve schedule: {str(e)}",
                "data": [],
                "weekly_grid": self._empty_weekly_grid()
            }
        finally:
            if 'cursor' in locals():
                cursor.close()
            if 'conn' in locals():
                conn.close()

    def get_student_semesters(self, student_id):
        """Get all available semesters for a student"""
        try:
            conn = self.db.get_db_connection()
            cursor = conn.cursor()
            
            semesters = self.schedule_progress_dal.get_available_semesters(cursor, student_id)
            
            formatted_semesters = []
            for semester in semesters:
                formatted_semester = {
                    'semester_id': semester[0],
                    'semester_name': semester[1],
                    'academic_year': semester[2],
                    'is_current': bool(semester[3]),
                    'course_count': semester[4]
                }
                formatted_semesters.append(formatted_semester)
            
            return {
                "status": "Success",
                "message": "Semesters retrieved successfully",
                "data": formatted_semesters
            }
            
        except Exception as e:
            return {
                "status": "Error",
                "message": f"Failed to retrieve semesters: {str(e)}",
                "data": []
            }
        finally:
            if 'cursor' in locals():
                cursor.close()
            if 'conn' in locals():
                conn.close()

    # ============ ACADEMIC PROGRESS SERVICES ============
    
    def get_student_academic_progress(self, student_id):
        """Get comprehensive academic progress information"""
        try:
            conn = self.db.get_db_connection()
            cursor = conn.cursor()
            
            # Get overall progress
            progress_data = self.schedule_progress_dal.get_student_progress(cursor, student_id)
            
            if not progress_data:
                return {
                    "status": "Error",
                    "message": "Student progress data not found",
                    "data": None
                }
            
            # Get completed courses
            completed_courses = self.schedule_progress_dal.get_completed_courses(cursor, student_id)
            
            # Get pending requirements
            pending_requirements = self.schedule_progress_dal.get_pending_requirements(cursor, student_id)
            
            # Get semester statistics
            semester_stats = self.schedule_progress_dal.get_student_semester_statistics(cursor, student_id)
            
            # Get grade distribution
            grade_distribution = self.schedule_progress_dal.get_grade_distribution(cursor, student_id)
            
            # Format the response
            formatted_progress = {
                'student_info': {
                    'student_id': progress_data[0],
                    'student_name': progress_data[1],
                    'degree_name': progress_data[2],
                    'degree_id': progress_data[3],
                    'year_of_study': progress_data[4]
                },
                'academic_summary': {
                    'completed_courses': progress_data[5],
                    'completed_credits': float(progress_data[6]) if progress_data[6] else 0.0,
                    'gpa': round(float(progress_data[7]), 2) if progress_data[7] else 0.0,
                    'current_courses': progress_data[8],
                    'current_credits': float(progress_data[9]) if progress_data[9] else 0.0,
                    'total_degree_credits': float(progress_data[10]) if progress_data[10] else 0.0,
                    'progress_percentage': round(float(progress_data[11]), 2) if progress_data[11] else 0.0
                },
                'completed_courses': self._format_completed_courses(completed_courses),
                'pending_requirements': self._format_pending_requirements(pending_requirements),
                'semester_statistics': self._format_semester_statistics(semester_stats),
                'grade_distribution': self._format_grade_distribution(grade_distribution)
            }
            
            return {
                "status": "Success",
                "message": "Academic progress retrieved successfully",
                "data": formatted_progress
            }
            
        except Exception as e:
            return {
                "status": "Error",
                "message": f"Failed to retrieve academic progress: {str(e)}",
                "data": None
            }
        finally:
            if 'cursor' in locals():
                cursor.close()
            if 'conn' in locals():
                conn.close()

    def get_degree_requirements_overview(self, degree_id):
        """Get all requirements for a specific degree program"""
        try:
            conn = self.db.get_db_connection()
            cursor = conn.cursor()
            
            requirements = self.schedule_progress_dal.get_degree_requirements(cursor, degree_id)
            
            formatted_requirements = []
            for req in requirements:
                formatted_req = {
                    'requirement_id': req[0],
                    'course_id': req[1],
                    'courseName': req[2],
                    'description': req[3],
                    'credits': req[4],
                    'is_core_requirement': bool(req[5]),
                    'year_requirement': req[6],
                    'requirement_type': req[7]
                }
                formatted_requirements.append(formatted_req)
            
            # Group by requirement type and year
            grouped_requirements = {
                'core_requirements': [],
                'elective_options': []
            }
            
            for req in formatted_requirements:
                if req['is_core_requirement']:
                    grouped_requirements['core_requirements'].append(req)
                else:
                    grouped_requirements['elective_options'].append(req)
            
            return {
                "status": "Success",
                "message": "Degree requirements retrieved successfully",
                "data": grouped_requirements
            }
            
        except Exception as e:
            return {
                "status": "Error",
                "message": f"Failed to retrieve degree requirements: {str(e)}",
                "data": None
            }
        finally:
            if 'cursor' in locals():
                cursor.close()
            if 'conn' in locals():
                conn.close()

    # ============ HELPER METHODS ============
    
    def _empty_weekly_grid(self):
        """Return empty weekly schedule grid"""
        return {
            'Monday': [],
            'Tuesday': [],
            'Wednesday': [],
            'Thursday': [],
            'Friday': [],
            'Saturday': [],
            'Sunday': []
        }
    
    def _format_completed_courses(self, completed_courses):
        """Format completed courses data"""
        formatted_courses = []
        for course in completed_courses:
            formatted_course = {
                'course_id': course[0],
                'courseName': course[1],
                'description': course[2],
                'credits': course[3],
                'marks': float(course[4]) if course[4] else None,
                'grade': self._calculate_letter_grade(course[4]) if course[4] else 'N/A',
                'markStatus': course[5],
                'semester': course[6] or 'Unknown',
                'academic_year': course[7] or 'Unknown',
                'instructor': course[8],
                'department': course[9]
            }
            formatted_courses.append(formatted_course)
        return formatted_courses
    
    def _format_pending_requirements(self, pending_requirements):
        """Format pending requirements data"""
        formatted_requirements = []
        for req in pending_requirements:
            formatted_req = {
                'course_id': req[0],
                'courseName': req[1],
                'description': req[2],
                'credits': req[3],
                'requirement_type': req[4],
                'year_requirement': req[5],
                'is_core_requirement': bool(req[6])
            }
            formatted_requirements.append(formatted_req)
        return formatted_requirements
    
    def _format_semester_statistics(self, semester_stats):
        """Format semester statistics data"""
        formatted_stats = []
        for stat in semester_stats:
            formatted_stat = {
                'semester_name': stat[0],
                'academic_year': stat[1],
                'total_courses': stat[2],
                'total_credits': stat[3],
                'semester_gpa': round(float(stat[4]), 2) if stat[4] else 0.0,
                'completed_courses': stat[5],
                'in_progress_courses': stat[6]
            }
            formatted_stats.append(formatted_stat)
        return formatted_stats
    
    def _format_grade_distribution(self, grade_distribution):
        """Format grade distribution data"""
        distribution = {'A': 0, 'B': 0, 'C': 0, 'D': 0, 'F': 0, 'Not Graded': 0}
        
        for grade_data in grade_distribution:
            grade = grade_data[0]
            count = grade_data[1]
            if grade in distribution:
                distribution[grade] = count
        
        return distribution
    
    def _calculate_letter_grade(self, marks):
        """Convert numeric marks to letter grade"""
        if marks is None:
            return 'N/A'
        
        marks = float(marks)
        if marks >= 90:
            return 'A'
        elif marks >= 80:
            return 'B'
        elif marks >= 70:
            return 'C'
        elif marks >= 60:
            return 'D'
        else:
            return 'F'

    # ============ VALIDATION METHODS ============
    
    def validate_student_access(self, student_id):
        """Validate if student exists and has access"""
        try:
            conn = self.db.get_db_connection()
            cursor = conn.cursor()
            
            query = "SELECT student_Id FROM Student WHERE student_Id = %s"
            cursor.execute(query, (student_id,))
            result = cursor.fetchone()
            
            return result is not None
            
        except Exception:
            return False
        finally:
            if 'cursor' in locals():
                cursor.close()
            if 'conn' in locals():
                conn.close()

    def get_current_semester_info(self):
        """Get current semester information"""
        try:
            conn = self.db.get_db_connection()
            cursor = conn.cursor()
            
            current_semester = self.schedule_progress_dal.get_current_semester(cursor)
            
            if not current_semester:
                return {
                    "status": "Error",
                    "message": "No current semester found",
                    "data": None
                }
            
            formatted_semester = {
                'semester_id': current_semester[0],
                'semester_name': current_semester[1],
                'academic_year': current_semester[2],
                'start_date': str(current_semester[3]),
                'end_date': str(current_semester[4])
            }
            
            return {
                "status": "Success",
                "message": "Current semester retrieved successfully",
                "data": formatted_semester
            }
            
        except Exception as e:
            return {
                "status": "Error",
                "message": f"Failed to retrieve current semester: {str(e)}",
                "data": None
            }
        finally:
            if 'cursor' in locals():
                cursor.close()
            if 'conn' in locals():
                conn.close()
