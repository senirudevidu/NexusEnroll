from flask import Flask , request,Blueprint,jsonify,render_template,session
from backend.adminService import AdminService
from backend.course import Course
from backend.dbconfig import dbconfig
from backend.departmentService import DepartmentService
from backend.facService import FacultyService
from backend.studentService import StudentService
from backend.degree import Degree

bp = Blueprint("routes",__name__)

@bp.route('/addUserForm')
def add_user_form():
    return render_template('addUser.html')

@bp.route('/addStudent', methods=['POST'])
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

@bp.route('/addFacultyMember', methods=['POST'])
def add_faculty_member():
    data = request.get_json()
    firstName = data.get("firstName")
    lastName = data.get("lastName")
    email = data.get("email")
    mobileNo = data.get("mobileNo")
    role = data.get("roleFaculty")

    service = FacultyService(dbconfig())
    result = service.add_faculty_member(firstName, lastName, email, mobileNo, role)
    return jsonify(result)

@bp.route('/course')
def course():
    session['user_id'] = 6  # Set user_id in session for demonstration
    return render_template('addCourse.html')

@bp.route('/adddepartment', methods = ['POST'])
def add_department():
    data = request.get_json()
    department_name = data.get("name")

    if not department_name:
        return jsonify({"status":"error","message":"Department name required"}), 400
    
    service = DepartmentService(dbconfig())
    result, status = service.addDepartment(department_name)
    return jsonify(result),status

@bp.route('/adddegree', methods = ['POST'])
def add_degree():
    data = request.get_json()
    degree_name = data.get("name")
    credit = data.get("credit")
    department_name = data.get("department")
    #definedBy= 

    if not degree_name or not credit or not department_name:
        return jsonify({"status": "error", "message": "All fields are required"}), 400

    service = Degree(dbconfig())
    result = service.addDegree(degree_name, credit, department_name)
    return jsonify(result)


@bp.route('/addCourse',methods=['POST'])
def add_course():
    data = request.get_json()
    courseName = data.get("courseName")
    description = data.get("description")
    capacity = data.get("capacity")
    availableSeats = data.get("capacity") # Asign same value as capacity
    credits = data.get("credits")
    degree_ID = data.get("degree_ID")
    dept_Id = data.get("dept_Id")
    preReqYear = data.get("preReqYear")
    allowedDeptID = data.get("dept_Id") # Asign same value as dept_Id
    facultyMem_Id = data.get("facultyMem_Id")
    addedBy = session['user_id']  # Assuming user_id is stored in session

    service = Course(dbconfig())
    result = service.addCourse(courseName, description, capacity, availableSeats, credits, degree_ID, dept_Id, preReqYear, allowedDeptID, facultyMem_Id, addedBy)
    return jsonify(result)