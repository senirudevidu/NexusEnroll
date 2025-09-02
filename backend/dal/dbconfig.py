import mysql.connector
class dbconfig:
    def __init__(self):
        self.host = "mysql-nexusenroll.alwaysdata.net"
        self.user = "427694"
        self.password = "Ugvle@123"
        self.database = "nexusenroll_db"

    def get_db_connection(self):
        conn = mysql.connector.connect(
            host=self.host,
            user=self.user,
            password=self.password,
            database=self.database
        )

        if conn.is_connected():
            return conn
        return None
