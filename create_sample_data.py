"""
Sample data insertion script for testing the Class Roster functionality
This script inserts sample faculty, students, courses, and enrollments for testing
"""

from backend.dal.dbconfig import dbconfig
import mysql.connector

def create_sample_data():
    """Create sample data for testing roster functionality"""
    db = dbconfig()
    conn = db.get_db_connection()
    cursor = conn.cursor()
    
    try:
        print("Creating sample data for roster testing...")
        
        # Sample Faculty Member (if not exists)
        cursor.execute("""
            INSERT IGNORE INTO Users (user_id, firstName, lastName, email, mobileNo, module, accountStatus) 
            VALUES (1, 'Sarah', 'Johnson', 'sarah.johnson@university.edu', '555-0101', 'faculty', 'Active')
        """)
        
        cursor.execute("""
            INSERT IGNORE INTO FacultyStaff (facultyMem_Id, role) 
            VALUES (1, 'Professor')
        """)
        
        # Sample Department
        cursor.execute("""
            INSERT IGNORE INTO Department (dept_Id, deptName) 
            VALUES (1, 'Computer Science')
        """)
        
        # Sample Degree
        cursor.execute("""
            INSERT IGNORE INTO Degree (degree_ID, name, credits, dept_Id) 
            VALUES (1, 'Computer Science', 120, 1)
        """)
        
        # Sample Course
        cursor.execute("""
            INSERT IGNORE INTO Course (course_id, courseName, description, capacity, availableSeats, credits, degree_ID, dept_Id, preReqYear, allowedDeptID, facultyMem_Id, addedBy) 
            VALUES (1, 'Introduction to Computer Science', 'Basic programming and computer science concepts', 30, 27, 3, 1, 1, 1, 1, 1, 1)
        """)
        
        # Sample Students
        student_data = [
            (2, 'John', 'Smith', 'john.smith@student.edu', '555-0201', 'student', 'Active'),
            (3, 'Jane', 'Doe', 'jane.doe@student.edu', '555-0202', 'student', 'Active'),
            (4, 'Mike', 'Wilson', 'mike.wilson@student.edu', '555-0203', 'student', 'Active')
        ]
        
        for user_id, first_name, last_name, email, phone, module, status in student_data:
            cursor.execute("""
                INSERT IGNORE INTO Users (user_id, firstName, lastName, email, mobileNo, module, accountStatus) 
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            """, (user_id, first_name, last_name, email, phone, module, status))
            
            cursor.execute("""
                INSERT IGNORE INTO Student (student_Id, YearOfStudy, degree_ID) 
                VALUES (%s, 1, 1)
            """, (user_id,))
        
        # Sample Enrollments
        enrollment_data = [
            (2, 1, 'Active', 'In Progress'),  # John Smith in CS101
            (3, 1, 'Active', 'In Progress'),  # Jane Doe in CS101
            (4, 1, 'Active', 'In Progress')   # Mike Wilson in CS101
        ]
        
        for student_id, course_id, enrollment_status, mark_status in enrollment_data:
            cursor.execute("""
                INSERT IGNORE INTO Enrollment (student_id, course_id, enrollmentStatus, markStatus) 
                VALUES (%s, %s, %s, %s)
            """, (student_id, course_id, enrollment_status, mark_status))
        
        conn.commit()
        print("Sample data created successfully!")
        
        # Verify the data was inserted
        cursor.execute("""
            SELECT c.courseName, u.firstName, u.lastName, u.email
            FROM Enrollment e
            JOIN Course c ON e.course_id = c.course_id
            JOIN Student s ON e.student_id = s.student_Id
            JOIN Users u ON s.student_Id = u.user_id
            WHERE c.facultyMem_Id = 1
        """)
        
        results = cursor.fetchall()
        print(f"\nEnrollment verification - Found {len(results)} enrollments:")
        for row in results:
            print(f"  {row[0]}: {row[1]} {row[2]} ({row[3]})")
            
    except Exception as e:
        print(f"Error creating sample data: {e}")
        conn.rollback()
    finally:
        cursor.close()
        conn.close()

if __name__ == "__main__":
    create_sample_data()
