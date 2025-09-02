# NexusEnroll - The Course Enrollment System

Project to modernize a legacy university course enrollment system. Focuses on building a scalable, modular, and user-friendly platform with real-time updates and mobile access. Designed for demonstration and educational purposes only.

## Table of Contents

- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Configuration](#configuration)
- [Running the Application](#running-the-application)
- [How to Use](#how-to-use)
- [Project Structure](#project-structure)
- [Features](#features)
- [Troubleshooting](#troubleshooting)

## Prerequisites

Before running this application, ensure you have the following installed:

### Required Software

1. **Python 3.8 or higher**

   - Download from [python.org](https://www.python.org/downloads/)
   - Verify installation: `python --version`

2. **MySQL Database**

   - Install MySQL Server from [mysql.com](https://dev.mysql.com/downloads/mysql/)
   - Or use a cloud MySQL service (the project is currently configured for a remote MySQL database)

3. **Git** (optional, for cloning)
   - Download from [git-scm.com](https://git-scm.com/downloads/)

### Required Python Packages

The application requires the following Python packages:

- Flask (web framework)
- mysql-connector-python (MySQL database connector)
- Other standard Python libraries

## Installation

### Step 1: Clone or Download the Project

```bash
git clone https://github.com/senirudevidu/NexusEnroll--The-Course-Enrolment-System.git
cd NexusEnroll--The-Course-Enrolment-System
```

### Step 2: Set Up Virtual Environment (Recommended)

```bash
# Create virtual environment
python -m venv env

# Activate virtual environment
# On Windows:
env\Scripts\activate
# On macOS/Linux:
source env/bin/activate
```

### Step 3: Install Required Packages

```bash
# Install Flask
pip install Flask

# Install MySQL connector
pip install mysql-connector-python

# Or install all at once
pip install Flask mysql-connector-python
```

## Configuration

### Database Configuration

The application is currently configured to use a remote MySQL database. The configuration is in `backend/dal/dbconfig.py`:

```python
host = "mysql-nexusenroll.alwaysdata.net"
user = "427694"
password = "Ugvle@123"
database = "nexusenroll_db"
```

**Note:** For production use, it's recommended to:

1. Use environment variables for database credentials
2. Set up your own MySQL database
3. Update the database configuration accordingly

### Local Database Setup (Optional)

If you want to set up a local MySQL database:

1. Create a new MySQL database
2. Update the credentials in `backend/dal/dbconfig.py`
3. Import the database schema (if available)

## Running the Application

### Step 1: Navigate to Project Directory

```bash
cd path/to/NexusEnroll
```

### Step 2: Activate Virtual Environment (if using)

```bash
# On Windows:
env\Scripts\activate
# On macOS/Linux:
source env/bin/activate
```

### Step 3: Run the Application

```bash
python app.py
```

### Step 4: Access the Application

Once the server starts, you'll see output similar to:

```
* Running on http://127.0.0.1:5000
* Debug mode: on
```

Open your web browser and navigate to:

- **Main Application:** http://127.0.0.1:5000 or http://localhost:5000

## How to Use

### User Roles and Dashboards

The system supports multiple user roles, each with their own dashboard:

1. **Student Dashboard** (`/student_dashboard`)

   - View available courses
   - Enroll in courses
   - View enrollment status
   - Track academic progress

2. **Faculty Dashboard** (`/faculty_dashboard`)

   - Manage course assignments
   - View student rosters
   - Submit grades
   - Generate reports

3. **Admin Dashboard** (`/admin_dashboard`)

   - Manage users (students, faculty, admin)
   - Manage courses and departments
   - View system reports
   - Handle course requests

4. **Reports Dashboard** (`/reports_dashboard`)
   - Generate enrollment statistics
   - Faculty workload reports
   - Department-wise reports

### Navigation

- **Login Page:** `/login` - Main entry point for user authentication
- **Home Page:** `/` - Landing page with system overview
- **Add Users:** `/add_user` - Administrative function to add new users
- **Add Courses:** `/add_course` - Administrative function to add new courses
- **Add Departments:** `/add_department` - Administrative function to add new departments
- **Add Degrees:** `/add_degree` - Administrative function to add new degree programs

## Testing Credentials

For testing purposes, the following accounts have been pre-configured in the system:

### Login Information

- **Username:** Email address used during registration
- **Password:** Mobile number provided during registration

### Test Accounts

| Role    | Username (Email)  | Password   |
| ------- | ----------------- | ---------- |
| Admin   | seniru@gmail.com  | 0712345678 |
| Faculty | minoli@gmail.com  | 0712345678 |
| Student | ramsith@gmail.com | 0712345678 |

### How to Login

1. Navigate to the login page: http://localhost:5000/login
2. Enter the email address as username
3. Enter the mobile number as password
4. Click login to access the respective dashboard

**Note:** These are test credentials for demonstration purposes only. In a production environment, ensure proper password security and user management practices.

## Project Structure

```
NexusEnroll/
├── app.py                 # Main Flask application entry point
├── README.md             # This file
├── backend/              # Backend application logic
│   ├── dal/              # Data Access Layer
│   │   ├── dbconfig.py   # Database configuration
│   │   ├── user.py       # User data models
│   │   ├── course.py     # Course data models
│   │   └── ...           # Other data models
│   ├── service/          # Business Logic Layer
│   │   ├── userService.py
│   │   ├── courseService.py
│   │   └── ...           # Other services
│   └── presentation/     # Presentation Layer
│       ├── routes.py     # Flask routes/endpoints
│       └── reports.py    # Report generation
├── static/               # Static files (CSS, JS)
│   ├── css/             # Stylesheets
│   └── js/              # JavaScript files
├── templates/           # HTML templates
└── env/                # Virtual environment (if using)
```

## Architecture

NexusEnroll follows a **3-Tier Layered Architecture** pattern that promotes separation of concerns and maintainability:

### 1. Presentation Layer (`backend/presentation/`)

- **Routes (`routes.py`)**: Handles HTTP requests, routing, and response formatting
- **Reports (`reports.py`)**: Manages report generation and presentation logic
- Responsible for user interface interaction and request/response handling

### 2. Business Logic Layer (`backend/service/`)

- Contains all business rules and application logic
- Services include: `userService.py`, `courseService.py`, `enrollmentService.py`, etc.
- Acts as an intermediary between presentation and data access layers

### 3. Data Access Layer (`backend/dal/`)

- **Database Configuration (`dbconfig.py`)**: Manages database connections
- **Data Models**: `user.py`, `course.py`, `enrollment.py`, etc.
- Handles all database operations and data persistence

## Design Patterns Implementation

The system implements several software design patterns to ensure code reusability, maintainability, and extensibility:

### 1. **Abstract Factory Pattern**

- **Location**: `backend/dal/user.py` (Lines 402-418)
- **Implementation**:
  - Abstract `UserFactory` class
  - Concrete factories: `StudentFactory`, `FacultyMemberFactory`, `AdminFactory`
- **Purpose**: Creates different types of user objects without specifying exact classes
- **Usage**: Used in service layer to create appropriate user instances

### 2. **Template Method Pattern**

- **Location**: `backend/presentation/reports.py` (Lines 1-21)
- **Implementation**:
  - Abstract `GenerateReport` class with template methods
  - Concrete implementations: `EnrollmentStatisticsReport`, `FacultyWorkloadReport`
- **Purpose**: Defines skeleton of report generation algorithm
- **Template Methods**: `getData()`, `processData()`, `outputData()`

### 3. **Observer Pattern**

- **Location**: `backend/service/notificationService.py` (Lines 8-100)
- **Implementation**:
  - `NotificationObserver` interface (Abstract Observer)
  - `NotificationSubject` interface (Abstract Subject)
  - `EnrollmentNotificationSubject` (Concrete Subject)
  - Various concrete observers: `StudentObserver`, `FacultyObserver`, etc.
- **Purpose**: Implements notification system for enrollment events
- **Demo**: Available at `/notification_demo` route

### 4. **Repository Pattern**

- **Location**: Throughout `backend/dal/` directory
- **Implementation**:
  - Data access objects encapsulate database operations
  - Each entity has its own repository (e.g., `user.py`, `course.py`, `enrollment.py`)
- **Purpose**: Abstracts data access logic and provides centralized data access

### 5. **Service Layer Pattern**

- **Location**: `backend/service/` directory
- **Implementation**: All business logic is encapsulated in service classes
- **Purpose**: Separates business logic from presentation and data access layers

### 6. **Strategy Pattern**

- **Location**: `backend/presentation/reports.py`
- **Implementation**: Different report generation strategies
- **Purpose**: Allows switching between different report generation algorithms at runtime

## Features

- **Multi-role Authentication**: Support for students, faculty, and administrators
- **Course Management**: Add, edit, and manage courses and departments
- **Enrollment System**: Student course enrollment and management
- **Grade Management**: Faculty grade submission and tracking
- **Reporting System**: Comprehensive reports for various stakeholders
- **Responsive Design**: Mobile-friendly interface
- **Real-time Updates**: Dynamic content updates
- **Design Pattern Demonstration**: Observer pattern demo available at `/notification_demo`

## Troubleshooting

### Common Issues

1. **Database Connection Error**

   - Verify MySQL server is running
   - Check database credentials in `dbconfig.py`
   - Ensure network connectivity to the database server

2. **Module Import Errors**

   - Ensure virtual environment is activated
   - Install missing packages: `pip install package_name`
   - Verify Python path includes the project directory

3. **Port Already in Use**

   - Change the port in `app.py`: `app.run(debug=True, port=5001)`
   - Or stop the process using port 5000

4. **Template Not Found Errors**

   - Ensure all HTML templates are in the `templates/` directory
   - Check file paths and naming conventions

5. **Static Files Not Loading**
   - Verify CSS and JS files are in the `static/` directory
   - Check file paths in HTML templates

### Getting Help

If you encounter issues:

1. Check the console output for error messages
2. Verify all prerequisites are installed
3. Ensure database connectivity
4. Review the project documentation

### Development Mode

The application runs in debug mode by default, which provides:

- Automatic reloading on code changes
- Detailed error messages
- Interactive debugger

For production deployment, disable debug mode in `app.py`:

```python
app.run(debug=False)
```


## UI
### Landing
<img width="1916" height="1199" alt="image" src="https://github.com/user-attachments/assets/412125e4-b77c-4e5c-83a7-7d416f06b13f" />

### Login
<img width="1911" height="1190" alt="image" src="https://github.com/user-attachments/assets/762b9078-d816-4b5f-ab54-97e2689fbf2f" />

### Admin
<img width="1889" height="1183" alt="image" src="https://github.com/user-attachments/assets/95f57254-fa22-4b06-8c58-dfd3f7643963" /><img width="1893" height="1187" alt="image" src="https://github.com/user-attachments/assets/b8bf1d13-6ca8-4290-8cc1-f9c240c3b7fb" /><img width="1915" height="1194" alt="image" src="https://github.com/user-attachments/assets/f9cec7b4-2071-4add-968f-bb9b888c030a" />

### Faculty
<img width="1916" height="984" alt="image" src="https://github.com/user-attachments/assets/1db5c005-c8ab-400e-aa75-dd8d8875cb8d" /><img width="1904" height="1177" alt="image" src="https://github.com/user-attachments/assets/50b8316b-1d4a-4668-8e7b-e0b91fd2160b" /><img width="1918" height="1195" alt="image" src="https://github.com/user-attachments/assets/019a49d9-69d3-4bf4-a417-e0f4bdd2c132" /><img width="1919" height="1196" alt="image" src="https://github.com/user-attachments/assets/cfe0884e-7355-48ea-ac00-28b1519eeb30" />

### Student
<img width="1915" height="1198" alt="image" src="https://github.com/user-attachments/assets/a1fb6744-fe1d-44fb-9212-e66f65e148ef" /><img width="1916" height="1181" alt="image" src="https://github.com/user-attachments/assets/b0965411-b979-4a75-a421-2c89499586a4" /><img width="1919" height="1171" alt="image" src="https://github.com/user-attachments/assets/88df1d31-2ac1-4a93-a26e-29c93edf0e42" />








