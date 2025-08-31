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
        conn = self.db.get_db_connection()
        cursor = conn.cursor()

        try:
            result = self.Course.getAllCourses(cursor)
            return result
        except Exception as e:
            return {"status": "Error", "message": str(e)}
        finally:
            cursor.close()
            conn.close()

    def getCourseById(self, course_id):
        conn = self.db.get_db_connection()
        cursor = conn.cursor()

        try:
            result = self.Course.getCourseById(cursor, course_id)
            return result
        except Exception as e:
            return {"status": "Error", "message": str(e)}
        finally:
            cursor.close()
            conn.close()

    def updateCourse(self, course_id, courseName, description, capacity, availableSeats, credits, degree_ID, dept_Id, preReqYear, allowedDeptID, facultyMem_Id):
        conn = self.db.get_db_connection()
        cursor = conn.cursor()

        try:
            result = self.Course.updateCourse(cursor, conn, course_id, courseName, description, capacity, availableSeats, credits, degree_ID, dept_Id, preReqYear, allowedDeptID, facultyMem_Id)
            return result
        except Exception as e:
            conn.rollback()
            return {"status": "Error", "message": str(e)}
        finally:
            cursor.close()
            conn.close()

    def deleteCourse(self, course_id):
        conn = self.db.get_db_connection()
        cursor = conn.cursor()

        try:
            result = self.Course.deleteCourse(cursor, conn, course_id)
            return result
        except Exception as e:
            conn.rollback()
            return {"status": "Error", "message": str(e)}
        finally:
            cursor.close()
            conn.close()
