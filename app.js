// Behavioral Pattern: Observer for Grade Submissions
class GradeObserver {
    update(gradeData) {
        console.log('Grade submitted:', gradeData);
        this.notifyAdmin(gradeData);
        this.updateStudentRecords(gradeData);
        this.sendConfirmation(gradeData);
    }

    notifyAdmin(gradeData) {
        console.log('📧 Admin notified about grade submission for:', gradeData.course);
        // Simulate email to admin
        const adminMessage = `
            NEW GRADE SUBMISSION
            Course: ${gradeData.course}
            Professor: ${gradeData.professor}
            Students Graded: ${gradeData.students.length}
            Submission Time: ${new Date(gradeData.timestamp).toLocaleString()}
        `;
        console.log('Admin Notification:', adminMessage);
    }

    updateStudentRecords(gradeData) {
        console.log('📊 Updating student records for:', gradeData.course);
        gradeData.students.forEach(student => {
            console.log(`✅ Updated ${student.name} (${student.id}): ${student.grade}`);
            // Simulate database update
        });
    }

    sendConfirmation(gradeData) {
        console.log('✉️ Confirmation sent to professor:', gradeData.professor);
        // Simulate confirmation email
    }
}

class GradeSubject {
    constructor() {
        this.observers = [];
    }

    attach(observer) {
        this.observers.push(observer);
    }

    notifyAll(gradeData) {
        this.observers.forEach(observer => observer.update(gradeData));
    }
}

// Initialize Observer Pattern
const gradeSubject = new GradeSubject();
gradeSubject.attach(new GradeObserver());

// Mock Data
const courses = {
    CS101: {
        name: "Introduction to Computer Science",
        schedule: "MWF 9:00-10:00 AM | Tech Building 101",
        enrollment: "25/30 students",
        students: [
            { id: "ST2024001", name: "Alex Thompson", email: "alex.thompson@university.edu", phone: "(555) 123-4567", grade: "" },
            { id: "ST2024002", name: "Sarah Wilson", email: "sarah.wilson@university.edu", phone: "(555) 234-5678", grade: "" },
            { id: "ST2024003", name: "Mike Chen", email: "mike.chen@university.edu", phone: "(555) 345-6789", grade: "" }
        ]
    },
    CS201: {
        name: "Advanced Programming",
        schedule: "TTh 2:00-3:30 PM | CS Building 205",
        enrollment: "18/25 students",
        students: [
            { id: "ST2024004", name: "Emily Davis", email: "emily.davis@university.edu", phone: "(555) 456-7890", grade: "" },
            { id: "ST2024005", name: "David Brown", email: "david.brown@university.edu", phone: "(555) 567-8901", grade: "" }
        ]
    }
};

// Tab navigation
function openTab(tabId) {
    document.querySelectorAll('.tab-pane').forEach(pane => {
        pane.classList.remove('active');
    });
    document.getElementById(tabId).classList.add('active');

    document.querySelectorAll('.tab-button').forEach(button => {
        button.classList.remove('active');
    });
    event.currentTarget.classList.add('active');

    // Load data when switching to specific tabs
    if (tabId === 'class-rosters') {
        loadRoster();
    } else if (tabId === 'grade-submission') {
        // Reset grade sheet when switching to this tab
        document.getElementById('grade-course-select').value = '';
        document.getElementById('grade-table-body').innerHTML = '';
        document.querySelector('.submit-btn').disabled = true;
    }
}

// Class Rosters Functions (First Tab)
function loadRoster() {
    const courseSelect = document.getElementById('roster-course-select');
    const courseCode = courseSelect.value;
    const tbody = document.getElementById('roster-table-body');

    tbody.innerHTML = '';

    if (courseCode && courses[courseCode]) {
        const course = courses[courseCode];
        
        // Add course header
        const headerRow = document.createElement('tr');
        headerRow.innerHTML = `
            <td colspan="4" style="background: #f0f8ff; font-weight: bold; text-align: center; padding: 15px;">
                ${courseCode}: ${course.name} - Total Students: ${course.students.length}
            </td>
        `;
        tbody.appendChild(headerRow);

        // Add student rows
        course.students.forEach(student => {
            const row = document.createElement('tr');
            row.innerHTML = `
                <td><strong>${student.id}</strong></td>
                <td>${student.name}</td>
                <td>${student.email}</td>
                <td>${student.phone}</td>
            `;
            tbody.appendChild(row);
        });
    }
}

// Grade Submission Functions (Second Tab)
function loadGradeSheet() {
    const courseSelect = document.getElementById('grade-course-select');
    const courseCode = courseSelect.value;
    const tbody = document.getElementById('grade-table-body');
    const submitBtn = document.querySelector('.submit-btn');

    tbody.innerHTML = '';
    submitBtn.disabled = true;

    if (courseCode && courses[courseCode]) {
        const course = courses[courseCode];
        
        // Add course header
        const headerRow = document.createElement('tr');
        headerRow.innerHTML = `
            <td colspan="4" style="background: #fffacd; font-weight: bold; text-align: center; padding: 15px;">
                ${courseCode}: ${course.name} - Grade Submission
            </td>
        `;
        tbody.appendChild(headerRow);

        // Add student rows with grade selection
        course.students.forEach(student => {
            const row = document.createElement('tr');
            row.innerHTML = `
                <td><strong>${student.id}</strong></td>
                <td>${student.name}</td>
                <td>
                    <select onchange="updateStudentGrade('${courseCode}', '${student.id}', this.value)" 
                            style="padding: 8px; border-radius: 4px; border: 1px solid #ccc; width: 100%;">
                        <option value="">Select Grade</option>
                        <option value="A" ${student.grade === 'A' ? 'selected' : ''}>A</option>
                        <option value="B" ${student.grade === 'B' ? 'selected' : ''}>B</option>
                        <option value="C" ${student.grade === 'C' ? 'selected' : ''}>C</option>
                        <option value="D" ${student.grade === 'D' ? 'selected' : ''}>D</option>
                        <option value="F" ${student.grade === 'F' ? 'selected' : ''}>F</option>
                    </select>
                </td>
                <td>
                    <span class="status-badge ${student.grade ? 'status-graded' : 'status-pending'}">
                        ${student.grade ? 'Graded' : 'Pending'}
                    </span>
                </td>
            `;
            tbody.appendChild(row);
        });
        submitBtn.disabled = false;
    }
}

function updateStudentGrade(courseCode, studentId, grade) {
    const student = courses[courseCode].students.find(s => s.id === studentId);
    if (student) {
        student.grade = grade;
        // Update status badge
        const rows = document.querySelectorAll('#grade-table-body tr');
        rows.forEach((row, index) => {
            if (index > 0) { // Skip header row
                const cells = row.cells;
                if (cells[0].textContent.includes(studentId)) {
                    cells[3].innerHTML = `
                        <span class="status-badge ${grade ? 'status-graded' : 'status-pending'}">
                            ${grade ? 'Graded' : 'Pending'}
                        </span>
                    `;
                }
            }
        });
    }
}

function submitGrades() {
    const courseSelect = document.getElementById('grade-course-select');
    const courseCode = courseSelect.value;
    
    if (courseCode && courses[courseCode]) {
        const gradedStudents = courses[courseCode].students.filter(s => s.grade);
        if (gradedStudents.length === courses[courseCode].students.length) {
            // Notify observers using Behavioral Pattern
            gradeSubject.notifyAll({
                course: courseCode,
                students: gradedStudents,
                timestamp: new Date().toISOString(),
                professor: "Dr. Sarah Johnson"
            });
            
            alert('✅ Grades submitted successfully!\n\nAdmin has been notified and student records have been updated.');
            
            // Reset form
            courseSelect.value = '';
            document.getElementById('grade-table-body').innerHTML = '';
            document.querySelector('.submit-btn').disabled = true;
            
        } else {
            const pendingCount = courses[courseCode].students.length - gradedStudents.length;
            alert(`Please grade all students before submitting. ${pendingCount} student(s) still need grades.`);
        }
    }
}

// My Courses Functions (Third Tab)
function updateCourseInfo(courseCode) {
    alert(`Update course information for ${courseCode}\n\nThis would open a course editing form.`);
}

function requestChanges(courseCode) {
    alert(`Request changes for ${courseCode}\n\nThis would open a change request form for administration.`);
}

// Initialize page
document.addEventListener('DOMContentLoaded', function() {
    // Set first tab as active
    openTab('class-rosters');
    
    console.log('Faculty dashboard initialized with Observer pattern');
});