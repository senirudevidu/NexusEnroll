-- Create CourseRequest table if it doesn't exist
CREATE TABLE IF NOT EXISTS CourseRequest (
    request_id INT AUTO_INCREMENT PRIMARY KEY,
    facultyMem_Id INT NOT NULL,
    course_id INT NOT NULL,
    requestType VARCHAR(50) NOT NULL,
    details TEXT,
    requestDate TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    status ENUM('Pending', 'Approved', 'Rejected') DEFAULT 'Pending',
    decisionDate TIMESTAMP NULL,
    approvedBy INT NULL,
    FOREIGN KEY (facultyMem_Id) REFERENCES Users(user_id),
    FOREIGN KEY (course_id) REFERENCES Course(course_id),
    FOREIGN KEY (approvedBy) REFERENCES Users(user_id)
);
