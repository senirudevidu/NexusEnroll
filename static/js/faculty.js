// Behavioral Pattern: Observer for Grade Submissions
class GradeObserver {
  update(gradeData) {
    console.log("Grade submitted:", gradeData);
    this.notifyAdmin(gradeData);
    this.updateStudentRecords(gradeData);
    this.sendConfirmation(gradeData);
  }

  notifyAdmin(gradeData) {
    console.log(
      "📧 Admin notified about grade submission for:",
      gradeData.course
    );
    // Simulate email to admin
    const adminMessage = `
            NEW GRADE SUBMISSION
            Course: ${gradeData.course}
            Professor: ${gradeData.professor}
            Students Graded: ${gradeData.students.length}
            Submission Time: ${new Date(gradeData.timestamp).toLocaleString()}
        `;
    console.log("Admin Notification:", adminMessage);
  }

  updateStudentRecords(gradeData) {
    console.log("📊 Updating student records for:", gradeData.course);
    gradeData.students.forEach((student) => {
      console.log(
        `✅ Updated ${student.name} (${student.id}): ${student.grade}`
      );
      // Simulate database update
    });
  }

  sendConfirmation(gradeData) {
    console.log("✉️ Confirmation sent to professor:", gradeData.professor);
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
    this.observers.forEach((observer) => observer.update(gradeData));
  }
}

// Initialize Observer Pattern
const gradeSubject = new GradeSubject();
gradeSubject.attach(new GradeObserver());

// Global variables for faculty data
let facultyId = null;
let facultyCourses = [];
let currentRosterData = {};

// Mock Data (keeping for grade submission demo)
const gradeMockData = {
  CS101: {
    name: "Introduction to Computer Science",
    schedule: "MWF 9:00-10:00 AM | Tech Building 101",
    enrollment: "25/30 students",
    students: [
      {
        id: "ST2024001",
        name: "Alex Thompson",
        email: "alex.thompson@university.edu",
        phone: "(555) 123-4567",
        grade: "",
      },
      {
        id: "ST2024002",
        name: "Sarah Wilson",
        email: "sarah.wilson@university.edu",
        phone: "(555) 234-5678",
        grade: "",
      },
      {
        id: "ST2024003",
        name: "Mike Chen",
        email: "mike.chen@university.edu",
        phone: "(555) 345-6789",
        grade: "",
      },
    ],
  },
  CS201: {
    name: "Advanced Programming",
    schedule: "TTh 2:00-3:30 PM | CS Building 205",
    enrollment: "18/25 students",
    students: [
      {
        id: "ST2024004",
        name: "Emily Davis",
        email: "emily.davis@university.edu",
        phone: "(555) 456-7890",
        grade: "",
      },
      {
        id: "ST2024005",
        name: "David Brown",
        email: "david.brown@university.edu",
        phone: "(555) 567-8901",
        grade: "",
      },
    ],
  },
};

// Grade submission state management
let currentGradeData = {};
let pendingGrades = new Map(); // Store pending grades before submission
let gradeSubmissionStatus = new Map(); // Track submission status per enrollment

async function fetchGradeData(courseId) {
  try {
    const response = await fetch(`/api/grades/${facultyId}/${courseId}`);
    const data = await response.json();

    if (data.status === "Success") {
      return data;
    } else {
      throw new Error(data.message);
    }
  } catch (error) {
    console.error("Error fetching grade data:", error);
    return { status: "Error", message: error.message };
  }
}

async function submitBatchGrades(courseId, gradeSubmissions) {
  try {
    const response = await fetch("/api/grades/submit", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        faculty_id: facultyId,
        course_id: courseId,
        grade_submissions: gradeSubmissions,
      }),
    });

    const data = await response.json();
    return data;
  } catch (error) {
    console.error("Error submitting grades:", error);
    return { status: "Error", message: error.message };
  }
}

async function updateSingleGrade(enrollmentId, newGrade) {
  try {
    const response = await fetch(`/api/grades/update/${enrollmentId}`, {
      method: "PUT",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        faculty_id: facultyId,
        grade: newGrade,
      }),
    });

    const data = await response.json();
    return data;
  } catch (error) {
    console.error("Error updating grade:", error);
    return { status: "Error", message: error.message };
  }
}

async function finalizeAllGrades(courseId) {
  try {
    const response = await fetch(`/api/grades/finalize/${courseId}`, {
      method: "PUT",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        faculty_id: facultyId,
      }),
    });

    const data = await response.json();
    return data;
  } catch (error) {
    console.error("Error finalizing grades:", error);
    return { status: "Error", message: error.message };
  }
}

async function validateGradeFormat(grade) {
  try {
    const response = await fetch("/api/grades/validate", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ grade: grade }),
    });

    const data = await response.json();
    return data;
  } catch (error) {
    console.error("Error validating grade:", error);
    return { status: "Error", message: error.message };
  }
}
async function fetchFacultyCourses() {
  try {
    // Get faculty ID from session - this should be set based on logged in user
    facultyId = getCurrentFacultyId();
    console.log("Fetching courses for faculty ID:", facultyId);

    const response = await fetch(`/api/roster/${facultyId}/courses`);
    console.log("API Response status:", response.status);

    const data = await response.json();
    console.log("API Response data:", data);

    if (data.status === "Success") {
      facultyCourses = data.courses;
      console.log("Faculty courses loaded:", facultyCourses);
      populateCourseSelectors();
    } else {
      console.error("Error fetching courses:", data.message);
      // Handle case where API returns error
      facultyCourses = [];
      populateCourseSelectors(); // This will show "No courses" message
      alert("Error loading your courses: " + (data.message || "Unknown error"));
    }
  } catch (error) {
    console.error("Error fetching faculty courses:", error);
    // Handle network or other errors
    facultyCourses = [];
    populateCourseSelectors(); // This will show "No courses" message
    alert(
      "Error loading your courses. Please check your connection and try again."
    );
  }
}

function populateCourseSelectors() {
  const rosterSelect = document.getElementById("roster-course-select");
  const gradeSelect = document.getElementById("grade-course-select");
  const requestSelect = document.getElementById("request-course-select");

  // Clear existing options
  rosterSelect.innerHTML = '<option value="">-- Choose Course --</option>';
  gradeSelect.innerHTML = '<option value="">-- Choose Course --</option>';
  requestSelect.innerHTML = '<option value="">-- Select Course --</option>';

  // Check if facultyCourses is properly formatted
  if (!facultyCourses || !Array.isArray(facultyCourses)) {
    console.error("Faculty courses not properly loaded:", facultyCourses);
    // Add message to dropdowns indicating no courses
    rosterSelect.innerHTML +=
      '<option value="" disabled>No courses assigned</option>';
    gradeSelect.innerHTML +=
      '<option value="" disabled>No courses assigned</option>';
    requestSelect.innerHTML +=
      '<option value="" disabled>No courses assigned</option>';
    return;
  }

  if (facultyCourses.length === 0) {
    console.log("No courses found for this faculty member");
    // Add message to dropdowns indicating no courses
    rosterSelect.innerHTML +=
      '<option value="" disabled>No courses assigned</option>';
    gradeSelect.innerHTML +=
      '<option value="" disabled>No courses assigned</option>';
    requestSelect.innerHTML +=
      '<option value="" disabled>No courses assigned</option>';
    // Still call populateCourseCards to show the "no courses" message
    populateCourseCards();
    return;
  }

  facultyCourses.forEach((course) => {
    // Handle data format from roster API
    let courseId, courseName, courseDescription;

    if (typeof course === "object" && course.course_id) {
      // Object format from roster API
      courseId = course.course_id;
      courseName = course.course_name;
      courseDescription = course.description;
    } else if (Array.isArray(course)) {
      // Array format fallback
      courseId = course[0];
      courseName = course[1];
      courseDescription = course[2];
    }

    if (courseId && courseName) {
      // Create option for roster dropdown
      const option1 = document.createElement("option");
      option1.value = courseId;
      option1.textContent = courseName;
      rosterSelect.appendChild(option1);

      // Create option for grade dropdown
      const option2 = document.createElement("option");
      option2.value = courseId;
      option2.textContent = courseName;
      gradeSelect.appendChild(option2);

      // Create option for request dropdown
      const option3 = document.createElement("option");
      option3.value = courseId;
      option3.textContent = courseDescription
        ? `${courseName} - ${courseDescription.substring(0, 50)}...`
        : courseName;
      requestSelect.appendChild(option3);
    }
  });

  // Also populate the course cards in "My Courses" tab
  populateCourseCards();

  console.log(
    `Populated course dropdowns with ${facultyCourses.length} courses`
  );
}

function populateCourseCards() {
  const courseListContainer = document.getElementById("course-list-container");

  if (!courseListContainer) {
    console.error("Course list container not found");
    return;
  }

  // Clear existing content
  courseListContainer.innerHTML = "";

  if (!facultyCourses || facultyCourses.length === 0) {
    courseListContainer.innerHTML =
      '<div class="no-courses-message">No courses assigned to you this semester.</div>';
    return;
  }

  facultyCourses.forEach((course) => {
    // Handle data format from roster API
    let courseId, courseName, courseDescription, capacity, enrolledCount;

    if (typeof course === "object" && course.course_id) {
      // Object format from roster API
      courseId = course.course_id;
      courseName = course.course_name;
      courseDescription = course.description;
      capacity = course.capacity;
      enrolledCount = course.enrolled_count || 0;
    } else if (Array.isArray(course)) {
      // Array format fallback
      courseId = course[0];
      courseName = course[1];
      courseDescription = course[2];
      capacity = course[3] || 30;
      enrolledCount = course[5] || 0; // Skip available_seats (index 4)
    }

    if (courseId && courseName) {
      const courseCard = document.createElement("div");
      courseCard.className = "course-card";

      courseCard.innerHTML = `
        <h4>${courseName}</h4>
        <p class="course-description">${
          courseDescription || "No description available"
        }</p>
        <p class="enrollment">Enrollment: ${enrolledCount}/${capacity} students</p>
        <div class="course-actions">
          <button class="action-btn" onclick="updateCourseInfo('${courseId}')">
            Update Course Info
          </button>
          <button class="action-btn" onclick="requestChanges('${courseId}')">
            Request Changes
          </button>
        </div>
      `;

      courseListContainer.appendChild(courseCard);
    }
  });
}

async function fetchClassRoster(courseId) {
  try {
    const response = await fetch(`/api/roster/${facultyId}/${courseId}`);
    const data = await response.json();

    if (data.status === "Success") {
      return data;
    } else {
      throw new Error(data.message);
    }
  } catch (error) {
    console.error("Error fetching class roster:", error);
    return { status: "Error", message: error.message };
  }
}

// Tab navigation
function openTab(tabId, eventObj = null) {
  document.querySelectorAll(".tab-pane").forEach((pane) => {
    pane.classList.remove("active");
  });
  document.getElementById(tabId).classList.add("active");

  document.querySelectorAll(".tab-button").forEach((button) => {
    button.classList.remove("active");
  });

  // Handle cases where there's an event (when user clicks tab)
  if (eventObj && eventObj.currentTarget) {
    eventObj.currentTarget.classList.add("active");
  } else {
    // Find and activate the button for this tab (during initialization or programmatic calls)
    const targetButton = document.querySelector(
      `[onclick*="openTab('${tabId}')"]`
    );
    if (targetButton) {
      targetButton.classList.add("active");
    }
  }

  // Load data when switching to specific tabs
  if (tabId === "class-rosters") {
    loadRoster();
  } else if (tabId === "grade-submission") {
    // Reset grade sheet when switching to this tab
    document.getElementById("grade-course-select").value = "";
    document.getElementById("grade-table-body").innerHTML = "";
    document.querySelector(".submit-btn").disabled = true;
  } else if (tabId === "my-courses") {
    // Refresh course cards when switching to this tab
    if (facultyCourses && facultyCourses.length > 0) {
      populateCourseCards();
    }
  }
}

// Class Rosters Functions (First Tab)
async function loadRoster() {
  const courseSelect = document.getElementById("roster-course-select");
  const courseId = courseSelect.value;
  const tbody = document.getElementById("roster-table-body");

  tbody.innerHTML = "";

  if (!courseId) {
    return;
  }

  try {
    // Show loading state
    tbody.innerHTML =
      '<tr><td colspan="5" style="text-align: center; padding: 20px;">Loading roster...</td></tr>';

    const data = await fetchClassRoster(courseId);
    tbody.innerHTML = "";

    if (data.status === "Success") {
      currentRosterData = data;

      // Add course header
      const headerRow = document.createElement("tr");
      headerRow.innerHTML = `
                <td colspan="5" style="background: #f0f8ff; font-weight: bold; text-align: center; padding: 15px;">
                    ${data.course} - Instructor: ${data.instructor}
                    <br>
                    <small>Total Students: ${
                      data.students ? data.students.length : 0
                    }</small>
                    ${
                      data.students && data.students.length > 0
                        ? `
                        <button onclick="exportRoster()" style="margin-left: 20px; padding: 5px 10px; background: #007bff; color: white; border: none; border-radius: 4px; cursor: pointer;">
                            Export CSV
                        </button>
                    `
                        : ""
                    }
                </td>
            `;
      tbody.appendChild(headerRow);

      if (data.students && data.students.length > 0) {
        // Add student rows
        data.students.forEach((student) => {
          const row = document.createElement("tr");
          row.innerHTML = `
                        <td><strong>${student.id}</strong></td>
                        <td>${student.name}</td>
                        <td>${student.email}</td>
                        <td>${student.phone}</td>
                        <td>
                            <span class="status-badge status-${student.enrollment_status.toLowerCase()}">
                                ${student.enrollment_status}
                            </span>
                        </td>
                    `;
          tbody.appendChild(row);
        });
      } else {
        const noDataRow = document.createElement("tr");
        noDataRow.innerHTML = `
                    <td colspan="5" style="text-align: center; padding: 20px; font-style: italic; color: #666;">
                        No students enrolled yet
                    </td>
                `;
        tbody.appendChild(noDataRow);
      }
    } else {
      const errorRow = document.createElement("tr");
      errorRow.innerHTML = `
                <td colspan="5" style="text-align: center; padding: 20px; color: #dc3545;">
                    Error: ${data.message}
                </td>
            `;
      tbody.appendChild(errorRow);
    }
  } catch (error) {
    tbody.innerHTML = `
            <tr>
                <td colspan="5" style="text-align: center; padding: 20px; color: #dc3545;">
                    Error loading roster: ${error.message}
                </td>
            </tr>
        `;
  }
}

async function exportRoster() {
  if (!currentRosterData || !currentRosterData.students) {
    alert("No roster data to export");
    return;
  }

  const courseSelect = document.getElementById("roster-course-select");
  const courseId = courseSelect.value;

  try {
    const response = await fetch(`/api/roster/${facultyId}/${courseId}/export`);

    if (response.ok) {
      const blob = await response.blob();
      const url = window.URL.createObjectURL(blob);
      const a = document.createElement("a");
      a.style.display = "none";
      a.href = url;
      a.download = `${currentRosterData.course.replace(
        /\s+/g,
        "_"
      )}_roster.csv`;
      document.body.appendChild(a);
      a.click();
      window.URL.revokeObjectURL(url);
      document.body.removeChild(a);
    } else {
      const error = await response.json();
      alert(`Export failed: ${error.message}`);
    }
  } catch (error) {
    alert(`Export failed: ${error.message}`);
  }
}

// Grade Submission Functions (Second Tab)
async function loadGradeSheet() {
  const courseSelect = document.getElementById("grade-course-select");
  const courseId = courseSelect.value;
  const tbody = document.getElementById("grade-table-body");
  const submitBtn = document.querySelector(".submit-btn");

  tbody.innerHTML = "";
  submitBtn.disabled = true;

  if (!courseId) {
    return;
  }

  try {
    // Show loading state
    tbody.innerHTML =
      '<tr><td colspan="5" style="text-align: center; padding: 20px;">Loading grade sheet...</td></tr>';

    const data = await fetchGradeData(courseId);

    if (data.status === "Success") {
      currentGradeData = data;
      displayGradeSheet(data);
      submitBtn.disabled = false;
    } else {
      tbody.innerHTML = `
        <tr>
          <td colspan="5" style="text-align: center; padding: 20px; color: #dc3545;">
            Error: ${data.message}
          </td>
        </tr>
      `;
    }
  } catch (error) {
    tbody.innerHTML = `
      <tr>
        <td colspan="5" style="text-align: center; padding: 20px; color: #dc3545;">
          Error loading grade sheet: ${error.message}
        </td>
      </tr>
    `;
  }
}

function displayGradeSheet(data) {
  const tbody = document.getElementById("grade-table-body");
  const courseInfo = data.course_info;
  const students = data.students || [];

  // Clear existing content
  tbody.innerHTML = "";

  // Add course header
  const headerRow = document.createElement("tr");
  headerRow.innerHTML = `
    <td colspan="5" style="background: #fffacd; font-weight: bold; text-align: center; padding: 15px;">
      ${courseInfo.course_name} - Grade Submission
      <br>
      <small>Instructor: ${courseInfo.instructor} | Total Students: ${students.length}</small>
    </td>
  `;
  tbody.appendChild(headerRow);

  if (students.length === 0) {
    const noStudentsRow = document.createElement("tr");
    noStudentsRow.innerHTML = `
      <td colspan="5" style="text-align: center; padding: 20px; font-style: italic; color: #666;">
        No students enrolled in this course
      </td>
    `;
    tbody.appendChild(noStudentsRow);
    return;
  }

  // Add student rows with grade input
  students.forEach((student) => {
    const row = document.createElement("tr");
    const enrollmentId = student[0];
    const studentId = student[1];
    const firstName = student[2];
    const lastName = student[3];
    const email = student[4];
    const markStatus = student[5];
    const currentGrade = student[6] || "";
    const lastUpdated = student[7];

    // Check if grade is already submitted (locked)
    const isLocked = markStatus === "Submitted";
    const isPending = markStatus === "Pending";

    row.innerHTML = `
      <td><strong>${studentId}</strong></td>
      <td>${firstName} ${lastName}<br><small style="color: #666;">${email}</small></td>
      <td>
        <div style="display: flex; flex-direction: column; gap: 5px;">
          <select 
            onchange="updateStudentGrade(${enrollmentId}, this.value)" 
            style="padding: 8px; border-radius: 4px; border: 1px solid #ccc; width: 100%;"
            ${isLocked ? "disabled" : ""}
            data-enrollment-id="${enrollmentId}">
            <option value="">Select Grade</option>
            <option value="A" ${
              currentGrade === "A" ? "selected" : ""
            }>A</option>
            <option value="B" ${
              currentGrade === "B" ? "selected" : ""
            }>B</option>
            <option value="C" ${
              currentGrade === "C" ? "selected" : ""
            }>C</option>
            <option value="D" ${
              currentGrade === "D" ? "selected" : ""
            }>D</option>
            <option value="F" ${
              currentGrade === "F" ? "selected" : ""
            }>F</option>
            ${
              currentGrade && !["A", "B", "C", "D", "F"].includes(currentGrade)
                ? `<option value="${currentGrade}" selected>${currentGrade}</option>`
                : ""
            }
          </select>
          <input 
            type="number" 
            min="0" 
            max="100" 
            step="0.01"
            placeholder="Or enter 0-100"
            onchange="updateStudentGrade(${enrollmentId}, this.value)"
            style="padding: 6px; border-radius: 4px; border: 1px solid #ccc; width: 100%; font-size: 12px;"
            ${isLocked ? "disabled" : ""}
            data-enrollment-id="${enrollmentId}"
            value="${
              !["A", "B", "C", "D", "F"].includes(currentGrade)
                ? currentGrade
                : ""
            }">
        </div>
      </td>
      <td>
        <span class="status-badge ${getStatusClass(markStatus)}">
          ${markStatus}
        </span>
        ${
          isPending || currentGrade
            ? `<br><small style="color: #666;">Grade: ${currentGrade}</small>`
            : ""
        }
      </td>
      <td>
        <div class="grade-actions" style="display: flex; flex-direction: column; gap: 5px;">
          ${
            !isLocked && currentGrade
              ? `
            <button onclick="saveSingleGrade(${enrollmentId})" 
              style="background: #28a745; color: white; border: none; padding: 4px 8px; border-radius: 4px; cursor: pointer; font-size: 12px;">
              Save as Pending
            </button>
          `
              : ""
          }
          <div class="validation-message" id="validation-${enrollmentId}" style="font-size: 11px; color: #dc3545;"></div>
        </div>
      </td>
    `;
    tbody.appendChild(row);

    // Store current grade in pending grades map
    if (currentGrade) {
      pendingGrades.set(enrollmentId, currentGrade);
    }
  });

  // Add summary and action row
  const summaryRow = document.createElement("tr");
  const pendingCount = students.filter((s) => s[5] === "Pending").length;
  const submittedCount = students.filter((s) => s[5] === "Submitted").length;
  const ungradedCount = students.filter((s) => s[5] === "In Progress").length;

  summaryRow.innerHTML = `
    <td colspan="5" style="background: #f8f9fa; padding: 15px; text-align: center;">
      <div style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 10px;">
        <div>
          <strong>Summary:</strong> 
          ${submittedCount} Submitted | 
          ${pendingCount} Pending | 
          ${ungradedCount} Ungraded
        </div>
        <div style="display: flex; gap: 10px; flex-wrap: wrap;">
          <button onclick="saveAllPendingGrades()" 
            style="background: #ffc107; color: #000; border: none; padding: 8px 16px; border-radius: 4px; cursor: pointer;">
            Save All as Pending
          </button>
          <button onclick="submitAllFinalGrades()" 
            style="background: #dc3545; color: white; border: none; padding: 8px 16px; border-radius: 4px; cursor: pointer;">
            Submit Final Grades
          </button>
        </div>
      </div>
    </td>
  `;
  tbody.appendChild(summaryRow);
}

function getStatusClass(markStatus) {
  switch (markStatus) {
    case "Pending":
      return "status-pending";
    case "Submitted":
      return "status-submitted";
    case "In Progress":
      return "status-in-progress";
    default:
      return "status-in-progress";
  }
}

async function updateStudentGrade(enrollmentId, grade) {
  // Store the grade in pending grades
  pendingGrades.set(enrollmentId, grade);

  // Clear any previous validation messages
  const validationDiv = document.getElementById(`validation-${enrollmentId}`);
  if (validationDiv) {
    validationDiv.textContent = "";
  }

  // Validate grade format
  if (grade && grade.trim() !== "") {
    const validation = await validateGradeFormat(grade);
    if (!validation.valid) {
      if (validationDiv) {
        validationDiv.textContent = validation.message;
      }
    } else if (validationDiv) {
      validationDiv.innerHTML = '<span style="color: #28a745;">✓ Valid</span>';
    }
  }

  // Update the corresponding input field if it wasn't the source
  const selectElement = document.querySelector(
    `select[data-enrollment-id="${enrollmentId}"]`
  );
  const inputElement = document.querySelector(
    `input[data-enrollment-id="${enrollmentId}"]`
  );

  if (selectElement && ["A", "B", "C", "D", "F"].includes(grade)) {
    selectElement.value = grade;
    if (inputElement) inputElement.value = "";
  } else if (inputElement && !["A", "B", "C", "D", "F"].includes(grade)) {
    if (selectElement) selectElement.value = "";
    inputElement.value = grade;
  }
}

async function saveSingleGrade(enrollmentId) {
  const grade = pendingGrades.get(enrollmentId);
  if (!grade) {
    alert("No grade to save");
    return;
  }

  try {
    const result = await updateSingleGrade(enrollmentId, grade);
    if (result.status === "Success") {
      // Reload the grade sheet to reflect changes
      loadGradeSheet();
      showNotification("Grade saved as pending successfully!", "success");
    } else {
      alert(`Error saving grade: ${result.message}`);
    }
  } catch (error) {
    alert(`Error saving grade: ${error.message}`);
  }
}

async function saveAllPendingGrades() {
  const courseSelect = document.getElementById("grade-course-select");
  const courseId = courseSelect.value;

  if (!courseId) {
    alert("Please select a course first");
    return;
  }

  // Prepare grade submissions from pending grades
  const gradeSubmissions = Array.from(pendingGrades.entries()).map(
    ([enrollmentId, grade]) => ({
      enrollment_id: parseInt(enrollmentId),
      grade: grade,
    })
  );

  if (gradeSubmissions.length === 0) {
    alert("No grades to save");
    return;
  }

  try {
    const result = await submitBatchGrades(courseId, gradeSubmissions);

    if (result.status === "Completed" || result.status === "Success") {
      // Notify observers
      gradeSubject.notifyAll({
        course: currentGradeData.course_info.course_name,
        action: "BATCH_SAVE_PENDING",
        successful: result.successful,
        failed: result.failed,
        timestamp: new Date().toISOString(),
        professor: currentGradeData.course_info.instructor,
      });

      // Reload the grade sheet
      loadGradeSheet();

      const message = `Batch save completed!\nSuccessful: ${result.successful}\nFailed: ${result.failed}`;
      showNotification(message, result.failed > 0 ? "warning" : "success");

      // Show detailed results if there were failures
      if (result.failed > 0) {
        const failedResults = result.results.filter(
          (r) => r.status === "Error"
        );
        console.log("Failed submissions:", failedResults);
      }
    } else {
      alert(`Error saving grades: ${result.message}`);
    }
  } catch (error) {
    alert(`Error saving grades: ${error.message}`);
  }
}

async function submitAllFinalGrades() {
  const courseSelect = document.getElementById("grade-course-select");
  const courseId = courseSelect.value;

  if (!courseId) {
    alert("Please select a course first");
    return;
  }

  // Confirm action
  const confirmed = confirm(
    "⚠️ FINAL SUBMISSION WARNING ⚠️\n\n" +
      "This will finalize ALL pending grades for this course.\n" +
      "Once submitted, grades cannot be modified.\n\n" +
      "Are you sure you want to proceed?"
  );

  if (!confirmed) return;

  try {
    const result = await finalizeAllGrades(courseId);

    if (result.status === "Success") {
      // Notify observers
      gradeSubject.notifyAll({
        course: currentGradeData.course_info.course_name,
        action: "FINALIZE_GRADES",
        finalized_count: result.finalized_count,
        timestamp: new Date().toISOString(),
        professor: currentGradeData.course_info.instructor,
      });

      // Reload the grade sheet
      loadGradeSheet();

      showNotification(
        `✅ Final submission completed!\n${result.finalized_count} grade(s) have been finalized and locked.`,
        "success"
      );
    } else {
      alert(`Error finalizing grades: ${result.message}`);
    }
  } catch (error) {
    alert(`Error finalizing grades: ${error.message}`);
  }
}

function showNotification(message, type = "info") {
  // Create notification element
  const notification = document.createElement("div");
  notification.style.cssText = `
    position: fixed;
    top: 20px;
    right: 20px;
    padding: 15px 20px;
    border-radius: 8px;
    color: white;
    font-weight: bold;
    z-index: 9999;
    max-width: 400px;
    box-shadow: 0 4px 12px rgba(0,0,0,0.3);
    animation: slideIn 0.3s ease;
  `;

  // Set background color based on type
  switch (type) {
    case "success":
      notification.style.backgroundColor = "#28a745";
      break;
    case "warning":
      notification.style.backgroundColor = "#ffc107";
      notification.style.color = "#000";
      break;
    case "error":
      notification.style.backgroundColor = "#dc3545";
      break;
    default:
      notification.style.backgroundColor = "#17a2b8";
  }

  notification.innerHTML = `
    <div style="display: flex; justify-content: space-between; align-items: flex-start;">
      <div style="flex: 1; white-space: pre-line;">${message}</div>
      <button onclick="this.parentElement.parentElement.remove()" 
        style="background: none; border: none; color: inherit; font-size: 18px; cursor: pointer; margin-left: 10px;">×</button>
    </div>
  `;

  // Add CSS animation
  const style = document.createElement("style");
  style.textContent = `
    @keyframes slideIn {
      from { transform: translateX(100%); opacity: 0; }
      to { transform: translateX(0); opacity: 1; }
    }
  `;
  document.head.appendChild(style);

  document.body.appendChild(notification);

  // Auto-remove after 5 seconds
  setTimeout(() => {
    if (notification.parentElement) {
      notification.remove();
    }
  }, 5000);
}

function showGradeSubmissionOptions() {
  const courseSelect = document.getElementById("grade-course-select");
  const courseId = courseSelect.value;

  if (!courseId) {
    alert("Please select a course first");
    return;
  }

  // Show modal with submission options
  const modal = createGradeSubmissionModal();
  document.body.appendChild(modal);
}

function createGradeSubmissionModal() {
  const modal = document.createElement("div");
  modal.style.cssText = `
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background: rgba(0,0,0,0.5);
    display: flex;
    justify-content: center;
    align-items: center;
    z-index: 10000;
  `;

  const content = document.createElement("div");
  content.style.cssText = `
    background: white;
    padding: 30px;
    border-radius: 12px;
    max-width: 500px;
    width: 90%;
    box-shadow: 0 8px 24px rgba(0,0,0,0.3);
  `;

  content.innerHTML = `
    <h3 style="margin-bottom: 20px; color: #0d2d66;">Grade Submission Options</h3>
    <p style="margin-bottom: 20px; color: #666;">Choose how you want to submit grades:</p>
    
    <div style="display: flex; flex-direction: column; gap: 15px;">
      <button onclick="saveAllPendingGrades(); closeModal(this)" 
        style="padding: 15px; border: 2px solid #ffc107; background: #ffc107; color: #000; border-radius: 8px; cursor: pointer; font-weight: bold;">
        💾 Save as Pending (Draft)
        <div style="font-size: 12px; font-weight: normal; margin-top: 5px;">
          Save grades but keep them editable. You can make changes later.
        </div>
      </button>
      
      <button onclick="submitAllFinalGrades(); closeModal(this)" 
        style="padding: 15px; border: 2px solid #dc3545; background: #dc3545; color: white; border-radius: 8px; cursor: pointer; font-weight: bold;">
        🔒 Submit Final Grades (Lock)
        <div style="font-size: 12px; font-weight: normal; margin-top: 5px;">
          Finalize all pending grades. Cannot be changed after submission.
        </div>
      </button>
      
      <button onclick="closeModal(this)" 
        style="padding: 10px; border: 1px solid #ccc; background: #f8f9fa; color: #666; border-radius: 8px; cursor: pointer;">
        Cancel
      </button>
    </div>
  `;

  modal.appendChild(content);

  // Close modal when clicking outside
  modal.addEventListener("click", (e) => {
    if (e.target === modal) {
      document.body.removeChild(modal);
    }
  });

  return modal;
}

function closeModal(button) {
  const modal = button.closest('div[style*="position: fixed"]');
  if (modal && modal.parentElement) {
    modal.parentElement.removeChild(modal);
  }
}
function updateCourseInfo(courseCode) {
  alert(
    `Update course information for ${courseCode}\n\nThis would open a course editing form.`
  );
}

function requestChanges(courseCode) {
  // Switch to course requests tab
  openTab("course-requests");

  // Pre-select the course if possible
  const courseSelect = document.getElementById("request-course-select");
  for (let option of courseSelect.options) {
    if (option.text.includes(courseCode)) {
      option.selected = true;
      break;
    }
  }
}

// Course Request Management Functions

function updateRequestForm() {
  const requestType = document.getElementById("request-type-select").value;
  const detailsContainer = document.getElementById("request-details-container");

  // Clear existing content
  detailsContainer.innerHTML = "";

  if (requestType === "UpdateDescription") {
    detailsContainer.innerHTML = `
      <textarea id="request-details" name="details" rows="4" 
                placeholder="Enter the new course description..." required></textarea>
    `;
  } else if (requestType === "ChangeCapacity") {
    detailsContainer.innerHTML = `
      <input type="number" id="request-details" name="details" 
             placeholder="Enter new capacity (e.g., 35)" min="1" max="200" required>
    `;
  } else if (requestType === "AddPrerequisite") {
    // Load available courses for prerequisite
    loadPrerequisiteOptions();
  } else {
    detailsContainer.innerHTML = `
      <textarea id="request-details" name="details" rows="4" 
                placeholder="Enter request details..." required></textarea>
    `;
  }
}

async function loadPrerequisiteOptions() {
  try {
    const response = await fetch("/api/courses/prerequisite-options");
    const result = await response.json();

    if (result.status === "Success") {
      const detailsContainer = document.getElementById(
        "request-details-container"
      );
      detailsContainer.innerHTML = `
        <select id="request-details" name="details" required>
          <option value="">-- Select Prerequisite Course --</option>
          ${result.courses
            .map(
              (course) => `<option value="${course[0]}">${course[1]}</option>`
            )
            .join("")}
        </select>
      `;
    }
  } catch (error) {
    console.error("Error loading prerequisite options:", error);
  }
}

async function submitCourseRequest(event) {
  event.preventDefault();

  const courseId = document.getElementById("request-course-select").value;
  const requestType = document.getElementById("request-type-select").value;
  const details = document.getElementById("request-details").value;

  if (!courseId || !requestType || !details) {
    alert("Please fill in all fields");
    return;
  }

  try {
    const response = await fetch("/api/course-requests", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        faculty_id: facultyId,
        course_id: courseId,
        requestType: requestType,
        details: details,
      }),
    });

    const result = await response.json();

    if (result.status === "Success") {
      alert("Request submitted successfully!");
      document.getElementById("course-request-form").reset();
      loadRequestHistory(); // Refresh the request history
    } else {
      alert("Error submitting request: " + result.message);
    }
  } catch (error) {
    console.error("Error submitting request:", error);
    alert("Error submitting request. Please try again.");
  }
}

async function loadRequestHistory() {
  try {
    if (!facultyId) return;

    const response = await fetch(`/api/course-requests/faculty/${facultyId}`);
    const result = await response.json();

    if (result.status === "Success") {
      const tbody = document.getElementById("request-history-body");
      tbody.innerHTML = "";

      result.requests.forEach((request) => {
        const row = document.createElement("tr");
        const statusClass =
          request[5] === "Pending"
            ? "status-pending"
            : request[5] === "Approved"
            ? "status-approved"
            : "status-rejected";

        row.innerHTML = `
          <td>${request[0]}</td>
          <td>${request[7]}</td>
          <td>${request[2]}</td>
          <td title="${request[3]}">${
          request[3].length > 50
            ? request[3].substring(0, 50) + "..."
            : request[3]
        }</td>
          <td>${new Date(request[4]).toLocaleDateString()}</td>
          <td><span class="status-badge ${statusClass}">${
          request[5]
        }</span></td>
          <td>${
            request[6] ? new Date(request[6]).toLocaleDateString() : "-"
          }</td>
          <td>${
            request[8] && request[9] ? `${request[8]} ${request[9]}` : "-"
          }</td>
        `;
        tbody.appendChild(row);
      });
    }
  } catch (error) {
    console.error("Error loading request history:", error);
  }
}

function getCurrentFacultyId() {
  // Get faculty ID from global variable set by the backend
  if (window.FACULTY_ID) {
    return window.FACULTY_ID;
  }

  // Fallback to default value for demo purposes
  console.warn("Faculty ID not found in session, using default value");
  return 1; // Default faculty ID for demo
}

// Initialize page
document.addEventListener("DOMContentLoaded", async function () {
  // Set first tab as active
  openTab("class-rosters");

  // Get faculty ID from session or user context
  facultyId = getCurrentFacultyId();
  console.log("Faculty ID:", facultyId);

  // Fetch faculty courses and populate all dropdowns
  await fetchFacultyCourses();

  // Load request history
  await loadRequestHistory();

  // Set up form submission handler
  document
    .getElementById("course-request-form")
    .addEventListener("submit", submitCourseRequest);

  console.log(
    "Faculty dashboard initialized with Observer pattern and real API integration"
  );
});
