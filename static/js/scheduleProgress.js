// Schedule and Progress Management JavaScript
class ScheduleProgressManager {
  constructor() {
    this.currentStudentId = null;
    this.availableSemesters = [];
    this.currentSchedule = null;
    this.academicProgress = null;
    this.currentSemester = null;
  }

  // ============ INITIALIZATION ============

  async initialize(studentId) {
    this.currentStudentId = studentId;

    try {
      // Load current semester info
      await this.loadCurrentSemester();

      // Load available semesters for the student
      await this.loadAvailableSemesters();

      // Load current schedule
      await this.loadStudentSchedule();

      // Load academic progress
      await this.loadAcademicProgress();

      this.setupEventListeners();
    } catch (error) {
      console.error(
        "Failed to initialize schedule and progress manager:",
        error
      );
      this.showError("Failed to load schedule and progress data");
    }
  }

  setupEventListeners() {
    // Semester selector change
    const semesterSelect = document.getElementById("semesterSelect");
    if (semesterSelect) {
      semesterSelect.addEventListener("change", (e) => {
        const semesterId = e.target.value || null;
        this.loadStudentSchedule(semesterId);
      });
    }

    // View toggle buttons
    const calendarViewBtn = document.getElementById("calendarViewBtn");
    const listViewBtn = document.getElementById("listViewBtn");

    if (calendarViewBtn) {
      calendarViewBtn.addEventListener("click", () => this.showCalendarView());
    }

    if (listViewBtn) {
      listViewBtn.addEventListener("click", () => this.showListView());
    }

    // Refresh buttons
    const refreshScheduleBtn = document.getElementById("refreshSchedule");
    const refreshProgressBtn = document.getElementById("refreshProgress");

    if (refreshScheduleBtn) {
      refreshScheduleBtn.addEventListener("click", () =>
        this.loadStudentSchedule()
      );
    }

    if (refreshProgressBtn) {
      refreshProgressBtn.addEventListener("click", () =>
        this.loadAcademicProgress()
      );
    }
  }

  // ============ SCHEDULE MANAGEMENT ============

  async loadCurrentSemester() {
    try {
      const response = await fetch("/api/academic/current-semester");
      const result = await response.json();

      if (result.status === "Success" && result.data) {
        this.currentSemester = result.data;
      }
    } catch (error) {
      console.error("Failed to load current semester:", error);
    }
  }

  async loadAvailableSemesters() {
    try {
      const response = await fetch(
        `/api/personal-schedule/${this.currentStudentId}/semesters`
      );
      const result = await response.json();

      if (result.status === "Success") {
        this.availableSemesters = result.data;
        this.populateSemesterSelector();
      } else {
        this.showError(result.message);
      }
    } catch (error) {
      console.error("Failed to load semesters:", error);
      this.showError("Failed to load available semesters");
    }
  }

  async loadStudentSchedule(semesterId = null) {
    try {
      this.showLoading("schedule");

      const url = semesterId
        ? `/api/personal-schedule/${this.currentStudentId}?semester=${semesterId}`
        : `/api/personal-schedule/${this.currentStudentId}`;

      const response = await fetch(url);
      const result = await response.json();

      if (result.status === "Success") {
        this.currentSchedule = result.data;
        this.displaySchedule(result.data, result.weekly_grid);
      } else {
        this.showError(result.message);
        this.displayEmptySchedule();
      }
    } catch (error) {
      console.error("Failed to load schedule:", error);
      this.showError("Failed to load schedule data");
      this.displayEmptySchedule();
    } finally {
      this.hideLoading("schedule");
    }
  }

  populateSemesterSelector() {
    const semesterSelect = document.getElementById("semesterSelect");
    if (!semesterSelect) return;

    semesterSelect.innerHTML = '<option value="">Current Semester</option>';

    this.availableSemesters.forEach((semester) => {
      const option = document.createElement("option");
      option.value = semester.semester_id;
      option.textContent = `${semester.semester_name} (${semester.course_count} courses)`;
      if (semester.is_current) {
        option.textContent += " - Current";
      }
      semesterSelect.appendChild(option);
    });
  }

  displaySchedule(scheduleData, weeklyGrid) {
    // Display calendar view
    this.displayCalendarView(weeklyGrid);

    // Display list view
    this.displayListView(scheduleData);

    // Update schedule summary
    this.updateScheduleSummary(scheduleData);
  }

  displayCalendarView(weeklyGrid) {
    const calendarContainer = document.getElementById("scheduleCalendar");
    if (!calendarContainer) return;

    // Time slots from 8 AM to 8 PM
    const timeSlots = [];
    for (let hour = 8; hour <= 20; hour++) {
      timeSlots.push(`${hour.toString().padStart(2, "0")}:00`);
    }

    const days = [
      "Monday",
      "Tuesday",
      "Wednesday",
      "Thursday",
      "Friday",
      "Saturday",
      "Sunday",
    ];

    let calendarHTML = '<div class="calendar-grid">';

    // Header row
    calendarHTML += '<div class="time-slot"></div>'; // Empty cell for time column
    days.forEach((day) => {
      calendarHTML += `<div class="day-header">${day}</div>`;
    });

    // Time slot rows
    timeSlots.forEach((time) => {
      calendarHTML += `<div class="time-slot">${this.formatTime(time)}</div>`;

      days.forEach((day) => {
        const courses = weeklyGrid[day] || [];
        const coursesInTimeSlot = courses.filter((course) => {
          return (
            course.startTime &&
            this.isTimeInSlot(course.startTime, course.endTime, time)
          );
        });

        calendarHTML += '<div class="schedule-cell">';
        coursesInTimeSlot.forEach((course) => {
          const courseType = this.determineCourseType(course.courseName);
          calendarHTML += `
                        <div class="course-block ${courseType}" title="${
            course.courseName
          } - ${course.instructor}">
                            <div class="course-name">${course.courseName}</div>
                            <div class="course-details">${
                              course.instructor
                            }</div>
                            <div class="course-location">${
                              course.location || "TBA"
                            }</div>
                        </div>
                    `;
        });
        calendarHTML += "</div>";
      });
    });

    calendarHTML += "</div>";
    calendarContainer.innerHTML = calendarHTML;
  }

  displayListView(scheduleData) {
    const listContainer = document.getElementById("scheduleList");
    if (!listContainer) return;

    // Group courses by day
    const coursesByDay = {};
    const days = [
      "Monday",
      "Tuesday",
      "Wednesday",
      "Thursday",
      "Friday",
      "Saturday",
      "Sunday",
    ];

    days.forEach((day) => (coursesByDay[day] = []));

    scheduleData.forEach((course) => {
      if (course.day && coursesByDay[course.day]) {
        coursesByDay[course.day].push(course);
      }
    });

    let listHTML = "";
    days.forEach((day) => {
      const courses = coursesByDay[day];
      if (courses.length > 0) {
        listHTML += `
                    <div class="schedule-day">
                        <h3 class="day-title">${day}</h3>
                        <div class="day-courses">
                `;

        courses.sort((a, b) =>
          (a.startTime || "").localeCompare(b.startTime || "")
        );

        courses.forEach((course) => {
          listHTML += `
                        <div class="course-item">
                            <div class="course-info">
                                <h4>${course.courseName}</h4>
                                <p>${course.instructor} • ${
            course.location || "TBA"
          }</p>
                                <div class="course-location-info">${
                                  course.credits
                                } credits</div>
                            </div>
                            <div class="course-time">
                                <div>${this.formatTimeRange(
                                  course.startTime,
                                  course.endTime
                                )}</div>
                                <div class="course-location-info">${
                                  course.markStatus
                                }</div>
                            </div>
                        </div>
                    `;
        });

        listHTML += "</div></div>";
      }
    });

    if (listHTML === "") {
      listHTML =
        '<div class="empty-state"><h3>No classes scheduled</h3><p>No courses found for the selected semester.</p></div>';
    }

    listContainer.innerHTML = listHTML;
  }

  updateScheduleSummary(scheduleData) {
    const summaryContainer = document.getElementById("scheduleSummary");
    if (!summaryContainer) return;

    const totalCourses = scheduleData.length;
    const totalCredits = scheduleData.reduce(
      (sum, course) => sum + (course.credits || 0),
      0
    );
    const inProgress = scheduleData.filter(
      (course) => course.markStatus === "In Progress"
    ).length;
    const completed = scheduleData.filter(
      (course) => course.markStatus === "Completed"
    ).length;

    summaryContainer.innerHTML = `
            <div class="progress-overview">
                <div class="progress-card primary">
                    <span class="progress-number">${totalCourses}</span>
                    <span class="progress-label">Total Courses</span>
                </div>
                <div class="progress-card success">
                    <span class="progress-number">${totalCredits}</span>
                    <span class="progress-label">Total Credits</span>
                </div>
                <div class="progress-card warning">
                    <span class="progress-number">${inProgress}</span>
                    <span class="progress-label">In Progress</span>
                </div>
                <div class="progress-card info">
                    <span class="progress-number">${completed}</span>
                    <span class="progress-label">Completed</span>
                </div>
            </div>
        `;
  }

  // ============ ACADEMIC PROGRESS MANAGEMENT ============

  async loadAcademicProgress() {
    try {
      this.showLoading("progress");

      const response = await fetch(`/api/progress/${this.currentStudentId}`);
      const result = await response.json();

      if (result.status === "Success") {
        this.academicProgress = result.data;
        this.displayAcademicProgress(result.data);
      } else {
        this.showError(result.message);
        this.displayEmptyProgress();
      }
    } catch (error) {
      console.error("Failed to load academic progress:", error);
      this.showError("Failed to load academic progress data");
      this.displayEmptyProgress();
    } finally {
      this.hideLoading("progress");
    }
  }

  displayAcademicProgress(progressData) {
    this.displayProgressOverview(progressData.academic_summary);
    this.displayCompletedCourses(progressData.completed_courses);
    this.displayPendingRequirements(progressData.pending_requirements);
    this.displayGradeDistribution(progressData.grade_distribution);
  }

  displayProgressOverview(summary) {
    const overviewContainer = document.getElementById("progressOverview");
    if (!overviewContainer) return;

    overviewContainer.innerHTML = `
            <div class="progress-overview">
                <div class="progress-card primary">
                    <span class="progress-number">${summary.completed_courses}</span>
                    <span class="progress-label">Completed Courses</span>
                </div>
                <div class="progress-card success">
                    <span class="progress-number">${summary.completed_credits}</span>
                    <span class="progress-label">Credits Earned</span>
                </div>
                <div class="progress-card warning">
                    <span class="progress-number">${summary.gpa}</span>
                    <span class="progress-label">Current GPA</span>
                </div>
                <div class="progress-card info">
                    <span class="progress-number">${summary.progress_percentage}%</span>
                    <span class="progress-label">Degree Progress</span>
                </div>
            </div>
            
            <div class="progress-bar-container">
                <div class="progress-bar-label">
                    <span>Degree Progress</span>
                    <span>${summary.completed_credits} / ${summary.total_degree_credits} credits</span>
                </div>
                <div class="progress-bar">
                    <div class="progress-fill" style="width: ${summary.progress_percentage}%"></div>
                </div>
            </div>
        `;
  }

  displayCompletedCourses(completedCourses) {
    const coursesContainer = document.getElementById("completedCourses");
    if (!coursesContainer) return;

    if (completedCourses.length === 0) {
      coursesContainer.innerHTML = `
                <div class="empty-state">
                    <div class="empty-state-icon">📚</div>
                    <h3>No Completed Courses</h3>
                    <p>You haven't completed any courses yet.</p>
                </div>
            `;
      return;
    }

    let coursesHTML = "";
    completedCourses.forEach((course) => {
      const gradeClass = this.getGradeClass(course.grade);

      coursesHTML += `
                <div class="completed-course-item">
                    <div class="course-header-info">
                        <div class="course-name-grade">
                            <h4>${course.courseName}</h4>
                            <div class="course-semester">${course.semester} • ${course.academic_year}</div>
                        </div>
                        <div class="grade-display ${gradeClass}">${course.grade}</div>
                    </div>
                    <div class="course-details-info">
                        <span>${course.instructor} • ${course.department}</span>
                        <span>${course.credits} credits</span>
                    </div>
                </div>
            `;
    });

    coursesContainer.innerHTML = `
            <h2 class="section-title">Completed Courses</h2>
            <div class="courses-grid">
                ${coursesHTML}
            </div>
        `;
  }

  displayPendingRequirements(pendingRequirements) {
    const requirementsContainer = document.getElementById(
      "pendingRequirements"
    );
    if (!requirementsContainer) return;

    if (pendingRequirements.length === 0) {
      requirementsContainer.innerHTML = `
                <h2 class="section-title">Pending Requirements</h2>
                <div class="empty-state">
                    <div class="empty-state-icon">🎉</div>
                    <h3>All Requirements Complete!</h3>
                    <p>Congratulations! You have completed all degree requirements.</p>
                </div>
            `;
      return;
    }

    // Group by requirement type
    const coreRequirements = pendingRequirements.filter(
      (req) => req.is_core_requirement
    );
    const electiveOptions = pendingRequirements.filter(
      (req) => !req.is_core_requirement
    );

    let requirementsHTML =
      '<h2 class="section-title">Pending Requirements</h2>';

    if (coreRequirements.length > 0) {
      requirementsHTML +=
        '<h3>Core Requirements</h3><div class="requirements-list">';
      coreRequirements.forEach((req) => {
        requirementsHTML += this.createRequirementItem(req, "core");
      });
      requirementsHTML += "</div>";
    }

    if (electiveOptions.length > 0) {
      requirementsHTML +=
        '<h3>Elective Options</h3><div class="requirements-list">';
      electiveOptions.forEach((req) => {
        requirementsHTML += this.createRequirementItem(req, "elective");
      });
      requirementsHTML += "</div>";
    }

    requirementsContainer.innerHTML = requirementsHTML;
  }

  createRequirementItem(requirement, type) {
    return `
            <div class="requirement-item ${type}">
                <div class="requirement-header">
                    <h4 class="requirement-name">${requirement.courseName}</h4>
                    <span class="requirement-type ${type}">${
      requirement.requirement_type
    }</span>
                </div>
                <p class="requirement-description">${
                  requirement.description || "No description available"
                }</p>
                <div class="requirement-details">
                    <span>${requirement.credits} credits</span>
                    <span>Recommended Year: ${
                      requirement.year_requirement || "Any"
                    }</span>
                </div>
            </div>
        `;
  }

  displayGradeDistribution(gradeDistribution) {
    const distributionContainer = document.getElementById("gradeDistribution");
    if (!distributionContainer) return;

    const totalGrades = Object.values(gradeDistribution).reduce(
      (sum, count) => sum + count,
      0
    );

    if (totalGrades === 0) {
      distributionContainer.innerHTML = "";
      return;
    }

    let distributionHTML =
      '<h3>Grade Distribution</h3><div class="grade-distribution-chart">';

    Object.entries(gradeDistribution).forEach(([grade, count]) => {
      if (count > 0) {
        const percentage = Math.round((count / totalGrades) * 100);
        const gradeClass = this.getGradeClass(grade);

        distributionHTML += `
                    <div class="grade-bar">
                        <div class="grade-label">${grade}</div>
                        <div class="grade-bar-fill ${gradeClass}" style="width: ${percentage}%"></div>
                        <div class="grade-count">${count}</div>
                    </div>
                `;
      }
    });

    distributionHTML += "</div>";
    distributionContainer.innerHTML = distributionHTML;
  }

  // ============ HELPER METHODS ============

  formatTime(time) {
    if (!time) return "";
    const [hours, minutes] = time.split(":");
    const hour = parseInt(hours);
    const ampm = hour >= 12 ? "PM" : "AM";
    const displayHour = hour % 12 || 12;
    return `${displayHour}:${minutes} ${ampm}`;
  }

  formatTimeRange(startTime, endTime) {
    if (!startTime || !endTime) return "Time TBA";
    return `${this.formatTime(startTime)} - ${this.formatTime(endTime)}`;
  }

  isTimeInSlot(courseStartTime, courseEndTime, slotTime) {
    if (!courseStartTime || !courseEndTime || !slotTime) return false;

    const slotHour = parseInt(slotTime.split(":")[0]);
    const courseStart = parseInt(courseStartTime.split(":")[0]);
    const courseEnd = parseInt(courseEndTime.split(":")[0]);

    return slotHour >= courseStart && slotHour < courseEnd;
  }

  determineCourseType(courseName) {
    if (!courseName) return "";

    const name = courseName.toLowerCase();
    if (name.includes("lab") || name.includes("practical")) return "lab";
    if (name.includes("elective")) return "elective";
    return "core";
  }

  getGradeClass(grade) {
    if (!grade) return "";
    switch (grade.toUpperCase()) {
      case "A":
        return "grade-a";
      case "B":
        return "grade-b";
      case "C":
        return "grade-c";
      case "D":
        return "grade-d";
      case "F":
        return "grade-f";
      default:
        return "";
    }
  }

  showCalendarView() {
    const calendarView = document.getElementById("scheduleCalendar");
    const listView = document.getElementById("scheduleList");
    const calendarBtn = document.getElementById("calendarViewBtn");
    const listBtn = document.getElementById("listViewBtn");

    if (calendarView) calendarView.style.display = "block";
    if (listView) listView.style.display = "none";
    if (calendarBtn) calendarBtn.classList.add("active");
    if (listBtn) listBtn.classList.remove("active");
  }

  showListView() {
    const calendarView = document.getElementById("scheduleCalendar");
    const listView = document.getElementById("scheduleList");
    const calendarBtn = document.getElementById("calendarViewBtn");
    const listBtn = document.getElementById("listViewBtn");

    if (calendarView) calendarView.style.display = "none";
    if (listView) listView.style.display = "block";
    if (calendarBtn) calendarBtn.classList.remove("active");
    if (listBtn) listBtn.classList.add("active");
  }

  displayEmptySchedule() {
    const calendarContainer = document.getElementById("scheduleCalendar");
    const listContainer = document.getElementById("scheduleList");

    const emptyHTML = `
            <div class="empty-state">
                <div class="empty-state-icon">📅</div>
                <h3>No Schedule Available</h3>
                <p>No courses found for the selected semester.</p>
            </div>
        `;

    if (calendarContainer) calendarContainer.innerHTML = emptyHTML;
    if (listContainer) listContainer.innerHTML = emptyHTML;
  }

  displayEmptyProgress() {
    const progressContainer = document.getElementById("progressContainer");
    if (progressContainer) {
      progressContainer.innerHTML = `
                <div class="empty-state">
                    <div class="empty-state-icon">📊</div>
                    <h3>No Progress Data</h3>
                    <p>Unable to load academic progress information.</p>
                </div>
            `;
    }
  }

  showLoading(section) {
    const container = document.getElementById(`${section}Container`);
    if (container) {
      container.innerHTML = `
                <div class="loading-spinner">
                    <div class="spinner"></div>
                </div>
            `;
    }
  }

  hideLoading(section) {
    // Loading will be hidden when content is displayed
  }

  showError(message) {
    // Create or update error message
    let errorContainer = document.getElementById("errorMessage");
    if (!errorContainer) {
      errorContainer = document.createElement("div");
      errorContainer.id = "errorMessage";
      errorContainer.className = "error-message";

      const mainContainer = document.querySelector(
        ".schedule-container, .progress-container"
      );
      if (mainContainer) {
        mainContainer.insertBefore(errorContainer, mainContainer.firstChild);
      }
    }

    errorContainer.innerHTML = `
            <strong>Error:</strong> ${message}
            <button onclick="this.parentElement.style.display='none'" style="float: right; background: none; border: none; color: inherit; cursor: pointer;">&times;</button>
        `;
    errorContainer.style.display = "block";

    // Auto-hide after 5 seconds
    setTimeout(() => {
      errorContainer.style.display = "none";
    }, 5000);
  }
}

// Global instance
let scheduleProgressManager = null;

// Initialize when DOM is loaded
document.addEventListener("DOMContentLoaded", function () {
  // This will be called from the student dashboard when needed
  window.initializeScheduleProgress = function (studentId) {
    scheduleProgressManager = new ScheduleProgressManager();
    scheduleProgressManager.initialize(studentId);
  };
});
