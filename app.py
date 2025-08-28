from flask import Flask , request
from backend.routes import bp as department_bp


app = Flask(__name__)
app.register_blueprint(department_bp)


if __name__ == '__main__':
    app.run(debug=True)