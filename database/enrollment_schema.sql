-- Enrollment table creation script for NexusEnroll system
-- This script creates the Enrollment table with all required fields

-- Create Enrollment table
CREATE TABLE IF NOT EXISTS Enrollment (
    enrollment_id INT PRIMARY KEY AUTO_INCREMENT,
    student_id INT NOT NULL,
    course_id INT NOT NULL,
    markStatus VARCHAR(20) DEFAULT 'In Progress',  -- 'In Progress', 'Completed', 'Failed'
    marks DECIMAL(5,2) DEFAULT NULL,
    lastUpdated TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    enrollmentStatus VARCHAR(20) DEFAULT 'Active', -- 'Active', 'Dropped', 'Pending'
    enrollmentDate TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    -- Foreign key constraints
    FOREIGN KEY (student_id) REFERENCES Student(student_Id) ON DELETE CASCADE,
    FOREIGN KEY (course_id) REFERENCES Course(course_id) ON DELETE CASCADE,
    
    -- Unique constraint to prevent duplicate enrollments
    UNIQUE KEY unique_enrollment (student_id, course_id, enrollmentStatus),
    
    -- Indexes for better performance
    INDEX idx_student_enrollments (student_id, enrollmentStatus),
    INDEX idx_course_enrollments (course_id, enrollmentStatus),
    INDEX idx_enrollment_status (enrollmentStatus),
    INDEX idx_mark_status (markStatus)
);

-- Optional: Create CourseSchedule table for time conflict checking
-- This table stores the schedule information for courses
CREATE TABLE IF NOT EXISTS CourseSchedule (
    schedule_id INT PRIMARY KEY AUTO_INCREMENT,
    course_id INT NOT NULL,
    day VARCHAR(50) NOT NULL,  -- Changed from day_of_week ENUM to day VARCHAR
    startTime TIME NOT NULL,   -- Changed from start_time to startTime
    endTime TIME NOT NULL,     -- Changed from end_time to endTime
    
    -- Foreign key constraint
    FOREIGN KEY (course_id) REFERENCES Course(course_id) ON DELETE CASCADE,
    
    -- Index for better performance
    INDEX idx_course_schedule (course_id, day)
);

-- Sample data insertion for testing (optional)
-- Insert some sample course schedules
INSERT IGNORE INTO CourseSchedule (course_id, day, startTime, endTime) VALUES
(1, 'Monday', '09:00:00', '10:00:00'),
(1, 'Wednesday', '09:00:00', '10:00:00'),
(1, 'Friday', '09:00:00', '10:00:00'),
(2, 'Tuesday', '11:00:00', '12:30:00'),
(2, 'Thursday', '11:00:00', '12:30:00');

-- Sample enrollment data (optional)
-- Note: This assumes student IDs and course IDs exist in your system
-- INSERT IGNORE INTO Enrollment (student_id, course_id, markStatus, enrollmentStatus) VALUES
-- (1, 1, 'In Progress', 'Active'),
-- (1, 2, 'In Progress', 'Active'),
-- (2, 1, 'Completed', 'Active'),
-- (3, 2, 'In Progress', 'Active');

-- Create a view for easy enrollment reporting
CREATE OR REPLACE VIEW EnrollmentReport AS
SELECT 
    e.enrollment_id,
    e.student_id,
    CONCAT(u.firstName, ' ', u.lastName) as student_name,
    e.course_id,
    c.courseName,
    c.credits,
    CONCAT(f.firstName, ' ', f.lastName) as instructor_name,
    d.deptName as department,
    e.markStatus,
    e.marks,
    e.enrollmentStatus,
    e.enrollmentDate,
    e.lastUpdated
FROM Enrollment e
JOIN Student s ON e.student_id = s.student_Id
JOIN Users u ON s.student_Id = u.user_id
JOIN Course c ON e.course_id = c.course_id
JOIN Users f ON c.facultyMem_Id = f.user_id
JOIN Department d ON c.dept_Id = d.dept_Id
WHERE e.enrollmentStatus = 'Active';

-- Create a view for course enrollment statistics
CREATE OR REPLACE VIEW CourseEnrollmentStats AS
SELECT 
    c.course_id,
    c.courseName,
    c.capacity,
    c.availableSeats,
    (c.capacity - c.availableSeats) as enrolled_count,
    ROUND(((c.capacity - c.availableSeats) / c.capacity) * 100, 2) as enrollment_percentage,
    d.deptName as department,
    CONCAT(u.firstName, ' ', u.lastName) as instructor_name
FROM Course c
JOIN Department d ON c.dept_Id = d.dept_Id
JOIN Users u ON c.facultyMem_Id = u.user_id
ORDER BY enrollment_percentage DESC;

-- Create a view for student enrollment summary
CREATE OR REPLACE VIEW StudentEnrollmentSummary AS
SELECT 
    s.student_Id,
    CONCAT(u.firstName, ' ', u.lastName) as student_name,
    u.email,
    d.name as degree_name,
    s.YearOfStudy,
    COUNT(e.enrollment_id) as total_enrollments,
    SUM(CASE WHEN e.markStatus = 'Completed' THEN 1 ELSE 0 END) as completed_courses,
    SUM(CASE WHEN e.markStatus = 'In Progress' THEN 1 ELSE 0 END) as in_progress_courses,
    SUM(CASE WHEN e.markStatus = 'Completed' THEN c.credits ELSE 0 END) as completed_credits,
    SUM(CASE WHEN e.markStatus = 'In Progress' THEN c.credits ELSE 0 END) as current_credits,
    AVG(CASE WHEN e.marks IS NOT NULL THEN e.marks ELSE NULL END) as gpa
FROM Student s
JOIN Users u ON s.student_Id = u.user_id
JOIN Degree d ON s.degree_ID = d.degree_ID
LEFT JOIN Enrollment e ON s.student_Id = e.student_id AND e.enrollmentStatus = 'Active'
LEFT JOIN Course c ON e.course_id = c.course_id
GROUP BY s.student_Id, u.firstName, u.lastName, u.email, d.name, s.YearOfStudy;

-- Triggers for automatic course capacity updates
DELIMITER //

-- Trigger to decrease available seats when enrollment is added
CREATE TRIGGER after_enrollment_insert
    AFTER INSERT ON Enrollment
    FOR EACH ROW
BEGIN
    IF NEW.enrollmentStatus = 'Active' THEN
        UPDATE Course 
        SET availableSeats = availableSeats - 1 
        WHERE course_id = NEW.course_id AND availableSeats > 0;
    END IF;
END//

-- Trigger to increase available seats when enrollment is dropped
CREATE TRIGGER after_enrollment_update
    AFTER UPDATE ON Enrollment
    FOR EACH ROW
BEGIN
    IF OLD.enrollmentStatus = 'Active' AND NEW.enrollmentStatus = 'Dropped' THEN
        UPDATE Course 
        SET availableSeats = availableSeats + 1 
        WHERE course_id = NEW.course_id AND availableSeats < capacity;
    ELSEIF OLD.enrollmentStatus = 'Dropped' AND NEW.enrollmentStatus = 'Active' THEN
        UPDATE Course 
        SET availableSeats = availableSeats - 1 
        WHERE course_id = NEW.course_id AND availableSeats > 0;
    END IF;
END//

DELIMITER ;

-- Indexes for optimization
CREATE INDEX idx_enrollment_date ON Enrollment(enrollmentDate);
CREATE INDEX idx_last_updated ON Enrollment(lastUpdated);
CREATE INDEX idx_student_course ON Enrollment(student_id, course_id);

-- Comments explaining the schema
-- enrollment_id: Primary key for the enrollment record
-- student_id: Foreign key referencing the student
-- course_id: Foreign key referencing the course
-- markStatus: Current status of the student in the course (In Progress, Completed, Failed)
-- marks: Final grade/marks received (null if not yet graded)
-- lastUpdated: Automatically updated timestamp for any changes
-- enrollmentStatus: Status of the enrollment (Active, Dropped, Pending)
-- enrollmentDate: When the student enrolled in the course
