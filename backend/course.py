class Course():
    def __init__(self, db):
        self.db = db        

    def addCourse(self,courseName,description,capacity,availableSeats,credits,degree_ID,dept_Id,preReqYear,allowedDeptID,facultyMem_Id,addedBy):
        conn = self.db.get_db_connection()
        cursor = conn.cursor()

        try:
            query = "INSERT INTO Course (courseName,description,capacity,availableSeats,credits,degree_ID,dept_Id,preReqYear,allowedDeptID,facultyMem_Id,addedBy)" \
            "VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
            cursor.execute(query, (courseName,description,capacity,availableSeats,credits,degree_ID,dept_Id,preReqYear,allowedDeptID,facultyMem_Id,addedBy))
            conn.commit()
            return {"status": "Success", "message": "Course added successfully"}
        except Exception as e:
            conn.rollback()
            return {"status": "Error", "message": str(e)}
        finally:
            cursor.close()
            conn.close()