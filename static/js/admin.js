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
