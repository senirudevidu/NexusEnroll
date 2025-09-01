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
          <button class="icon-btn edit-btn" onclick="editCourse(${course[6]})">✏️</button>
          <button class="icon-btn delete-btn" onclick="deleteCourse(${course[6]})">🗑️</button>
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
        const statusClass =
          user[3] === "active" ? "active-button" : "inactive-button";
        const actionText = user[3] === "active" ? "Deactivate" : "Activate";
        row.innerHTML = `
        <td>${user[0]}</td>
        <td>${user[1]} ${user[2]}</td>
        <td>Student</td>
        <td>${user[5]}</td>
        <td><button class="${statusClass}">${user[3]}</button></td>
        <td>
          <button class="icon-btn edit-btn" onclick="editUser(${user[0]}, 'student')">✏️</button>
          <button class="deactive-button" onclick="deactivateUser(${user[0]}, 'student')">${actionText}</button>
        </td>
      `;
        userTbody.appendChild(row);
      });

      // Faculty
      const facultyTbody = document.getElementById("faculty-table-body");
      facultyTbody.innerHTML = "";
      data.faculty_members.forEach((faculty) => {
        const row = document.createElement("tr");
        const statusClass =
          faculty[3] === "active" ? "active-button" : "inactive-button";
        const actionText = faculty[3] === "active" ? "Deactivate" : "Activate";
        row.innerHTML = `
        <td>${faculty[0]}</td>
        <td>${faculty[1]} ${faculty[2]}</td>
        <td>Faculty</td>
        <td>${faculty[4]}</td>
        <td><button class="${statusClass}">${faculty[3]}</button></td>
        <td>
          <button class="icon-btn edit-btn" onclick="editUser(${faculty[0]}, 'faculty')">✏️</button>
          <button class="deactive-button" onclick="deactivateUser(${faculty[0]}, 'faculty')">${actionText}</button>
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
  // Load quick metrics and alerts first
  loadQuickMetrics();
  loadRecentAlerts();

  // Then load legacy reports if containers exist
  AjaxHelper.get(
    "/api/reports",
    function (data) {
      // Enrollment Statistics (Legacy)
      const enrollmentContainer = document.getElementById(
        "enrollment-report-container"
      );
      const enrollmentError = document.getElementById("enrollment-error");

      if (enrollmentContainer) {
        enrollmentContainer.innerHTML = "";
        if (
          Array.isArray(data.enrollment_data) &&
          data.enrollment_data.length > 0
        ) {
          if (enrollmentError) enrollmentError.style.display = "none";
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
          if (enrollmentError) enrollmentError.style.display = "block";
        }
      }

      // Faculty Workload (Legacy)
      const facultyContainer = document.getElementById(
        "faculty-workload-container"
      );
      const facultyError = document.getElementById("faculty-error");

      if (facultyContainer) {
        facultyContainer.innerHTML = "";
        if (
          Array.isArray(data.faculty_workload) &&
          data.faculty_workload.length > 0
        ) {
          if (facultyError) facultyError.style.display = "none";
          data.faculty_workload.forEach((fac) => {
            const card = document.createElement("div");
            card.className = "report-card";
            card.innerHTML = `
              <div class="card-header">
                <span>Faculty: ${fac.facultyName}</span>
                <span>ID: ${fac.facultyId}</span>
              </div>
              <div class="card-body">
                <div class="card-row"><span class="label">Number of Courses:</span> <span>${fac.numberOfCourses}</span></div>
                <div class="card-row"><span class="label">Number of Students:</span> <span>${fac.numberOfStudents}</span></div>
              </div>
            `;
            facultyContainer.appendChild(card);
          });
        } else {
          if (facultyError) facultyError.style.display = "block";
        }
      }
    },
    function (error) {
      console.error("Failed to load legacy reports:", error);
      const enrollmentError = document.getElementById("enrollment-error");
      const facultyError = document.getElementById("faculty-error");
      if (enrollmentError) enrollmentError.style.display = "block";
      if (facultyError) facultyError.style.display = "block";
    }
  );
}

function editCourse(courseId) {
  // Get course details first
  AjaxHelper.get(
    `/api/courses/${courseId}`,
    function (course) {
      // Get departments and degrees for dropdowns
      Promise.all([
        fetch("/api/departments").then((response) => response.json()),
        fetch("/api/degrees").then((response) => response.json()),
        fetch("/api/faculty").then((response) => response.json()),
      ])
        .then(([departments, degrees, faculty]) => {
          showEditCourseModal(course, departments, degrees, faculty);
        })
        .catch((error) => {
          console.error("Error fetching dropdown data:", error);
          // Show modal with basic fields only
          showEditCourseModal(course, [], [], []);
        });
    },
    function (error) {
      alert("Failed to load course details");
    }
  );
}

function showEditCourseModal(
  course,
  departments = [],
  degrees = [],
  faculty = []
) {
  const modal = document.createElement("div");
  modal.className = "modal";

  // Create department options - matching addCourse.html format
  const departmentOptions = departments
    .map(
      (dept) =>
        `<option value="${dept[0]}" ${
          dept[0] === course[7] ? "selected" : ""
        }>${dept[1]}</option>`
    )
    .join("");

  // Create degree options - matching addCourse.html format
  const degreeOptions = degrees
    .map(
      (degree) =>
        `<option value="${degree[0]}" ${
          degree[0] === course[6] ? "selected" : ""
        }>${degree[1]}</option>`
    )
    .join("");

  // Create faculty options - matching addCourse.html format
  const facultyOptions = faculty
    .map(
      (fac) =>
        `<option value="${fac[0]}" ${fac[0] === course[10] ? "selected" : ""}>${
          fac[1]
        } ${fac[2]}</option>`
    )
    .join("");

  modal.innerHTML = `
    <div class="modal-content">
      <div class="modal-header">
        <h2>Edit Course</h2>
        <span class="close" onclick="closeModal()">&times;</span>
      </div>
      <div class="modal-body">
        <form id="editCourseForm">
          <input type="hidden" id="editCourseId" value="${course[0]}">
          
          <div class="form-group">
            <label for="editCourseName">Course Name:</label>
            <input type="text" id="editCourseName" name="courseName" value="${course[1]}" required placeholder="Enter course name">
          </div>
          
          <div class="form-group">
            <label for="editDescription">Description:</label>
            <textarea id="editDescription" name="description" required placeholder="Enter course description">${course[2]}</textarea>
          </div>
          
          <div class="form-group">
            <label for="editCapacity">Capacity:</label>
            <input type="number" id="editCapacity" name="capacity" value="${course[3]}" min="1" required placeholder="Enter course capacity">
          </div>
          
          <div class="form-group">
            <label for="editCredits">Credits:</label>
            <input type="number" id="editCredits" name="credits" value="${course[5]}" min="0" required placeholder="Enter course credits">
          </div>
          
          <div class="form-group">
            <label for="editPreReqYear">Pre-requisite Year:</label>
            <input type="number" id="editPreReqYear" name="preReqYear" value="${course[8]}" min="1" max="4" placeholder="Only this year students can enroll" required>
          </div>
          
          <div class="form-group">
            <label for="editDegree">Degree:</label>
            <select id="editDegree" name="degree_ID" required>
              <option value="">--Select Degree--</option>
              ${degreeOptions}
            </select>
          </div>
          
          <div class="form-group">
            <label for="editDepartment">Department:</label>
            <select id="editDepartment" name="dept_Id" required>
              <option value="">--Select Department--</option>
              ${departmentOptions}
            </select>
          </div>
          
          <div class="form-group">
            <label for="editFaculty">Faculty Member:</label>
            <select id="editFaculty" name="facultyMem_Id" required>
              <option value="">--Select Faculty Member--</option>
              ${facultyOptions}
            </select>
          </div>
          
          <div class="form-actions">
            <button type="button" onclick="updateCourse()">Update Course</button>
            <button type="button" onclick="closeModal()">Cancel</button>
          </div>
        </form>
      </div>
    </div>
  `;

  document.body.appendChild(modal);
  modal.style.display = "block";
}

function updateCourse() {
  const courseId = document.getElementById("editCourseId").value;
  const courseName = document.getElementById("editCourseName").value;
  const description = document.getElementById("editDescription").value;
  const capacity = parseInt(document.getElementById("editCapacity").value);
  const credits = parseInt(document.getElementById("editCredits").value);
  const preReqYear = parseInt(document.getElementById("editPreReqYear").value);
  const degreeId = document.getElementById("editDegree").value;
  const departmentId = document.getElementById("editDepartment").value;
  const facultyId = document.getElementById("editFaculty").value;

  const courseData = {
    courseName: courseName,
    description: description,
    capacity: capacity,
    availableSeats: capacity,
    credits: credits,
    preReqYear: preReqYear,
    degree_ID: degreeId,
    dept_Id: departmentId,
    allowedDeptID: departmentId,
    facultyMem_Id: facultyId,
  };

  AjaxHelper.put(
    `/api/courses/${courseId}`,
    courseData,
    function (response) {
      alert(response.message);
      closeModal();
      loadCourses(); // Refresh the course list
    },
    function (error) {
      alert("Failed to update course: " + (error.message || "Unknown error"));
    }
  );
}

function deleteCourse(courseId) {
  if (
    confirm(
      "Are you sure you want to delete this course? This action cannot be undone."
    )
  ) {
    AjaxHelper.delete(
      `/api/courses/${courseId}`,
      function (response) {
        alert(response.message);
        loadCourses(); // Refresh the course list
      },
      function (error) {
        alert("Failed to delete course: " + (error.message || "Unknown error"));
      }
    );
  }
}

function closeModal() {
  const modal = document.querySelector(".modal");
  if (modal) {
    modal.remove();
  }
}

function editUser(userId, userType) {
  // Get user details first
  AjaxHelper.get(
    `/api/users/${userId}`,
    function (user) {
      if (userType === "student") {
        // Get degrees for dropdown
        fetch("/api/degrees")
          .then((response) => response.json())
          .then((degrees) => {
            showEditUserModal(user, degrees);
          })
          .catch((error) => {
            console.error("Error fetching degrees:", error);
            showEditUserModal(user, []);
          });
      } else {
        showEditUserModal(user, []);
      }
    },
    function (error) {
      alert("Failed to load user details");
    }
  );
}

function showEditUserModal(user, degrees = []) {
  const modal = document.createElement("div");
  modal.className = "modal";

  let userSpecificFields = "";

  if (user.user_type === "student") {
    const degreeOptions = degrees
      .map(
        (degree) =>
          `<option value="${degree[0]}" ${
            degree[1] === user.degree ? "selected" : ""
          }>${degree[1]}</option>`
      )
      .join("");

    userSpecificFields = `
      <div class="form-group">
        <label for="editYearOfStudy">Year of Study:</label>
        <input type="number" id="editYearOfStudy" name="yearOfStudy" value="${
          user.yearOfStudy || ""
        }" min="1" max="4" placeholder="Enter year of study">
      </div>
      
      <div class="form-group">
        <label for="editDegree">Degree:</label>
        <select id="editDegree" name="degreeID">
          <option value="">--Select Degree--</option>
          ${degreeOptions}
        </select>
      </div>
    `;
  } else if (user.user_type === "faculty") {
    userSpecificFields = `
      <div class="form-group">
        <label for="editRole">Role:</label>
        <input type="text" id="editRole" name="role" value="${
          user.role || ""
        }" placeholder="Enter faculty role">
      </div>
    `;
  }

  modal.innerHTML = `
    <div class="modal-content">
      <div class="modal-header">
        <h2>Edit ${
          user.user_type.charAt(0).toUpperCase() + user.user_type.slice(1)
        }</h2>
        <span class="close" onclick="closeModal()">&times;</span>
      </div>
      <div class="modal-body">
        <form id="editUserForm">
          <input type="hidden" id="editUserId" value="${user.user_id}">
          <input type="hidden" id="editUserType" value="${user.user_type}">
          
          <div class="form-group">
            <label for="editFirstName">First Name:</label>
            <input type="text" id="editFirstName" name="firstName" value="${
              user.firstName || ""
            }" required placeholder="Enter first name">
          </div>
          
          <div class="form-group">
            <label for="editLastName">Last Name:</label>
            <input type="text" id="editLastName" name="lastName" value="${
              user.lastName || ""
            }" required placeholder="Enter last name">
          </div>
          
          <div class="form-group">
            <label for="editEmail">Email:</label>
            <input type="email" id="editEmail" name="email" value="${
              user.email || ""
            }" required placeholder="Enter email address">
          </div>
          
          <div class="form-group">
            <label for="editMobileNo">Mobile Number:</label>
            <input type="tel" id="editMobileNo" name="mobileNo" value="${
              user.mobileNo || ""
            }" placeholder="Enter mobile number">
          </div>
          
          ${userSpecificFields}
          
          <div class="form-actions">
            <button type="button" onclick="updateUser()">Update User</button>
            <button type="button" onclick="closeModal()">Cancel</button>
          </div>
        </form>
      </div>
    </div>
  `;

  document.body.appendChild(modal);
  modal.style.display = "block";
}

function updateUser() {
  const userId = document.getElementById("editUserId").value;
  const userType = document.getElementById("editUserType").value;
  const firstName = document.getElementById("editFirstName").value;
  const lastName = document.getElementById("editLastName").value;
  const email = document.getElementById("editEmail").value;
  const mobileNo = document.getElementById("editMobileNo").value;

  const userData = {
    user_id: parseInt(userId),
    user_type: userType,
    firstName: firstName,
    lastName: lastName,
    email: email,
    mobileNo: mobileNo,
  };

  // Add user-type specific fields
  if (userType === "student") {
    const yearOfStudy = document.getElementById("editYearOfStudy")?.value;
    const degreeID = document.getElementById("editDegree")?.value;
    if (yearOfStudy) userData.yearOfStudy = parseInt(yearOfStudy);
    if (degreeID) userData.degreeID = parseInt(degreeID);
  } else if (userType === "faculty") {
    const role = document.getElementById("editRole")?.value;
    if (role) userData.role = role;
  }

  AjaxHelper.put(
    `/api/users/${userId}`,
    userData,
    function (response) {
      alert(response.message);
      closeModal();
      loadUsers(); // Refresh the user list
    },
    function (error) {
      alert("Failed to update user: " + (error.message || "Unknown error"));
    }
  );
}

function deactivateUser(userId, userType) {
  const action = event.target.textContent.toLowerCase();
  const confirmMessage = `Are you sure you want to ${action} this ${userType}?`;

  if (confirm(confirmMessage)) {
    const requestData = {
      user_type: userType,
    };

    AjaxHelper.post(
      `/api/users/${userId}/deactivate`,
      requestData,
      function (response) {
        alert(response.message);
        loadUsers(); // Refresh the user list
      },
      function (error) {
        alert(
          `Failed to ${action} ${userType}: ` +
            (error.message || "Unknown error")
        );
      }
    );
  }
}

// ============= REPORTING & ANALYTICS QUICK ACTIONS =============

function loadReports() {
  // Load legacy reports
  AjaxHelper.get(
    "/api/reports",
    function (data) {
      // Enrollment Statistics
      const enrollmentContainer = document.getElementById(
        "enrollment-report-container"
      );
      const enrollmentError = document.getElementById("enrollment-error");
      if (enrollmentContainer) {
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
      }
    },
    function (error) {
      console.error("Failed to load legacy reports:", error);
    }
  );

  // Load quick metrics
  loadQuickMetrics();
  loadRecentAlerts();
}

function loadQuickMetrics() {
  // Load dashboard data for quick metrics
  AjaxHelper.get(
    "/api/reports/dashboard",
    function (result) {
      if (result.status === "Success") {
        const data = result.data;

        // Update metrics
        const totalEnrollments =
          data.enrollmentStatistics?.reduce(
            (sum, course) => sum + course.filledSeats,
            0
          ) || 0;
        const activeFaculty = data.facultyWorkload?.length || 0;
        const highCapacityCount = data.highCapacityCourses?.length || 0;
        const avgUtilization =
          data.departmentAnalytics?.reduce(
            (sum, dept) => sum + dept.avgUtilization,
            0
          ) / (data.departmentAnalytics?.length || 1) || 0;

        // Update DOM elements
        updateMetric(
          "totalEnrollmentsMetric",
          totalEnrollments,
          "enrollmentTrend",
          "students enrolled"
        );
        updateMetric(
          "activeFacultyMetric",
          activeFaculty,
          "facultyWorkloadTrend",
          "faculty members"
        );
        updateMetric(
          "highCapacityMetric",
          highCapacityCount,
          "capacityTrend",
          "courses need attention"
        );
        updateMetric(
          "avgUtilizationMetric",
          `${avgUtilization.toFixed(1)}%`,
          "utilizationTrend",
          "average utilization"
        );
      }
    },
    function (error) {
      console.error("Failed to load quick metrics:", error);
    }
  );
}

function updateMetric(metricId, value, trendId, description) {
  const metricElement = document.getElementById(metricId);
  const trendElement = document.getElementById(trendId);

  if (metricElement) {
    metricElement.textContent = value;
  }

  if (trendElement) {
    trendElement.textContent = description;
  }
}

function loadRecentAlerts() {
  // Load recent high capacity alerts
  AjaxHelper.get(
    "/api/reports/high-capacity-courses?threshold=90",
    function (result) {
      if (result.status === "Success") {
        const alertsList = document.getElementById("alertsList");
        if (alertsList) {
          alertsList.innerHTML = "";

          if (result.data && result.data.length > 0) {
            // Show only top 3 most critical alerts
            const topAlerts = result.data.slice(0, 3);

            topAlerts.forEach((course) => {
              const alertDiv = document.createElement("div");
              alertDiv.style.cssText = `
                padding: 12px; 
                border: 1px solid #fecaca; 
                border-radius: 8px; 
                background: #fef2f2; 
                display: flex; 
                justify-content: space-between; 
                align-items: center;
              `;

              alertDiv.innerHTML = `
                <div>
                  <strong style="color: #dc2626;">${course.courseName}</strong>
                  <p style="margin: 4px 0 0 0; color: #7f1d1d; font-size: 14px;">
                    ${course.department} - ${course.utilizationPercentage}% capacity (${course.enrolledCount}/${course.capacity})
                  </p>
                </div>
                <div style="background: #dc2626; color: white; padding: 4px 8px; border-radius: 4px; font-size: 12px; font-weight: 600;">
                  ${course.status}
                </div>
              `;

              alertsList.appendChild(alertDiv);
            });
          } else {
            alertsList.innerHTML =
              '<p style="color: #10b981; font-style: italic;">✅ No high capacity alerts - all courses are within normal limits</p>';
          }
        }
      }
    },
    function (error) {
      console.error("Failed to load recent alerts:", error);
      const alertsList = document.getElementById("alertsList");
      if (alertsList) {
        alertsList.innerHTML =
          '<p style="color: #64748b; font-style: italic;">Failed to load alerts</p>';
      }
    }
  );
}

function generateQuickBusinessReport() {
  // Show loading state
  const alertsList = document.getElementById("alertsList");
  if (alertsList) {
    alertsList.innerHTML =
      '<p style="color: #64748b; font-style: italic;">🔄 Generating Business School report...</p>';
  }

  AjaxHelper.get(
    "/api/reports/business-school-capacity",
    function (result) {
      if (result.status === "Success") {
        const alertsList = document.getElementById("alertsList");
        if (alertsList) {
          alertsList.innerHTML = "";

          // Add summary header
          const summaryDiv = document.createElement("div");
          summaryDiv.style.cssText = `
            padding: 16px; 
            border: 2px solid #3b82f6; 
            border-radius: 8px; 
            background: #eff6ff; 
            margin-bottom: 12px;
          `;

          summaryDiv.innerHTML = `
            <h5 style="margin: 0 0 8px 0; color: #1e40af; display: flex; align-items: center; gap: 8px;">
              📊 Business School Report Summary
            </h5>
            <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(120px, 1fr)); gap: 12px; font-size: 14px;">
              <div><strong>Department:</strong> ${result.summary.department}</div>
              <div><strong>Courses Found:</strong> ${result.summary.totalCourses}</div>
              <div><strong>Threshold:</strong> ${result.summary.threshold}%</div>
              <div><strong>Avg Utilization:</strong> ${result.summary.averageUtilization}%</div>
            </div>
          `;

          alertsList.appendChild(summaryDiv);

          if (result.data && result.data.length > 0) {
            result.data.forEach((course) => {
              const courseDiv = document.createElement("div");
              courseDiv.style.cssText = `
                padding: 12px; 
                border: 1px solid #d1d5db; 
                border-radius: 8px; 
                background: white; 
                margin-bottom: 8px;
              `;

              courseDiv.innerHTML = `
                <div style="display: flex; justify-content: space-between; align-items: center;">
                  <div>
                    <strong style="color: #1e293b;">${
                      course.courseName
                    }</strong>
                    <p style="margin: 4px 0 0 0; color: #64748b; font-size: 14px;">
                      Instructor: ${course.instructor} | Enrolled: ${
                course.enrolledStudents
              }/${course.totalCapacity}
                    </p>
                  </div>
                  <div style="text-align: right;">
                    <div style="background: ${
                      course.utilizationPercentage >= 95 ? "#dc2626" : "#ea580c"
                    }; color: white; padding: 4px 8px; border-radius: 4px; font-size: 12px; font-weight: 600; margin-bottom: 4px;">
                      ${course.utilizationPercentage}%
                    </div>
                    <div style="color: #64748b; font-size: 12px;">${
                      course.status
                    }</div>
                  </div>
                </div>
              `;

              alertsList.appendChild(courseDiv);
            });
          } else {
            const noDataDiv = document.createElement("div");
            noDataDiv.innerHTML =
              '<p style="color: #10b981; font-style: italic;">✅ No Business school courses found above the capacity threshold</p>';
            alertsList.appendChild(noDataDiv);
          }
        }
      }
    },
    function (error) {
      console.error("Failed to generate business report:", error);
      const alertsList = document.getElementById("alertsList");
      if (alertsList) {
        alertsList.innerHTML =
          '<p style="color: #ef4444; font-style: italic;">❌ Failed to generate Business School report</p>';
      }
    }
  );
}

function generateHighCapacityAlert() {
  // Redirect to full dashboard with capacity focus
  window.location.href = "/reports#capacity";
}

function generateFacultyWorkloadReport() {
  // Show loading state
  const alertsList = document.getElementById("alertsList");
  if (alertsList) {
    alertsList.innerHTML =
      '<p style="color: #64748b; font-style: italic;">🔄 Loading faculty workload summary...</p>';
  }

  AjaxHelper.get(
    "/api/reports/faculty-workload",
    function (result) {
      if (result.status === "Success") {
        const alertsList = document.getElementById("alertsList");
        if (alertsList) {
          alertsList.innerHTML = "";

          // Add summary header
          const summaryDiv = document.createElement("div");
          summaryDiv.style.cssText = `
            padding: 16px; 
            border: 2px solid #f59e0b; 
            border-radius: 8px; 
            background: #fffbeb; 
            margin-bottom: 12px;
          `;

          const totalFaculty = result.data.length;
          const totalCourses = result.data.reduce(
            (sum, faculty) => sum + faculty.numberOfCourses,
            0
          );
          const totalStudents = result.data.reduce(
            (sum, faculty) => sum + faculty.totalEnrolledStudents,
            0
          );

          summaryDiv.innerHTML = `
            <h5 style="margin: 0 0 8px 0; color: #d97706; display: flex; align-items: center; gap: 8px;">
              👥 Faculty Workload Summary
            </h5>
            <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(120px, 1fr)); gap: 12px; font-size: 14px;">
              <div><strong>Total Faculty:</strong> ${totalFaculty}</div>
              <div><strong>Total Courses:</strong> ${totalCourses}</div>
              <div><strong>Total Students:</strong> ${totalStudents}</div>
              <div><strong>Avg Courses/Faculty:</strong> ${(
                totalCourses / totalFaculty
              ).toFixed(1)}</div>
            </div>
          `;

          alertsList.appendChild(summaryDiv);

          // Show top 5 faculty by workload
          const topFaculty = result.data
            .sort((a, b) => b.numberOfCourses - a.numberOfCourses)
            .slice(0, 5);

          topFaculty.forEach((faculty) => {
            const facultyDiv = document.createElement("div");
            facultyDiv.style.cssText = `
              padding: 12px; 
              border: 1px solid #d1d5db; 
              border-radius: 8px; 
              background: white; 
              margin-bottom: 8px;
            `;

            facultyDiv.innerHTML = `
              <div style="display: flex; justify-content: space-between; align-items: center;">
                <div>
                  <strong style="color: #1e293b;">${faculty.facultyName}</strong>
                  <p style="margin: 4px 0 0 0; color: #64748b; font-size: 14px;">
                    Department: ${faculty.department}
                  </p>
                </div>
                <div style="text-align: right; font-size: 14px;">
                  <div style="color: #1e293b; font-weight: 600;">${faculty.numberOfCourses} courses</div>
                  <div style="color: #64748b;">${faculty.totalEnrolledStudents} students</div>
                  <div style="color: #64748b; font-size: 12px;">Avg: ${faculty.avgStudentsPerCourse}/course</div>
                </div>
              </div>
            `;

            alertsList.appendChild(facultyDiv);
          });
        }
      }
    },
    function (error) {
      console.error("Failed to generate faculty workload report:", error);
      const alertsList = document.getElementById("alertsList");
      if (alertsList) {
        alertsList.innerHTML =
          '<p style="color: #ef4444; font-style: italic;">❌ Failed to generate faculty workload report</p>';
      }
    }
  );
}
