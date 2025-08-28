from backend.user import Admin, AdminFactory

class AdminService:
    def __init__(self, db):
        self.db = db

    def add_admin(self, firstName, lastName, email, mobileNo):
        conn = self.db.get_db_connection()
        cursor = conn.cursor()

        try:
            if Admin.exist(self.db, email):
                return {"status": "Error", "message": "There is an admin already exist with that email"}
            
            admin_factory = AdminFactory()
            admin = admin_factory.create_user(self.db, firstName, lastName, email, mobileNo)
            admin.adduser()
            return {"status": "Success", "message": "Admin added successfully"}
        except Exception as e:
                return {"status": "Error", "message": str(e)}
        finally:
            cursor.close()
            conn.close()