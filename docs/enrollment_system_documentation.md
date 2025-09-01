# Enrollment System Documentation

## Overview

The Enrollment System is a comprehensive module for managing student course enrollments in the NexusEnroll university course management system. It provides full validation, enrollment, and dropping capabilities with proper error handling and user feedback.

## Features

### Core Functionality

- **Student Enrollment**: Enroll students in courses with comprehensive validation
- **Course Dropping**: Allow students to drop courses with proper capacity management
- **Validation System**: Multi-level validation including prerequisites, capacity, and time conflicts
- **Real-time Updates**: Automatic course capacity updates and enrollment tracking

### Validation Rules

1. **Prerequisite Check**: Ensures students meet year requirements before enrollment
2. **Capacity Check**: Verifies course has available seats
3. **Time Conflict Check**: Prevents enrollment in courses with schedule conflicts
4. **Duplicate Check**: Prevents students from enrolling in the same course twice

## Database Schema

### Enrollment Table

```sql
CREATE TABLE Enrollment (
    enrollment_id INT PRIMARY KEY AUTO_INCREMENT,
    student_id INT NOT NULL,
    course_id INT NOT NULL,
    markStatus VARCHAR(20) DEFAULT 'In Progress',
    marks DECIMAL(5,2) DEFAULT NULL,
    lastUpdated TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    enrollmentStatus VARCHAR(20) DEFAULT 'Active',
    enrollmentDate TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY (student_id) REFERENCES Student(student_Id),
    FOREIGN KEY (course_id) REFERENCES Course(course_id),
    UNIQUE KEY unique_enrollment (student_id, course_id, enrollmentStatus)
);
```

### CourseSchedule Table (Optional)

```sql
CREATE TABLE CourseSchedule (
    schedule_id INT PRIMARY KEY AUTO_INCREMENT,
    course_id INT NOT NULL,
    day VARCHAR(50) NOT NULL,
    startTime TIME NOT NULL,
    endTime TIME NOT NULL,

    FOREIGN KEY (course_id) REFERENCES Course(course_id)
);
```

## API Endpoints

### 1. Enroll Student

**POST** `/api/enroll`

Enrolls a student in a course with full validation.

**Request Body:**

```json
{
  "student_id": 1,
  "course_id": 2
}
```

**Response:**

```json
{
  "status": "Success",
  "message": "Student enrolled successfully"
}
```

**Error Response:**

```json
{
  "status": "Error",
  "message": "Course is full. No available seats."
}
```

### 2. Validate Enrollment

**POST** `/api/enrollment/validate`

Validates enrollment requirements without actually enrolling.

**Request Body:**

```json
{
  "student_id": 1,
  "course_id": 2
}
```

**Response:**

```json
{
  "can_enroll": true,
  "issues": []
}
```

**Error Response:**

```json
{
  "can_enroll": false,
  "issues": ["Course is full", "Time conflict with Math 101"]
}
```

### 3. Drop Course

**DELETE** `/api/drop/{enrollment_id}`

Drops a student from a course.

**Response:**

```json
{
  "status": "Success",
  "message": "Course dropped successfully"
}
```

### 4. Get Student Enrollments

**GET** `/api/enrollments/{student_id}`

Retrieves all active enrollments for a student.

**Response:**

```json
{
  "status": "Success",
  "data": [
    [
      1,
      1,
      2,
      "CS101",
      "Introduction to Computer Science",
      3,
      30,
      25,
      "John Doe",
      "Computer Science",
      "In Progress",
      null,
      "2024-01-15 10:30:00",
      "Active"
    ]
  ]
}
```

### 5. Get Available Courses

**GET** `/api/student/{student_id}/available-courses`

Gets courses available for enrollment for a specific student.

**Response:**

```json
{
  "status": "Success",
  "courses": [
    {
      "course_id": 2,
      "courseName": "CS102",
      "instructor": "Jane Smith",
      "department": "Computer Science",
      "availableSeats": 15,
      "capacity": 30,
      "can_enroll": true,
      "issues": []
    }
  ]
}
```

### 6. Get Schedule Summary

**GET** `/api/student/{student_id}/schedule`

Gets student's current schedule summary.

**Response:**

```json
{
    "status": "Success",
    "schedule": [...],
    "total_credits": 12,
    "course_count": 4
}
```

### 7. Get Enrollment Statistics

**GET** `/api/enrollment/statistics`

Gets enrollment statistics for courses.

**Query Parameters:**

- `course_id` (optional): Get statistics for specific course

**Response:**

```json
{
  "status": "Success",
  "data": [[1, "CS101", 30, 25, 5, 16.67]]
}
```

## Frontend Components

### EnrollmentManager Class

The main JavaScript class that handles all enrollment-related operations.

**Key Methods:**

- `loadStudentEnrollments()`: Loads and displays current enrollments
- `loadAvailableCourses()`: Loads courses available for enrollment
- `validateAndEnroll(courseId, courseName)`: Validates and enrolls student
- `confirmDropEnrollment(enrollmentId, courseName)`: Drops course enrollment
- `validateEnrollment(courseId, courseName)`: Validates enrollment eligibility

### Usage Example

```javascript
// Initialize enrollment manager
const enrollmentManager = new EnrollmentManager();

// Enroll in a course
enrollmentManager.validateAndEnroll(123, "CS101");

// Drop a course
enrollmentManager.confirmDropEnrollment(456, "Math 201");

// Validate enrollment
enrollmentManager.validateEnrollment(789, "Physics 101");
```

## CSS Classes

### Main Container Classes

- `.enrollment-container`: Main container for enrollment sections
- `.enrollment-section`: Individual sections within the enrollment interface
- `.enrollment-card`: Cards displaying enrollment information
- `.available-course-card`: Cards for available courses

### State Classes

- `.can-enroll`: Courses that student can enroll in
- `.cannot-enroll`: Courses that student cannot enroll in
- `.loading-container`: Loading state display
- `.error-container`: Error state display

### Button Classes

- `.enroll-btn`: Primary enrollment button
- `.drop-btn`: Course dropping button
- `.validate-btn`: Validation button
- `.details-btn`: Course details button

## File Structure

```
backend/
├── dal/
│   └── enrollment.py          # Data Access Layer for enrollment operations
├── service/
│   └── enrollmentService.py   # Business logic for enrollment
└── presentation/
    └── routes.py              # API endpoints (updated)

static/
├── css/
│   └── enrollment.css         # Enrollment-specific styles
└── js/
    └── enrollment.js          # Frontend enrollment management

templates/
└── student_dashboard.html     # Updated with enrollment interface

tests/
└── test_enrollment.py         # Comprehensive test suite

database/
└── enrollment_schema.sql      # Database schema and setup
```

## Setup Instructions

### 1. Database Setup

Run the SQL script to create required tables:

```bash
mysql -u username -p database_name < database/enrollment_schema.sql
```

### 2. Backend Setup

The enrollment system integrates with the existing Flask application. No additional setup required.

### 3. Frontend Integration

Include the enrollment CSS and JavaScript files in your student dashboard:

```html
<link
  rel="stylesheet"
  href="{{ url_for('static', filename='css/enrollment.css') }}"
/>
<script src="{{ url_for('static', filename='js/enrollment.js') }}"></script>
```

## Testing

### Running Tests

```bash
cd tests
python test_enrollment.py
```

### Manual Testing

1. Access the student dashboard
2. Navigate to the "Enrollment Management" tab
3. Test enrollment validation
4. Test course enrollment
5. Test course dropping
6. Verify capacity updates

## Error Handling

### Common Errors

1. **Course Full**: "Course is full. No available seats."
2. **Prerequisites Not Met**: "Student must be in year X or higher"
3. **Time Conflict**: "Time conflict detected with course: [Course Name]"
4. **Already Enrolled**: "Student is already enrolled in this course"
5. **Course Not Found**: "Course not found"

### Error Response Format

All API endpoints return errors in a consistent format:

```json
{
  "status": "Error",
  "message": "Descriptive error message"
}
```

## Security Considerations

1. **Input Validation**: All inputs are validated and sanitized
2. **SQL Injection Prevention**: Parameterized queries used throughout
3. **Authorization**: Student can only access their own enrollment data
4. **Data Integrity**: Foreign key constraints and unique constraints

## Performance Optimization

1. **Database Indexes**: Optimized indexes for common queries
2. **Batch Operations**: Efficient batch processing for multiple operations
3. **Caching**: Consider implementing caching for course catalogs
4. **Connection Pooling**: Database connection management

## Future Enhancements

1. **Waitlist System**: Automatic enrollment from waitlist when seats become available
2. **Prerequisite Courses**: More complex prerequisite checking
3. **Email Notifications**: Notify students of enrollment status changes
4. **Mobile App Support**: REST API ready for mobile applications
5. **Analytics Dashboard**: Enrollment analytics for administrators
6. **Semester Management**: Support for different academic terms

## Troubleshooting

### Common Issues

1. **Database Connection Issues**

   - Check database credentials in `dbconfig.py`
   - Ensure database server is running
   - Verify network connectivity

2. **Missing Tables**

   - Run the enrollment schema SQL script
   - Check that all foreign key tables exist

3. **JavaScript Errors**

   - Check browser console for errors
   - Ensure jQuery/FontAwesome dependencies are loaded
   - Verify API endpoints are accessible

4. **Permission Issues**
   - Check database user permissions
   - Verify file system permissions for logs

### Debug Mode

Enable debug mode in Flask for detailed error messages:

```python
app.debug = True
```

## Support

For technical support or questions about the enrollment system:

1. Check the error logs in the application
2. Review the test cases for usage examples
3. Consult the database schema documentation
4. Review API endpoint documentation

## Changelog

### Version 1.0.0

- Initial enrollment system implementation
- Complete validation system
- Frontend interface
- API endpoints
- Database schema
- Test suite
- Documentation
