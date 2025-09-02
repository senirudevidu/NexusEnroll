// Reports Dashboard JavaScript
class ReportsManager {
  constructor() {
    this.currentData = {};
    this.charts = {};
    this.init();
  }

  init() {
    // Load initial dashboard data
    this.loadDashboardData();

    // Set up event listeners
    this.setupEventListeners();
  }

  setupEventListeners() {
    // Tab switching
    document.querySelectorAll(".tab-btn").forEach((btn) => {
      btn.addEventListener("click", (e) => {
        const tabName = e.target
          .getAttribute("onclick")
          .match(/showTab\('(.+)'\)/)[1];
        this.showTab(tabName);
      });
    });
  }

  showTab(tabName) {
    // Remove active class from all tabs and content
    document
      .querySelectorAll(".tab-btn")
      .forEach((btn) => btn.classList.remove("active"));
    document
      .querySelectorAll(".tab-content")
      .forEach((content) => content.classList.remove("active"));

    // Add active class to selected tab and content
    document
      .querySelector(`[onclick="showTab('${tabName}')"]`)
      .classList.add("active");
    document.getElementById(tabName).classList.add("active");

    // Load data for the selected tab if needed
    this.loadTabData(tabName);
  }

  showLoading() {
    document.getElementById("loadingSpinner").style.display = "flex";
  }

  hideLoading() {
    document.getElementById("loadingSpinner").style.display = "none";
  }

  async loadDashboardData() {
    this.showLoading();
    try {
      const response = await fetch("/api/reports/dashboard");
      const result = await response.json();

      if (result.status === "Success") {
        this.currentData = result.data;
        this.updateOverviewMetrics();
        this.createCharts();
      } else {
        console.error("Failed to load dashboard data:", result.message);
      }
    } catch (error) {
      console.error("Error loading dashboard data:", error);
    } finally {
      this.hideLoading();
    }
  }

  updateOverviewMetrics() {
    const data = this.currentData;

    // Calculate metrics
    const totalCourses = data.enrollmentStatistics?.length || 0;
    const totalEnrollments =
      data.enrollmentStatistics?.reduce(
        (sum, course) => sum + course.filledSeats,
        0
      ) || 0;
    const avgUtilization =
      data.departmentAnalytics?.reduce(
        (sum, dept) => sum + dept.avgUtilization,
        0
      ) / (data.departmentAnalytics?.length || 1) || 0;
    const highCapacityCount = data.highCapacityCourses?.length || 0;

    // Update DOM elements
    document.getElementById("totalCourses").textContent = totalCourses;
    document.getElementById("totalEnrollments").textContent = totalEnrollments;
    document.getElementById(
      "avgUtilization"
    ).textContent = `${avgUtilization.toFixed(1)}%`;
    document.getElementById("highCapacityCount").textContent =
      highCapacityCount;
  }

  createCharts() {
    this.createDepartmentChart();
    this.createPopularityChart();
  }

  createDepartmentChart() {
    const ctx = document.getElementById("departmentChart").getContext("2d");
    const data = this.currentData.departmentAnalytics || [];

    if (this.charts.department) {
      this.charts.department.destroy();
    }

    this.charts.department = new Chart(ctx, {
      type: "bar",
      data: {
        labels: data.map((dept) => dept.departmentName),
        datasets: [
          {
            label: "Utilization %",
            data: data.map((dept) => dept.avgUtilization),
            backgroundColor: "rgba(37, 99, 235, 0.7)",
            borderColor: "rgba(37, 99, 235, 1)",
            borderWidth: 1,
          },
        ],
      },
      options: {
        responsive: true,
        scales: {
          y: {
            beginAtZero: true,
            max: 100,
          },
        },
      },
    });
  }

  createPopularityChart() {
    const ctx = document.getElementById("popularityChart").getContext("2d");
    const data = this.currentData.popularCourses || [];

    if (this.charts.popularity) {
      this.charts.popularity.destroy();
    }

    this.charts.popularity = new Chart(ctx, {
      type: "doughnut",
      data: {
        labels: data.map((course) => course.courseName),
        datasets: [
          {
            data: data.map((course) => course.enrolledCount),
            backgroundColor: [
              "#2563eb",
              "#10b981",
              "#f59e0b",
              "#ef4444",
              "#8b5cf6",
              "#06b6d4",
              "#84cc16",
              "#f97316",
              "#ec4899",
              "#6366f1",
            ],
          },
        ],
      },
      options: {
        responsive: true,
        plugins: {
          legend: {
            position: "bottom",
          },
        },
      },
    });
  }

  loadTabData(tabName) {
    switch (tabName) {
      case "enrollment":
        this.loadEnrollmentStats();
        break;
      case "faculty":
        this.loadFacultyWorkload();
        break;
      case "popularity":
        this.loadCoursePopularity();
        break;
      case "capacity":
        this.loadHighCapacityCourses();
        break;
      case "departments":
        this.loadDepartmentAnalytics();
        break;
    }
  }

  async loadEnrollmentStats() {
    const departmentId = document.getElementById(
      "enrollmentDepartmentFilter"
    ).value;

    this.showLoading();
    try {
      const url = departmentId
        ? `/api/reports/enrollment-statistics?department_id=${departmentId}`
        : "/api/reports/enrollment-statistics";

      const response = await fetch(url);
      const result = await response.json();

      if (result.status === "Success") {
        this.displayEnrollmentStatsTable(result.data);
      } else {
        console.error("Failed to load enrollment statistics:", result.message);
      }
    } catch (error) {
      console.error("Error loading enrollment statistics:", error);
    } finally {
      this.hideLoading();
    }
  }

  displayEnrollmentStatsTable(data) {
    const container = document.getElementById("enrollmentStatsTable");

    if (!data || data.length === 0) {
      container.innerHTML = "<p>No enrollment data available.</p>";
      return;
    }

    const table = this.createTable(
      [
        "Course Name",
        "Department",
        "Instructor",
        "Capacity",
        "Filled",
        "Available",
        "Utilization %",
        "Status",
      ],
      data.map((course) => [
        course.courseName,
        course.department,
        course.instructor,
        course.capacity,
        course.filledSeats,
        course.availableSeats,
        this.createUtilizationBar(course.utilizationPercentage),
        this.createStatusBadge(course.status),
      ])
    );

    container.innerHTML = "";
    container.appendChild(table);
  }

  async loadFacultyWorkload() {
    this.showLoading();
    try {
      const response = await fetch("/api/reports/faculty-workload");
      const result = await response.json();

      if (result.status === "Success") {
        this.displayFacultyWorkloadTable(result.data);
      } else {
        console.error("Failed to load faculty workload:", result.message);
      }
    } catch (error) {
      console.error("Error loading faculty workload:", error);
    } finally {
      this.hideLoading();
    }
  }

  displayFacultyWorkloadTable(data) {
    const container = document.getElementById("facultyWorkloadTable");

    if (!data || data.length === 0) {
      container.innerHTML = "<p>No faculty workload data available.</p>";
      return;
    }

    const table = this.createTable(
      [
        "Faculty Name",
        "Department",
        "Number of Courses",
        "Total Students",
        "Avg Students per Course",
      ],
      data.map((faculty) => [
        faculty.facultyName,
        faculty.department,
        faculty.numberOfCourses,
        faculty.totalEnrolledStudents,
        faculty.avgStudentsPerCourse,
      ])
    );

    container.innerHTML = "";
    container.appendChild(table);
  }

  async loadCoursePopularity() {
    const limit = document.getElementById("popularityLimit").value;

    this.showLoading();
    try {
      const response = await fetch(
        `/api/reports/course-popularity?limit=${limit}`
      );
      const result = await response.json();

      if (result.status === "Success") {
        this.displayCoursePopularityTable(result.data);
      } else {
        console.error("Failed to load course popularity:", result.message);
      }
    } catch (error) {
      console.error("Error loading course popularity:", error);
    } finally {
      this.hideLoading();
    }
  }

  displayCoursePopularityTable(data) {
    const container = document.getElementById("coursePopularityTable");

    if (!data || data.length === 0) {
      container.innerHTML = "<p>No course popularity data available.</p>";
      return;
    }

    const table = this.createTable(
      [
        "Rank",
        "Course Name",
        "Department",
        "Instructor",
        "Enrolled",
        "Capacity",
        "Popularity %",
      ],
      data.map((course) => [
        course.rank,
        course.courseName,
        course.department,
        course.instructor,
        course.enrolledCount,
        course.capacity,
        `${course.popularityPercentage}%`,
      ])
    );

    container.innerHTML = "";
    container.appendChild(table);
  }

  async loadHighCapacityCourses() {
    const department = document.getElementById(
      "capacityDepartmentFilter"
    ).value;
    const threshold = document.getElementById("capacityThreshold").value;

    this.showLoading();
    try {
      const params = new URLSearchParams();
      if (department) params.append("department", department);
      if (threshold) params.append("threshold", threshold);

      const response = await fetch(
        `/api/reports/high-capacity-courses?${params}`
      );
      const result = await response.json();

      if (result.status === "Success") {
        this.displayHighCapacityTable(result.data);
      } else {
        console.error("Failed to load high capacity courses:", result.message);
      }
    } catch (error) {
      console.error("Error loading high capacity courses:", error);
    } finally {
      this.hideLoading();
    }
  }

  displayHighCapacityTable(data) {
    const container = document.getElementById("highCapacityTable");

    if (!data || data.length === 0) {
      container.innerHTML = "<p>No high capacity courses found.</p>";
      return;
    }

    const table = this.createTable(
      [
        "Course Name",
        "Department",
        "Instructor",
        "Capacity",
        "Enrolled",
        "Utilization %",
        "Status",
      ],
      data.map((course) => [
        course.courseName,
        course.department,
        course.instructor,
        course.capacity,
        course.enrolledCount,
        this.createUtilizationBar(course.utilizationPercentage),
        this.createStatusBadge(course.status),
      ])
    );

    container.innerHTML = "";
    container.appendChild(table);
  }

  async loadDepartmentAnalytics() {
    this.showLoading();
    try {
      const response = await fetch("/api/reports/department-analytics");
      const result = await response.json();

      if (result.status === "Success") {
        this.displayDepartmentAnalyticsTable(result.data);
      } else {
        console.error("Failed to load department analytics:", result.message);
      }
    } catch (error) {
      console.error("Error loading department analytics:", error);
    } finally {
      this.hideLoading();
    }
  }

  displayDepartmentAnalyticsTable(data) {
    const container = document.getElementById("departmentAnalyticsTable");

    if (!data || data.length === 0) {
      container.innerHTML = "<p>No department analytics data available.</p>";
      return;
    }

    const table = this.createTable(
      [
        "Department",
        "Total Courses",
        "Total Capacity",
        "Total Enrolled",
        "Available Seats",
        "Avg Utilization %",
        "Faculty Count",
      ],
      data.map((dept) => [
        dept.departmentName,
        dept.totalCourses,
        dept.totalCapacity,
        dept.totalEnrolled,
        dept.totalAvailable,
        `${dept.avgUtilization}%`,
        dept.facultyCount,
      ])
    );

    container.innerHTML = "";
    container.appendChild(table);
  }

  async loadBusinessSchoolReport() {
    this.showLoading();
    try {
      const response = await fetch("/api/reports/business-school-capacity");
      const result = await response.json();

      if (result.status === "Success") {
        this.displayBusinessSchoolReport(result);
      } else {
        console.error("Failed to load business school report:", result.message);
      }
    } catch (error) {
      console.error("Error loading business school report:", error);
    } finally {
      this.hideLoading();
    }
  }

  displayBusinessSchoolReport(result) {
    const container = document.getElementById("highCapacityTable");
    const { data, summary } = result;

    if (!data || data.length === 0) {
      container.innerHTML =
        "<p>No Business school courses found above the capacity threshold.</p>";
      return;
    }

    // Add summary information
    const summaryHtml = `
            <div class="report-summary" style="margin-bottom: 1rem; padding: 1rem; background: #f8fafc; border-radius: 0.5rem;">
                <h4>Business School High Capacity Report Summary</h4>
                <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(150px, 1fr)); gap: 1rem; margin-top: 0.5rem;">
                    <div><strong>Department:</strong> ${summary.department}</div>
                    <div><strong>Threshold:</strong> ${summary.threshold}%</div>
                    <div><strong>Total Courses:</strong> ${summary.totalCourses}</div>
                    <div><strong>Avg Utilization:</strong> ${summary.averageUtilization}%</div>
                </div>
            </div>
        `;

    const table = this.createTable(
      [
        "Course Name",
        "Instructor",
        "Total Capacity",
        "Enrolled Students",
        "Utilization %",
        "Available Seats",
        "Status",
      ],
      data.map((course) => [
        course.courseName,
        course.instructor,
        course.totalCapacity,
        course.enrolledStudents,
        this.createUtilizationBar(course.utilizationPercentage),
        course.availableSeats,
        this.createStatusBadge(course.status),
      ])
    );

    container.innerHTML = summaryHtml;
    container.appendChild(table);
  }

  createTable(headers, rows) {
    const table = document.createElement("table");
    table.className = "report-table";

    // Create header
    const thead = document.createElement("thead");
    const headerRow = document.createElement("tr");
    headers.forEach((header) => {
      const th = document.createElement("th");
      th.textContent = header;
      headerRow.appendChild(th);
    });
    thead.appendChild(headerRow);
    table.appendChild(thead);

    // Create body
    const tbody = document.createElement("tbody");
    rows.forEach((row) => {
      const tr = document.createElement("tr");
      row.forEach((cell) => {
        const td = document.createElement("td");
        if (typeof cell === "string") {
          td.textContent = cell;
        } else {
          td.appendChild(cell);
        }
        tr.appendChild(td);
      });
      tbody.appendChild(tr);
    });
    table.appendChild(tbody);

    return table;
  }

  createUtilizationBar(percentage) {
    const container = document.createElement("div");
    container.style.display = "flex";
    container.style.alignItems = "center";
    container.style.gap = "0.5rem";

    const bar = document.createElement("div");
    bar.className = "utilization-bar";

    const fill = document.createElement("div");
    fill.className = "utilization-fill";
    fill.style.width = `${percentage}%`;

    if (percentage < 70) fill.classList.add("low");
    else if (percentage < 90) fill.classList.add("medium");
    else fill.classList.add("high");

    bar.appendChild(fill);

    const text = document.createElement("span");
    text.textContent = `${percentage}%`;
    text.style.fontSize = "0.75rem";
    text.style.fontWeight = "600";

    container.appendChild(bar);
    container.appendChild(text);

    return container;
  }

  createStatusBadge(status) {
    const badge = document.createElement("span");
    badge.className = "status-badge";
    badge.textContent = status;

    switch (status.toLowerCase()) {
      case "open":
        badge.classList.add("status-open");
        break;
      case "full":
        badge.classList.add("status-full");
        break;
      case "critical":
        badge.classList.add("status-critical");
        break;
      case "high":
      case "high capacity":
        badge.classList.add("status-high");
        break;
    }

    return badge;
  }

  async exportReport(reportType, format) {
    this.showLoading();
    try {
      const url = `/api/reports/export/${format}?type=${reportType}`;
      const response = await fetch(url);

      if (response.ok) {
        const blob = await response.blob();
        const downloadUrl = window.URL.createObjectURL(blob);
        const a = document.createElement("a");
        a.href = downloadUrl;
        a.download = `${reportType}_report.${format}`;
        document.body.appendChild(a);
        a.click();
        document.body.removeChild(a);
        window.URL.revokeObjectURL(downloadUrl);
      } else {
        console.error("Failed to export report");
      }
    } catch (error) {
      console.error("Error exporting report:", error);
    } finally {
      this.hideLoading();
    }
  }

  // Quick action methods
  async generateBusinessReport() {
    this.showTab("capacity");
    await this.loadBusinessSchoolReport();
  }

  async generateHighCapacityReport() {
    this.showTab("capacity");
    document.getElementById("capacityThreshold").value = "90";
    await this.loadHighCapacityCourses();
  }

  async generateFacultyReport() {
    this.showTab("faculty");
    await this.loadFacultyWorkload();
  }
}

// Global functions for template onclick handlers
function showTab(tabName) {
  window.reportsManager.showTab(tabName);
}

function loadEnrollmentStats() {
  window.reportsManager.loadEnrollmentStats();
}

function loadFacultyWorkload() {
  window.reportsManager.loadFacultyWorkload();
}

function loadCoursePopularity() {
  window.reportsManager.loadCoursePopularity();
}

function loadHighCapacityCourses() {
  window.reportsManager.loadHighCapacityCourses();
}

function loadBusinessSchoolReport() {
  window.reportsManager.loadBusinessSchoolReport();
}

function loadDepartmentAnalytics() {
  window.reportsManager.loadDepartmentAnalytics();
}

function exportReport(reportType, format) {
  window.reportsManager.exportReport(reportType, format);
}

function generateBusinessReport() {
  window.reportsManager.generateBusinessReport();
}

function generateHighCapacityReport() {
  window.reportsManager.generateHighCapacityReport();
}

function generateFacultyReport() {
  window.reportsManager.generateFacultyReport();
}

function closeExportModal() {
  document.getElementById("exportModal").style.display = "none";
}

// Initialize the reports manager when the page loads
document.addEventListener("DOMContentLoaded", function () {
  window.reportsManager = new ReportsManager();
});
