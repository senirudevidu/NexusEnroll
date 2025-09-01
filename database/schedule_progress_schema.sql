-- Schedule Management and Academic Progress Tracking Schema
-- This script creates tables for semester management and degree requirements

-- Create AcademicSemester table to manage different semesters
CREATE TABLE IF NOT EXISTS AcademicSemester (
    semester_id INT PRIMARY KEY AUTO_INCREMENT,
    semester_name VARCHAR(50) NOT NULL,  -- e.g., "Fall 2024", "Spring 2025"
    start_date DATE NOT NULL,
    end_date DATE NOT NULL,
    is_current BOOLEAN DEFAULT FALSE,
    academic_year VARCHAR(10) NOT NULL,  -- e.g., "2024-25"
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    -- Ensure only one current semester at a time
    UNIQUE KEY unique_current_semester (is_current),
    INDEX idx_academic_year (academic_year),
    INDEX idx_semester_dates (start_date, end_date)
);

-- Create DegreeRequirements table to track what courses are required for each degree
CREATE TABLE IF NOT EXISTS DegreeRequirements (
    requirement_id INT PRIMARY KEY AUTO_INCREMENT,
    degree_id INT NOT NULL,
    course_id INT NOT NULL,
    is_core_requirement BOOLEAN DEFAULT TRUE,  -- TRUE for core, FALSE for elective
    year_requirement INT DEFAULT NULL,  -- Which year this should typically be taken
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    FOREIGN KEY (degree_id) REFERENCES Degree(degree_ID) ON DELETE CASCADE,
    FOREIGN KEY (course_id) REFERENCES Course(course_id) ON DELETE CASCADE,
    
    -- Prevent duplicate requirements
    UNIQUE KEY unique_degree_course (degree_id, course_id),
    INDEX idx_degree_requirements (degree_id),
    INDEX idx_course_requirements (course_id)
);

-- Add semester_id to Enrollment table for tracking which semester courses were taken
ALTER TABLE Enrollment 
ADD COLUMN semester_id INT DEFAULT NULL,
ADD FOREIGN KEY (semester_id) REFERENCES AcademicSemester(semester_id) ON DELETE SET NULL,
ADD INDEX idx_enrollment_semester (semester_id);

-- Add location field to CourseSchedule for room information
ALTER TABLE CourseSchedule 
ADD COLUMN location VARCHAR(100) DEFAULT NULL AFTER endTime;

-- Insert sample academic semesters
INSERT IGNORE INTO AcademicSemester (semester_name, start_date, end_date, is_current, academic_year) VALUES
('Fall 2023', '2023-08-15', '2023-12-15', FALSE, '2023-24'),
('Spring 2024', '2024-01-15', '2024-05-15', FALSE, '2023-24'),
('Fall 2024', '2024-08-15', '2024-12-15', TRUE, '2024-25'),
('Spring 2025', '2025-01-15', '2025-05-15', FALSE, '2024-25');

-- Sample degree requirements (assuming some courses exist)
-- Note: Adjust course_id values based on your actual Course table
INSERT IGNORE INTO DegreeRequirements (degree_id, course_id, is_core_requirement, year_requirement) VALUES
-- Computer Science degree requirements (assuming degree_id = 1)
(1, 1, TRUE, 1),   -- Core course for year 1
(1, 2, TRUE, 1),   -- Core course for year 1
(1, 3, FALSE, 2),  -- Elective for year 2
(1, 4, TRUE, 2),   -- Core course for year 2
-- Engineering degree requirements (assuming degree_id = 2)
(2, 1, TRUE, 1),   -- Shared core course
(2, 2, FALSE, 1),  -- Elective
(2, 5, TRUE, 2);   -- Core course for year 2

-- Create view for student schedule with semester information
CREATE OR REPLACE VIEW StudentScheduleView AS
SELECT 
    e.student_id,
    e.course_id,
    c.courseName,
    CONCAT(u.firstName, ' ', u.lastName) as instructor_name,
    cs.day,
    cs.startTime,
    cs.endTime,
    cs.location,
    sem.semester_name,
    sem.academic_year,
    c.credits,
    e.marks,
    e.markStatus,
    e.enrollmentStatus
FROM Enrollment e
JOIN Course c ON e.course_id = c.course_id
JOIN Users u ON c.facultyMem_Id = u.user_id
LEFT JOIN CourseSchedule cs ON c.course_id = cs.course_id
LEFT JOIN AcademicSemester sem ON e.semester_id = sem.semester_id
WHERE e.enrollmentStatus = 'Active'
ORDER BY e.student_id, cs.day, cs.startTime;

-- Create view for academic progress tracking
CREATE OR REPLACE VIEW StudentProgressView AS
SELECT 
    s.student_Id,
    CONCAT(u.firstName, ' ', u.lastName) as student_name,
    d.name as degree_name,
    d.degree_ID,
    s.YearOfStudy,
    
    -- Completed courses statistics
    COUNT(CASE WHEN e.markStatus = 'Completed' AND e.enrollmentStatus = 'Active' THEN 1 END) as completed_courses,
    SUM(CASE WHEN e.markStatus = 'Completed' AND e.enrollmentStatus = 'Active' THEN c.credits ELSE 0 END) as completed_credits,
    AVG(CASE WHEN e.markStatus = 'Completed' AND e.marks IS NOT NULL THEN e.marks END) as gpa,
    
    -- Current semester statistics
    COUNT(CASE WHEN e.markStatus = 'In Progress' AND e.enrollmentStatus = 'Active' THEN 1 END) as current_courses,
    SUM(CASE WHEN e.markStatus = 'In Progress' AND e.enrollmentStatus = 'Active' THEN c.credits ELSE 0 END) as current_credits,
    
    -- Total degree credit requirement
    d.credit as total_degree_credits,
    
    -- Progress percentage
    ROUND((SUM(CASE WHEN e.markStatus = 'Completed' AND e.enrollmentStatus = 'Active' THEN c.credits ELSE 0 END) / d.credit) * 100, 2) as progress_percentage

FROM Student s
JOIN Users u ON s.student_Id = u.user_id
JOIN Degree d ON s.degree_ID = d.degree_ID
LEFT JOIN Enrollment e ON s.student_Id = e.student_id
LEFT JOIN Course c ON e.course_id = c.course_id
GROUP BY s.student_Id, u.firstName, u.lastName, d.name, d.degree_ID, s.YearOfStudy, d.credit;

-- Create view for pending degree requirements
CREATE OR REPLACE VIEW PendingRequirementsView AS
SELECT 
    s.student_Id,
    d.degree_ID,
    dr.requirement_id,
    c.course_id,
    c.courseName,
    c.description,
    c.credits,
    dr.is_core_requirement,
    dr.year_requirement,
    CASE 
        WHEN dr.is_core_requirement = TRUE THEN 'Core Requirement'
        ELSE 'Elective Option'
    END as requirement_type
FROM Student s
JOIN Degree d ON s.degree_ID = d.degree_ID
JOIN DegreeRequirements dr ON d.degree_ID = dr.degree_id
JOIN Course c ON dr.course_id = c.course_id
LEFT JOIN Enrollment e ON (s.student_Id = e.student_id AND c.course_id = e.course_id AND e.enrollmentStatus = 'Active')
WHERE e.enrollment_id IS NULL  -- Student hasn't taken this required course
ORDER BY s.student_Id, dr.is_core_requirement DESC, dr.year_requirement ASC;

-- Indexes for better performance
CREATE INDEX idx_enrollment_semester_status ON Enrollment(semester_id, enrollmentStatus);
CREATE INDEX idx_student_progress ON Enrollment(student_id, markStatus, enrollmentStatus);
CREATE INDEX idx_degree_requirements_lookup ON DegreeRequirements(degree_id, is_core_requirement);

-- Comments
-- AcademicSemester: Manages different academic terms/semesters
-- DegreeRequirements: Defines what courses are required for each degree program
-- StudentScheduleView: Provides complete schedule information for students
-- StudentProgressView: Shows academic progress statistics for each student
-- PendingRequirementsView: Shows what courses students still need to complete their degree
