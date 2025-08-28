from abc import ABC, abstractmethod
# Department Factory
class DefaultDepartmentFactory(ABC):
    @abstractmethod
    def create_department(self, name):
        pass

class Department():
    def __init__(self, name):
        self.name = name

    def save(self, cursor, conn):
        cursor.execute("INSERT INTO Department (deptName) VALUES (%s)", (self.name,))
        conn.commit()
        self.id = cursor.lastrowid if hasattr(cursor, 'lastrowid') else cursor.lastrowid
        return self.id

    @staticmethod
    def exists(cursor, name):
        cursor.execute("SELECT * FROM Department WHERE deptName = %s", (name,))
        return cursor.fetchone() is not None

class DepartmentFactory(DefaultDepartmentFactory):
    def create_department(self, name):
        return Department(name)

