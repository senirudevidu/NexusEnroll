class Course():
    def __init__(self, db):
        self.db = db        

    def addCourse(self,cursor,conn,courseName,description,capacity,availableSeats,credits,degree_ID,dept_Id,preReqYear,allowedDeptID,facultyMem_Id,addedBy):
        query = """INSERT INTO Course (courseName,description,capacity,availableSeats,credits,degree_ID,dept_Id,preReqYear,allowedDeptID,facultyMem_Id,addedBy)
            VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"""
        cursor.execute(query, (courseName,description,capacity,availableSeats,credits,degree_ID,dept_Id,preReqYear,allowedDeptID,facultyMem_Id,addedBy))
        conn.commit()
        return {"status": "Success", "message": "Course added successfully"}
    
    def getAllCourses(self, cursor):
        query = """
        SELECT C.courseName,U.firstName,U.lastName,dept.deptName,C.availableSeats,C.capacity
        FROM Course AS C
        JOIN Users as U ON C.facultyMem_Id = U.user_id
        JOIN Department as dept ON C.dept_Id = dept.dept_Id
        """
        cursor.execute(query)
        courses = cursor.fetchall()
        return courses