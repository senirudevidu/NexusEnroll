let addDegreeForm = document.getElementById("addDegree");

addDegreeForm.addEventListener("submit", async function(event) {
    event.preventDefault(); // Prevent the default form submission
    let response = await FormHelper.postJSON('/addDegree', addDegreeForm);
});
