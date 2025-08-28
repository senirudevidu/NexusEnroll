from flask import Flask , request,Blueprint,jsonify
from backend.dbconfig import dbconfig
from backend.departmentService import DepartmentService

bp = Blueprint("department_routes",__name__)

@bp.route('/adddepartment', methods = ['POST'])
def add_department():
    data = request.get_json()
    department_name = data.get("name")

    if not department_name:
        return jsonify({"status":"error","message":"Department name required"}), 400
    
    service = DepartmentService(dbconfig())
    result, status = service.addDepartment(department_name)
    return jsonify(result),status