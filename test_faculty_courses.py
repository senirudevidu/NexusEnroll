#!/usr/bin/env python3
"""
Test script to verify faculty courses API and database connectivity
"""

from backend.dal.dbconfig import dbconfig
from backend.service.rosterService import RosterService
import json

def test_faculty_courses():
    """Test faculty courses functionality"""
    print("Testing faculty courses API...")
    
    try:
        # Test direct database query
        db = dbconfig()
        conn = db.get_db_connection()
        cursor = conn.cursor()
        
        print("Database connection successful")
        
        # Check if there are any courses with faculty assigned
        cursor.execute("""
        SELECT c.course_id, c.courseName, c.facultyMem_Id, u.firstName, u.lastName
        FROM Course c
        JOIN Users u ON c.facultyMem_Id = u.user_id
        LIMIT 5
        """)
        
        courses = cursor.fetchall()
        print(f"Found {len(courses)} courses with faculty assigned:")
        for course in courses:
            print(f"  Course ID: {course[0]}, Name: {course[1]}, Faculty: {course[3]} {course[4]} (ID: {course[2]})")
        
        cursor.close()
        conn.close()
        
        # Test the service
        print("\nTesting RosterService...")
        service = RosterService(dbconfig())
        
        # Test with faculty ID 1
        result = service.get_faculty_courses(1)
        print(f"Faculty ID 1 courses result: {json.dumps(result, indent=2)}")
        
        # Test with a different faculty ID if needed
        if result["status"] == "Success" and len(result["courses"]) == 0:
            print("No courses found for faculty ID 1, trying faculty ID 2...")
            result2 = service.get_faculty_courses(2)
            print(f"Faculty ID 2 courses result: {json.dumps(result2, indent=2)}")
        
    except Exception as e:
        print(f"Error during testing: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_faculty_courses()
