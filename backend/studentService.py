from backend.user import Student, StudentFactory

class StudentService:
    def __init__(self,db):
        self.db = db
        self.factory = StudentFactory()

    def addStudent(self,firstName,lastName,email,mobileNo,yearOfStudy,degreeName):
        conn = self.db.get_db_connection()
        cursor = conn.cursor()

        try:
            if Student.exist(self.db, email):
                return {"status": "Error" , "message":"There is a student already exist with that email"}

            student = self.factory.create_user(self.db, firstName, lastName, email, mobileNo, yearOfStudy, degreeName)
            student_id = student.adduser()

            return {
                "status": "Success",
                "id": student_id,
                "firstName": firstName,
                "lastName": lastName,
                "email": email,
                "mobileNo": mobileNo,
                "yearOfStudy": yearOfStudy,
                "degreeName": degreeName,
                "message": "Student added successfully"
            }, 200
        except Exception as e:
            return {"status": "Error" , "message": str(e)}, 500

        finally:
            cursor.close()
            conn.close()