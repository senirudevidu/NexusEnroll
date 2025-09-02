from turtle import st
from flask import request,Blueprint,jsonify,render_template,session,redirect,url_for,make_response
from backend.service.adminService import AdminService
from backend.dal.course import Course
from backend.service.courseService import CourseService
from backend.dal.dbconfig import dbconfig
from backend.service.departmentService import DepartmentService
from backend.service.facService import FacultyService
from backend.service.studentService import StudentService
from backend.dal.degree import Degree
from backend.service.degreeService import DegreeService
from backend.presentation.reports import FacultyWorkloadReport, EnrollmentStatisticsReport
from backend.service.userService import UserService
from backend.service.enrollmentService import EnrollmentService
from backend.service.scheduleProgressService import ScheduleProgressService
from backend.service.reportingService import ReportingService
from backend.service.rosterService import RosterService
from backend.service.gradeSubmissionService import GradeSubmissionService
from backend.service.courseRequestService import CourseRequestService
bp = Blueprint("routes",__name__)

@bp.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        userType = request.form.get('userType')
        userService = UserService()
        login_result = userService.login(username, password, userType)
        if login_result['status'] == 'success':
            session['username'] = username
            session['user_id'] = login_result['user_id']
            session['username'] = username
            session['firstName'] = login_result['firstName']
            session['lastName'] = login_result['lastName']
            session['module'] = login_result['module']
            # Redirect to dashboard based on userType
            if userType == 'admin':
                return redirect('/admin')
            elif userType == 'faculty':
                return redirect('/faculty')
            elif userType == 'student':
                return redirect('/student')
            else:
                return render_template('index.html', error='Invalid user type')
        else:
            return render_template('index.html', error='Please fill in all fields.')
    return render_template('index.html')

@bp.route('/admin')
def admin_dashboard():
    return render_template('admin_dashboard.html', firstName=session['firstName'], lastName=session['lastName'])

@bp.route('/faculty')
def faculty_dashboard():
    # Set default values if session data is missing (for demo purposes)
    first_name = session.get('firstName', 'Dr. Sarah')
    last_name = session.get('lastName', 'Johnson')
    faculty_id = session.get('user_id', 1)  # Get faculty ID from session, default to 1 for demo
    return render_template('faculty_dashboard.html', firstName=first_name, lastName=last_name, facultyId=faculty_id)

@bp.route('/roster-test')
def roster_test():
    """Test page for roster functionality"""
    return render_template('roster_test.html')


@bp.route('/student')
def student_dashboard():
    return render_template('student_dashboard.html', firstName=session['firstName'], lastName=session['lastName'])

@bp.route('/notification-demo')
def notification_demo():
    """Notification System Demo Page"""
    return render_template('notification_demo.html')

@bp.route('/addUserForm')
def add_user_form():
    degree_service = DegreeService(dbconfig())
    degrees = degree_service.get_degrees()
    return render_template('addUser.html', degrees=degrees)

@bp.route('/addStudent', methods=['POST'])
def add_student():
    data = request.get_json()
    firstName = data.get("firstName")
    lastName = data.get("lastName")
    email = data.get("email")
    mobileNo = data.get("mobileNo")
    yearOfStudy = data.get("yearOfStudy")
    degreeID = data.get("degree_ID")

    service = StudentService(dbconfig())
    result, status = service.addStudent(firstName, lastName, email, mobileNo, yearOfStudy, degreeID)
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
    department_service = DepartmentService(dbconfig())
    departments = department_service.getDepartments()
    degree_service = DegreeService(dbconfig())
    degrees = degree_service.get_degrees()
    faculty_service = FacultyService(dbconfig())
    faculty_members = faculty_service.get_faculty_members()
    print("DEBUG faculty_members:", faculty_members)  # Debug print
    return render_template('addCourse.html', departments=departments, degrees=degrees, faculty_members=faculty_members)

@bp.route('/departments')
def departments():
    return render_template('addDepartment.html')

@bp.route('/addDepartment', methods = ['POST'])
def add_department():
    data = request.get_json()
    department_name = data.get("name")

    if not department_name:
        return jsonify({"status":"error","message":"Department name required"}), 400
    
    service = DepartmentService(dbconfig())
    result, status = service.addDepartment(department_name)
    return jsonify(result),status

@bp.route('/degrees')
def degrees():
    department_service = DepartmentService(dbconfig())
    departments = department_service.getDepartments()
    print("DEBUG departments:", departments)  # Debug print
    return render_template('addDegree.html', departments=departments)

@bp.route('/addDegree', methods = ['POST'])
def add_degree():
    data = request.get_json()
    degree_name = data.get("name")
    credit = data.get("credit")
    department_name = data.get("department")
    # session['user_id'] = 6
    # definedBy= session['user_id']  # Assuming user_id is stored in session

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
    addedBy = 6  # Assuming user_id is stored in session

    service = CourseService(dbconfig())
    result = service.addCourse(courseName, description, capacity, availableSeats, credits, degree_ID, dept_Id, preReqYear, allowedDeptID, facultyMem_Id, addedBy)
    return jsonify(result)

@bp.route('/api/users')
def api_users():
    student_service = StudentService(dbconfig())
    users = student_service.displayStudents()
    faculty_service = FacultyService(dbconfig())
    faculty_members = faculty_service.get_faculty_members()
    return jsonify({'users': users, 'faculty_members': faculty_members})

@bp.route('/api/reports')
def api_reports():
    enrollmentReport = EnrollmentStatisticsReport(3)
    enrollment_data = enrollmentReport.outputData()
    facultyWorkLoadReport = FacultyWorkloadReport()
    fac_report_data = facultyWorkLoadReport.outputData()
    return jsonify({'enrollment_data': enrollment_data, 'faculty_workload': fac_report_data})

@bp.route('/api/courses')
def api_courses():
    service = CourseService(dbconfig())
    courses = service.getAllCourses()
    return jsonify(courses)

@bp.route('/api/courses/search')
def api_search_courses():
    # Get query parameters
    department = request.args.get('department')
    course_number = request.args.get('course_number')
    keyword = request.args.get('keyword')
    instructor_name = request.args.get('instructor_name')
    
    service = CourseService(dbconfig())
    courses = service.searchCourses(department, course_number, keyword, instructor_name)
    
    if isinstance(courses, dict) and courses.get("status") == "Error":
        return jsonify(courses), 500
    
    return jsonify(courses)

@bp.route('/api/courses/department-instructor')
def api_courses_by_department_instructor():
    # Get query parameters
    department = request.args.get('department')
    instructor_name = request.args.get('instructor_name')
    
    if not department or not instructor_name:
        return jsonify({"status": "Error", "message": "Both department and instructor_name parameters are required"}), 400
    
    service = CourseService(dbconfig())
    courses = service.getCoursesByDepartmentAndInstructor(department, instructor_name)
    
    if isinstance(courses, dict) and courses.get("status") == "Error":
        return jsonify(courses), 500
    
    return jsonify(courses)

@bp.route('/api/courses/<int:course_id>')
def api_get_course(course_id):
    service = CourseService(dbconfig())
    course = service.getCourseById(course_id)
    if course:
        return jsonify(course)
    else:
        return jsonify({"status": "Error", "message": "Course not found"}), 404

@bp.route('/api/courses/<int:course_id>', methods=['PUT'])
def api_update_course(course_id):
    data = request.get_json()
    courseName = data.get("courseName")
    description = data.get("description")
    capacity = data.get("capacity")
    availableSeats = data.get("availableSeats", capacity)  # Default to capacity if not provided
    credits = data.get("credits")
    degree_ID = data.get("degree_ID")
    dept_Id = data.get("dept_Id")
    preReqYear = data.get("preReqYear")
    allowedDeptID = data.get("allowedDeptID", dept_Id)  # Default to dept_Id if not provided
    facultyMem_Id = data.get("facultyMem_Id")

    service = CourseService(dbconfig())
    result = service.updateCourse(course_id, courseName, description, capacity, availableSeats, credits, degree_ID, dept_Id, preReqYear, allowedDeptID, facultyMem_Id)
    
    if result.get("status") == "Success":
        return jsonify(result), 200
    else:
        return jsonify(result), 400

@bp.route('/api/courses/<int:course_id>', methods=['DELETE'])
def api_delete_course(course_id):
    service = CourseService(dbconfig())
    result = service.deleteCourse(course_id)
    
    if result.get("status") == "Success":
        return jsonify(result), 200
    else:
        return jsonify(result), 400

@bp.route('/api/departments')
def api_departments():
    service = DepartmentService(dbconfig())
    departments = service.getDepartments()
    return jsonify(departments)

@bp.route('/api/degrees')
def api_degrees():
    service = DegreeService(dbconfig())
    degrees = service.get_degrees()
    return jsonify(degrees)

@bp.route('/api/faculty')
def api_faculty():
    service = FacultyService(dbconfig())
    faculty = service.get_faculty_members()
    return jsonify(faculty)

# ============= ROSTER MANAGEMENT ENDPOINTS =============

@bp.route('/api/roster/<int:faculty_id>/<int:course_id>')
def api_get_class_roster(faculty_id, course_id):
    """Get class roster for a specific course taught by a faculty member"""
    service = RosterService(dbconfig())
    result = service.get_class_roster(faculty_id, course_id)
    
    if result["status"] == "Success":
        return jsonify(result), 200
    else:
        return jsonify(result), 400

@bp.route('/api/roster/<int:faculty_id>/courses')
def api_get_faculty_courses(faculty_id):
    """Get all courses taught by a faculty member"""
    service = RosterService(dbconfig())
    result = service.get_faculty_courses(faculty_id)
    
    if result["status"] == "Success":
        return jsonify(result), 200
    else:
        return jsonify(result), 400

@bp.route('/api/roster/<int:faculty_id>/<int:course_id>/export')
def api_export_roster_csv(faculty_id, course_id):
    """Export class roster to CSV"""
    service = RosterService(dbconfig())
    result = service.export_roster_csv(faculty_id, course_id)
    
    if result["status"] == "Success":
        response = make_response(result["content"])
        response.headers["Content-Disposition"] = f"attachment; filename={result['filename']}"
        response.headers["Content-type"] = "text/csv"
        return response
    else:
        return jsonify(result), 400

# ============= GRADE SUBMISSION ENDPOINTS =============

@bp.route('/api/grades/<int:faculty_id>/<int:course_id>')
def api_get_course_for_grading(faculty_id, course_id):
    """Get course enrollments for grade submission"""
    service = GradeSubmissionService(dbconfig())
    result = service.get_course_for_grading(faculty_id, course_id)
    
    if result["status"] == "Success":
        return jsonify(result), 200
    else:
        return jsonify(result), 400

@bp.route('/api/grades/submit', methods=['POST'])
def api_submit_batch_grades():
    """Batch submit grades with individual validation"""
    data = request.get_json()
    
    # Extract required fields
    faculty_id = data.get('faculty_id')
    course_id = data.get('course_id')
    grade_submissions = data.get('grade_submissions', [])
    
    if not faculty_id or not course_id or not grade_submissions:
        return jsonify({
            "status": "Error",
            "message": "Missing required fields: faculty_id, course_id, grade_submissions"
        }), 400
    
    service = GradeSubmissionService(dbconfig())
    result = service.submit_batch_grades(faculty_id, course_id, grade_submissions)
    
    if result["status"] in ["Success", "Completed"]:
        return jsonify(result), 200
    else:
        return jsonify(result), 400

@bp.route('/api/grades/update/<int:enrollment_id>', methods=['PUT'])
def api_update_pending_grade(enrollment_id):
    """Update/correct a pending grade"""
    data = request.get_json()
    
    faculty_id = data.get('faculty_id')
    new_grade = data.get('grade')
    
    if not faculty_id or new_grade is None:
        return jsonify({
            "status": "Error",
            "message": "Missing required fields: faculty_id, grade"
        }), 400
    
    service = GradeSubmissionService(dbconfig())
    result = service.update_single_grade(faculty_id, enrollment_id, new_grade)
    
    if result["status"] == "Success":
        return jsonify(result), 200
    else:
        return jsonify(result), 400

@bp.route('/api/grades/finalize/<int:course_id>', methods=['PUT'])
def api_finalize_course_grades(course_id):
    """Finalize all pending grades for a course (set markStatus='Submitted')"""
    data = request.get_json()
    
    faculty_id = data.get('faculty_id')
    
    if not faculty_id:
        return jsonify({
            "status": "Error",
            "message": "Missing required field: faculty_id"
        }), 400
    
    service = GradeSubmissionService(dbconfig())
    result = service.finalize_all_grades(faculty_id, course_id)
    
    if result["status"] == "Success":
        return jsonify(result), 200
    else:
        return jsonify(result), 400

@bp.route('/api/grades/summary/<int:faculty_id>/<int:course_id>')
def api_get_grading_summary(faculty_id, course_id):
    """Get detailed summary of grade submission status for a course"""
    service = GradeSubmissionService(dbconfig())
    result = service.get_grading_summary(faculty_id, course_id)
    
    if result["status"] == "Success":
        return jsonify(result), 200
    else:
        return jsonify(result), 400

@bp.route('/api/grades/courses/<int:faculty_id>')
def api_get_faculty_courses_grading_status(faculty_id):
    """Get faculty courses with grading status information"""
    service = GradeSubmissionService(dbconfig())
    result = service.get_faculty_courses_with_grading_status(faculty_id)
    
    if result["status"] == "Success":
        return jsonify(result), 200
    else:
        return jsonify(result), 400

@bp.route('/api/grades/validate', methods=['POST'])
def api_validate_grade():
    """Validate grade format without saving"""
    data = request.get_json()
    grade = data.get('grade')
    
    if grade is None:
        return jsonify({
            "status": "Error",
            "message": "Missing grade field"
        }), 400
    
    service = GradeSubmissionService(dbconfig())
    result = service.validate_grade_format(grade)
    
    return jsonify(result), 200

# User Update Routes
@bp.route('/api/users/<int:user_id>', methods=['PUT'])
def api_update_user(user_id):
    data = request.get_json()
    user_type = data.get('user_type')
    
    firstName = data.get('firstName')
    lastName = data.get('lastName')
    email = data.get('email')
    mobileNo = data.get('mobileNo')
    
    if user_type == 'student':
        yearOfStudy = data.get('yearOfStudy')
        degreeID = data.get('degreeID')
        service = StudentService(dbconfig())
        result, status = service.updateStudent(user_id, firstName, lastName, email, mobileNo, yearOfStudy, degreeID)
    elif user_type == 'faculty':
        role = data.get('role')
        service = FacultyService(dbconfig())
        result, status = service.updateFacultyMember(user_id, firstName, lastName, email, mobileNo, role)
    elif user_type == 'admin':
        service = AdminService(dbconfig())
        result, status = service.updateAdmin(user_id, firstName, lastName, email, mobileNo)
    else:
        return jsonify({"status": "Error", "message": "Invalid user type"}), 400
    
    return jsonify(result), status

@bp.route('/api/users/<int:user_id>/deactivate', methods=['POST'])
def api_deactivate_user(user_id):
    data = request.get_json()
    user_type = data.get('user_type')
    
    if user_type == 'student':
        service = StudentService(dbconfig())
        result, status = service.deactivateStudent(user_id)
    elif user_type == 'faculty':
        service = FacultyService(dbconfig())
        result, status = service.deactivateFacultyMember(user_id)
    elif user_type == 'admin':
        service = AdminService(dbconfig())
        result, status = service.deactivateAdmin(user_id)
    else:
        return jsonify({"status": "Error", "message": "Invalid user type"}), 400
    
    return jsonify(result), status

@bp.route('/api/users/<int:user_id>', methods=['GET'])
def api_get_user(user_id):
    # Get user details for editing
    student_service = StudentService(dbconfig())
    faculty_service = FacultyService(dbconfig())
    
    # Try to find user in students first
    students = student_service.displayStudents()
    for student in students:
        if student[0] == user_id:  # user_id is first column
            return jsonify({
                "user_id": student[0],
                "firstName": student[1],
                "lastName": student[2],
                "accountStatus": student[3],
                "yearOfStudy": student[4],
                "degree": student[5],
                "user_type": "student"
            })
    
    # Try to find user in faculty
    faculty_members = faculty_service.get_faculty_members()
    for faculty in faculty_members:
        if faculty[0] == user_id:  # user_id is first column
            return jsonify({
                "user_id": faculty[0],
                "firstName": faculty[1],
                "lastName": faculty[2],
                "accountStatus": faculty[3],
                "role": faculty[4],
                "user_type": "faculty"
            })
    
    return jsonify({"status": "Error", "message": "User not found"}), 404

# ===============================
# ENROLLMENT MANAGEMENT ENDPOINTS
# ===============================

@bp.route('/api/enroll', methods=['POST'])
def api_enroll_student():
    """Enroll a student in a course with validation checks"""
    data = request.get_json()
    student_id = data.get('student_id')
    course_id = data.get('course_id')
    
    if not student_id or not course_id:
        return jsonify({"status": "Error", "message": "Both student_id and course_id are required"}), 400
    
    service = EnrollmentService(dbconfig())
    result = service.enroll_student_in_course(student_id, course_id)
    
    if result["status"] == "Success":
        return jsonify(result), 200
    else:
        return jsonify(result), 400

@bp.route('/api/enrollment/validate', methods=['POST'])
def api_validate_enrollment():
    """Validate enrollment requirements without actually enrolling"""
    data = request.get_json()
    student_id = data.get('student_id')
    course_id = data.get('course_id')
    
    if not student_id or not course_id:
        return jsonify({"status": "Error", "message": "Both student_id and course_id are required"}), 400
    
    service = EnrollmentService(dbconfig())
    result = service.validate_enrollment_requirements(student_id, course_id)
    
    return jsonify(result), 200

@bp.route('/api/drop/<int:enrollment_id>', methods=['DELETE'])
def api_drop_enrollment(enrollment_id):
    """Drop a course enrollment"""
    service = EnrollmentService(dbconfig())
    result = service.drop_student_from_course(enrollment_id)
    
    if result["status"] == "Success":
        return jsonify(result), 200
    else:
        return jsonify(result), 400

@bp.route('/api/enrollments/<int:student_id>')
def api_get_student_enrollments(student_id):
    """Get all active enrollments for a student"""
    service = EnrollmentService(dbconfig())
    result = service.get_student_enrollments(student_id)
    
    if result["status"] == "Success":
        return jsonify(result), 200
    else:
        return jsonify(result), 400

@bp.route('/api/student/<int:student_id>/schedule')
def api_get_student_schedule(student_id):
    """Get student's current schedule summary"""
    service = EnrollmentService(dbconfig())
    result = service.get_student_schedule_summary(student_id)
    
    if result["status"] == "Success":
        return jsonify(result), 200
    else:
        return jsonify(result), 400

@bp.route('/api/enrollment/statistics')
def api_enrollment_statistics():
    """Get enrollment statistics for all courses"""
    course_id = request.args.get('course_id')
    
    service = EnrollmentService(dbconfig())
    result = service.get_enrollment_statistics(course_id)
    
    if result["status"] == "Success":
        return jsonify(result), 200
    else:
        return jsonify(result), 400

@bp.route('/api/student/<int:student_id>/available-courses')
def api_get_available_courses_for_student(student_id):
    """Get courses available for enrollment for a specific student"""
    service = EnrollmentService(dbconfig())
    course_service = CourseService(dbconfig())
    
    # Get all courses
    all_courses = course_service.getAllCourses()
    
    # Get student's current enrollments
    enrollments_result = service.get_student_enrollments(student_id)
    enrolled_course_ids = []
    
    if enrollments_result["status"] == "Success":
        enrolled_course_ids = [enrollment[2] for enrollment in enrollments_result["data"]]
    
    # Filter out courses the student is already enrolled in
    available_courses = []
    for course in all_courses:
        course_id = course[6]  # Assuming course_id is at index 6 in getAllCourses result
        if course_id not in enrolled_course_ids:
            # Validate if student can enroll
            validation = service.validate_enrollment_requirements(student_id, course_id)
            course_data = {
                "course_id": course_id,
                "courseName": course[0],
                "instructor": f"{course[1]} {course[2]}",
                "department": course[3],
                "availableSeats": course[4],
                "capacity": course[5],
                "can_enroll": validation["can_enroll"],
                "issues": validation.get("issues", [])
            }
            available_courses.append(course_data)
    
    return jsonify({"status": "Success", "courses": available_courses}), 200


# ============ NOTIFICATION SYSTEM API ENDPOINTS ============

@bp.route('/api/notifications/statistics')
def api_notification_statistics():
    """Get notification system statistics"""
    try:
        service = EnrollmentService(dbconfig())
        result = service.get_notification_statistics()
        return jsonify(result), 200
    except Exception as e:
        return jsonify({"status": "Error", "message": str(e)}), 500

@bp.route('/api/notifications/demo', methods=['POST'])
def api_notification_demo():
    """Run notification system demonstration"""
    try:
        service = EnrollmentService(dbconfig())
        result = service.demo_notification_system()
        return jsonify(result), 200
    except Exception as e:
        return jsonify({"status": "Error", "message": str(e)}), 500

@bp.route('/api/notifications/observers', methods=['POST'])
def api_manage_notification_observers():
    """Manage notification observers (attach/detach)"""
    try:
        data = request.get_json()
        action = data.get('action')  # 'attach', 'detach', 'attach_all'
        observer_type = data.get('observer_type')  # 'student', 'advisor', 'admin'
        
        service = EnrollmentService(dbconfig())
        result = service.manage_notification_observers(action, observer_type)
        return jsonify(result), 200
    except Exception as e:
        return jsonify({"status": "Error", "message": str(e)}), 500

@bp.route('/api/notifications/test-events', methods=['POST'])
def api_test_notification_events():
    """Test specific notification events"""
    try:
        data = request.get_json()
        event_type = data.get('event_type')
        student_id = data.get('student_id', 1)
        course_id = data.get('course_id', 1)
        course_name = data.get('course_name', 'Test Course')
        
        service = EnrollmentService(dbconfig())
        
        if event_type == 'course_dropped':
            service.notification_manager.notify_course_dropped(student_id, course_id, course_name)
        elif event_type == 'enrollment_successful':
            service.notification_manager.notify_enrollment_successful(student_id, course_id, course_name)
        elif event_type == 'enrollment_failed':
            reason = data.get('reason', 'Test failure reason')
            service.notification_manager.notify_enrollment_failed(student_id, course_id, course_name, reason)
        elif event_type == 'system_error':
            error_type = data.get('error_type', 'Test Error')
            error_message = data.get('error_message', 'This is a test error')
            component = data.get('component', 'Test Component')
            service.notification_manager.notify_system_error(error_type, error_message, component)
        else:
            return jsonify({"status": "Error", "message": "Invalid event_type"}), 400
        
        return jsonify({"status": "Success", "message": f"Triggered {event_type} notification"}), 200
    except Exception as e:
        return jsonify({"status": "Error", "message": str(e)}), 500


# ============ SCHEDULE MANAGEMENT API ENDPOINTS ============

@bp.route('/api/personal-schedule/<int:student_id>')
def api_get_personal_schedule(student_id):
    """
    Get student's schedule for a specific semester or current semester
    Query Parameters:
    - semester: semester_id (optional, defaults to current semester)
    """
    semester_id = request.args.get('semester')
    
    service = ScheduleProgressService()
    
    # Validate student access
    if not service.validate_student_access(student_id):
        return jsonify({
            "status": "Error",
            "message": "Student not found or access denied"
        }), 404
    
    # Convert semester_id to int if provided
    if semester_id:
        try:
            semester_id = int(semester_id)
        except ValueError:
            return jsonify({
                "status": "Error",
                "message": "Invalid semester ID format"
            }), 400
    
    result = service.get_student_schedule(student_id, semester_id)
    
    if result["status"] == "Success":
        return jsonify(result), 200
    else:
        return jsonify(result), 400

@bp.route('/api/personal-schedule/<int:student_id>/semesters')
def api_get_personal_schedule_semesters(student_id):
    """Get all available semesters for a student"""
    service = ScheduleProgressService()
    
    # Validate student access
    if not service.validate_student_access(student_id):
        return jsonify({
            "status": "Error",
            "message": "Student not found or access denied"
        }), 404
    
    result = service.get_student_semesters(student_id)
    
    if result["status"] == "Success":
        return jsonify(result), 200
    else:
        return jsonify(result), 400

@bp.route('/api/academic/current-semester')
def api_get_current_semester():
    """Get current semester information"""
    service = ScheduleProgressService()
    
    result = service.get_current_semester_info()
    
    if result["status"] == "Success":
        return jsonify(result), 200
    else:
        return jsonify(result), 400

# ============ ACADEMIC PROGRESS TRACKING API ENDPOINTS ============

@bp.route('/api/progress/<int:student_id>')
def api_get_student_progress(student_id):
    """
    Get comprehensive academic progress for a student including:
    - Completed courses with grades
    - Pending degree requirements
    - Academic statistics
    - Progress percentage
    """
    service = ScheduleProgressService()
    
    # Validate student access
    if not service.validate_student_access(student_id):
        return jsonify({
            "status": "Error",
            "message": "Student not found or access denied"
        }), 404
    
    result = service.get_student_academic_progress(student_id)
    
    if result["status"] == "Success":
        return jsonify(result), 200
    else:
        return jsonify(result), 400

@bp.route('/api/progress/degree-requirements/<int:degree_id>')
def api_get_degree_requirements(degree_id):
    """Get all requirements for a specific degree program"""
    service = ScheduleProgressService()
    
    result = service.get_degree_requirements_overview(degree_id)
    
    if result["status"] == "Success":
        return jsonify(result), 200
    else:
        return jsonify(result), 400


# ============= REPORTING & ANALYTICS ENDPOINTS =============

@bp.route('/reports')
def reports_dashboard():
    """Render the reports dashboard page"""
    return render_template('reports_dashboard.html', 
                         firstName=session.get('firstName', ''), 
                         lastName=session.get('lastName', ''))

@bp.route('/api/reports/enrollment-statistics')
def api_enrollment_statistics_detailed():
    """Get detailed enrollment statistics by department and semester"""
    department_id = request.args.get('department_id', type=int)
    semester = request.args.get('semester')
    
    service = ReportingService()
    result = service.get_enrollment_statistics_by_department(department_id, semester)
    service.close_connection()
    
    if result["status"] == "Success":
        return jsonify(result), 200
    else:
        return jsonify(result), 400

@bp.route('/api/reports/faculty-workload')
def api_faculty_workload_detailed():
    """Get detailed faculty workload reports"""
    faculty_id = request.args.get('faculty_id', type=int)
    
    service = ReportingService()
    result = service.get_faculty_workload_report(faculty_id)
    service.close_connection()
    
    if result["status"] == "Success":
        return jsonify(result), 200
    else:
        return jsonify(result), 400

@bp.route('/api/reports/course-popularity')
def api_course_popularity_trends():
    """Get course popularity trends"""
    semester = request.args.get('semester')
    limit = request.args.get('limit', default=10, type=int)
    
    service = ReportingService()
    result = service.get_course_popularity_trends(semester, limit)
    service.close_connection()
    
    if result["status"] == "Success":
        return jsonify(result), 200
    else:
        return jsonify(result), 400

@bp.route('/api/reports/high-capacity-courses')
def api_high_capacity_courses():
    """Get courses with high capacity utilization"""
    department_name = request.args.get('department')
    threshold = request.args.get('threshold', default=90, type=float)
    
    service = ReportingService()
    result = service.get_high_capacity_courses(department_name, threshold)
    service.close_connection()
    
    if result["status"] == "Success":
        return jsonify(result), 200
    else:
        return jsonify(result), 400

@bp.route('/api/reports/business-school-capacity')
def api_business_school_high_capacity():
    """
    Specific use case: Get Business school courses over 90% capacity
    with course details including instructor, capacity, and utilization
    """
    threshold = request.args.get('threshold', default=90, type=float)
    
    service = ReportingService()
    result = service.get_business_school_high_capacity_report(threshold)
    service.close_connection()
    
    if result["status"] == "Success":
        return jsonify(result), 200
    else:
        return jsonify(result), 400

@bp.route('/api/reports/department-analytics')
def api_department_analytics():
    """Get comprehensive department analytics"""
    semester = request.args.get('semester')
    
    service = ReportingService()
    result = service.get_department_analytics(semester)
    service.close_connection()
    
    if result["status"] == "Success":
        return jsonify(result), 200
    else:
        return jsonify(result), 400

@bp.route('/api/reports/dashboard')
def api_comprehensive_dashboard():
    """Get all analytics data for comprehensive dashboard"""
    service = ReportingService()
    result = service.get_comprehensive_analytics_dashboard()
    service.close_connection()
    
    if result["status"] == "Success":
        return jsonify(result), 200
    else:
        return jsonify(result), 400

@bp.route('/api/reports/export/json')
def api_export_report_json():
    """Export report data as JSON"""
    report_type = request.args.get('type', 'enrollment')
    department_id = request.args.get('department_id', type=int)
    
    service = ReportingService()
    
    # Get the appropriate report data
    if report_type == 'enrollment':
        report_result = service.get_enrollment_statistics_by_department(department_id)
    elif report_type == 'faculty':
        report_result = service.get_faculty_workload_report()
    elif report_type == 'popularity':
        report_result = service.get_course_popularity_trends()
    elif report_type == 'business-capacity':
        report_result = service.get_business_school_high_capacity_report()
    else:
        service.close_connection()
        return jsonify({"status": "Error", "message": "Invalid report type"}), 400
    
    if report_result["status"] == "Success":
        export_result = service.export_report_as_json(report_result["data"])
        service.close_connection()
        
        if export_result["status"] == "Success":
            response = make_response(export_result["data"])
            response.headers['Content-Type'] = 'application/json'
            response.headers['Content-Disposition'] = f'attachment; filename="{report_type}_report.json"'
            return response
        else:
            return jsonify(export_result), 400
    else:
        service.close_connection()
        return jsonify(report_result), 400

@bp.route('/api/reports/export/html')
def api_export_report_html():
    """Export report data as HTML table"""
    report_type = request.args.get('type', 'enrollment')
    department_id = request.args.get('department_id', type=int)
    
    service = ReportingService()
    
    # Get the appropriate report data
    if report_type == 'enrollment':
        report_result = service.get_enrollment_statistics_by_department(department_id)
        title = "Enrollment Statistics Report"
    elif report_type == 'faculty':
        report_result = service.get_faculty_workload_report()
        title = "Faculty Workload Report"
    elif report_type == 'popularity':
        report_result = service.get_course_popularity_trends()
        title = "Course Popularity Report"
    elif report_type == 'business-capacity':
        report_result = service.get_business_school_high_capacity_report()
        title = "Business School High Capacity Report"
    else:
        service.close_connection()
        return jsonify({"status": "Error", "message": "Invalid report type"}), 400
    
    if report_result["status"] == "Success":
        export_result = service.export_report_as_html(report_result["data"], title)
        service.close_connection()
        
        if export_result["status"] == "Success":
            response = make_response(export_result["data"])
            response.headers['Content-Type'] = 'text/html'
            response.headers['Content-Disposition'] = f'attachment; filename="{report_type}_report.html"'
            return response
        else:
            return jsonify(export_result), 400
    else:
        service.close_connection()
        return jsonify(report_result), 400


# Course Request Management API Endpoints

@bp.route('/api/course-requests', methods=['POST'])
def submit_course_request():
    """Instructor submits a course change request"""
    try:
        data = request.get_json()
        faculty_id = data.get('faculty_id')
        course_id = data.get('course_id')
        request_type = data.get('requestType')
        details = data.get('details')
        
        if not all([faculty_id, course_id, request_type, details]):
            return jsonify({"status": "Error", "message": "Missing required fields"}), 400
        
        service = CourseRequestService(dbconfig())
        result = service.submit_request(faculty_id, course_id, request_type, details)
        
        if result["status"] == "Success":
            return jsonify(result), 201
        else:
            return jsonify(result), 400
            
    except Exception as e:
        return jsonify({"status": "Error", "message": str(e)}), 500

@bp.route('/api/course-requests/pending', methods=['GET'])
def get_pending_requests():
    """Admin views all pending course requests"""
    try:
        service = CourseRequestService(dbconfig())
        result = service.get_pending_requests()
        
        if result["status"] == "Success":
            return jsonify(result), 200
        else:
            return jsonify(result), 400
            
    except Exception as e:
        return jsonify({"status": "Error", "message": str(e)}), 500

@bp.route('/api/course-requests/faculty/<int:faculty_id>', methods=['GET'])
def get_faculty_requests(faculty_id):
    """Get all requests submitted by a specific faculty member"""
    try:
        service = CourseRequestService(dbconfig())
        result = service.get_faculty_requests(faculty_id)
        
        if result["status"] == "Success":
            return jsonify(result), 200
        else:
            return jsonify(result), 400
            
    except Exception as e:
        return jsonify({"status": "Error", "message": str(e)}), 500

@bp.route('/api/course-requests/<int:request_id>/approve', methods=['PUT'])
def approve_request(request_id):
    """Admin approves a course request"""
    try:
        data = request.get_json()
        admin_id = data.get('admin_id')
        
        if not admin_id:
            return jsonify({"status": "Error", "message": "Admin ID is required"}), 400
        
        service = CourseRequestService(dbconfig())
        result = service.approve_request(request_id, admin_id)
        
        if result["status"] == "Success":
            return jsonify(result), 200
        else:
            return jsonify(result), 400
            
    except Exception as e:
        return jsonify({"status": "Error", "message": str(e)}), 500

@bp.route('/api/course-requests/<int:request_id>/reject', methods=['PUT'])
def reject_request(request_id):
    """Admin rejects a course request"""
    try:
        data = request.get_json()
        admin_id = data.get('admin_id')
        
        if not admin_id:
            return jsonify({"status": "Error", "message": "Admin ID is required"}), 400
        
        service = CourseRequestService(dbconfig())
        result = service.reject_request(request_id, admin_id)
        
        if result["status"] == "Success":
            return jsonify(result), 200
        else:
            return jsonify(result), 400
            
    except Exception as e:
        return jsonify({"status": "Error", "message": str(e)}), 500

@bp.route('/api/course-requests/<int:request_id>', methods=['GET'])
def get_request_details(request_id):
    """Get details of a specific request"""
    try:
        service = CourseRequestService(dbconfig())
        result = service.get_request_details(request_id)
        
        if result["status"] == "Success":
            return jsonify(result), 200
        else:
            return jsonify(result), 404
            
    except Exception as e:
        return jsonify({"status": "Error", "message": str(e)}), 500

@bp.route('/api/faculty/<int:faculty_id>/courses', methods=['GET'])
def get_faculty_courses(faculty_id):
    """Get all courses taught by a faculty member"""
    try:
        service = CourseRequestService(dbconfig())
        result = service.get_faculty_courses(faculty_id)
        
        if result["status"] == "Success":
            return jsonify(result), 200
        else:
            return jsonify(result), 400
            
    except Exception as e:
        return jsonify({"status": "Error", "message": str(e)}), 500

@bp.route('/api/courses/prerequisite-options', methods=['GET'])
def get_prerequisite_options():
    """Get all courses that can be used as prerequisites"""
    try:
        service = CourseRequestService(dbconfig())
        result = service.get_all_courses_for_prerequisite()
        
        if result["status"] == "Success":
            return jsonify(result), 200
        else:
            return jsonify(result), 400
            
    except Exception as e:
        return jsonify({"status": "Error", "message": str(e)}), 500

