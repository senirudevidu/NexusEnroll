class Course():
    def __init__(self, db):
        self.db = db        

    def addCourse(self,cursor,conn,courseName,description,capacity,availableSeats,credits,degree_ID,dept_Id,preReqYear,allowedDeptID,facultyMem_Id,addedBy):
        query = """INSERT INTO Course (courseName,description,capacity,availableSeats,credits,degree_ID,dept_Id,preReqYear,allowedDeptID,facultyMem_Id,addedBy)
            VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"""
        cursor.execute(query, (courseName,description,capacity,availableSeats,credits,degree_ID,dept_Id,preReqYear,allowedDeptID,facultyMem_Id,addedBy))
        conn.commit()
        return {"status": "Success", "message": "Course added successfully"}
    
    def getAllCourses(self):
        conn = self.db.get_db_connection()
        cursor = conn.cursor()
        try:
            query = "SELECT courseName, FROM Course"
            cursor.execute(query)
            courses = cursor.fetchall()
        except Exception as e:
            print("Error fetching courses:", e)
        finally:
            cursor.close()
            conn.close()
        return courses