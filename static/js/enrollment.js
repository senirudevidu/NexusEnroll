// Enrollment Management JavaScript
class EnrollmentManager {
  constructor() {
    this.currentStudentId = this.getCurrentStudentId();
    this.enrollmentData = [];
    this.availableCourses = [];
    this.init();
  }

  init() {
    this.loadStudentEnrollments();
    this.loadAvailableCourses();
    this.setupEventListeners();
  }

  getCurrentStudentId() {
    // In a real application, this would come from session/authentication
    // For demo purposes, we'll use a default student ID
    return sessionStorage.getItem("student_id") || 1;
  }

  setupEventListeners() {
    // Enrollment form submission
    const enrollForm = document.getElementById("enrollmentForm");
    if (enrollForm) {
      enrollForm.addEventListener("submit", (e) => {
        e.preventDefault();
        this.handleEnrollment();
      });
    }

    // Course search and filter
    const searchBtn = document.getElementById("searchAvailableCourses");
    if (searchBtn) {
      searchBtn.addEventListener("click", () => this.searchAvailableCourses());
    }

    // Refresh buttons
    const refreshEnrollmentsBtn = document.getElementById("refreshEnrollments");
    if (refreshEnrollmentsBtn) {
      refreshEnrollmentsBtn.addEventListener("click", () =>
        this.loadStudentEnrollments()
      );
    }
  }

  async loadStudentEnrollments() {
    try {
      this.showLoading("enrollmentsList");

      const response = await fetch(`/api/enrollments/${this.currentStudentId}`);
      const data = await response.json();

      if (data.status === "Success") {
        this.enrollmentData = data.data;
        this.displayEnrollments();
        this.updateEnrollmentSummary();
      } else {
        this.showError("enrollmentsList", data.message);
      }
    } catch (error) {
      console.error("Error loading enrollments:", error);
      this.showError("enrollmentsList", "Failed to load enrollments");
    }
  }

  async loadAvailableCourses() {
    try {
      this.showLoading("availableCoursesList");

      const response = await fetch(
        `/api/student/${this.currentStudentId}/available-courses`
      );
      const data = await response.json();

      if (data.status === "Success") {
        this.availableCourses = data.courses;
        this.displayAvailableCourses();
      } else {
        this.showError("availableCoursesList", data.message);
      }
    } catch (error) {
      console.error("Error loading available courses:", error);
      this.showError(
        "availableCoursesList",
        "Failed to load available courses"
      );
    }
  }

  displayEnrollments() {
    const container = document.getElementById("enrollmentsList");
    if (!container) return;

    if (this.enrollmentData.length === 0) {
      container.innerHTML = `
                <div class="no-enrollments">
                    <p>You are not currently enrolled in any courses.</p>
                    <button onclick="showTab('catalog')" class="enroll-now-btn">Browse Course Catalog</button>
                </div>
            `;
      return;
    }

    const enrollmentsHTML = this.enrollmentData
      .map((enrollment) => {
        // enrollment format: [enrollment_id, student_id, course_id, courseName, description, credits, capacity, availableSeats, instructor_name, deptName, markStatus, marks, lastUpdated, enrollmentStatus]
        const [
          enrollmentId,
          studentId,
          courseId,
          courseName,
          description,
          credits,
          capacity,
          availableSeats,
          instructorName,
          deptName,
          markStatus,
          marks,
          lastUpdated,
          enrollmentStatus,
        ] = enrollment;

        return `
                <div class="enrollment-card" data-enrollment-id="${enrollmentId}">
                    <div class="course-header">
                        <h4 class="course-title">${courseName}</h4>
                        <span class="course-credits">${credits} Credits</span>
                    </div>
                    
                    <div class="course-details">
                        <div class="course-info">
                            <p class="course-description">${
                              description || "No description available"
                            }</p>
                            <div class="course-meta">
                                <span class="instructor">
                                    <i class="fas fa-user"></i>
                                    Instructor: ${instructorName}
                                </span>
                                <span class="department">
                                    <i class="fas fa-building"></i>
                                    Department: ${deptName}
                                </span>
                                <span class="status">
                                    <i class="fas fa-info-circle"></i>
                                    Status: ${markStatus}
                                </span>
                                ${
                                  marks
                                    ? `<span class="marks"><i class="fas fa-star"></i>Grade: ${marks}</span>`
                                    : ""
                                }
                            </div>
                        </div>
                        
                        <div class="enrollment-actions">
                            <button class="drop-btn" onclick="enrollmentManager.confirmDropEnrollment(${enrollmentId}, '${courseName}')">
                                <i class="fas fa-times"></i>
                                Drop Course
                            </button>
                            <button class="details-btn" onclick="enrollmentManager.showCourseDetails(${courseId})">
                                <i class="fas fa-info"></i>
                                Details
                            </button>
                        </div>
                    </div>
                </div>
            `;
      })
      .join("");

    container.innerHTML = enrollmentsHTML;
  }

  displayAvailableCourses() {
    const container = document.getElementById("availableCoursesList");
    if (!container) return;

    if (this.availableCourses.length === 0) {
      container.innerHTML = `
                <div class="no-courses">
                    <p>No courses available for enrollment at this time.</p>
                </div>
            `;
      return;
    }

    const coursesHTML = this.availableCourses
      .map((course) => {
        const canEnrollClass = course.can_enroll
          ? "can-enroll"
          : "cannot-enroll";
        const enrollButtonDisabled = course.can_enroll ? "" : "disabled";
        const issues =
          course.issues.length > 0
            ? `<div class="enrollment-issues"><strong>Issues:</strong> ${course.issues.join(
                ", "
              )}</div>`
            : "";

        return `
                <div class="available-course-card ${canEnrollClass}" data-course-id="${
          course.course_id
        }">
                    <div class="course-header">
                        <h4 class="course-title">${course.courseName}</h4>
                        <div class="course-capacity">
                            <span class="available">${
                              course.availableSeats
                            }</span>/<span class="total">${
          course.capacity
        }</span> seats
                        </div>
                    </div>
                    
                    <div class="course-details">
                        <div class="course-meta">
                            <span class="instructor">
                                <i class="fas fa-user"></i>
                                ${course.instructor}
                            </span>
                            <span class="department">
                                <i class="fas fa-building"></i>
                                ${course.department}
                            </span>
                        </div>
                        
                        ${issues}
                        
                        <div class="course-actions">
                            <button class="enroll-btn" ${enrollButtonDisabled} 
                                    onclick="enrollmentManager.validateAndEnroll(${
                                      course.course_id
                                    }, '${course.courseName}')">
                                <i class="fas fa-plus"></i>
                                ${
                                  course.can_enroll ? "Enroll" : "Cannot Enroll"
                                }
                            </button>
                            <button class="validate-btn" onclick="enrollmentManager.validateEnrollment(${
                              course.course_id
                            }, '${course.courseName}')">
                                <i class="fas fa-check"></i>
                                Check Eligibility
                            </button>
                        </div>
                    </div>
                </div>
            `;
      })
      .join("");

    container.innerHTML = coursesHTML;
  }

  async validateAndEnroll(courseId, courseName) {
    if (!confirm(`Are you sure you want to enroll in ${courseName}?`)) {
      return;
    }

    try {
      this.showToast("Processing enrollment...", "info");

      const response = await fetch("/api/enroll", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          student_id: this.currentStudentId,
          course_id: courseId,
        }),
      });

      const data = await response.json();

      if (data.status === "Success") {
        this.showToast(`Successfully enrolled in ${courseName}!`, "success");
        // Refresh both lists
        this.loadStudentEnrollments();
        this.loadAvailableCourses();
      } else {
        this.showToast(`Enrollment failed: ${data.message}`, "error");
      }
    } catch (error) {
      console.error("Error enrolling:", error);
      this.showToast("Enrollment failed. Please try again.", "error");
    }
  }

  async validateEnrollment(courseId, courseName) {
    try {
      const response = await fetch("/api/enrollment/validate", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          student_id: this.currentStudentId,
          course_id: courseId,
        }),
      });

      const data = await response.json();

      let message = `Enrollment validation for ${courseName}:\n\n`;

      if (data.can_enroll) {
        message += "✅ You are eligible to enroll in this course!";
      } else {
        message += "❌ You cannot enroll in this course.\n\nIssues:\n";
        data.issues.forEach((issue) => {
          message += `• ${issue}\n`;
        });
      }

      alert(message);
    } catch (error) {
      console.error("Error validating enrollment:", error);
      this.showToast("Validation failed. Please try again.", "error");
    }
  }

  async confirmDropEnrollment(enrollmentId, courseName) {
    if (
      !confirm(
        `Are you sure you want to drop ${courseName}? This action cannot be undone.`
      )
    ) {
      return;
    }

    try {
      this.showToast("Processing drop request...", "info");

      const response = await fetch(`/api/drop/${enrollmentId}`, {
        method: "DELETE",
      });

      const data = await response.json();

      if (data.status === "Success") {
        this.showToast(`Successfully dropped ${courseName}`, "success");
        // Refresh both lists
        this.loadStudentEnrollments();
        this.loadAvailableCourses();
      } else {
        this.showToast(`Drop failed: ${data.message}`, "error");
      }
    } catch (error) {
      console.error("Error dropping course:", error);
      this.showToast("Drop failed. Please try again.", "error");
    }
  }

  updateEnrollmentSummary() {
    const summaryContainer = document.getElementById("enrollmentSummary");
    if (!summaryContainer) return;

    const totalCourses = this.enrollmentData.length;
    const totalCredits = this.enrollmentData.reduce(
      (sum, enrollment) => sum + (enrollment[5] || 0),
      0
    );
    const completedCourses = this.enrollmentData.filter(
      (enrollment) => enrollment[10] === "Completed"
    ).length;
    const inProgressCourses = this.enrollmentData.filter(
      (enrollment) => enrollment[10] === "In Progress"
    ).length;

    summaryContainer.innerHTML = `
            <div class="summary-grid">
                <div class="summary-item">
                    <span class="summary-number">${totalCourses}</span>
                    <span class="summary-label">Total Courses</span>
                </div>
                <div class="summary-item">
                    <span class="summary-number">${totalCredits}</span>
                    <span class="summary-label">Total Credits</span>
                </div>
                <div class="summary-item">
                    <span class="summary-number">${inProgressCourses}</span>
                    <span class="summary-label">In Progress</span>
                </div>
                <div class="summary-item">
                    <span class="summary-number">${completedCourses}</span>
                    <span class="summary-label">Completed</span>
                </div>
            </div>
        `;
  }

  async searchAvailableCourses() {
    const searchKeyword =
      document.getElementById("courseSearchKeyword")?.value || "";
    const departmentFilter =
      document.getElementById("courseSearchDepartment")?.value || "";

    // Filter available courses based on search criteria
    let filteredCourses = this.availableCourses;

    if (searchKeyword) {
      filteredCourses = filteredCourses.filter(
        (course) =>
          course.courseName
            .toLowerCase()
            .includes(searchKeyword.toLowerCase()) ||
          course.instructor
            .toLowerCase()
            .includes(searchKeyword.toLowerCase()) ||
          course.department.toLowerCase().includes(searchKeyword.toLowerCase())
      );
    }

    if (departmentFilter) {
      filteredCourses = filteredCourses.filter((course) =>
        course.department.toLowerCase().includes(departmentFilter.toLowerCase())
      );
    }

    // Temporarily update the available courses for display
    const originalCourses = this.availableCourses;
    this.availableCourses = filteredCourses;
    this.displayAvailableCourses();
    this.availableCourses = originalCourses;
  }

  showCourseDetails(courseId) {
    // This would show detailed course information in a modal
    alert(`Showing details for course ID: ${courseId}`);
  }

  showLoading(containerId) {
    const container = document.getElementById(containerId);
    if (container) {
      container.innerHTML = `
                <div class="loading-container">
                    <div class="loading-spinner"></div>
                    <p>Loading...</p>
                </div>
            `;
    }
  }

  showError(containerId, message) {
    const container = document.getElementById(containerId);
    if (container) {
      container.innerHTML = `
                <div class="error-container">
                    <i class="fas fa-exclamation-triangle"></i>
                    <p>Error: ${message}</p>
                    <button onclick="location.reload()" class="retry-btn">Retry</button>
                </div>
            `;
    }
  }

  showToast(message, type = "info") {
    // Create toast notification
    const toast = document.createElement("div");
    toast.className = `toast toast-${type}`;
    toast.innerHTML = `
            <i class="fas fa-${
              type === "success"
                ? "check-circle"
                : type === "error"
                ? "exclamation-circle"
                : "info-circle"
            }"></i>
            <span>${message}</span>
        `;

    // Add to page
    document.body.appendChild(toast);

    // Show toast
    setTimeout(() => toast.classList.add("show"), 100);

    // Remove toast after 3 seconds
    setTimeout(() => {
      toast.classList.remove("show");
      setTimeout(() => document.body.removeChild(toast), 300);
    }, 3000);
  }
}

// Initialize enrollment manager when DOM is loaded
document.addEventListener("DOMContentLoaded", function () {
  window.enrollmentManager = new EnrollmentManager();
});

// Utility functions for backward compatibility
function enrollInCourse(courseId, courseName) {
  if (window.enrollmentManager) {
    window.enrollmentManager.validateAndEnroll(courseId, courseName);
  }
}

function dropCourse(enrollmentId, courseName) {
  if (window.enrollmentManager) {
    window.enrollmentManager.confirmDropEnrollment(enrollmentId, courseName);
  }
}
