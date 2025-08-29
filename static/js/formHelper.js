// This class is made to assist with form data handling

class FormHelper{
    // Take form elements and convert it to a JSON object
    static formtoJSON(form){
        const data = {}
        new FormData(form).forEach((value,key) => {
            data[key] = value
        });
        return data;
    }

    // Send the JSON data to the server route
    static async postJSON(url,form){
        const data = FormHelper.formtoJSON(form);
        const response = await fetch(url,{method:'POST', headers:{"Content-Type": "application/JSON"} , body: JSON.stringify(data)});
        if (response) {
            console.log('Full backend response:', response);
            if (response.success) {
                console.log('User added successfully');
            } else {
                console.error('Error adding user');
            }
        } else {
            console.error('No response from backend');
        }
        return response.json();
    }
}

