from backend.degree import Degree

class DegreeService:
    def __init__(self, db):
        self.db = db
        self.degree = Degree(db)

    def add_degree(self, name, credit, department_name):
        return self.degree.addDegree(name, credit, department_name)

    def get_degrees(self):
        conn = self.db.get_db_connection()
        cursor = conn.cursor()
        degree = Degree(self.db)
        try:
            degrees = degree.getDegrees(conn,cursor)
            return degrees
        except Exception as e:
            return {"status": "Error", "message": str(e)}
        finally:
            cursor.close()
            conn.close()