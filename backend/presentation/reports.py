from abc import ABC, abstractmethod
from backend.dal.dbconfig import dbconfig
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
    def __init__(self):
        self.db = dbconfig()
        self.conn = self.db.get_db_connection()
        self.cursor = self.conn.cursor()

    def getData(self):
        # Execute query and fetch faculty workload data for all faculty
        query = """
            SELECT f.facultyMem_Id, d.deptName, COUNT(C.course_Id) AS numberOfCourses,
                   SUM(C.capacity - C.availableSeats) AS numberOfStudents
            FROM FacultyStaff AS f
            LEFT JOIN Course AS C ON f.facultyMem_Id = C.facultyMem_Id
            JOIN Department AS d ON C.dept_Id = d.dept_Id
            GROUP BY f.facultyMem_Id, d.deptName;
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
                "numberOfCourses": row[2] or 0,
                "numberOfStudents": row[3] or 0
            })
        return processed

    def outputData(self):
        # Output the processed faculty workload data for all faculty
        return self.processData()