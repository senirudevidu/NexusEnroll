from flask import Flask , request,Blueprint,jsonify
from backend.adminService import AdminService
from backend.dbconfig import dbconfig
from backend.departmentService import DepartmentService
from backend.studentService import StudentService

bp = Blueprint("routes",__name__)

@bp.route('/adddepartment', methods = ['POST'])
def add_department():
    data = request.get_json()
    department_name = data.get("name")

    if not department_name:
        return jsonify({"status":"error","message":"Department name required"}), 400
    
    service = DepartmentService(dbconfig())
    result, status = service.addDepartment(department_name)
    return jsonify(result),status


@bp.route('/addstudent', methods=['POST'])
def add_student():
    data = request.get_json()
    firstName = data.get("firstName")
    lastName = data.get("lastName")
    email = data.get("email")
    mobileNo = data.get("mobileNo")
    yearOfStudy = data.get("yearOfStudy")
    degreeName = data.get("degreeName")

    service = StudentService(dbconfig())
    result, status = service.addStudent(firstName, lastName, email, mobileNo, yearOfStudy, degreeName)
    return jsonify(result), status

@bp.route('/addAdmin', methods=['POST'])
def add_admin():
    data = request.get_json()
    firstName = data.get("firstName")
    lastName = data.get("lastName")
    email = data.get("email")
    mobileNo = data.get("mobileNo")

    service = AdminService(dbconfig())
    result = service.add_admin(firstName, lastName, email, mobileNo)
    return jsonify(result)