from backend.department import DepartmentFactory , Department

class DepartmentService:
    def __init__(self,db):
        self.db = db
        self.factory = DepartmentFactory()
        

    def addDepartment(self,name):
        conn = self.db.get_db_connection()
        cursor = conn.cursor()

        try:
            # Check Duplicates
            if Department.exists(cursor, name):
                return {"status" : "error", "message" : "Department already exists."}, 400
            department = self.factory.create_department(name)
            dept_id = department.save(cursor, conn)

            return {
                "status" : "success",
                "id": dept_id,
                "name": name,
                "message": "Department added successfully"
            }, 200
        except Exception as e:
            return {"status": "error","message": str(e)}, 500
        
        finally:
            cursor.close() #close the connection after all done
            conn.close()

        



