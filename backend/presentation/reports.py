from abc import ABC, abstractmethod
from backend.dal.dbconfig import dbconfig
import json
from datetime import datetime

class GenerateReport(ABC):
    @abstractmethod
    def getData(self):
        # Execute query and fetch data
        pass

    @abstractmethod
    def processData(self):
        # Logic to process self.data
        pass

    @abstractmethod
    def outputData(self):
        # Logic to output the processed data
        pass

class EnrollmentStatisticsReport(GenerateReport):
    def __init__(self, dept_id=None, semester=None):
        self.db = dbconfig()
        self.conn = self.db.get_db_connection()
        self.cursor = self.conn.cursor()
        self.dept_id = dept_id
        self.semester = semester

    def getData(self):
        # Execute query and fetch enrollment statistics data
        if self.dept_id:
            query = """
            SELECT C.course_id, C.courseName, dept.deptName, C.availableSeats, C.capacity,
                   (C.capacity - C.availableSeats) as filled_seats,
                   CONCAT(U.firstName, ' ', U.lastName) as instructor_name
            FROM Course AS C
            JOIN Department as dept ON C.dept_Id = dept.dept_Id
            JOIN Users as U ON C.facultyMem_Id = U.user_id
            WHERE dept.dept_Id = %s
            ORDER BY C.courseName;
            """
            self.cursor.execute(query, (self.dept_id,))
        else:
            query = """
            SELECT C.course_id, C.courseName, dept.deptName, C.availableSeats, C.capacity,
                   (C.capacity - C.availableSeats) as filled_seats,
                   CONCAT(U.firstName, ' ', U.lastName) as instructor_name
            FROM Course AS C
            JOIN Department as dept ON C.dept_Id = dept.dept_Id
            JOIN Users as U ON C.facultyMem_Id = U.user_id
            ORDER BY dept.deptName, C.courseName;
            """
            self.cursor.execute(query)
        courses = self.cursor.fetchall()
        return courses

    def processData(self):
        # Logic to process enrollment statistics data
        courses = self.getData()
        processed_data = []
        for course in courses:
            course_id, course_name, dept_name, available_seats, capacity, filled_seats, instructor = course
            utilization_percentage = (filled_seats / capacity * 100) if capacity > 0 else 0
            
            processed_data.append({
                "course_id": course_id,
                "courseName": course_name,
                "department": dept_name,
                "instructor": instructor,
                "availableSeats": available_seats,
                "capacity": capacity,
                "filledSeats": filled_seats,
                "utilizationPercentage": round(utilization_percentage, 2),
                "status": "Full" if available_seats == 0 else "Open"
            })
        return processed_data

    def outputData(self):
        # Logic to output the processed enrollment statistics data
        departmentCourses = self.processData()
        return departmentCourses
class FacultyWorkloadReport(GenerateReport):
    def __init__(self, faculty_id=None):
        self.db = dbconfig()
        self.conn = self.db.get_db_connection()
        self.cursor = self.conn.cursor()
        self.faculty_id = faculty_id

    def getData(self):
        # Execute query and fetch faculty workload data
        if self.faculty_id:
            query = """
            SELECT f.facultyMem_Id, CONCAT(u.firstName, ' ', u.lastName) as facultyName, 
                   d.deptName, COUNT(C.course_Id) AS numberOfCourses,
                   SUM(C.capacity - C.availableSeats) AS totalEnrolledStudents,
                   AVG(C.capacity - C.availableSeats) AS avgStudentsPerCourse
            FROM FacultyStaff AS f
            JOIN Users as u ON f.facultyMem_Id = u.user_id
            LEFT JOIN Course AS C ON f.facultyMem_Id = C.facultyMem_Id
            LEFT JOIN Department AS d ON C.dept_Id = d.dept_Id
            WHERE f.facultyMem_Id = %s
            GROUP BY f.facultyMem_Id, u.firstName, u.lastName, d.deptName;
            """
            self.cursor.execute(query, (self.faculty_id,))
        else:
            query = """
            SELECT f.facultyMem_Id, CONCAT(u.firstName, ' ', u.lastName) as facultyName, 
                   d.deptName, COUNT(C.course_Id) AS numberOfCourses,
                   SUM(C.capacity - C.availableSeats) AS totalEnrolledStudents,
                   AVG(C.capacity - C.availableSeats) AS avgStudentsPerCourse
            FROM FacultyStaff AS f
            JOIN Users as u ON f.facultyMem_Id = u.user_id
            LEFT JOIN Course AS C ON f.facultyMem_Id = C.facultyMem_Id
            LEFT JOIN Department AS d ON C.dept_Id = d.dept_Id
            GROUP BY f.facultyMem_Id, u.firstName, u.lastName, d.deptName
            ORDER BY d.deptName, u.lastName;
            """
            self.cursor.execute(query)
        results = self.cursor.fetchall()
        return results

    def processData(self):
        # Process the data to a list of dicts
        results = self.getData()
        processed = []
        for row in results:
            processed.append({
                "facultyId": row[0],
                "facultyName": row[1],
                "department": row[2] or "Unassigned",
                "numberOfCourses": row[3] or 0,
                "totalEnrolledStudents": row[4] or 0,
                "avgStudentsPerCourse": round(row[5] or 0, 2)
            })
        return processed

    def outputData(self):
        # Output the processed faculty workload data
        return self.processData()


class CoursePopularityReport(GenerateReport):
    def __init__(self, semester=None, limit=10):
        self.db = dbconfig()
        self.conn = self.db.get_db_connection()
        self.cursor = self.conn.cursor()
        self.semester = semester
        self.limit = limit

    def getData(self):
        # Get course popularity data based on enrollment
        query = """
        SELECT C.course_id, C.courseName, dept.deptName,
               CONCAT(U.firstName, ' ', U.lastName) as instructor_name,
               C.capacity, C.availableSeats,
               (C.capacity - C.availableSeats) as enrolled_count,
               ROUND(((C.capacity - C.availableSeats) / C.capacity) * 100, 2) as popularity_percentage
        FROM Course AS C
        JOIN Department as dept ON C.dept_Id = dept.dept_Id
        JOIN Users as U ON C.facultyMem_Id = U.user_id
        WHERE C.capacity > 0
        ORDER BY enrolled_count DESC, popularity_percentage DESC
        LIMIT %s;
        """
        self.cursor.execute(query, (self.limit,))
        results = self.cursor.fetchall()
        return results

    def processData(self):
        results = self.getData()
        processed = []
        for i, row in enumerate(results, 1):
            processed.append({
                "rank": i,
                "course_id": row[0],
                "courseName": row[1],
                "department": row[2],
                "instructor": row[3],
                "capacity": row[4],
                "availableSeats": row[5],
                "enrolledCount": row[6],
                "popularityPercentage": row[7]
            })
        return processed

    def outputData(self):
        return self.processData()


class HighCapacityCoursesReport(GenerateReport):
    def __init__(self, department_name=None, threshold_percentage=90):
        self.db = dbconfig()
        self.conn = self.db.get_db_connection()
        self.cursor = self.conn.cursor()
        self.department_name = department_name
        self.threshold_percentage = threshold_percentage

    def getData(self):
        # Get courses above the capacity threshold
        if self.department_name:
            query = """
            SELECT C.course_id, C.courseName, dept.deptName,
                   CONCAT(U.firstName, ' ', U.lastName) as instructor_name,
                   C.capacity, C.availableSeats,
                   (C.capacity - C.availableSeats) as enrolled_count,
                   ROUND(((C.capacity - C.availableSeats) / C.capacity) * 100, 2) as utilization_percentage
            FROM Course AS C
            JOIN Department as dept ON C.dept_Id = dept.dept_Id
            JOIN Users as U ON C.facultyMem_Id = U.user_id
            WHERE dept.deptName LIKE %s
            AND C.capacity > 0
            AND ((C.capacity - C.availableSeats) / C.capacity) * 100 >= %s
            ORDER BY utilization_percentage DESC;
            """
            self.cursor.execute(query, (f"%{self.department_name}%", self.threshold_percentage))
        else:
            query = """
            SELECT C.course_id, C.courseName, dept.deptName,
                   CONCAT(U.firstName, ' ', U.lastName) as instructor_name,
                   C.capacity, C.availableSeats,
                   (C.capacity - C.availableSeats) as enrolled_count,
                   ROUND(((C.capacity - C.availableSeats) / C.capacity) * 100, 2) as utilization_percentage
            FROM Course AS C
            JOIN Department as dept ON C.dept_Id = dept.dept_Id
            JOIN Users as U ON C.facultyMem_Id = U.user_id
            WHERE C.capacity > 0
            AND ((C.capacity - C.availableSeats) / C.capacity) * 100 >= %s
            ORDER BY utilization_percentage DESC;
            """
            self.cursor.execute(query, (self.threshold_percentage,))
        results = self.cursor.fetchall()
        return results

    def processData(self):
        results = self.getData()
        processed = []
        for row in results:
            processed.append({
                "course_id": row[0],
                "courseName": row[1],
                "department": row[2],
                "instructor": row[3],
                "capacity": row[4],
                "availableSeats": row[5],
                "enrolledCount": row[6],
                "utilizationPercentage": row[7],
                "status": "Critical" if row[7] >= 95 else "High"
            })
        return processed

    def outputData(self):
        return self.processData()


class DepartmentAnalyticsReport(GenerateReport):
    def __init__(self, semester=None):
        self.db = dbconfig()
        self.conn = self.db.get_db_connection()
        self.cursor = self.conn.cursor()
        self.semester = semester

    def getData(self):
        # Get comprehensive department analytics
        query = """
        SELECT 
            dept.dept_Id,
            dept.deptName,
            COUNT(C.course_id) as total_courses,
            SUM(C.capacity) as total_capacity,
            SUM(C.capacity - C.availableSeats) as total_enrolled,
            SUM(C.availableSeats) as total_available,
            ROUND(AVG((C.capacity - C.availableSeats) / C.capacity * 100), 2) as avg_utilization,
            COUNT(DISTINCT C.facultyMem_Id) as faculty_count
        FROM Department dept
        LEFT JOIN Course C ON dept.dept_Id = C.dept_Id
        WHERE C.capacity > 0
        GROUP BY dept.dept_Id, dept.deptName
        ORDER BY avg_utilization DESC;
        """
        self.cursor.execute(query)
        results = self.cursor.fetchall()
        return results

    def processData(self):
        results = self.getData()
        processed = []
        for row in results:
            processed.append({
                "departmentId": row[0],
                "departmentName": row[1],
                "totalCourses": row[2] or 0,
                "totalCapacity": row[3] or 0,
                "totalEnrolled": row[4] or 0,
                "totalAvailable": row[5] or 0,
                "avgUtilization": row[6] or 0,
                "facultyCount": row[7] or 0
            })
        return processed

    def outputData(self):
        return self.processData()


class ReportExporter:
    @staticmethod
    def export_to_json(data, filename=None):
        """Export report data to JSON format"""
        if not filename:
            filename = f"report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        
        export_data = {
            "generated_at": datetime.now().isoformat(),
            "data": data
        }
        
        return json.dumps(export_data, indent=2, default=str)
    
    @staticmethod
    def export_to_html_table(data, title="Report"):
        """Export report data to HTML table format"""
        if not data:
            return f"<h2>{title}</h2><p>No data available</p>"
        
        # Get column headers from the first item
        headers = list(data[0].keys()) if data else []
        
        html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>{title}</title>
            <style>
                body {{ font-family: Arial, sans-serif; margin: 20px; }}
                table {{ border-collapse: collapse; width: 100%; }}
                th, td {{ border: 1px solid #ddd; padding: 8px; text-align: left; }}
                th {{ background-color: #f2f2f2; }}
                .high-capacity {{ background-color: #ffebee; }}
                .critical-capacity {{ background-color: #ffcdd2; }}
                h1 {{ color: #333; }}
                .report-meta {{ color: #666; font-size: 0.9em; margin-bottom: 20px; }}
            </style>
        </head>
        <body>
            <h1>{title}</h1>
            <div class="report-meta">Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</div>
            <table>
                <thead>
                    <tr>
                        {"".join(f"<th>{header.replace('_', ' ').title()}</th>" for header in headers)}
                    </tr>
                </thead>
                <tbody>
        """
        
        for row in data:
            # Add CSS class based on utilization percentage if available
            css_class = ""
            if 'utilizationPercentage' in row:
                if row['utilizationPercentage'] >= 95:
                    css_class = ' class="critical-capacity"'
                elif row['utilizationPercentage'] >= 90:
                    css_class = ' class="high-capacity"'
            
            html += f'<tr{css_class}>'
            for header in headers:
                value = row.get(header, "")
                if isinstance(value, float):
                    value = f"{value:.2f}"
                html += f"<td>{value}</td>"
            html += "</tr>"
        
        html += """
                </tbody>
            </table>
        </body>
        </html>
        """
        
        return html