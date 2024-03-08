
function showButtons() {
    var processSelect = document.getElementById("processSelect");
    var selectedProcess = processSelect.options[processSelect.selectedIndex].value;
    var exportExcelButton = document.querySelector(".export-excel-button");
    var runButton = document.querySelector(".run-button");

    if (selectedProcess === "extraido") {
        exportExcelButton.style.display = "block"; // Show export button for devolution
        runButton.style.display = "block"; // Show run button for devolution
    } else if (selectedProcess === "termianado") {
        exportExcelButton.style.display = "none"; // Hide export button for rendimientos
        runButton.style.display = "block"; // Show run button for rendimientos
    } else {
        exportExcelButton.style.display = "none"; // Hide export button for other processes
        runButton.style.display = "none"; // Hide run button for other processes
    }

    // Hide the form fields when changing the process selection
    document.getElementById("credentialsFormFields").style.display = "none";
}


function toggleCredentials() {
    var credentialsFormFields = document.getElementById("credentialsFormFields");
    if (credentialsFormFields.style.display === "none") {
        credentialsFormFields.style.display = "block";
    } else {
        credentialsFormFields.style.display = "none";
    }
}

function submitCredentials(event) {
    event.preventDefault();
    var credentialsButton = document.querySelector(".credentials-button");
    var submitCredentialsButton = document.getElementById("submitCredentialsButton");
    var credentialsFormFields = document.getElementById("credentialsFormFields");
    credentialsFormFields.style.display = "none"
    // Perform form submission handling here
    
    // Change color and text of the button to indicate saved
    credentialsButton.style.backgroundColor = "green";
    credentialsButton.innerText = "Credentials Saved";
}

function run(operation) {
    var processSelect = document.getElementById("processSelect");
    var selectedProcess = processSelect.options[processSelect.selectedIndex].value;

    // Retrieve username, password, and frequency from the form fields
    var username = document.getElementById("username").value;
    var password = document.getElementById("password").value;
    var frequency = document.getElementById("frequency").value;
    
    // Send the appropriate parameter based on the selected process type
    if (operation === 'export') {
        // Call the API and wait for it to complete
        callAPI(username, password, 'export', frequency, selectedProcess)
        .then(response => {
            // Check if the API call was successful
            if (response.ok) {
                // If the API call was successful, submit the download form
                document.getElementById("downloadForm").submit();
            } else {
                // If the API call was not successful, log an error
                console.error('API request failed:', response.statusText);
            }
        })
        .catch(error => {
            // Handle any errors that occur during the API call
            console.error('Error:', error);
        });
    } else if (operation === 'run') {
        // For 'run' operation, simply call the API without waiting for completion
        callAPI(username,password, 'run', frequency, selectedProcess)
    }
}


function callAPI(username,password,operation,frequency, processType) {
    console.log(processType, operation);
    
    // Construct the URL for your API endpoint
    const apiUrl = 'http://localhost:5000';

    // Prepare the request body
    const requestBody = {
        processType: processType,
        operation: operation,
        username: username,
        password: password,
        frequency: frequency,
    };

    // Check if the operation is 'export'
    if (operation === 'export') {
        // If it's 'export', wait for the result
        return fetch(apiUrl, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(requestBody),
        });
    } else {
        // If it's not 'export', don't wait for the result
        // Return a resolved Promise
        return Promise.resolve();
    }
}

