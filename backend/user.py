# User registration
from abc import ABC, abstractmethod
from flask import request


class User(ABC):
    @abstractmethod
    def adduser(self):
        pass

class Student(User):
    def adduser(self):
        if request.method == 'POST':
            self.firstName = request.form['firstName']
            self.lastName = request.form['lastName']
            self.email = request.form['email']
            self.mobileNo = request.form['mobileNo']
            self.yearOfStudy = request.form['yearofstudy']
            # degree id
            return f"Student {self.firstName} {self.lastName} added"
        return "Invalid request"

class FacultyMember(User):
    def adduser(self):
        if request.method == 'POST':
            self.firstName = request.form['firstName']
            self.lastName = request.form['lastName']
            self.email = request.form['email']
            self.mobileNo = request.form['mobileNo']
            self.role = request.form['role']
            return f"Faculty {self.firstName} {self.lastName} added"
        return "Invalid request"

class Admin(User):
    def adduser(self):
        if request.method == 'POST':
            self.firstName = request.form['firstName']
            self.lastName = request.form['lastName']
            self.email = request.form['email']
            self.mobileNo = request.form['mobileNo']
            return f"Admin {self.firstName} {self.lastName} added"
        return "Invalid request"

class UserFactory(ABC):
    def create_user(self):
        pass

class StudentFactory(UserFactory):
    def create_user(self):
        return Student()

class FacultyMemberFactory(UserFactory):
    def create_user(self):
        return FacultyMember()

class AdminFactory(UserFactory):
    def create_user(self):
        return Admin()
    