// Example student data (this would normally come from Flask API)
const students = [
  { id: "ST2024001", name: "Alex Thompson", grade: "", status: "Pending" },
  { id: "ST2024002", name: "Sarah Wilson", grade: "", status: "Pending" }
];

function renderTable() {
  const tbody = document.getElementById("grade-body");
  tbody.innerHTML = "";

  students.forEach((student, index) => {
    const row = document.createElement("tr");

    row.innerHTML = `
      <td>${student.id}</td>
      <td>${student.name}</td>
      <td>
        <select onchange="updateGrade(${index}, this.value)">
          <option value="">Grade</option>
          <option value="A">A</option>
          <option value="B">B</option>
          <option value="C">C</option>
          <option value="D">D</option>
          <option value="F">F</option>
        </select>
      </td>
      <td><span class="status ${student.status.toLowerCase()}">${student.status}</span></td>
    `;

    tbody.appendChild(row);
  });
}

function updateGrade(index, grade) {
  students[index].grade = grade;
}

document.getElementById("submit-btn").addEventListener("click", () => {
  // In real app, this would POST to Flask REST API
  console.log("Submitting grades:", students);

  students.forEach(student => {
    if (student.grade !== "") {
      student.status = "Submitted";
    }
  });

  alert("Grades submitted successfully!");
  renderTable();
});

// Initial render
renderTable();
