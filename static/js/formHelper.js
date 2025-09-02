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
        const response = await fetch(url, {
            method: 'POST',
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(data)
        });
        const result = await response.json();
        console.log('Full backend response:', result);
        if (result.status === "success") {
            console.log('Department added successfully');
        } else {
            console.error('Error adding department:', result.message);
        }
        return result;
    }
}

