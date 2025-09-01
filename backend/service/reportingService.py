from backend.dal.dbconfig import dbconfig
from backend.presentation.reports import (
    EnrollmentStatisticsReport, 
    FacultyWorkloadReport, 
    CoursePopularityReport,
    HighCapacityCoursesReport,
    DepartmentAnalyticsReport,
    ReportExporter
)

class ReportingService:
    def __init__(self):
        self.db = dbconfig()
        self.conn = self.db.get_db_connection()
        self.cursor = self.conn.cursor()

    def get_enrollment_statistics_by_department(self, department_id=None, semester=None):
        """Get enrollment statistics for a specific department or all departments"""
        try:
            report = EnrollmentStatisticsReport(dept_id=department_id, semester=semester)
            data = report.outputData()
            return {"status": "Success", "data": data}
        except Exception as e:
            return {"status": "Error", "message": str(e)}

    def get_faculty_workload_report(self, faculty_id=None):
        """Get faculty workload report for specific faculty or all faculty"""
        try:
            report = FacultyWorkloadReport(faculty_id=faculty_id)
            data = report.outputData()
            return {"status": "Success", "data": data}
        except Exception as e:
            return {"status": "Error", "message": str(e)}

    def get_course_popularity_trends(self, semester=None, limit=10):
        """Get course popularity trends based on enrollment numbers"""
        try:
            report = CoursePopularityReport(semester=semester, limit=limit)
            data = report.outputData()
            return {"status": "Success", "data": data}
        except Exception as e:
            return {"status": "Error", "message": str(e)}

    def get_high_capacity_courses(self, department_name=None, threshold_percentage=90):
        """Get courses above a certain capacity threshold"""
        try:
            report = HighCapacityCoursesReport(
                department_name=department_name, 
                threshold_percentage=threshold_percentage
            )
            data = report.outputData()
            return {"status": "Success", "data": data}
        except Exception as e:
            return {"status": "Error", "message": str(e)}

    def get_department_analytics(self, semester=None):
        """Get comprehensive analytics for all departments"""
        try:
            report = DepartmentAnalyticsReport(semester=semester)
            data = report.outputData()
            return {"status": "Success", "data": data}
        except Exception as e:
            return {"status": "Error", "message": str(e)}

    def get_business_school_high_capacity_report(self, threshold_percentage=90):
        """
        Specific use case: Generate a report for Business school courses 
        that are currently at over 90% capacity
        """
        try:
            # First, get the Business department ID
            dept_query = "SELECT dept_Id FROM Department WHERE deptName LIKE %s"
            self.cursor.execute(dept_query, ("%Business%",))
            dept_result = self.cursor.fetchone()
            
            if not dept_result:
                return {"status": "Error", "message": "Business department not found"}
            
            # Get detailed course information for Business school
            query = """
            SELECT C.course_id, C.courseName, 
                   CONCAT(U.firstName, ' ', U.lastName) as instructor_name,
                   C.capacity, C.availableSeats,
                   (C.capacity - C.availableSeats) as enrolled_students,
                   ROUND(((C.capacity - C.availableSeats) / C.capacity) * 100, 2) as utilization_percentage,
                   dept.deptName
            FROM Course AS C
            JOIN Department as dept ON C.dept_Id = dept.dept_Id
            JOIN Users as U ON C.facultyMem_Id = U.user_id
            WHERE dept.deptName LIKE %s
            AND C.capacity > 0
            AND ((C.capacity - C.availableSeats) / C.capacity) * 100 >= %s
            ORDER BY utilization_percentage DESC;
            """
            
            self.cursor.execute(query, ("%Business%", threshold_percentage))
            results = self.cursor.fetchall()
            
            # Process the data
            processed_data = []
            for row in results:
                processed_data.append({
                    "courseId": row[0],
                    "courseName": row[1],
                    "instructor": row[2],
                    "totalCapacity": row[3],
                    "enrolledStudents": row[5],
                    "utilizationPercentage": row[6],
                    "department": row[7],
                    "availableSeats": row[4],
                    "status": "Critical" if row[6] >= 95 else "High Capacity"
                })
            
            return {
                "status": "Success", 
                "data": processed_data,
                "summary": {
                    "totalCourses": len(processed_data),
                    "department": "Business",
                    "threshold": threshold_percentage,
                    "averageUtilization": round(sum(course["utilizationPercentage"] for course in processed_data) / len(processed_data), 2) if processed_data else 0
                }
            }
            
        except Exception as e:
            return {"status": "Error", "message": str(e)}

    def export_report_as_json(self, report_data):
        """Export any report data as JSON"""
        try:
            json_data = ReportExporter.export_to_json(report_data)
            return {"status": "Success", "data": json_data}
        except Exception as e:
            return {"status": "Error", "message": str(e)}

    def export_report_as_html(self, report_data, title="University Report"):
        """Export any report data as HTML table"""
        try:
            html_data = ReportExporter.export_to_html_table(report_data, title)
            return {"status": "Success", "data": html_data}
        except Exception as e:
            return {"status": "Error", "message": str(e)}

    def get_comprehensive_analytics_dashboard(self):
        """Get all analytics data for a comprehensive dashboard"""
        try:
            # Get all different types of reports
            enrollment_stats = self.get_enrollment_statistics_by_department()
            faculty_workload = self.get_faculty_workload_report()
            course_popularity = self.get_course_popularity_trends(limit=5)
            high_capacity = self.get_high_capacity_courses(threshold_percentage=85)
            department_analytics = self.get_department_analytics()
            
            return {
                "status": "Success",
                "data": {
                    "enrollmentStatistics": enrollment_stats.get("data", []),
                    "facultyWorkload": faculty_workload.get("data", []),
                    "popularCourses": course_popularity.get("data", []),
                    "highCapacityCourses": high_capacity.get("data", []),
                    "departmentAnalytics": department_analytics.get("data", [])
                }
            }
        except Exception as e:
            return {"status": "Error", "message": str(e)}

    def close_connection(self):
        """Close database connections"""
        if self.cursor:
            self.cursor.close()
        if self.conn:
            self.conn.close()
