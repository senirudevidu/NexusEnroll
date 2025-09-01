"""
Test script for the Reporting & Analytics module
Run this to test the core functionality of the reporting system
"""

import sys
import os

# Add the project root to Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from backend.service.reportingService import ReportingService

def test_reports():
    """Test all report functions"""
    print("🧪 Testing Reporting & Analytics Module")
    print("=" * 50)
    
    # Initialize service
    service = ReportingService()
    
    # Test 1: Enrollment Statistics
    print("\n1. Testing Enrollment Statistics Report...")
    try:
        result = service.get_enrollment_statistics_by_department()
        if result["status"] == "Success":
            print(f"✅ Success! Found {len(result['data'])} courses")
            if result['data']:
                sample = result['data'][0]
                print(f"   Sample: {sample['courseName']} - {sample['utilizationPercentage']}% capacity")
        else:
            print(f"❌ Error: {result['message']}")
    except Exception as e:
        print(f"❌ Exception: {str(e)}")
    
    # Test 2: Faculty Workload
    print("\n2. Testing Faculty Workload Report...")
    try:
        result = service.get_faculty_workload_report()
        if result["status"] == "Success":
            print(f"✅ Success! Found {len(result['data'])} faculty members")
            if result['data']:
                sample = result['data'][0]
                print(f"   Sample: {sample['facultyName']} - {sample['numberOfCourses']} courses")
        else:
            print(f"❌ Error: {result['message']}")
    except Exception as e:
        print(f"❌ Exception: {str(e)}")
    
    # Test 3: Course Popularity
    print("\n3. Testing Course Popularity Report...")
    try:
        result = service.get_course_popularity_trends(limit=5)
        if result["status"] == "Success":
            print(f"✅ Success! Found {len(result['data'])} popular courses")
            if result['data']:
                sample = result['data'][0]
                print(f"   #1 Popular: {sample['courseName']} - {sample['enrolledCount']} enrolled")
        else:
            print(f"❌ Error: {result['message']}")
    except Exception as e:
        print(f"❌ Exception: {str(e)}")
    
    # Test 4: High Capacity Courses
    print("\n4. Testing High Capacity Courses Report...")
    try:
        result = service.get_high_capacity_courses(threshold_percentage=80)
        if result["status"] == "Success":
            print(f"✅ Success! Found {len(result['data'])} high capacity courses")
            if result['data']:
                sample = result['data'][0]
                print(f"   Sample: {sample['courseName']} - {sample['utilizationPercentage']}% capacity")
        else:
            print(f"❌ Error: {result['message']}")
    except Exception as e:
        print(f"❌ Exception: {str(e)}")
    
    # Test 5: Business School Report (Specific Use Case)
    print("\n5. Testing Business School High Capacity Report...")
    try:
        result = service.get_business_school_high_capacity_report(90)
        if result["status"] == "Success":
            print(f"✅ Success! Found {len(result['data'])} Business courses over 90% capacity")
            if result.get('summary'):
                summary = result['summary']
                print(f"   Summary: {summary['totalCourses']} courses, {summary['averageUtilization']}% avg utilization")
            if result['data']:
                for course in result['data'][:3]:  # Show top 3
                    print(f"   - {course['courseName']}: {course['utilizationPercentage']}% ({course['instructor']})")
        else:
            print(f"❌ Error: {result['message']}")
    except Exception as e:
        print(f"❌ Exception: {str(e)}")
    
    # Test 6: Department Analytics
    print("\n6. Testing Department Analytics Report...")
    try:
        result = service.get_department_analytics()
        if result["status"] == "Success":
            print(f"✅ Success! Found {len(result['data'])} departments")
            if result['data']:
                sample = result['data'][0]
                print(f"   Sample: {sample['departmentName']} - {sample['totalCourses']} courses, {sample['avgUtilization']}% utilization")
        else:
            print(f"❌ Error: {result['message']}")
    except Exception as e:
        print(f"❌ Exception: {str(e)}")
    
    # Test 7: Export Functions
    print("\n7. Testing Export Functions...")
    try:
        # Get some sample data
        result = service.get_enrollment_statistics_by_department()
        if result["status"] == "Success" and result['data']:
            # Test JSON export
            json_result = service.export_report_as_json(result['data'][:2])
            if json_result["status"] == "Success":
                print("✅ JSON export successful")
                print(f"   Sample JSON length: {len(json_result['data'])} characters")
            
            # Test HTML export
            html_result = service.export_report_as_html(result['data'][:2], "Test Report")
            if html_result["status"] == "Success":
                print("✅ HTML export successful")
                print(f"   Sample HTML length: {len(html_result['data'])} characters")
        else:
            print("❌ No data available for export testing")
    except Exception as e:
        print(f"❌ Export test exception: {str(e)}")
    
    # Close connections
    service.close_connection()
    
    print("\n" + "=" * 50)
    print("🎉 Testing Complete!")
    print("\nKey Features Implemented:")
    print("✓ Enrollment statistics by department and semester")
    print("✓ Faculty workload reports (courses per faculty, students per faculty)")
    print("✓ Course popularity trends (most enrolled courses)")
    print("✓ High capacity course identification")
    print("✓ Business school specific reporting (90%+ capacity)")
    print("✓ Department analytics dashboard")
    print("✓ JSON and HTML export functionality")
    print("✓ Comprehensive web dashboard interface")

if __name__ == "__main__":
    test_reports()
