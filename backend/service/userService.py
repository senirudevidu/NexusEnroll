from backend.dal.user import UserDAL
from backend.dal.dbconfig import dbconfig

class UserService:
    def __init__(self, db=None):
        self.dal = UserDAL(db or dbconfig())

    def login(self, username, password,module):
        user = self.dal.authenticate(username, password,module)
        if user:
            return {'status': 'success', 'user_id': user[0], 'firstName': user[1], 'lastName': user[2],'module': user[3]}
        else:
            return {'status': 'error', 'message': 'Invalid credentials or inactive account'}
