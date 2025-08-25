from flask import Flask , request
from backend.dbconfig import dbconfig
from backend.user import UserFactory, StudentFactory, FacultyMemberFactory, AdminFactory

app = Flask(__name__)

# @app.route('/dbconfig')
# def databaseinit():
#     db = dbconfig()
#     conn = db.get_db_connection()
#     if conn:
#         return "Database connection successful"
#     return "Database connection failed"

@app.route('/adduser' , methods = ['POST'])
def addUser():
    module = request.form['module']

    if module == 'student':
        factory = StudentFactory()
    elif module == 'faculty':
        factory = FacultyMemberFactory()
    elif module == 'admin':
        factory = AdminFactory()
    else:
        return "Invalid module"

    user = factory.create_user()
    result = user.adduser()
    return result

if __name__ == '__main__':
    app.run(debug=True)