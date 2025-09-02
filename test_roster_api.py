"""
Test script for the Class Roster API endpoints
"""
import requests
import json

BASE_URL = "http://127.0.0.1:5000"

def test_faculty_courses():
    """Test fetching faculty courses"""
    print("Testing faculty courses endpoint...")
    faculty_id = 1  # Test with faculty ID 1
    
    try:
        response = requests.get(f"{BASE_URL}/api/roster/{faculty_id}/courses")
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print("Response:", json.dumps(data, indent=2))
        else:
            print("Error:", response.text)
            
    except Exception as e:
        print(f"Error making request: {e}")

def test_class_roster():
    """Test fetching class roster"""
    print("\nTesting class roster endpoint...")
    faculty_id = 1  # Test with faculty ID 1
    course_id = 1   # Test with course ID 1
    
    try:
        response = requests.get(f"{BASE_URL}/api/roster/{faculty_id}/{course_id}")
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print("Response:", json.dumps(data, indent=2))
        else:
            print("Error:", response.text)
            
    except Exception as e:
        print(f"Error making request: {e}")

def test_export_roster():
    """Test exporting roster to CSV"""
    print("\nTesting roster export endpoint...")
    faculty_id = 1  # Test with faculty ID 1
    course_id = 1   # Test with course ID 1
    
    try:
        response = requests.get(f"{BASE_URL}/api/roster/{faculty_id}/{course_id}/export")
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            print("CSV Content:")
            print(response.text)
        else:
            print("Error:", response.text)
            
    except Exception as e:
        print(f"Error making request: {e}")

if __name__ == "__main__":
    print("Testing Class Roster API Endpoints")
    print("=" * 50)
    
    test_faculty_courses()
    test_class_roster()
    test_export_roster()
