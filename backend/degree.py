
class Degree():
    def __init__(self,db):
        self.db = db
        
    def addDegree(self, name, credit, dept_Id):
        conn = self.db.get_db_connection()
        cursor = conn.cursor()
        try:
            query = "INSERT INTO Degree (name, credit, dept_Id) VALUES (%s, %s, %s)"
            cursor.execute(query, (name, credit, dept_Id))
            conn.commit()
            return {"status": "Success", "message": "Degree added successfully"}
        except Exception as e:
            conn.rollback()
            return {"status": "Error", "message": str(e)}
        finally:
            cursor.close()
            conn.close()

    def getDegrees(self,conn,cursor):
        query = 'SELECT degree_ID,name FROM Degree'
        cursor.execute(query)
        degrees = cursor.fetchall()
        cursor.close()
        conn.close()
        return degrees