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

## Features

- **Multi-role Authentication**: Support for students, faculty, and administrators
- **Course Management**: Add, edit, and manage courses and departments
- **Enrollment System**: Student course enrollment and management
- **Grade Management**: Faculty grade submission and tracking
- **Reporting System**: Comprehensive reports for various stakeholders
- **Responsive Design**: Mobile-friendly interface
- **Real-time Updates**: Dynamic content updates

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
