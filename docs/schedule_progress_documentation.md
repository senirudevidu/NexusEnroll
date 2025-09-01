# 📅 Schedule Management & Academic Progress Tracking System

A comprehensive personal schedule management and academic progress tracking system for the NexusEnroll university enrollment platform.

## 🌟 Features Overview

### Personal Schedule Management

- **Weekly Calendar View**: Interactive calendar grid displaying courses with times, instructors, and locations
- **List View**: Alternative view showing courses organized by day
- **Semester Selection**: Switch between current and past semesters
- **Real-time Updates**: Automatic refresh and synchronization with enrollment data
- **Responsive Design**: Works seamlessly on desktop and mobile devices

### Academic Progress Tracking

- **Progress Overview**: Visual progress cards showing completion statistics
- **Completed Courses**: Table view of all completed courses with grades and semesters
- **Pending Requirements**: Checklist of remaining degree requirements
- **Grade Distribution**: Analytics showing grade patterns
- **Degree Progress Bar**: Visual representation of degree completion percentage

## 🏗️ System Architecture

### Database Schema

```sql
-- Academic Semester Management
AcademicSemester (semester_id, semester_name, start_date, end_date, is_current, academic_year)

-- Degree Requirements Tracking
DegreeRequirements (requirement_id, degree_id, course_id, is_core_requirement, year_requirement)

-- Enhanced Enrollment with Semester Tracking
Enrollment (enrollment_id, student_id, course_id, semester_id, markStatus, marks, ...)

-- Course Schedule with Location
CourseSchedule (schedule_id, course_id, day, startTime, endTime, location)
```

### API Architecture

- **RESTful Design**: Clean, predictable API endpoints
- **Error Handling**: Comprehensive validation and error responses
- **Data Validation**: Student access control and parameter validation
- **Flexible Queries**: Support for semester filtering and optional parameters

## 🔌 API Endpoints

### Schedule Management

#### Get Student Schedule

```http
GET /api/schedule/{student_id}?semester={semester_id}
```

**Parameters:**

- `student_id` (required): Student identifier
- `semester` (optional): Specific semester ID, defaults to current semester

**Response:**

```json
{
  "status": "Success",
  "message": "Schedule retrieved successfully",
  "data": [
    {
      "course_id": 1,
      "courseName": "CS 101: Introduction to Programming",
      "instructor": "Dr. John Smith",
      "day": "Monday",
      "startTime": "09:00:00",
      "endTime": "10:30:00",
      "location": "Computer Lab 101",
      "semester": "Fall 2024",
      "academic_year": "2024-25",
      "credits": 3,
      "marks": null,
      "markStatus": "In Progress"
    }
  ],
  "weekly_grid": {
    "Monday": [...],
    "Tuesday": [...],
    ...
  }
}
```

#### Get Available Semesters

```http
GET /api/schedule/{student_id}/semesters
```

**Response:**

```json
{
  "status": "Success",
  "data": [
    {
      "semester_id": 1,
      "semester_name": "Fall 2024",
      "academic_year": "2024-25",
      "is_current": true,
      "course_count": 4
    }
  ]
}
```

#### Get Current Semester

```http
GET /api/schedule/current-semester
```

### Academic Progress Tracking

#### Get Student Progress

```http
GET /api/progress/{student_id}
```

**Response:**

```json
{
  "status": "Success",
  "data": {
    "student_info": {
      "student_id": 1,
      "student_name": "John Doe",
      "degree_name": "Computer Science",
      "degree_id": 1,
      "year_of_study": 2
    },
    "academic_summary": {
      "completed_courses": 8,
      "completed_credits": 24.0,
      "gpa": 3.75,
      "current_courses": 4,
      "current_credits": 13.0,
      "total_degree_credits": 120.0,
      "progress_percentage": 30.8
    },
    "completed_courses": [...],
    "pending_requirements": [...],
    "semester_statistics": [...],
    "grade_distribution": {...}
  }
}
```

#### Get Degree Requirements

```http
GET /api/progress/degree-requirements/{degree_id}
```

## 🎨 Frontend Components

### Schedule Manager (JavaScript Class)

```javascript
// Initialize schedule management
const scheduleManager = new ScheduleProgressManager();
scheduleManager.initialize(studentId);

// Load specific semester schedule
scheduleManager.loadStudentSchedule(semesterId);

// Switch between calendar and list views
scheduleManager.showCalendarView();
scheduleManager.showListView();
```

### Key Features:

- **Calendar Grid Generation**: Dynamic 7-day x 12-hour grid
- **Time Slot Management**: Intelligent course placement in time slots
- **View Switching**: Toggle between calendar and list views
- **Responsive Design**: Mobile-friendly layout adaptations

### Progress Tracker (JavaScript Class)

```javascript
// Load academic progress
scheduleManager.loadAcademicProgress();

// Display components
scheduleManager.displayProgressOverview(summary);
scheduleManager.displayCompletedCourses(courses);
scheduleManager.displayPendingRequirements(requirements);
```

## 📱 User Interface

### Schedule Calendar View

- **Time Grid**: 8 AM - 8 PM time slots
- **Day Columns**: Monday through Sunday
- **Course Blocks**: Color-coded by course type (core, elective, lab)
- **Hover Details**: Instructor, location, and course information
- **Responsive**: Collapses to list view on small screens

### Progress Dashboard

- **Progress Cards**: Key statistics with visual indicators
- **Progress Bar**: Animated degree completion percentage
- **Completed Courses**: Sortable table with grades and semesters
- **Requirements Checklist**: Core requirements vs. elective options
- **Grade Analytics**: Distribution charts and GPA tracking

## 🎯 Use Cases

### Personal Schedule Management

#### Use Case 1: View Current Semester Schedule

```
As a student,
I want to view my weekly class schedule,
So that I can plan my daily activities around my courses.
```

**Steps:**

1. Navigate to "My Schedule" tab
2. System displays current semester schedule in calendar format
3. Student can see course times, instructors, and locations
4. Student can switch between calendar and list views

#### Use Case 2: View Past Semester Schedules

```
As a student,
I want to view schedules from previous semesters,
So that I can reference past course arrangements.
```

**Steps:**

1. Access semester selector dropdown
2. Choose desired past semester
3. System loads historical schedule data
4. Student can review past course schedules

### Academic Progress Tracking

#### Use Case 3: Track Degree Progress

```
As a student,
I want to see my overall degree progress,
So that I can understand how close I am to graduation.
```

**Features:**

- Progress percentage calculation
- Credit completion tracking
- GPA monitoring
- Semester-by-semester statistics

#### Use Case 4: View Remaining Requirements

```
As a student,
I want to see what courses I still need to complete,
So that I can plan my future enrollments.
```

**Features:**

- Core requirement identification
- Elective options display
- Year-level recommendations
- Credit hour tracking

## 🔧 Technical Implementation

### Backend Service Layer

```python
class ScheduleProgressService:
    def get_student_schedule(self, student_id, semester_id=None)
    def get_student_academic_progress(self, student_id)
    def get_degree_requirements_overview(self, degree_id)
    def validate_student_access(self, student_id)
```

### Data Access Layer

```python
class ScheduleProgress:
    def get_student_schedule(self, cursor, student_id, semester_id=None)
    def get_weekly_schedule_grid(self, cursor, student_id, semester_id=None)
    def get_student_progress(self, cursor, student_id)
    def get_completed_courses(self, cursor, student_id)
    def get_pending_requirements(self, cursor, student_id)
```

### Database Views

```sql
-- Optimized queries through database views
CREATE VIEW StudentScheduleView AS ...
CREATE VIEW StudentProgressView AS ...
CREATE VIEW PendingRequirementsView AS ...
```

## 🚀 Setup Instructions

### 1. Database Setup

```sql
-- Run the schema creation script
SOURCE database/schedule_progress_schema.sql;

-- Insert sample data
INSERT INTO AcademicSemester ...
INSERT INTO DegreeRequirements ...
```

### 2. Backend Configuration

```python
# Add imports to routes.py
from backend.service.scheduleProgressService import ScheduleProgressService

# Service is automatically available via dependency injection
```

### 3. Frontend Integration

```html
<!-- Add CSS and JavaScript files -->
<link rel="stylesheet" href="static/css/scheduleProgress.css" />
<script src="static/js/scheduleProgress.js"></script>

<!-- Initialize in your page -->
<script>
  const manager = new ScheduleProgressManager();
  manager.initialize(studentId);
</script>
```

## 📊 Performance Optimization

### Database Optimizations

- **Indexed Queries**: Strategic indexes on frequently accessed columns
- **Database Views**: Pre-computed complex queries
- **Query Optimization**: Efficient JOINs and filtered queries

### Frontend Optimizations

- **Lazy Loading**: Load data only when tabs are accessed
- **Caching**: Cache semester and course data
- **Responsive Design**: Efficient mobile layouts

## 🔒 Security Features

### Access Control

- **Student Validation**: Verify student exists and has access
- **Data Isolation**: Students can only access their own data
- **Session Management**: Integrate with existing authentication

### Data Protection

- **SQL Injection Prevention**: Parameterized queries throughout
- **Input Validation**: All parameters validated and sanitized
- **Error Handling**: Secure error messages without data exposure

## 🧪 Testing

### API Testing

```bash
# Test schedule API
curl -X GET "http://localhost:5000/api/schedule/1"

# Test progress API
curl -X GET "http://localhost:5000/api/progress/1"

# Test with semester parameter
curl -X GET "http://localhost:5000/api/schedule/1?semester=2"
```

### Demo Page

Access the interactive demo at `/schedule-progress-demo` to:

- Test all functionality with sample data
- Explore API endpoints
- View responsive design adaptations
- Test error handling scenarios

## 📈 Future Enhancements

### Planned Features

1. **Export Functionality**: Export schedules to calendar apps (iCal, Google Calendar)
2. **Notifications**: Reminders for upcoming classes and deadlines
3. **Study Planner**: Integration with assignment and exam schedules
4. **Academic Advisor Integration**: Share progress with advisors
5. **Mobile App**: Native mobile application
6. **Predictive Analytics**: Suggest optimal course sequences

### Integration Opportunities

1. **LMS Integration**: Connect with learning management systems
2. **Student Information System**: Sync with university databases
3. **Financial Aid**: Link progress to scholarship requirements
4. **Career Services**: Connect progress to career planning

## 🐛 Troubleshooting

### Common Issues

#### Schedule Not Loading

```
Symptoms: Empty calendar or "No schedule found" message
Solutions:
1. Check if student has active enrollments
2. Verify semester_id parameter
3. Ensure CourseSchedule table has data
4. Check database connections
```

#### Progress Data Missing

```
Symptoms: Progress cards showing zeros or "No progress data"
Solutions:
1. Verify student exists in database
2. Check enrollment records
3. Ensure degree requirements are configured
4. Validate course completion data
```

#### API Errors

```
Symptoms: 404 or 500 errors from API endpoints
Solutions:
1. Check student_id validity
2. Verify database connections
3. Review server logs for specific errors
4. Test with demo student IDs
```

## 📞 Support

### Documentation

- **API Documentation**: Detailed endpoint specifications
- **Database Schema**: Complete table structures and relationships
- **Frontend Guide**: Component usage and customization
- **Deployment Guide**: Production setup instructions

### Demo and Testing

- **Live Demo**: `/schedule-progress-demo`
- **API Testing**: Built-in testing interface
- **Sample Data**: Pre-configured test scenarios

---

**📅 Schedule Management & Academic Progress Tracking System - Enhancing Student Academic Success Through Comprehensive Planning and Monitoring**

_Built with Flask, MySQL, JavaScript, and modern web technologies for scalable, efficient student management._
