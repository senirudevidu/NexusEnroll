"""
Database setup script for Course Request Management module
Creates the necessary tables for course change requests and prerequisites
"""

from backend.dal.dbconfig import dbconfig
import mysql.connector

def create_course_request_tables():
    """Create the CourseRequest and Prerequisite tables"""
    db = dbconfig()
    conn = db.get_db_connection()
    cursor = conn.cursor()
    
    try:
        print("Creating Course Request Management tables...")
        
        # Create CourseRequest table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS CourseRequest (
                request_id INT PRIMARY KEY AUTO_INCREMENT,
                facultyMem_Id INT NOT NULL,
                course_id INT NOT NULL,
                requestType VARCHAR(50) NOT NULL,
                details TEXT NOT NULL,
                requestDate TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                decisionDate TIMESTAMP NULL,
                approvedBy INT NULL,
                status VARCHAR(20) DEFAULT 'Pending',
                
                FOREIGN KEY (facultyMem_Id) REFERENCES Users(user_id),
                FOREIGN KEY (course_id) REFERENCES Course(course_id),
                FOREIGN KEY (approvedBy) REFERENCES Users(user_id),
                
                INDEX idx_status (status),
                INDEX idx_faculty (facultyMem_Id),
                INDEX idx_course (course_id),
                INDEX idx_request_date (requestDate)
            )
        """)
        print("✓ CourseRequest table created successfully")
        
        # Create Prerequisite table if it doesn't exist
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS Prerequisite (
                prerequisite_id INT PRIMARY KEY AUTO_INCREMENT,
                course_id INT NOT NULL,
                prerequisite_course_id INT NOT NULL,
                created_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                
                FOREIGN KEY (course_id) REFERENCES Course(course_id),
                FOREIGN KEY (prerequisite_course_id) REFERENCES Course(course_id),
                
                UNIQUE KEY unique_prerequisite (course_id, prerequisite_course_id),
                INDEX idx_course (course_id),
                INDEX idx_prerequisite (prerequisite_course_id)
            )
        """)
        print("✓ Prerequisite table created successfully")
        
        conn.commit()
        print("✓ All tables created successfully!")
        
    except mysql.connector.Error as e:
        print(f"Error creating tables: {e}")
        conn.rollback()
    finally:
        cursor.close()
        conn.close()

def insert_sample_data():
    """Insert some sample data for testing"""
    db = dbconfig()
    conn = db.get_db_connection()
    cursor = conn.cursor()
    
    try:
        print("Inserting sample course request data...")
        
        # Insert a sample course request
        cursor.execute("""
            INSERT IGNORE INTO CourseRequest 
            (request_id, facultyMem_Id, course_id, requestType, details, status) 
            VALUES 
            (1, 1, 1, 'UpdateDescription', 
             'Update course description to include new programming languages and modern development practices', 
             'Pending')
        """)
        
        cursor.execute("""
            INSERT IGNORE INTO CourseRequest 
            (request_id, facultyMem_Id, course_id, requestType, details, status) 
            VALUES 
            (2, 1, 1, 'ChangeCapacity', '35', 'Pending')
        """)
        
        conn.commit()
        print("✓ Sample data inserted successfully!")
        
    except mysql.connector.Error as e:
        print(f"Error inserting sample data: {e}")
        conn.rollback()
    finally:
        cursor.close()
        conn.close()

if __name__ == "__main__":
    create_course_request_tables()
    insert_sample_data()
    print("\nCourse Request Management module database setup complete!")
    print("\nYou can now:")
    print("- Submit course change requests as faculty")
    print("- View and manage requests as admin")
    print("- Track request history and status")
