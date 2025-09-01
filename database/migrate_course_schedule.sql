-- Migration script to update CourseSchedule table column names
-- This script renames columns to match your database schema

-- If you already have a CourseSchedule table with the old column names, 
-- use this script to rename them to the new names

-- Rename columns in existing CourseSchedule table
ALTER TABLE CourseSchedule 
CHANGE COLUMN day_of_week day VARCHAR(50) NOT NULL,
CHANGE COLUMN start_time startTime TIME NOT NULL,
CHANGE COLUMN end_time endTime TIME NOT NULL;

-- Drop the location column if it exists and you don't need it
-- ALTER TABLE CourseSchedule DROP COLUMN location;

-- Update the index to use the new column name
DROP INDEX idx_course_schedule ON CourseSchedule;
CREATE INDEX idx_course_schedule ON CourseSchedule (course_id, day);

-- Verify the changes
DESCRIBE CourseSchedule;
