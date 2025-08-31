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

    def get_faculty_members(self):
        conn = self.db.get_db_connection()
        cursor = conn.cursor()
        try:
            faculty_member = FacultyMember(self.db)
            result = faculty_member.get_faculty_members(cursor)
            return result
        except Exception as e:
            return {"status": "Error", "message": str(e)}
        finally:
            cursor.close()
            conn.close()
    
    def updateFacultyMember(self, user_id, firstName=None, lastName=None, email=None, mobileNo=None, role=None):
        try:
            faculty_member = FacultyMember(self.db)
            result = faculty_member.update_user(user_id, firstName, lastName, email, mobileNo, role)
            if result["status"] == "Success":
                return result, 200
            else:
                return result, 400
        except Exception as e:
            return {"status": "Error", "message": str(e)}, 500
    
    def deactivateFacultyMember(self, user_id):
        try:
            faculty_member = FacultyMember(self.db)
            result = faculty_member.deactivate_user(user_id)
            if result["status"] == "Success":
                return result, 200
            else:
                return result, 400
        except Exception as e:
            return {"status": "Error", "message": str(e)}, 500