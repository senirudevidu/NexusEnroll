# User registration
from abc import ABC, abstractmethod
from flask import request


class User(ABC):
    @abstractmethod
    def adduser(self):
        pass

    def exists():
        pass

class Student(User):
    def __init__(self,db,firstName,lastName,email,mobileNo,yearOfStudy,degreeName):
        self.db = db
        self.firstName = firstName
        self.lastName = lastName
        self.email = email
        self.mobileNo = mobileNo
        self.yearOfStudy = yearOfStudy
        self.degreeName = degreeName

    def getDegreeId(self):
        conn = self.db.get_db_connection()
        cursor = conn.cursor()
        query = "SELECT Degree_ID FROM Degree WHERE name=%s"
        cursor.execute(query, (self.degreeName,))
        result = cursor.fetchone()
        cursor.close()
        conn.close()
        if result:
            return result[0]
        else:
            return {"status": "Error", "message": "Degree not found"}
        
    def adduser(self):
        conn = self.db.get_db_connection()
        cursor = conn.cursor()
        self.degreeId = self.getDegreeId()

        # If degreeId is an error dict, raise an exception
        if isinstance(self.degreeId, dict):
            cursor.close()
            conn.close()
            raise Exception(self.degreeId.get("message", "Degree not found"))

        try:
            # Insert into Users table
            query = "INSERT INTO Users (firstName, lastName, mobileNo, email) VALUES (%s, %s, %s, %s)"
            cursor.execute(query, (self.firstName, self.lastName, self.mobileNo, self.email))
            user_id = cursor.lastrowid  # Get the last inserted user ID
            conn.commit()

            # Insert into Students table, linking to user_id
            query2 = "INSERT INTO Students (user_id, YearOfStudy, degree_ID) VALUES (%s, %s, %s)"
            cursor.execute(query2, (user_id, self.yearOfStudy, self.degreeId))
            conn.commit()
            result = {"status": "Success", "message": "Student added successfully"}
        except Exception as e:
                result = {"status": "Error", "message": str(e)}
        finally:
            cursor.close()
            conn.close()
        return result

    @staticmethod
    def exist(db, email):
        conn = db.get_db_connection()
        cursor = conn.cursor()
        query = "SELECT user_id FROM Users WHERE email = %s"
        cursor.execute(query, (email,))
        result = cursor.fetchone()
        cursor.close()
        conn.close()
        return result is not None

class FacultyMember(User):
    def __init__(self,db,firstName,lastName,email,mobileNo,role):
        self.db = db
        self.firstName = firstName
        self.lastName = lastName
        self.email = email
        self.mobileNo = mobileNo
        self.role = role
    
    def adduser(self):
        conn = self.db.get_db_connection()
        cursor = conn.cursor()
        
        # Insert into Users table
        query = "INSERT INTO Users (firstName, lastName, mobileNo, email) VALUES (%s, %s, %s, %s)"
        cursor.execute(query, (self.firstName, self.lastName, self.mobileNo, self.email))
        user_id = cursor.lastrowid  # Get the last inserted user ID
        conn.commit()

        # Insert into FacultyMembers table, linking to user_id
        query2 = "INSERT INTO FacultyStaff (facultyMem_Id, role) VALUES (%s, %s)"
        cursor.execute(query2, (user_id, self.role))
        conn.commit()
        
        return {"status": "Success", "message": "Faculty member added successfully"}

    @staticmethod
    def exist(db, email):
        conn = db.get_db_connection()
        cursor = conn.cursor()
        query = "SELECT user_id FROM Users WHERE email = %s"
        cursor.execute(query, (email,))
        result = cursor.fetchone()
        cursor.close()
        conn.close()
        return result is not None

class Admin(User):
    def __init__(self,db,firstName,lastName,email,mobileNo):
        self.db = db
        self.firstName = firstName
        self.lastName = lastName
        self.email = email
        self.mobileNo = mobileNo
    
    def adduser(self):
        conn = self.db.get_db_connection()
        cursor = conn.cursor()

    # Insert into Users table
        query = "INSERT INTO Users (firstName, lastName, mobileNo, email) VALUES (%s, %s, %s, %s)"
        cursor.execute(query, (self.firstName, self.lastName, self.mobileNo, self.email))
        user_id = cursor.lastrowid  # Get the last inserted user ID
        conn.commit()

        query2 = "INSERT INTO Admin (admin_id) VALUES (%s)"
        cursor.execute(query2, (user_id,))
        conn.commit()

        return {"status": "Success", "message": "Admin added successfully"}
    
    @staticmethod
    def exist(db, email):
        conn = db.get_db_connection()
        cursor = conn.cursor()
        query = "SELECT user_id FROM Users WHERE email = %s"
        cursor.execute(query, (email,))
        result = cursor.fetchone()
        cursor.close()
        conn.close()
        return result is not None



class UserFactory(ABC):
    def create_user(self):
        pass

class StudentFactory(UserFactory):
    def create_user(self, db, firstName, lastName, email, mobileNo, yearOfStudy, degreeName):
        return Student(db, firstName, lastName, email, mobileNo, yearOfStudy, degreeName)

class FacultyMemberFactory(UserFactory):
    def create_user(self, db, firstName, lastName, email, mobileNo, role):
        return FacultyMember(db, firstName, lastName, email, mobileNo, role)

class AdminFactory(UserFactory):
    def create_user(self,db,firstName,lastName,email,mobileNo):
        return Admin(db,firstName,lastName,email,mobileNo)
