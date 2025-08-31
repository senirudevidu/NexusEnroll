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
      if (
        Array.isArray(data.faculty_workload) &&
        data.faculty_workload.length > 0
      ) {
        facultyError.style.display = "none";
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
        facultyError.style.display = "block";
      }
    },
    function (error) {
      document.getElementById("enrollment-error").style.display = "block";
      document.getElementById("faculty-error").style.display = "block";
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
