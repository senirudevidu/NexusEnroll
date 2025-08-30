from backend.course import Course


class CourseService:
    def __init__(self, db):
        self.db = db
        self.Course = Course(self.db)

    def addCourse(self,courseName,description,capacity,availableSeats,credits,degree_ID,dept_Id,preReqYear,allowedDeptID,facultyMem_Id,addedBy):
        conn = self.db.get_db_connection()
        cursor = conn.cursor()

        try:
            result = self.Course.addCourse(cursor,conn,courseName,description,capacity,availableSeats,credits,degree_ID,dept_Id,preReqYear,allowedDeptID,facultyMem_Id,addedBy)
            return result
        except Exception as e:
            conn.rollback()
            return {"status": "Error", "message": str(e)}
        finally:
            cursor.close()
            conn.close()
    
    def getAllCourses(self):
        return self.Course.getAllCourses()