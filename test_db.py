from backend.dal.dbconfig import dbconfig

try:
    print("Testing database connection...")
    db = dbconfig()
    conn = db.get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute("SELECT 1")
    result = cursor.fetchone()
    print(f"Database connection successful: {result}")
    
    cursor.execute("SELECT COUNT(*) FROM Course WHERE facultyMem_Id = 1")
    count = cursor.fetchone()[0]
    print(f"Courses for faculty ID 1: {count}")
    
    cursor.close()
    conn.close()
    
except Exception as e:
    print(f"Database error: {e}")
