# Reporting & Analytics Module Documentation

## Overview

The Reporting & Analytics module provides comprehensive reporting capabilities for the NexusEnroll university enrollment system. It offers detailed insights into enrollment statistics, faculty workload, course popularity, and department performance.

## Features

### 📊 Core Reports

1. **Enrollment Statistics by Department**

   - Total seats, filled seats, and capacity percentage by department
   - Semester-based filtering
   - Course-level details with instructor information

2. **Faculty Workload Reports**

   - Number of courses per faculty member
   - Total enrolled students per faculty
   - Average students per course
   - Department-wise faculty distribution

3. **Course Popularity Trends**

   - Most enrolled courses per semester
   - Enrollment percentage rankings
   - Department and instructor details

4. **High Capacity Course Alerts**

   - Courses above specified capacity thresholds (80%, 90%, 95%)
   - Critical capacity warnings
   - Department filtering capabilities

5. **Department Analytics Dashboard**
   - Comprehensive department performance metrics
   - Total courses, capacity, enrollment statistics
   - Faculty count per department
   - Average utilization rates

### 🎯 Specific Use Case Implementation

**Business School High Capacity Report**

- Generates reports for Business school courses at 90%+ capacity
- Includes course name, instructor, total capacity, enrolled students, and utilization percentage
- Provides summary statistics and organized HTML/JSON output
- Supports downloadable spreadsheet export

## Technical Architecture

### Backend Components

```
backend/
├── presentation/
│   └── reports.py              # Report generation classes using Template Method pattern
├── service/
│   └── reportingService.py     # Business logic and service layer
└── dal/
    └── dbconfig.py            # Database configuration (existing)
```

### Frontend Components

```
static/
├── css/
│   └── reports.css            # Modern dashboard styling
├── js/
│   └── reports.js             # Interactive dashboard functionality
└── templates/
    └── reports_dashboard.html  # Comprehensive analytics dashboard
```

## API Endpoints

### Base Reports

- `GET /reports` - Render reports dashboard
- `GET /api/reports/dashboard` - Get comprehensive dashboard data

### Specific Reports

- `GET /api/reports/enrollment-statistics?department_id=X&semester=Y`
- `GET /api/reports/faculty-workload?faculty_id=X`
- `GET /api/reports/course-popularity?semester=X&limit=Y`
- `GET /api/reports/high-capacity-courses?department=X&threshold=Y`
- `GET /api/reports/business-school-capacity?threshold=X`
- `GET /api/reports/department-analytics?semester=X`

### Export Endpoints

- `GET /api/reports/export/json?type=enrollment&department_id=X`
- `GET /api/reports/export/html?type=faculty`

## Usage Examples

### 1. Business School High Capacity Report

```python
from backend.service.reportingService import ReportingService

# Initialize service
service = ReportingService()

# Get Business school courses over 90% capacity
result = service.get_business_school_high_capacity_report(90)

if result["status"] == "Success":
    courses = result["data"]
    summary = result["summary"]

    print(f"Found {summary['totalCourses']} Business courses over 90% capacity")
    print(f"Average utilization: {summary['averageUtilization']}%")

    for course in courses:
        print(f"- {course['courseName']}: {course['utilizationPercentage']}%")
        print(f"  Instructor: {course['instructor']}")
        print(f"  Capacity: {course['enrolledStudents']}/{course['totalCapacity']}")
```

### 2. Faculty Workload Analysis

```python
# Get all faculty workload data
result = service.get_faculty_workload_report()

if result["status"] == "Success":
    faculty_data = result["data"]

    for faculty in faculty_data:
        print(f"{faculty['facultyName']} ({faculty['department']})")
        print(f"  Courses: {faculty['numberOfCourses']}")
        print(f"  Students: {faculty['totalEnrolledStudents']}")
        print(f"  Avg per course: {faculty['avgStudentsPerCourse']}")
```

### 3. Export Reports

```python
# Export as JSON
json_result = service.export_report_as_json(report_data)
with open('report.json', 'w') as f:
    f.write(json_result["data"])

# Export as HTML
html_result = service.export_report_as_html(report_data, "University Report")
with open('report.html', 'w') as f:
    f.write(html_result["data"])
```

## Dashboard Features

### Interactive Analytics

- **Real-time Data**: Auto-refreshing charts and metrics
- **Filtering**: Department, semester, and threshold-based filtering
- **Visualization**: Charts using Chart.js for trends and distributions
- **Export**: One-click export to JSON/HTML formats

### User Interface

- **Tabbed Navigation**: Organized sections for different report types
- **Responsive Design**: Mobile-friendly interface
- **Status Indicators**: Color-coded capacity and status badges
- **Progress Bars**: Visual utilization percentage displays

## Database Schema Requirements

The module works with existing tables:

- `Course` - Course information and capacity data
- `Department` - Department details
- `Users` - Faculty information
- `FacultyStaff` - Faculty-course relationships
- `Enrollment` - Student enrollment data

## Setup and Installation

### 1. Backend Setup

All backend components are ready to use with the existing Flask application.

### 2. Frontend Integration

Add to your base template or admin dashboard:

```html
<link
  rel="stylesheet"
  href="{{ url_for('static', filename='css/reports.css') }}"
/>
<script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
<script src="{{ url_for('static', filename='js/reports.js') }}"></script>
```

### 3. Navigation Link

Add to admin dashboard:

```html
<a href="/reports" class="btn btn-primary">📊 Reports & Analytics</a>
```

## Testing

Run the test script to verify functionality:

```bash
python test_reports.py
```

This will test:

- All report generation functions
- Data export capabilities
- Error handling
- Database connectivity

## Performance Considerations

1. **Database Optimization**

   - Indexed queries on commonly filtered columns
   - Efficient JOINs across related tables
   - Pagination for large datasets

2. **Caching Strategy**

   - Consider implementing Redis for frequently accessed reports
   - Cache department and faculty lists
   - Implement query result caching

3. **Export Optimization**
   - Stream large exports to prevent memory issues
   - Implement background job processing for large reports

## Security Features

1. **Access Control**

   - Role-based access (admin only for sensitive reports)
   - Session validation
   - Parameter sanitization

2. **Data Protection**
   - SQL injection prevention through parameterized queries
   - Input validation and sanitization
   - Secure file download mechanisms

## Future Enhancements

1. **Advanced Analytics**

   - Predictive enrollment modeling
   - Capacity planning recommendations
   - Student performance correlation analysis

2. **Additional Export Formats**

   - Excel/CSV export capabilities
   - PDF report generation
   - Email report scheduling

3. **Real-time Dashboards**
   - Live enrollment tracking
   - WebSocket-based updates
   - Alert notifications

## Troubleshooting

### Common Issues

1. **Database Connection Errors**

   - Verify database configuration in `dbconfig.py`
   - Check database permissions
   - Ensure all required tables exist

2. **Missing Data**

   - Verify course and enrollment data exists
   - Check department name spellings (case-sensitive)
   - Ensure faculty-course relationships are properly set

3. **Chart Display Issues**
   - Verify Chart.js library is loaded
   - Check browser console for JavaScript errors
   - Ensure data format matches chart expectations

## Support

For technical support or feature requests:

1. Check the test script output for specific errors
2. Review database query logs
3. Verify API endpoint responses using browser developer tools
4. Contact the development team with specific error messages

---

_Generated for NexusEnroll University Enrollment System_
_Version 1.0 - Comprehensive Reporting & Analytics Module_
