let addCourseForm = document.getElementById("addCourse");

addCourseForm.addEventListener("submit", async (event) => {
  event.preventDefault();
  let response = await FormHelper.postJSON("/addCourse", addCourseForm);
  if (response && response.success) {
    console.log("User added successfully");
  } else {
    console.error("Error adding user");
  }
});
