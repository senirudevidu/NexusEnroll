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
        SELECT C.courseName,U.firstName,U.lastName,dept.deptName,C.availableSeats,C.capacity,C.course_id
        FROM Course AS C
        JOIN Users as U ON C.facultyMem_Id = U.user_id
        JOIN Department as dept ON C.dept_Id = dept.dept_Id
        """
        cursor.execute(query)
        courses = cursor.fetchall()
        return courses
    
    def getCourseById(self, cursor, course_id):
        query = """
        SELECT C.course_id, C.courseName, C.description, C.capacity, C.availableSeats, 
               C.credits, C.degree_ID, C.dept_Id, C.preReqYear, C.allowedDeptID, 
               C.facultyMem_Id, C.addedBy
        FROM Course AS C
        WHERE C.course_id = %s
        """
        cursor.execute(query, (course_id,))
        course = cursor.fetchone()
        return course
    
    def updateCourse(self, cursor, conn, course_id, courseName, description, capacity, availableSeats, credits, degree_ID, dept_Id, preReqYear, allowedDeptID, facultyMem_Id):
        query = """
        UPDATE Course 
        SET courseName = %s, description = %s, capacity = %s, availableSeats = %s, 
            credits = %s, degree_ID = %s, dept_Id = %s, preReqYear = %s, 
            allowedDeptID = %s, facultyMem_Id = %s
        WHERE course_id = %s
        """
        cursor.execute(query, (courseName, description, capacity, availableSeats, credits, 
                              degree_ID, dept_Id, preReqYear, allowedDeptID, facultyMem_Id, course_id))
        conn.commit()
        return {"status": "Success", "message": "Course updated successfully"}
    
    def deleteCourse(self, cursor, conn, course_id):
        # Check if course exists first
        check_query = "SELECT course_id FROM Course WHERE course_id = %s"
        cursor.execute(check_query, (course_id,))
        if not cursor.fetchone():
            return {"status": "Error", "message": "Course not found"}
        
        # Delete the course
        delete_query = "DELETE FROM Course WHERE course_id = %s"
        cursor.execute(delete_query, (course_id,))
        conn.commit()
        return {"status": "Success", "message": "Course deleted successfully"}
    
    def searchCourses(self, cursor, department=None, course_number=None, keyword=None, instructor_name=None):
        """
        Search courses with various filters
        """
        query = """
        SELECT C.course_id, C.courseName, C.description, C.capacity, C.availableSeats, 
               C.credits, C.preReqYear, dept.deptName, U.firstName, U.lastName,
               deg.name
        FROM Course AS C
        JOIN Users as U ON C.facultyMem_Id = U.user_id
        JOIN Department as dept ON C.dept_Id = dept.dept_Id
        JOIN Degree as deg ON C.degree_ID = deg.degree_ID
        WHERE 1=1
        """
        
        params = []
        
        # Add department filter
        if department:
            query += " AND dept.deptName LIKE %s"
            params.append(f"%{department}%")
        
        # Add course number filter (assuming course number is part of courseName)
        if course_number:
            query += " AND C.courseName LIKE %s"
            params.append(f"%{course_number}%")
        
        # Add keyword filter (search in course name and description)
        if keyword:
            query += " AND (C.courseName LIKE %s OR C.description LIKE %s)"
            params.append(f"%{keyword}%")
            params.append(f"%{keyword}%")
        
        # Add instructor name filter
        if instructor_name:
            query += " AND (U.firstName LIKE %s OR U.lastName LIKE %s OR CONCAT(U.firstName, ' ', U.lastName) LIKE %s)"
            params.append(f"%{instructor_name}%")
            params.append(f"%{instructor_name}%")
            params.append(f"%{instructor_name}%")
        
        query += " ORDER BY dept.deptName, C.courseName"
        
        cursor.execute(query, params)
        courses = cursor.fetchall()
        return courses
    
    def getCoursesByDepartmentAndInstructor(self, cursor, department, instructor_name):
        """
        Specific use case: Get all courses from a department taught by a specific instructor
        """
        query = """
        SELECT C.course_id, C.courseName, C.description, C.capacity, C.availableSeats, 
               C.credits, C.preReqYear, dept.deptName, U.firstName, U.lastName,
               deg.name
        FROM Course AS C
        JOIN Users as U ON C.facultyMem_Id = U.user_id
        JOIN Department as dept ON C.dept_Id = dept.dept_Id
        JOIN Degree as deg ON C.degree_ID = deg.degree_ID
        WHERE dept.deptName LIKE %s 
        AND (U.firstName LIKE %s OR U.lastName LIKE %s OR CONCAT(U.firstName, ' ', U.lastName) LIKE %s)
        ORDER BY C.courseName
        """
        
        params = [f"%{department}%", f"%{instructor_name}%", f"%{instructor_name}%", f"%{instructor_name}%"]
        cursor.execute(query, params)
        courses = cursor.fetchall()
        return courses