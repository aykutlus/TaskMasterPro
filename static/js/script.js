
function showButtons() {
    var processSelect = document.getElementById("processSelect");
    var selectedProcess = processSelect.options[processSelect.selectedIndex].value;
    var exportExcelButton = document.querySelector(".export-excel-button");
    var runButton = document.querySelector(".run-button");

    if (selectedProcess === "devolution") {
        exportExcelButton.style.display = "block"; // Show export button for devolution
        runButton.style.display = "block"; // Show run button for devolution
    } else if (selectedProcess === "rendimientos") {
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