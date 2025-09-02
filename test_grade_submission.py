"""
Grade Submission System Test Script
This script tests the grade submission functionality for instructors.
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from backend.dal.dbconfig import dbconfig
from backend.service.gradeSubmissionService import GradeSubmissionService

def test_grade_submission_system():
    """Test the grade submission system with sample data"""
    
    print("🧪 Testing Grade Submission System")
    print("=" * 50)
    
    # Initialize service
    db = dbconfig()
    service = GradeSubmissionService(db)
    
    # Test parameters (adjust these based on your test data)
    faculty_id = 1  # Adjust this to match an actual faculty ID in your database
    course_id = 1   # Adjust this to match an actual course taught by the faculty
    
    # Test 1: Get course for grading
    print("\n1. Testing: Get course enrollments for grading")
    result = service.get_course_for_grading(faculty_id, course_id)
    print(f"Status: {result['status']}")
    if result['status'] == 'Success':
        course_info = result['course_info']
        students = result['students']
        print(f"Course: {course_info['course_name']}")
        print(f"Instructor: {course_info['instructor']}")
        print(f"Students enrolled: {len(students)}")
        
        if students:
            print("Sample student:")
            student = students[0]
            print(f"  - ID: {student[1]}, Name: {student[2]} {student[3]}")
            print(f"  - Current Status: {student[5]}, Grade: {student[6]}")
    else:
        print(f"Error: {result['message']}")
        return
    
    # Test 2: Validate grade formats
    print("\n2. Testing: Grade validation")
    test_grades = ["A", "B", "C", "D", "F", "85", "92.5", "Invalid", "150", "-10"]
    for grade in test_grades:
        validation = service.validate_grade_format(grade)
        status = "✅ Valid" if validation['valid'] else "❌ Invalid"
        print(f"  Grade '{grade}': {status}")
        if not validation['valid']:
            print(f"    Reason: {validation['message']}")
    
    # Test 3: Batch grade submission (using first few students if available)
    if result['status'] == 'Success' and result['students']:
        print("\n3. Testing: Batch grade submission")
        students = result['students'][:3]  # Test with first 3 students
        
        grade_submissions = []
        for i, student in enumerate(students):
            enrollment_id = student[0]
            test_grade = ["A", "B", "C"][i]  # Assign different grades
            grade_submissions.append({
                "enrollment_id": enrollment_id,
                "grade": test_grade
            })
        
        print(f"Submitting {len(grade_submissions)} grades as pending...")
        batch_result = service.submit_batch_grades(faculty_id, course_id, grade_submissions)
        print(f"Batch Status: {batch_result['status']}")
        print(f"Successful: {batch_result.get('successful', 0)}")
        print(f"Failed: {batch_result.get('failed', 0)}")
        
        if batch_result.get('results'):
            for result_item in batch_result['results']:
                status_icon = "✅" if result_item['status'] == 'Success' else "❌"
                print(f"  Enrollment {result_item['enrollment_id']}: {status_icon} {result_item['status']}")
                if result_item['status'] == 'Error':
                    print(f"    Error: {result_item['message']}")
    
    # Test 4: Get grading summary
    print("\n4. Testing: Get grading summary")
    summary_result = service.get_grading_summary(faculty_id, course_id)
    if summary_result['status'] == 'Success':
        summary = summary_result['summary']
        stats = summary['completion_stats']
        print(f"Course: {summary['course_name']}")
        print(f"Total Students: {stats['total_students']}")
        print(f"Pending Grades: {stats['pending_grades']}")
        print(f"Submitted Grades: {stats['submitted_grades']}")
        print(f"Completion: {stats['completion_percentage']}%")
    
    # Test 5: Get faculty courses with grading status
    print("\n5. Testing: Get faculty courses with grading status")
    courses_result = service.get_faculty_courses_with_grading_status(faculty_id)
    if courses_result['status'] == 'Success':
        courses = courses_result['courses']
        print(f"Faculty teaches {len(courses)} course(s):")
        for course in courses:
            print(f"  - {course['course_name']}: {course['submitted_grades']}/{course['total_students']} graded ({course['completion_percentage']}%)")
    
    print("\n" + "=" * 50)
    print("✅ Grade submission system test completed!")
    print("\nNext steps:")
    print("1. Start your Flask application")
    print("2. Navigate to the Faculty Dashboard")
    print("3. Test the Grade Submission tab")
    print("4. Try the following workflows:")
    print("   - Load grade sheet for a course")
    print("   - Enter grades and save as pending")
    print("   - Update pending grades")
    print("   - Submit final grades")

def create_sample_enrollment_data():
    """Create sample enrollment data for testing (optional)"""
    print("\n📊 Creating sample enrollment data...")
    
    # This function can be expanded to create test data
    # For now, it just provides instructions
    print("""
    To test the grade submission system, ensure you have:
    
    1. Faculty member in the database (Users table with module='faculty')
    2. Course assigned to that faculty (Course table with facultyMem_Id)
    3. Students enrolled in the course (Enrollment table with enrollmentStatus='Active')
    
    Sample SQL to check your test data:
    
    -- Check faculty
    SELECT u.user_id, u.firstName, u.lastName, u.module 
    FROM Users u WHERE u.module = 'faculty';
    
    -- Check courses for faculty
    SELECT c.course_id, c.courseName, c.facultyMem_Id 
    FROM Course c WHERE c.facultyMem_Id = 1;  -- Replace 1 with actual faculty ID
    
    -- Check enrollments
    SELECT e.enrollment_id, e.student_id, e.course_id, e.markStatus, e.marks
    FROM Enrollment e WHERE e.course_id = 1 AND e.enrollmentStatus = 'Active';
    """)

if __name__ == "__main__":
    try:
        test_grade_submission_system()
    except Exception as e:
        print(f"❌ Test failed with error: {str(e)}")
        print("Make sure your database is running and contains test data.")
        
        # Offer to show sample data creation instructions
        print("\n" + "=" * 50)
        create_sample_enrollment_data()
