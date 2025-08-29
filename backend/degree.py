
class Degree():
    def __init__(self,db):
        self.db = db

    def getDeptId(self,deptName):
        conn = self.db.get_db_connection()
        cursor = conn.cursor()
        query = "SELECT dept_Id FROM Department WHERE deptName=%s"
        cursor.execute(query, (deptName,))
        result = cursor.fetchone()
        cursor.close()
        conn.close()
        if result:
            return result[0]
        else:
            return {"status": "Error", "message": "Department not found"}

    def addDegree(self, name, credit, department_name):
        conn = self.db.get_db_connection()
        cursor = conn.cursor()
        try:
            self.deptID = self.getDeptId(department_name)
            if isinstance(self.deptID, dict):
                return self.deptID
            query = "INSERT INTO Degree (name, credit, dept_Id) VALUES (%s, %s, %s)"
            cursor.execute(query, (name, credit, self.deptID))
            conn.commit()
            return {"status": "Success", "message": "Degree added successfully"}
        except Exception as e:
            conn.rollback()
            return {"status": "Error", "message": str(e)}
        finally:
            cursor.close()
            conn.close()