# Class Roster Viewing Feature - Implementation Documentation

## Overview

The Class Roster Viewing feature allows instructors to view real-time lists of students currently enrolled in their courses, including detailed contact information and enrollment status.

## Features Implemented

### 1. Backend Implementation

#### Database Layer (DAL)

- **File**: `backend/dal/enrollment.py`
- **New Methods**:
  - `get_class_roster(cursor, faculty_id, course_id)`: Retrieves roster with student contact info
  - `get_faculty_courses(cursor, faculty_id)`: Gets all courses taught by a faculty member

#### Service Layer

- **File**: `backend/service/rosterService.py`
- **Methods**:
  - `get_class_roster(faculty_id, course_id)`: Main roster retrieval with formatted response
  - `get_faculty_courses(faculty_id)`: Faculty course listing
  - `export_roster_csv(faculty_id, course_id)`: CSV export functionality

#### API Endpoints

- **File**: `backend/presentation/routes.py`
- **Endpoints**:
  - `GET /api/roster/{faculty_id}/courses` - Get all courses for a faculty member
  - `GET /api/roster/{faculty_id}/{course_id}` - Get class roster for specific course
  - `GET /api/roster/{faculty_id}/{course_id}/export` - Export roster to CSV

### 2. Frontend Implementation

#### JavaScript (Enhanced)

- **File**: `static/js/faculty.js`
- **Features**:
  - Real-time API integration replacing mock data
  - Automatic course loading from database
  - Dynamic roster display with student information
  - CSV export functionality
  - Error handling and loading states

#### HTML Template (Updated)

- **File**: `templates/faculty_dashboard.html`
- **Changes**:
  - Added Status column to roster table
  - Updated table structure for better data display

#### CSS Styling

- **File**: `static/css/faculty.css`
- **Enhancements**:
  - Status badge styles for enrollment states
  - Responsive table design

### 3. Data Structure

#### API Response Format

```json
{
  "status": "Success",
  "course": "Introduction to Computer Science",
  "instructor": "Dr. Sarah Johnson",
  "students": [
    {
      "id": 2,
      "name": "John Smith",
      "email": "john.smith@student.edu",
      "phone": "555-0201",
      "enrollment_status": "Active",
      "mark_status": "In Progress"
    }
  ]
}
```

#### Database Query

The roster query joins multiple tables:

- `Enrollment` - for enrollment data
- `Student` - for student information
- `Users` - for contact information (email, phone)
- `Course` - for course details

### 4. Security Features

#### Access Control

- Faculty members can only view rosters for courses they teach
- Verification query ensures course belongs to requesting faculty
- Returns "Course not found or access denied" for unauthorized requests

#### Data Validation

- Faculty ID and Course ID validation
- Error handling for database connection issues
- Proper HTTP status codes (200 for success, 400 for errors)

### 5. Error Handling

#### Frontend

- Loading states during API calls
- Error messages for failed requests
- Graceful handling of empty rosters ("No students enrolled yet")

#### Backend

- Database connection error handling
- Invalid parameter validation
- Proper exception handling with rollback

### 6. Export Functionality

#### CSV Export

- **Endpoint**: `GET /api/roster/{faculty_id}/{course_id}/export`
- **Response**: CSV file download
- **Headers**: Student ID, Name, Email, Phone, Enrollment Status, Mark Status
- **Filename**: `{CourseName}_roster.csv`

### 7. Usage Examples

#### Viewing Roster

1. Faculty logs into dashboard
2. Navigates to "Class Rosters" tab
3. Selects course from dropdown
4. Roster loads automatically with real-time data

#### Exporting Data

1. Load roster for desired course
2. Click "Export CSV" button
3. File downloads automatically

### 8. Testing

#### Test Page

- **URL**: `/roster-test`
- **Features**:
  - API endpoint testing
  - Interactive roster viewer
  - CSV export testing
  - Error scenario validation

#### Sample Data

- Created sample faculty, students, and enrollments
- Test data includes proper relationships
- Verification queries ensure data integrity

### 9. Technical Specifications

#### Dependencies

- Flask for web framework
- MySQL connector for database access
- Requests library for API testing

#### Performance Considerations

- Efficient JOIN queries to minimize database calls
- Proper indexing on foreign keys
- Connection pooling with proper cleanup

### 10. Future Enhancements

#### Potential Improvements

1. Real-time updates using WebSockets
2. Excel export format
3. Student photo integration
4. Attendance tracking integration
5. Grade quick-entry from roster view
6. Email student functionality
7. Roster comparison between semesters

## File Structure

```
backend/
├── dal/
│   └── enrollment.py          # Enhanced with roster queries
├── service/
│   └── rosterService.py       # New service for roster operations
└── presentation/
    └── routes.py              # New roster API endpoints

static/
├── css/
│   └── faculty.css           # Updated with roster styles
└── js/
    └── faculty.js            # Enhanced with real API integration

templates/
├── faculty_dashboard.html    # Updated roster table
└── roster_test.html         # New test page
```

## Installation & Setup

1. Ensure database connection is configured in `backend/dal/dbconfig.py`
2. Install required Python packages: `pip install flask mysql-connector-python requests`
3. Run sample data creation: `python create_sample_data.py`
4. Start Flask application: `python app.py`
5. Access faculty dashboard: `http://localhost:5000/faculty`
6. Test API functionality: `http://localhost:5000/roster-test`

## API Documentation

### Get Faculty Courses

- **Method**: GET
- **URL**: `/api/roster/{faculty_id}/courses`
- **Response**: List of courses taught by faculty member

### Get Class Roster

- **Method**: GET
- **URL**: `/api/roster/{faculty_id}/{course_id}`
- **Response**: Detailed student roster with contact information

### Export Roster

- **Method**: GET
- **URL**: `/api/roster/{faculty_id}/{course_id}/export`
- **Response**: CSV file download

All endpoints return proper HTTP status codes and error messages for validation and debugging.
