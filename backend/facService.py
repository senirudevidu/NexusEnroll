from backend.user import FacultyMemberFactory,FacultyMember

class FacultyService:
    def __init__(self, db):
        self.db = db

    def add_faculty_member(self, firstName, lastName, email, mobileNo, role):
        conn = self.db.get_db_connection()
        cursor = conn.cursor()

        factory = FacultyMemberFactory()

        try:
            if FacultyMember.exist(self.db, email):
                return {"status": "Error", "message": "Faculty member with this email already exists."}
            faculty_member = factory.create_user(self.db, firstName, lastName, email, mobileNo, role)
            return faculty_member.adduser()
        
        except Exception as e:
            return {"status": "Error", "message": str(e)}
        finally:
            cursor.close()
            conn.close()
