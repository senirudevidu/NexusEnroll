# Faculty Module API Documentation

## Overview

This document provides comprehensive API documentation for the Faculty Module endpoints. All endpoints follow RESTful conventions and return JSON responses.

## Base URL

```
http://localhost:5000
```

## Authentication

- Faculty endpoints require faculty user session
- Admin endpoints require admin user session
- Course access is validated based on faculty-course relationships

---

## 1. Class Roster Management

### Get Class Roster

Retrieve the complete roster for a specific course taught by a faculty member.

**Endpoint:** `GET /api/roster/{faculty_id}/{course_id}`

**Parameters:**

- `faculty_id` (int): Faculty member's user ID
- `course_id` (int): Course ID

**Response:**

```json
{
  "status": "Success",
  "course": "Introduction to Computer Science",
  "instructor": "John Doe",
  "students": [
    {
      "id": 12345,
      "name": "Alice Johnson",
      "email": "alice.johnson@university.edu",
      "phone": "(555) 123-4567",
      "enrollment_status": "Active",
      "mark_status": "In Progress"
    }
  ]
}
```

**Error Response:**

```json
{
  "status": "Error",
  "message": "Course not found or access denied"
}
```

---

### Get Faculty Courses

Retrieve all courses taught by a specific faculty member.

**Endpoint:** `GET /api/roster/{faculty_id}/courses`

**Parameters:**

- `faculty_id` (int): Faculty member's user ID

**Response:**

```json
{
  "status": "Success",
  "courses": [
    {
      "course_id": 1,
      "course_name": "Computer Science 101",
      "description": "Introduction to programming",
      "capacity": 30,
      "available_seats": 5,
      "enrolled_count": 25,
      "department": "Computer Science"
    }
  ]
}
```

---

### Export Roster to CSV

Export class roster in CSV format.

**Endpoint:** `GET /api/roster/{faculty_id}/{course_id}/export`

**Parameters:**

- `faculty_id` (int): Faculty member's user ID
- `course_id` (int): Course ID

**Response:** CSV file download with headers:

```
Student ID,Name,Email,Phone,Enrollment Status,Mark Status
```

---

## 2. Grade Submission Management

### Get Course for Grading

Retrieve course information and enrolled students for grade submission.

**Endpoint:** `GET /api/grades/{faculty_id}/{course_id}`

**Parameters:**

- `faculty_id` (int): Faculty member's user ID
- `course_id` (int): Course ID

**Response:**

```json
{
  "status": "Success",
  "course_info": {
    "course_id": 1,
    "course_name": "Computer Science 101",
    "instructor": "John Doe"
  },
  "students": [
    {
      "enrollment_id": 1,
      "student_id": 12345,
      "firstName": "Alice",
      "lastName": "Johnson",
      "email": "alice.johnson@university.edu",
      "markStatus": "In Progress",
      "marks": null,
      "lastUpdated": "2024-01-15T10:30:00"
    }
  ]
}
```

---

### Batch Submit Grades

Submit multiple grades simultaneously with individual validation.

**Endpoint:** `POST /api/grades/submit`

**Request Body:**

```json
{
  "faculty_id": 1,
  "course_id": 1,
  "grade_submissions": [
    {
      "enrollment_id": 1,
      "grade": "A"
    },
    {
      "enrollment_id": 2,
      "grade": "85"
    }
  ]
}
```

**Response:**

```json
{
  "status": "Completed",
  "total_submitted": 2,
  "successful": 2,
  "failed": 0,
  "results": [
    {
      "enrollment_id": 1,
      "status": "Success",
      "message": "Grade updated successfully"
    },
    {
      "enrollment_id": 2,
      "status": "Success",
      "message": "Grade updated successfully"
    }
  ]
}
```

---

### Update Pending Grade

Update or correct a pending grade (not yet submitted).

**Endpoint:** `PUT /api/grades/update/{enrollment_id}`

**Parameters:**

- `enrollment_id` (int): Enrollment record ID

**Request Body:**

```json
{
  "faculty_id": 1,
  "grade": "B+"
}
```

**Response:**

```json
{
  "status": "Success",
  "message": "Grade updated successfully",
  "enrollment_id": 1,
  "updated_grade": "B+",
  "timestamp": "2024-01-15T10:30:00"
}
```

---

### Finalize Course Grades

Convert all pending grades to submitted status (locks them).

**Endpoint:** `PUT /api/grades/finalize/{course_id}`

**Parameters:**

- `course_id` (int): Course ID

**Request Body:**

```json
{
  "faculty_id": 1
}
```

**Response:**

```json
{
  "status": "Success",
  "message": "Finalized 25 grade(s)",
  "finalized_count": 25
}
```

---

### Validate Grade Format

Validate grade format without saving to database.

**Endpoint:** `POST /api/grades/validate`

**Request Body:**

```json
{
  "grade": "A"
}
```

**Response:**

```json
{
  "valid": true,
  "normalized_grade": "A"
}
```

**Error Response:**

```json
{
  "valid": false,
  "message": "Invalid grade format. Use A-F or 0-100"
}
```

---

### Get Grading Summary

Get detailed summary of grade submission status for a course.

**Endpoint:** `GET /api/grades/summary/{faculty_id}/{course_id}`

**Parameters:**

- `faculty_id` (int): Faculty member's user ID
- `course_id` (int): Course ID

**Response:**

```json
{
  "status": "Success",
  "summary": {
    "course_id": 1,
    "course_name": "Computer Science 101",
    "total_students": 25,
    "status_breakdown": {
      "In Progress": 5,
      "Pending": 10,
      "Submitted": 10
    },
    "grade_details": [...]
  }
}
```

---

## 3. Course Request Management

### Submit Course Request

Faculty submits a request for course changes.

**Endpoint:** `POST /api/course-requests`

**Request Body:**

```json
{
  "faculty_id": 1,
  "course_id": 1,
  "requestType": "UpdateDescription",
  "details": "New course description with updated content"
}
```

**Valid Request Types:**

- `UpdateDescription`: Update course description
- `ChangeCapacity`: Change course capacity (provide new number)
- `AddPrerequisite`: Add course prerequisite (provide prerequisite course ID)

**Response:**

```json
{
  "status": "Success",
  "message": "Course request submitted successfully",
  "request_id": 123
}
```

---

### Get Pending Requests (Admin)

Admin view of all pending course requests.

**Endpoint:** `GET /api/course-requests/pending`

**Response:**

```json
{
  "status": "Success",
  "data": [
    [
      1, // request_id
      1, // facultyMem_Id
      1, // course_id
      "UpdateDescription", // requestType
      "New description", // details
      "2024-01-15T10:30:00", // requestDate
      "Pending", // status
      "John", // faculty firstName
      "Doe", // faculty lastName
      "CS 101" // courseName
    ]
  ]
}
```

---

### Get Faculty Requests

Retrieve all requests submitted by a specific faculty member.

**Endpoint:** `GET /api/course-requests/faculty/{faculty_id}`

**Parameters:**

- `faculty_id` (int): Faculty member's user ID

**Response:**

```json
{
  "status": "Success",
  "data": [
    [
      1, // request_id
      1, // course_id
      "UpdateDescription", // requestType
      "New description", // details
      "2024-01-15T10:30:00", // requestDate
      "Pending", // status
      null, // decisionDate
      "CS 101", // courseName
      null, // admin firstName (if approved)
      null // admin lastName (if approved)
    ]
  ]
}
```

---

### Approve Course Request (Admin)

Admin approves a pending course request and applies changes.

**Endpoint:** `PUT /api/course-requests/{request_id}/approve`

**Parameters:**

- `request_id` (int): Request ID

**Request Body:**

```json
{
  "admin_id": 1
}
```

**Response:**

```json
{
  "status": "Success",
  "message": "Request approved and changes applied"
}
```

---

### Reject Course Request (Admin)

Admin rejects a pending course request.

**Endpoint:** `PUT /api/course-requests/{request_id}/reject`

**Parameters:**

- `request_id` (int): Request ID

**Request Body:**

```json
{
  "admin_id": 1
}
```

**Response:**

```json
{
  "status": "Success",
  "message": "Request rejected"
}
```

---

### Get Request Details

Retrieve details of a specific course request.

**Endpoint:** `GET /api/course-requests/{request_id}`

**Parameters:**

- `request_id` (int): Request ID

**Response:**

```json
{
  "status": "Success",
  "data": [
    1, // request_id
    1, // facultyMem_Id
    1, // course_id
    "UpdateDescription", // requestType
    "New description", // details
    "2024-01-15T10:30:00", // requestDate
    "Approved", // status
    "2024-01-16T09:15:00", // decisionDate
    "John", // faculty firstName
    "Doe", // faculty lastName
    "CS 101", // courseName
    "Admin", // admin firstName
    "User" // admin lastName
  ]
}
```

---

## 4. Utility Endpoints

### Get Faculty Courses for Requests

Get all courses taught by faculty for request submission.

**Endpoint:** `GET /api/faculty/{faculty_id}/courses`

**Parameters:**

- `faculty_id` (int): Faculty member's user ID

**Response:**

```json
{
  "status": "Success",
  "data": [
    [
      1, // course_id
      "CS 101", // courseName
      "Introduction to Computer Science", // description
      30, // capacity
      5, // availableSeats
      "Computer Science" // department
    ]
  ]
}
```

---

### Get Prerequisite Options

Get all courses that can be used as prerequisites.

**Endpoint:** `GET /api/courses/prerequisite-options`

**Response:**

```json
{
  "status": "Success",
  "data": [
    [
      1, // course_id
      "CS 101", // courseName
      "Introduction to Computer Science" // description
    ]
  ]
}
```

---

## Error Handling

### Standard Error Response

All endpoints return standardized error responses:

```json
{
  "status": "Error",
  "message": "Detailed error description"
}
```

### HTTP Status Codes

- `200`: Success
- `201`: Created (for POST requests)
- `400`: Bad Request (validation errors, missing fields)
- `401`: Unauthorized (session/permission issues)
- `404`: Not Found (resource doesn't exist)
- `500`: Internal Server Error

### Common Error Messages

- `"Course not found or access denied"`: Faculty doesn't teach the specified course
- `"Missing required fields"`: Request body missing required parameters
- `"Invalid grade format. Use A-F or 0-100"`: Grade validation failed
- `"Cannot update submitted grade"`: Attempting to modify locked grade
- `"Request not found or already processed"`: Invalid request ID or already handled

---

## Rate Limiting & Security

### Security Measures

- Faculty-course relationship validation
- SQL injection prevention
- Input sanitization and validation
- Transaction-based operations for data consistency

### Best Practices

- Always verify faculty permissions before data access
- Use transaction rollback on errors
- Validate all input parameters
- Log important actions for audit trail

---

## Integration Notes

### Frontend Integration

- Use JavaScript fetch API for all requests
- Handle loading states for better UX
- Implement proper error display
- Cache course data when appropriate

### Database Requirements

- Ensure proper foreign key constraints
- Index on faculty_id and course_id for performance
- Regular backup of grade data
- Audit trail for grade changes

### Testing

- Test all endpoints with valid/invalid data
- Verify permission checking
- Test transaction rollback scenarios
- Load testing for batch operations
