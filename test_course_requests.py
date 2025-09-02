"""
Test script for Course Request Management module
Tests the API endpoints and functionality
"""

import requests
import json

BASE_URL = "http://localhost:5000"

def test_course_request_api():
    """Test the course request API endpoints"""
    print("Testing Course Request Management API...")
    
    # Test 1: Submit a course request
    print("\n1. Testing course request submission...")
    request_data = {
        "faculty_id": 1,
        "course_id": 1,
        "requestType": "UpdateDescription",
        "details": "Updated course description to include modern web development frameworks and practices"
    }
    
    try:
        response = requests.post(f"{BASE_URL}/api/course-requests", json=request_data)
        print(f"   Status Code: {response.status_code}")
        print(f"   Response: {response.json()}")
    except Exception as e:
        print(f"   Error: {e}")
    
    # Test 2: Get pending requests (admin view)
    print("\n2. Testing pending requests retrieval...")
    try:
        response = requests.get(f"{BASE_URL}/api/course-requests/pending")
        print(f"   Status Code: {response.status_code}")
        result = response.json()
        print(f"   Found {len(result.get('requests', []))} pending requests")
    except Exception as e:
        print(f"   Error: {e}")
    
    # Test 3: Get faculty courses
    print("\n3. Testing faculty courses retrieval...")
    try:
        response = requests.get(f"{BASE_URL}/api/faculty/1/courses")
        print(f"   Status Code: {response.status_code}")
        result = response.json()
        print(f"   Found {len(result.get('courses', []))} courses for faculty")
    except Exception as e:
        print(f"   Error: {e}")
    
    # Test 4: Get prerequisite options
    print("\n4. Testing prerequisite options...")
    try:
        response = requests.get(f"{BASE_URL}/api/courses/prerequisite-options")
        print(f"   Status Code: {response.status_code}")
        result = response.json()
        print(f"   Found {len(result.get('courses', []))} courses available as prerequisites")
    except Exception as e:
        print(f"   Error: {e}")

if __name__ == "__main__":
    print("Course Request Management API Test")
    print("=" * 50)
    print("Make sure the Flask server is running on localhost:5000")
    print("and the database tables have been created.")
    print()
    
    test_course_request_api()
    
    print("\n" + "=" * 50)
    print("Test completed!")
    print("\nTo use the system:")
    print("1. Navigate to faculty dashboard to submit requests")
    print("2. Navigate to admin dashboard to approve/reject requests")
    print("3. Check the Course Requests tab in admin panel")
