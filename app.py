from flask import Flask , request
from backend.presentation.routes import bp as routes



app = Flask(__name__)
app.secret_key = 'replace_with_a_secure_random_key'  # Required for session support
app.register_blueprint(routes)


if __name__ == '__main__':
    app.run(debug=True)