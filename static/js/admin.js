function showTab(tabId) {
  document
    .querySelectorAll(".tab-content")
    .forEach((sec) => sec.classList.remove("active"));
  document.getElementById(tabId).classList.add("active");

  document
    .querySelectorAll(".tabs button")
    .forEach((btn) => btn.classList.remove("active"));
  event.target.classList.add("active");

  if (tabId === "course-management") {
    loadCourses();
  } else if (tabId === "user-management") {
    loadUsers();
  } else if (tabId === "reports") {
    loadReports();
  }
}

function loadCourses() {
  AjaxHelper.get(
    "/api/courses",
    function (courses) {
      const tbody = document.getElementById("course-table-body");
      tbody.innerHTML = "";
      courses.forEach((course) => {
        const row = document.createElement("tr");
        row.innerHTML = `
        <td>${course[0]}</td>
        <td>${course[1]} ${course[2]}</td>
        <td>${course[3]}</td>
        <td>${course[4]}/${course[5]}</td>
        <td>
          <button class="icon-btn">✏️</button>
          <button class="icon-btn">🗑️</button>
        </td>
      `;
        tbody.appendChild(row);
      });
    },
    function (error) {
      alert("Failed to load courses");
    }
  );
}

function loadUsers() {
  AjaxHelper.get(
    "/api/users",
    function (data) {
      // Students
      const userTbody = document.getElementById("user-table-body");
      userTbody.innerHTML = "";
      data.users.forEach((user) => {
        const row = document.createElement("tr");
        row.innerHTML = `
        <td>${user[0]}</td>
        <td>${user[1]} ${user[2]}</td>
        <td>Student</td>
        <td>${user[5]}</td>
        <td><button class="active-button">${user[3]}</button></td>
        <td>
          <button class="icon-btn">✏️</button>
          <button class="deactive-button">Deactivate</button>
        </td>
      `;
        userTbody.appendChild(row);
      });

      // Faculty
      const facultyTbody = document.getElementById("faculty-table-body");
      facultyTbody.innerHTML = "";
      data.faculty_members.forEach((faculty) => {
        const row = document.createElement("tr");
        row.innerHTML = `
        <td>${faculty[0]}</td>
        <td>${faculty[1]} ${faculty[2]}</td>
        <td>Faculty</td>
        <td>${faculty[4]}</td>
        <td><button class="active-button">${faculty[3]}</button></td>
        <td>
          <button class="icon-btn">✏️</button>
          <button class="deactive-button">Deactivate</button>
        </td>
      `;
        facultyTbody.appendChild(row);
      });
    },
    function (error) {
      alert("Failed to load users");
    }
  );
}

function loadReports() {
  AjaxHelper.get(
    "/api/reports",
    function (data) {
      // Enrollment Statistics
      const enrollmentContainer = document.getElementById(
        "enrollment-report-container"
      );
      const enrollmentError = document.getElementById("enrollment-error");
      enrollmentContainer.innerHTML = "";
      if (
        Array.isArray(data.enrollment_data) &&
        data.enrollment_data.length > 0
      ) {
        enrollmentError.style.display = "none";
        data.enrollment_data.forEach((course) => {
          const card = document.createElement("div");
          card.className = "report-card";
          card.innerHTML = `
            <div class="card-header">
              <span class="course-name">${course.courseName || "-"}</span>
              <span class="status ${
                course.status ? course.status.toLowerCase() : ""
              }">${course.status || "-"}</span>
            </div>
            <div class="card-body">
              <div class="card-row"><span class="label">Department:</span> <span>${
                course.department || "-"
              }</span></div>
              <div class="card-row"><span class="label">Available Seats:</span> <span>${
                course.availableSeats || "-"
              }</span></div>
              <div class="card-row"><span class="label">Capacity:</span> <span>${
                course.capacity || "-"
              }</span></div>
              <div class="card-row"><span class="label">Enrolled %:</span> <span>${
                course.enrolledPercentage
                  ? course.enrolledPercentage.toFixed(2) + "%"
                  : "-"
              }</span></div>
            </div>
          `;
          enrollmentContainer.appendChild(card);
        });
      } else {
        enrollmentError.style.display = "block";
      }

      // Faculty Workload
      const facultyContainer = document.getElementById(
        "faculty-workload-container"
      );
      const facultyError = document.getElementById("faculty-error");
      facultyContainer.innerHTML = "";
      if (data.fac_report_data && !data.fac_report_data.error) {
        facultyError.style.display = "none";
        const card = document.createElement("div");
        card.className = "report-card";
        card.innerHTML = `
          <div class="card-header">
            <span class="course-name">Faculty Workload</span>
          </div>
          <div class="card-body">
            <div class="card-row"><span class="label">Number of Courses:</span> <span>${
              data.fac_report_data.numberOfCourses || "-"
            }</span></div>
            <div class="card-row"><span class="label">Total Students:</span> <span>${
              data.fac_report_data.totalStudents || "-"
            }</span></div>
          </div>
        `;
        facultyContainer.appendChild(card);
      } else {
        facultyError.style.display = "block";
        if (data.fac_report_data && data.fac_report_data.error) {
          facultyError.textContent = data.fac_report_data.error;
        }
      }
    },
    function (error) {
      document.getElementById("enrollment-error").style.display = "block";
      document.getElementById("faculty-error").style.display = "block";
    }
  );
}
