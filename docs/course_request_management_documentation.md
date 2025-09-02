# Course Information Management Module Documentation

## Overview

The Course Information Management module allows instructors to submit requests for course changes and administrators to approve or reject them. This ensures proper oversight and control over course modifications while maintaining academic integrity.

## Features

### For Instructors (Faculty)

- **Submit Course Change Requests**: Request changes for courses they teach
- **Request Types**:
  - Update course descriptions
  - Add prerequisites
  - Change course capacity
- **Track Request Status**: View history of submitted requests and their approval status
- **Request Validation**: Built-in validation to prevent invalid requests

### For Administrators

- **Review Pending Requests**: View all pending course change requests
- **Approve/Reject Requests**: Make decisions on course changes
- **Apply Changes Automatically**: Approved changes are automatically applied to the database
- **Audit Trail**: Complete history of who approved/rejected requests and when
- **Request Statistics**: Dashboard showing pending and total request counts

## Database Schema

### CourseRequest Table

```sql
CREATE TABLE CourseRequest (
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
    FOREIGN KEY (approvedBy) REFERENCES Users(user_id)
);
```

### Prerequisite Table

```sql
CREATE TABLE Prerequisite (
    prerequisite_id INT PRIMARY KEY AUTO_INCREMENT,
    course_id INT NOT NULL,
    prerequisite_course_id INT NOT NULL,
    created_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY (course_id) REFERENCES Course(course_id),
    FOREIGN KEY (prerequisite_course_id) REFERENCES Course(course_id),
    UNIQUE KEY unique_prerequisite (course_id, prerequisite_course_id)
);
```

## API Endpoints

### POST /api/course-requests

Submit a new course change request.

**Request Body:**

```json
{
  "faculty_id": 1,
  "course_id": 1,
  "requestType": "UpdateDescription",
  "details": "New course description"
}
```

**Response:**

```json
{
  "status": "Success",
  "message": "Course request submitted successfully",
  "request_id": 123
}
```

### GET /api/course-requests/pending

Get all pending course requests (Admin only).

**Response:**

```json
{
    "status": "Success",
    "requests": [
        [request_id, faculty_id, course_id, requestType, details, requestDate, status, firstName, lastName, courseName]
    ]
}
```

### GET /api/course-requests/faculty/{faculty_id}

Get all requests submitted by a specific faculty member.

### PUT /api/course-requests/{request_id}/approve

Approve a course request and apply changes.

**Request Body:**

```json
{
  "admin_id": 1
}
```

### PUT /api/course-requests/{request_id}/reject

Reject a course request.

### GET /api/faculty/{faculty_id}/courses

Get all courses taught by a faculty member.

### GET /api/courses/prerequisite-options

Get all courses available as prerequisites.

## Frontend Components

### Faculty Dashboard - Course Requests Tab

- **Course Selection**: Dropdown to select from courses taught by the faculty
- **Request Type Selection**: Choose from UpdateDescription, ChangeCapacity, or AddPrerequisite
- **Dynamic Form Fields**: Form changes based on request type
- **Request History Table**: Shows all submitted requests with status
- **Status Indicators**: Visual badges for Pending, Approved, Rejected status

### Admin Dashboard - Course Requests Tab

- **Pending Requests View**: Table showing all pending requests
- **Request Statistics**: Dashboard showing counts of pending and total requests
- **Status Filtering**: Filter requests by status (All, Pending, Approved, Rejected)
- **Approval Actions**: Approve/Reject buttons for pending requests
- **Request Details**: Full details of each request with faculty and course information

## Validation Rules

### Faculty Request Submission

- Faculty can only submit requests for courses they teach
- Request type must be valid (UpdateDescription, ChangeCapacity, AddPrerequisite)
- Capacity changes must be positive numbers
- Capacity cannot be reduced below current enrollment
- Prerequisite courses must exist in the system
- Courses cannot be prerequisites of themselves
- Descriptions cannot be empty and have a 1000 character limit

### Admin Approval Process

- Only pending requests can be approved/rejected
- Approved changes are automatically applied to the Course table
- Prerequisites are added to the Prerequisite table
- Capacity changes update both capacity and available seats
- All changes maintain referential integrity

## Error Handling

### Common Error Responses

- **400 Bad Request**: Invalid data, missing fields, validation errors
- **401 Unauthorized**: Faculty trying to request changes for courses they don't teach
- **404 Not Found**: Request ID not found
- **500 Internal Server Error**: Database or server errors

### Validation Messages

- "You are not authorized to make requests for this course"
- "Invalid request type"
- "Capacity must be a positive number"
- "Cannot reduce capacity below current enrollment"
- "Prerequisite course does not exist"
- "Course cannot be a prerequisite of itself"
- "Description cannot be empty"

## Security Features

- **Authorization Checks**: Faculty can only request changes for their own courses
- **Admin Verification**: Only admins can approve/reject requests
- **SQL Injection Prevention**: All queries use parameterized statements
- **Data Validation**: Server-side validation for all input data
- **Audit Trail**: Complete logging of who made what changes when

## Usage Instructions

### For Faculty Members

1. **Navigate to Faculty Dashboard**
2. **Go to Course Requests Tab**
3. **Submit New Request:**
   - Select the course from dropdown
   - Choose request type
   - Enter appropriate details
   - Click Submit Request
4. **Track Requests:** View history table to see request status

### For Administrators

1. **Navigate to Admin Dashboard**
2. **Go to Course Requests Tab**
3. **Review Pending Requests:**
   - View all pending requests in the table
   - Check request details and faculty information
4. **Make Decisions:**
   - Click "Approve" to accept and apply changes
   - Click "Reject" to deny the request
5. **Monitor Statistics:** Check pending and total request counts

## Installation and Setup

1. **Create Database Tables:**

   ```bash
   python setup_course_request_db.py
   ```

2. **Start Flask Application:**

   ```bash
   python app.py
   ```

3. **Test API Endpoints:**
   ```bash
   python test_course_requests.py
   ```

## File Structure

```
backend/
├── dal/
│   └── courseRequest.py          # Database access layer
├── service/
│   └── courseRequestService.py   # Business logic layer
└── presentation/
    └── routes.py                 # API endpoints (updated)

frontend/
├── templates/
│   ├── faculty_dashboard.html    # Faculty interface (updated)
│   └── admin_dashboard.html      # Admin interface (updated)
├── static/css/
│   ├── faculty.css              # Faculty styles (updated)
│   └── admin.css                # Admin styles (updated)
└── static/js/
    ├── faculty.js               # Faculty functionality (updated)
    └── admin.js                 # Admin functionality (updated)

setup_course_request_db.py       # Database setup script
test_course_requests.py          # API testing script
```

## Future Enhancements

1. **Email Notifications**: Send emails to faculty when requests are approved/rejected
2. **Bulk Operations**: Allow admins to approve/reject multiple requests at once
3. **Request Comments**: Allow admins to add comments when rejecting requests
4. **Request Priorities**: Add priority levels for urgent course changes
5. **Advanced Prerequisites**: Support for complex prerequisite logic (AND/OR conditions)
6. **Request Templates**: Pre-defined templates for common request types
7. **Workflow Stages**: Multi-stage approval process for complex changes
8. **Integration**: Connect with course catalog and student information systems

## Troubleshooting

### Common Issues

1. **Database Connection Errors**: Check database credentials in dbconfig.py
2. **Permission Errors**: Ensure faculty and admin IDs are correctly set
3. **Request Not Appearing**: Check if request was submitted successfully and refresh the page
4. **Approval Failures**: Verify admin permissions and request status

### Debug Steps

1. Check browser console for JavaScript errors
2. Verify API endpoints are responding correctly
3. Check database for table creation and data integrity
4. Review server logs for error messages
5. Test with the provided test script

## Support

For issues or questions regarding the Course Information Management module:

1. Check the troubleshooting section above
2. Review the API documentation
3. Test with the provided test script
4. Check database table structure and data
