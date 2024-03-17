
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

    } else if (selectedProcess === "rendimientos") {
        exportExcelButton.style.display = "block"; // Show export button for devolution
        runButton.style.display = "block"; // Show run button for devolution

    } else if (selectedProcess === "controlPreparacion") {
        exportExcelButton.style.display = "none"; // Hide export button for rendimientos
        runButton.style.display = "block"; // Show run button for rendimientos

    } else if (selectedProcess === "devolucionTienda") {
        exportExcelButton.style.display = "block"; // Hide export button for rendimientos
        runButton.style.display = "none"; // Show run button for rendimientos

    } else {
        exportExcelButton.style.display = "none"; // Hide export button for other processes
        runButton.style.display = "none"; // Hide run button for other processes
    }

    // Hide the form fields when changing the process selection
    document.getElementById("credentialsFormFields").style.display = "none";
}

function populateProcesses() {
    var systemSelect = document.getElementById("systemSelect");
    var processSelect = document.getElementById("processSelect");

    var selectedSystem = systemSelect.value;

    // Clear previous options
    processSelect.innerHTML = "";

    // Populate options based on selected system
    if (selectedSystem === "sislog") {
        var options = ["extraido", "termianado", "rendimientos", "controlPreparacion"];
    } else if (selectedSystem === "sage") {
        var options = ["devolucionTienda",]; // Add options for Sage system
    }

    // Add options to processSelect
    options.forEach(function(option) {
        var optionElement = document.createElement("option");
        optionElement.value = option;
        if(option === "extraido"){
            optionElement.textContent = "Extraido";
        }
        if(option === "termianado"){
            optionElement.textContent = "Termianado";
        }
        if(option === "rendimientos"){
            optionElement.textContent = "Rendimientos";
        }
        if(option === "controlPreparacion"){
            optionElement.textContent = "Control de Preparacion";
        }
        if(option === "devolucionTienda"){
            optionElement.textContent = "Devolucion de Tienda";
        }
        processSelect.appendChild(optionElement);
    });

    // Show buttons and form fields
    showButtons();
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
    } else if (operation === 'run') {
        // For 'run' operation, simply call the API without waiting for completion
        callAPI(username,password, 'run', frequency, selectedProcess)
    }
}


function callAPI(username,password,operation,frequency, processType) {
    console.log(processType, operation);

    // Prepare the request body
    const requestBody = {
        processType: processType,
        operation: operation,
        username: username,
        password: password,
        frequency: frequency,
    };
    console.log(JSON.stringify(requestBody));

    var xhr = new XMLHttpRequest();
    xhr.open('POST', '/run-process', true);
    xhr.setRequestHeader('Content-Type', 'application/json');
    xhr.send(JSON.stringify(requestBody));



    // Check if the operation is 'export'
    if (operation === 'export') {
        xhr.onload = function () {
            if (xhr.status >= 200 && xhr.status < 300) {
                // Resolve the promise with the response text (or JSON if preferred)
                resolve(xhr.response);
            } 
        };
    } 
}

function toggleFullscreen() {
    var elem = document.getElementById("selenium_iframe");

    if (!document.fullscreenElement && !document.mozFullScreenElement &&
        !document.webkitFullscreenElement && !document.msFullscreenElement) {
        if (elem.requestFullscreen) {
            elem.requestFullscreen();
        } else if (elem.msRequestFullscreen) {
            elem.msRequestFullscreen();
        } else if (elem.mozRequestFullScreen) { // Note the capital 'S' in 'Screen'
            elem.mozRequestFullScreen();
        } else if (elem.webkitRequestFullscreen) {
            elem.webkitRequestFullscreen();
        }
    } else {
        if (document.exitFullscreen) {
            document.exitFullscreen();
        } else if (document.msExitFullscreen) {
            document.msExitFullscreen();
        } else if (document.mozCancelFullScreen) { // Note the capital 'S' in 'Screen'
            document.mozCancelFullScreen();
        } else if (document.webkitExitFullscreen) {
            document.webkitExitFullscreen();
        }
    }
}
