let departmentAddForm = document.getElementById('addDepartment')

departmentAddForm.addEventListener('submit', async(event) => {
    event.preventDefault();
    let response = await FormHelper.postJSON("/addDepartment",departmentAddForm);
    console.log('Full response from backend:', response);
})