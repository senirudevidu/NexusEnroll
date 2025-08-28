from flask import Flask , request
from backend.routes import bp as routes


app = Flask(__name__)
app.register_blueprint(routes)


if __name__ == '__main__':
    app.run(debug=True)