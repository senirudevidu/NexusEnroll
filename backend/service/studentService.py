from backend.dal.user import Student, StudentFactory

class StudentService:
    def __init__(self,db):
        self.db = db
        self.factory = StudentFactory()
        self.student = Student(self.db)

    def addStudent(self,firstName,lastName,email,mobileNo,yearOfStudy,degreeID):
        conn = self.db.get_db_connection()
        cursor = conn.cursor()

        try:
            if Student.exist(self.db, email):
                return {"status": "Error" , "message":"There is a student already exist with that email"}, 400

            student = self.factory.create_user(self.db, firstName, lastName, email, mobileNo, yearOfStudy, degreeID)
            result = student.adduser()
            if result["status"] == "Success":
                return {
                    "status": "Success",
                    "id": result.get("id"),
                    "firstName": firstName,
                    "lastName": lastName,
                    "email": email,
                    "mobileNo": mobileNo,
                    "yearOfStudy": yearOfStudy,
                    "degreeID": degreeID,
                    "message": "Student added successfully"
                }, 200
            else:
                return result, 500
        except Exception as e:
            return {"status": "Error" , "message": str(e)}, 500

        finally:
            cursor.close()
            conn.close()

    def displayStudents(self):
        conn = self.db.get_db_connection()
        cursor = conn.cursor()

        try:
            students = self.student.displayStudents()
            return students
        except Exception as e:
            return {"status": "Error", "message": str(e)}, 500
        finally:
            cursor.close()
            conn.close()
    
    def updateStudent(self, user_id, firstName=None, lastName=None, email=None, mobileNo=None, yearOfStudy=None, degreeID=None):
        try:
            result = self.student.update_user(user_id, firstName, lastName, email, mobileNo, yearOfStudy, degreeID)
            if result["status"] == "Success":
                return result, 200
            else:
                return result, 400
        except Exception as e:
            return {"status": "Error", "message": str(e)}, 500
    
    def deactivateStudent(self, user_id):
        try:
            result = self.student.deactivate_user(user_id)
            if result["status"] == "Success":
                return result, 200
            else:
                return result, 400
        except Exception as e:
            return {"status": "Error", "message": str(e)}, 500