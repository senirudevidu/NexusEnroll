// Include FormHelper.js before this script in HTML
let addUserForm = document.getElementById('addUserForm');

addUserForm.addEventListener('submit', async (event) => {

    let module = document.getElementById('module').value;  
    let response; // declare here to use later

    if(module === 'student') {
        response = await FormHelper.postJSON('/addStudent', addUserForm);
    } else if(module === 'admin') {
        response = await FormHelper.postJSON('/addAdmin', addUserForm);
    } else if(module === 'faculty') {
        response = await FormHelper.postJSON('/addFacultyMember', addUserForm);
    }

    if (response && response.success) {
        console.log('User added successfully');
    } else {
        console.error('Error adding user');
    }
});
