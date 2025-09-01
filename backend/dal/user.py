# User registration
from abc import ABC, abstractmethod
from flask import request
from backend.dal.dbconfig import dbconfig


class User(ABC):
    @abstractmethod
    def adduser(self):
        pass

    def exists():
        pass
    
    @abstractmethod
    def update_user(self):
        pass
    
    @abstractmethod
    def deactivate_user(self):
        pass

class Student(User):
    def __init__(self,db,firstName=None,lastName=None,email=None,mobileNo=None,yearOfStudy=None,degreeID=None):
        self.db = db
        self.firstName = firstName
        self.lastName = lastName
        self.email = email
        self.mobileNo = mobileNo
        self.yearOfStudy = yearOfStudy
        self.degreeID = degreeID

    # def getDegreeId(self):
    #     conn = self.db.get_db_connection()
    #     cursor = conn.cursor()
    #     query = "SELECT Degree_ID FROM Degree WHERE name=%s"
    #     cursor.execute(query, (self.degreeName,))
    #     result = cursor.fetchone()
    #     cursor.close()
    #     conn.close()
    #     if result:
    #         return result[0]
    #     else:
    #         return {"status": "Error", "message": "Degree not found"}
        
    def adduser(self):
        conn = self.db.get_db_connection()
        cursor = conn.cursor()
        try:
            # Insert into Users table
            query = "INSERT INTO Users (firstName, lastName, mobileNo, email,module) VALUES (%s, %s, %s, %s,%s)"
            cursor.execute(query, (self.firstName, self.lastName, self.mobileNo, self.email,"student"))
            user_id = cursor.lastrowid  # Get the last inserted user ID
            conn.commit()

            # Insert into Students table, linking to user_id
            query2 = "INSERT INTO Student (student_Id, YearOfStudy, degree_ID) VALUES (%s, %s, %s)"
            cursor.execute(query2, (user_id, self.yearOfStudy, self.degreeID))
            conn.commit()
            result = {"status": "Success", "message": "Student added successfully", "id": user_id}
        except Exception as e:
            result = {"status": "Error", "message": str(e)}
        finally:
            cursor.close()
            conn.close()
        return result

    
    def displayStudents(self):
        conn = self.db.get_db_connection()
        cursor = conn.cursor()
        query = """
            SELECT u.user_id,u.firstName,u.lastName,u.accountStatus,s.YearOfStudy,d.name
            FROM Users as u
            JOIN Student as s ON u.user_id = s.student_Id
            JOIN Degree as d on s.degree_ID = d.degree_ID;
            """
        cursor.execute(query)
        result = cursor.fetchall()
        cursor.close()
        conn.close()
        return result
        
    def update_user(self, user_id, firstName=None, lastName=None, email=None, mobileNo=None, yearOfStudy=None, degreeID=None):
        conn = self.db.get_db_connection()
        cursor = conn.cursor()
        try:
            # Check if user exists
            cursor.execute("SELECT user_id FROM Users WHERE user_id = %s", (user_id,))
            if not cursor.fetchone():
                return {"status": "Error", "message": "User not found"}
            
            # Update Users table
            update_fields = []
            update_values = []
            
            if firstName is not None:
                update_fields.append("firstName = %s")
                update_values.append(firstName)
            if lastName is not None:
                update_fields.append("lastName = %s")
                update_values.append(lastName)
            if email is not None:
                update_fields.append("email = %s")
                update_values.append(email)
            if mobileNo is not None:
                update_fields.append("mobileNo = %s")
                update_values.append(mobileNo)
            
            if update_fields:
                query = f"UPDATE Users SET {', '.join(update_fields)} WHERE user_id = %s"
                update_values.append(user_id)
                cursor.execute(query, tuple(update_values))
                conn.commit()
            
            # Update Student-specific fields
            student_update_fields = []
            student_update_values = []
            
            if yearOfStudy is not None:
                student_update_fields.append("YearOfStudy = %s")
                student_update_values.append(yearOfStudy)
            if degreeID is not None:
                student_update_fields.append("degree_ID = %s")
                student_update_values.append(degreeID)
            
            if student_update_fields:
                query2 = f"UPDATE Student SET {', '.join(student_update_fields)} WHERE student_Id = %s"
                student_update_values.append(user_id)
                cursor.execute(query2, tuple(student_update_values))
                conn.commit()
            
            result = {"status": "Success", "message": "Student updated successfully"}
        except Exception as e:
            result = {"status": "Error", "message": str(e)}
        finally:
            cursor.close()
            conn.close()
        return result
    
    def deactivate_user(self, user_id):
        conn = self.db.get_db_connection()
        cursor = conn.cursor()
        try:
            # Check if user exists
            cursor.execute("SELECT user_id, accountStatus FROM Users WHERE user_id = %s", (user_id,))
            user = cursor.fetchone()
            if not user:
                return {"status": "Error", "message": "User not found"}
            
            current_status = user[1]
            new_status = "inactive" if current_status == "active" else "active"
            
            # Update account status
            query = "UPDATE Users SET accountStatus = %s WHERE user_id = %s"
            cursor.execute(query, (new_status, user_id))
            conn.commit()
            
            action = "deactivated" if new_status == "inactive" else "activated"
            result = {"status": "Success", "message": f"Student {action} successfully", "new_status": new_status}
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
    def __init__(self,db=None,firstName=None,lastName=None,email=None,mobileNo=None,role=None):
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
        query = "INSERT INTO Users (firstName, lastName, mobileNo, email,module) VALUES (%s, %s, %s, %s,%s)"
        cursor.execute(query, (self.firstName, self.lastName, self.mobileNo, self.email,"faculty"))
        user_id = cursor.lastrowid  # Get the last inserted user ID
        conn.commit()

        # Insert into FacultyMembers table, linking to user_id
        query2 = "INSERT INTO FacultyStaff (facultyMem_Id, role) VALUES (%s, %s)"
        cursor.execute(query2, (user_id, self.role))
        conn.commit()
        
        return {"status": "Success", "message": "Faculty member added successfully"}

    def update_user(self, user_id, firstName=None, lastName=None, email=None, mobileNo=None, role=None):
        conn = self.db.get_db_connection()
        cursor = conn.cursor()
        try:
            # Check if user exists
            cursor.execute("SELECT user_id FROM Users WHERE user_id = %s", (user_id,))
            if not cursor.fetchone():
                return {"status": "Error", "message": "User not found"}
            
            # Update Users table
            update_fields = []
            update_values = []
            
            if firstName is not None:
                update_fields.append("firstName = %s")
                update_values.append(firstName)
            if lastName is not None:
                update_fields.append("lastName = %s")
                update_values.append(lastName)
            if email is not None:
                update_fields.append("email = %s")
                update_values.append(email)
            if mobileNo is not None:
                update_fields.append("mobileNo = %s")
                update_values.append(mobileNo)
            
            if update_fields:
                query = f"UPDATE Users SET {', '.join(update_fields)} WHERE user_id = %s"
                update_values.append(user_id)
                cursor.execute(query, tuple(update_values))
                conn.commit()
            
            # Update Faculty-specific fields
            if role is not None:
                query2 = "UPDATE FacultyStaff SET role = %s WHERE facultyMem_Id = %s"
                cursor.execute(query2, (role, user_id))
                conn.commit()
            
            result = {"status": "Success", "message": "Faculty member updated successfully"}
        except Exception as e:
            result = {"status": "Error", "message": str(e)}
        finally:
            cursor.close()
            conn.close()
        return result
    
    def deactivate_user(self, user_id):
        conn = self.db.get_db_connection()
        cursor = conn.cursor()
        try:
            # Check if user exists
            cursor.execute("SELECT user_id, accountStatus FROM Users WHERE user_id = %s", (user_id,))
            user = cursor.fetchone()
            if not user:
                return {"status": "Error", "message": "User not found"}
            
            current_status = user[1]
            new_status = "inactive" if current_status == "active" else "active"
            
            # Update account status
            query = "UPDATE Users SET accountStatus = %s WHERE user_id = %s"
            cursor.execute(query, (new_status, user_id))
            conn.commit()
            
            action = "deactivated" if new_status == "inactive" else "activated"
            result = {"status": "Success", "message": f"Faculty member {action} successfully", "new_status": new_status}
        except Exception as e:
            result = {"status": "Error", "message": str(e)}
        finally:
            cursor.close()
            conn.close()
        return result

    def get_faculty_members(self,cursor):
        query = """SELECT U.user_id, U.firstName, U.lastName, U.accountStatus, Fac.role
        FROM Users AS U 
        JOIN FacultyStaff AS Fac ON U.user_id = Fac.facultyMem_Id;
        """
        cursor.execute(query)
        result = cursor.fetchall()
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
        query = "INSERT INTO Users (firstName, lastName, mobileNo, email,module) VALUES (%s, %s, %s, %s,%s)"
        cursor.execute(query, (self.firstName, self.lastName, self.mobileNo, self.email,"admin"))
        user_id = cursor.lastrowid  # Get the last inserted user ID
        conn.commit()

        query2 = "INSERT INTO Admin (admin_id) VALUES (%s)"
        cursor.execute(query2, (user_id,))
        conn.commit()

        return {"status": "Success", "message": "Admin added successfully"}
    
    def update_user(self, user_id, firstName=None, lastName=None, email=None, mobileNo=None):
        conn = self.db.get_db_connection()
        cursor = conn.cursor()
        try:
            # Check if user exists
            cursor.execute("SELECT user_id FROM Users WHERE user_id = %s", (user_id,))
            if not cursor.fetchone():
                return {"status": "Error", "message": "User not found"}
            
            # Update Users table
            update_fields = []
            update_values = []
            
            if firstName is not None:
                update_fields.append("firstName = %s")
                update_values.append(firstName)
            if lastName is not None:
                update_fields.append("lastName = %s")
                update_values.append(lastName)
            if email is not None:
                update_fields.append("email = %s")
                update_values.append(email)
            if mobileNo is not None:
                update_fields.append("mobileNo = %s")
                update_values.append(mobileNo)
            
            if update_fields:
                query = f"UPDATE Users SET {', '.join(update_fields)} WHERE user_id = %s"
                update_values.append(user_id)
                cursor.execute(query, tuple(update_values))
                conn.commit()
            
            result = {"status": "Success", "message": "Admin updated successfully"}
        except Exception as e:
            result = {"status": "Error", "message": str(e)}
        finally:
            cursor.close()
            conn.close()
        return result
    
    def deactivate_user(self, user_id):
        conn = self.db.get_db_connection()
        cursor = conn.cursor()
        try:
            # Check if user exists
            cursor.execute("SELECT user_id, accountStatus FROM Users WHERE user_id = %s", (user_id,))
            user = cursor.fetchone()
            if not user:
                return {"status": "Error", "message": "User not found"}
            
            current_status = user[1]
            new_status = "inactive" if current_status == "active" else "active"
            
            # Update account status
            query = "UPDATE Users SET accountStatus = %s WHERE user_id = %s"
            cursor.execute(query, (new_status, user_id))
            conn.commit()
            
            action = "deactivated" if new_status == "inactive" else "activated"
            result = {"status": "Success", "message": f"Admin {action} successfully", "new_status": new_status}
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



class UserFactory(ABC):
    def create_user(self):
        pass

class StudentFactory(UserFactory):
    def create_user(self, db, firstName, lastName, email, mobileNo, yearOfStudy, degreeID):
        return Student(db, firstName, lastName, email, mobileNo, yearOfStudy, degreeID)

class FacultyMemberFactory(UserFactory):
    def create_user(self, db, firstName, lastName, email, mobileNo, role):
        return FacultyMember(db, firstName, lastName, email, mobileNo, role)

class AdminFactory(UserFactory):
    def create_user(self,db,firstName,lastName,email,mobileNo):
        return Admin(db,firstName,lastName,email,mobileNo)

class UserDAL:
    def __init__(self, db=None):
        self.database = dbconfig()
        self.db = self.database.get_db_connection()

    def authenticate(self, username, password,module):
        cursor = self.db.cursor()
        query = """
            SELECT user_id, firstName,lastName,module FROM Users
            WHERE email = %s AND mobileNo = %s AND accountStatus = 'active' AND module = %s
        """
        cursor.execute(query, (username, password,module))
        result = cursor.fetchone()
        cursor.close()
        return result
