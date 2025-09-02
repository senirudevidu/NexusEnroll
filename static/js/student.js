function showTab(tabId) {
  document
    .querySelectorAll(".tab-content")
    .forEach((sec) => sec.classList.remove("active"));
  document.getElementById(tabId).classList.add("active");

  document
    .querySelectorAll(".tabs button")
    .forEach((btn) => btn.classList.remove("active"));
  event.target.classList.add("active");

  // Load appropriate content when tabs are shown
  if (tabId === "catalog") {
    loadAllCourses();
  } else if (tabId === "enrollment") {
    // Trigger enrollment manager refresh if it exists
    if (window.enrollmentManager) {
      window.enrollmentManager.loadStudentEnrollments();
      window.enrollmentManager.loadAvailableCourses();
    }
  }
}

// Course catalog functionality
let allCourses = [];
let filteredCourses = [];

// Load departments when page loads
document.addEventListener("DOMContentLoaded", function () {
  loadDepartments();
  loadAllCourses();
});

async function loadDepartments() {
  try {
    const response = await fetch("/api/departments");
    const departments = await response.json();

    const departmentFilter = document.getElementById("departmentFilter");
    const useCaseDepartment = document.getElementById("useCaseDepartment");

    // Clear existing options except the first one
    departmentFilter.innerHTML = '<option value="">All Departments</option>';
    useCaseDepartment.innerHTML = '<option value="">Select Department</option>';

    departments.forEach((dept) => {
      const option1 = new Option(dept[1], dept[1]); // dept[1] is department name
      const option2 = new Option(dept[1], dept[1]);
      departmentFilter.appendChild(option1);
      useCaseDepartment.appendChild(option2);
    });
  } catch (error) {
    console.error("Error loading departments:", error);
  }
}

async function loadAllCourses() {
  showLoading(true);
  try {
    const response = await fetch("/api/courses/search");
    const courses = await response.json();

    if (Array.isArray(courses)) {
      allCourses = courses;
      filteredCourses = [...courses];
      displayCourses(filteredCourses);
    } else {
      showError("Failed to load courses");
    }
  } catch (error) {
    console.error("Error loading courses:", error);
    showError("Failed to load courses");
  } finally {
    showLoading(false);
  }
}

async function searchCourses() {
  const keyword = document.getElementById("searchKeyword").value.trim();
  const instructor = document.getElementById("searchInstructor").value.trim();
  const department = document.getElementById("departmentFilter").value;
  const courseNumber = document.getElementById("courseNumber").value.trim();

  const params = new URLSearchParams();
  if (keyword) params.append("keyword", keyword);
  if (instructor) params.append("instructor_name", instructor);
  if (department) params.append("department", department);
  if (courseNumber) params.append("course_number", courseNumber);

  showLoading(true);
  try {
    const response = await fetch(`/api/courses/search?${params.toString()}`);
    const courses = await response.json();

    if (Array.isArray(courses)) {
      filteredCourses = courses;
      displayCourses(filteredCourses);
    } else {
      showError(courses.message || "Search failed");
    }
  } catch (error) {
    console.error("Error searching courses:", error);
    showError("Search failed");
  } finally {
    showLoading(false);
  }
}

async function searchByDepartmentAndInstructor() {
  const department = document.getElementById("useCaseDepartment").value;
  const instructor = document.getElementById("useCaseInstructor").value.trim();

  if (!department || !instructor) {
    alert("Please select a department and enter an instructor name");
    return;
  }

  const params = new URLSearchParams();
  params.append("department", department);
  params.append("instructor_name", instructor);

  showLoading(true);
  try {
    const response = await fetch(
      `/api/courses/department-instructor?${params.toString()}`
    );
    const courses = await response.json();

    if (Array.isArray(courses)) {
      filteredCourses = courses;
      displayCourses(filteredCourses);
    } else {
      showError(courses.message || "Search failed");
    }
  } catch (error) {
    console.error("Error searching courses:", error);
    showError("Search failed");
  } finally {
    showLoading(false);
  }
}

function clearFilters() {
  document.getElementById("searchKeyword").value = "";
  document.getElementById("searchInstructor").value = "";
  document.getElementById("departmentFilter").value = "";
  document.getElementById("courseNumber").value = "";
  document.getElementById("useCaseDepartment").value = "";
  document.getElementById("useCaseInstructor").value = "";

  filteredCourses = [...allCourses];
  displayCourses(filteredCourses);
}

function displayCourses(courses) {
  const courseList = document.getElementById("courseList");
  const noResults = document.getElementById("noResults");

  if (!courses || courses.length === 0) {
    courseList.innerHTML = "";
    noResults.style.display = "block";
    return;
  }

  noResults.style.display = "none";

  courseList.innerHTML = courses
    .map((course) => {
      const [
        courseId,
        courseName,
        description,
        capacity,
        availableSeats,
        credits,
        preReqYear,
        deptName,
        firstName,
        lastName,
        degreeName,
      ] = course;

      const instructorName = `${firstName} ${lastName}`;
      const availabilityClass = getAvailabilityClass(availableSeats, capacity);
      const enrollmentDisabled = availableSeats <= 0;

      return `
      <div class="detailed-course-card">
        <div class="course-header">
          <h4 class="course-title">${courseName}</h4>
          <span class="course-id">ID: ${courseId}</span>
        </div>
        
        <p class="course-description">${
          description || "No description available"
        }</p>
        
        <div class="course-details">
          <div class="detail-item">
            <span class="detail-label">Instructor:</span>
            <span class="instructor-info">${instructorName}</span>
          </div>
          
          <div class="detail-item">
            <span class="detail-label">Department:</span>
            <span>${deptName}</span>
          </div>
          
          <div class="detail-item">
            <span class="detail-label">Credits:</span>
            <span>${credits}</span>
          </div>
          
          <div class="detail-item">
            <span class="detail-label">Degree:</span>
            <span>${degreeName}</span>
          </div>
          
          <div class="detail-item">
            <span class="detail-label">Seats:</span>
            <span class="seats-info ${availabilityClass}">${availableSeats}/${capacity}</span>
          </div>
          
          ${
            preReqYear
              ? `
          <div class="detail-item">
            <span class="detail-label">Prerequisites:</span>
            <span>Year ${preReqYear} or higher</span>
          </div>
          `
              : ""
          }
        </div>
        
        <div class="course-actions">
          <button class="enroll-btn" ${enrollmentDisabled ? "disabled" : ""} 
                  onclick="enrollInCourse(${courseId}, '${courseName}')">
            ${enrollmentDisabled ? "Full" : "Enroll"}
          </button>
          <button class="view-details-btn" onclick="viewCourseDetails(${courseId})">
            View Details
          </button>
        </div>
      </div>
    `;
    })
    .join("");
}

function getAvailabilityClass(available, total) {
  const percentage = (available / total) * 100;
  if (available === 0) return "seats-full";
  if (percentage <= 20) return "seats-low";
  return "seats-available";
}

function sortCourses() {
  const sortBy = document.getElementById("sortBy").value;

  const sorted = [...filteredCourses].sort((a, b) => {
    switch (sortBy) {
      case "courseName":
        return a[1].localeCompare(b[1]); // course name
      case "department":
        return a[7].localeCompare(b[7]); // department name
      case "instructor":
        const instructorA = `${a[8]} ${a[9]}`;
        const instructorB = `${b[8]} ${b[9]}`;
        return instructorA.localeCompare(instructorB);
      case "availability":
        return b[4] - a[4]; // available seats (descending)
      default:
        return 0;
    }
  });

  filteredCourses = sorted;
  displayCourses(filteredCourses);
}

function showLoading(show) {
  document.getElementById("loadingSpinner").style.display = show
    ? "block"
    : "none";
}

function showError(message) {
  const noResults = document.getElementById("noResults");
  noResults.innerHTML = `<p>Error: ${message}</p>`;
  noResults.style.display = "block";
  document.getElementById("courseList").innerHTML = "";
}

function enrollInCourse(courseId, courseName) {
  // Use the new enrollment manager if available
  if (window.enrollmentManager) {
    window.enrollmentManager.validateAndEnroll(courseId, courseName);
  } else {
    // Fallback to simple confirmation
    if (confirm(`Are you sure you want to enroll in ${courseName}?`)) {
      alert(
        `Enrollment request submitted for ${courseName}. Please check the Enrollment Management tab for details.`
      );
    }
  }
}

function viewCourseDetails(courseId) {
  // This would show detailed course information
  alert(`Viewing details for course ID: ${courseId}`);
}

// Existing functions for other tabs
function enroll(courseCode, schedule, location) {
  const enrolled = document.getElementById("enrolled-list");
  const li = document.createElement("li");
  li.innerHTML = `${courseCode} - ${schedule} at ${location} <button class="drop-button" onclick="drop(this)">Drop</button>`;
  enrolled.appendChild(li);
}

function drop(button) {
  if (confirm("Are you sure you want to drop this course?")) {
    button.parentElement.remove();
  }
}
