from flask import request
from abc import ABC

class Course(ABC):
    def myCourse(self):
        self.courseName = request.form['courseName']
        self.courseDescription = request.form['courseDescription']
        self.capacity = request.form['capacity']
        self.credits = request.form['credits']
        self.preReqYear = request.form['preReqYear']

        #available seats
        #degreeid
        #deptId
        #allowedDeptId
        #facultymemId
        #addedby
        pass

class ComputerScience(Course):
    def myCourse(self):
        return "CS"
    
class InformationSystem(Course):
    def myCourse(self):
        return "IS"
    
class CourseFactory(ABC):
    def createCourse(self):
        pass

class CSFactory(CourseFactory):
    def createCourse(self):
        return ComputerScience()
    
class ISFactory(CourseFactory):
    def createCourse(self):
        return InformationSystem()
    
