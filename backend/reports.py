from abc import ABC, abstractmethod
from backend.dbconfig import dbconfig
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
    def __init__(self, dept_id):
        self.db = dbconfig()
        self.conn = self.db.get_db_connection()
        self.cursor = self.conn.cursor()
        self.dept_id = dept_id

    def getData(self):
        # Execute query and fetch enrollment statistics data
        query = """
        SELECT C.courseName, dept.deptName, C.availableSeats, C.capacity
        FROM Course AS C
        JOIN Department as dept ON C.dept_Id = dept.dept_Id
        WHERE dept.dept_Id = %s;
        """
        self.cursor.execute(query, (self.dept_id,))
        courses = self.cursor.fetchall()
        return courses

    def processData(self):
        # Logic to process enrollment statistics data
        courses = self.getData()
        processed_data = []
        for course in courses:
            processed_data.append({
                "courseName": course[0],
                "department": course[1],
                "availableSeats": course[2],
                "capacity": course[3],
                "enrolledPercentage": (course[2] / course[3] * 100) if course[3] > 0 else 0,
                "status": "Full" if course[2] < course[3] else "Open"
            })
        return processed_data

    def outputData(self):
        # Logic to output the processed enrollment statistics data
        departmentCourses = self.processData()
        return departmentCourses
    

class FacultyWorkloadReport(GenerateReport):
    def __init__(self, faculty_id):
        self.db = dbconfig()
        self.conn = self.db.get_db_connection()
        self.cursor = self.conn.cursor()
        self.faculty_id = faculty_id

    def getData(self):
        # Execute query and fetch faculty workload data
        query = """
            SELECT COUNT(*) AS numberOfCourses, 
            SUM(C.availableSeats) AS totalStudents
            FROM Course AS C
            JOIN FacultyStaff AS f ON C.facultyMem_Id = f.facultyMem_Id
            WHERE f.facultyMem_Id = %s;
            """
        try:
            self.cursor.execute(query, (self.faculty_id,))
            result = self.cursor.fetchone()
            return {
                "numberOfCourses": result[0] or 0,
                "totalStudents": result[1] or 0
            }
        except Exception as e:
            return {"error": str(e)}

    def processData(self):
        return self.getData()

    def outputData(self):
        # Logic to output the processed faculty workload data
        facultyCourses = self.processData()
        return facultyCourses