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
  }
}

function loadCourses() {
  AjaxHelper.get(
    "/api/courses",
    function (courses) {
      const tbody = document.getElementById("course-table-body");
      tbody.innerHTML = "";
      courses.forEach((course) => {
        // Adjust indices based on your course tuple structure
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
