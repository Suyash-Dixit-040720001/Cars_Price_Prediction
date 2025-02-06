document.getElementById('analyzeButton').addEventListener('click', function(event) {
    event.preventDefault();  // Prevent the form from submitting the traditional way

    // Define mappings for each dropdown field
    const trimMapping = {
        "Limited" : 600,
        "Sport" : 500,
        "SE" : 400,
        "Base" : 300
    }
    const transmissionMapping = {
        "Automatic": 1, 
        "Manual": 0      
    };

    const engineMapping = {
        "V6 Cylinder Engine": 1200,
        "V4 Cylinder Engine": 800,
        "3.5L Four Cylinder Engine": 600,
        "2.5L Four Cylinder Engine": 500,
        "2L Four Cylinder Engine": 400
    };

    const drivetrainMapping = {
        "All-Wheel Drive": 2100,
        "Front-Wheel Drive": 4800,
        "Rear-Wheel Drive": 1800
    };

    const conditionMapping = {
        "Used": 8000,
        "Certified Pre Owned": 200,
        "New": 150
    };

    const bodyStyleMapping = {
        "Sedan": 3358,
        "SUV": 3236,
        "Coupe": 596,
        "Pickup_Truck": 552,
        "Pickup": 453,
        "Convertible": 422,
        "Hatchback": 340,
        "Wagon": 138,
        "MiniVan": 118,
        "Van": 103
    };

    const locationMapping = {
        "SF": 3412,
        "LA": 3072,
        "Austin": 2832
    };

    const interiorColorMapping = {
        "Gray": 800,
        "Black": 700,
        "Tan": 600,
        "Brown": 600,
        "Red": 800,
        "Ceramic": 500,
        "Silver": 650,
        "Yellow": 300,
        "Beige": 800,
        "Cognac": 900
    };

    const exteriorColorMapping = {
        "Gray": 800,
        "Black": 2000,
        "White": 1400,
        "Brown": 700,
        "Red": 600,
        "Clearcoat": 632,
        "Silver": 700,
        "Yellow": 180,
        "Green": 200,
        "Pink": 205
    };

    // Get the selected values and convert them to numeric values using the mappings
    const trim = document.getElementById('trim').value;  // Send the string value for trim
    const transmission = document.getElementById('transmission').value;  // Send the string value for transmission
    const engine = document.getElementById('engine').value;
    const drivetrain = document.getElementById('drivetrain').value;
    const condition = document.getElementById('condition').value;
    const bodyStyle = document.getElementById('bodyStyle').value;
    const location = document.getElementById('location').value;
    const interiorColor = document.getElementById('interiorColor').value;
    const exteriorColor = document.getElementById('exteriorColor').value;
    const mileage = parseFloat(document.getElementById('mileage').value);

    // Create the formData object
    const formData = {
        trim : trim,  // Now send the string value for trim
        transmission: transmission,  // Now send the string value for transmission
        engine: engine,
        drivetrain: drivetrain,
        condition: condition,
        bodyStyle: bodyStyle,
        location: location,
        interiorColor: interiorColor,
        exteriorColor: exteriorColor,
        mileage: mileage
    };

    // Log the formData to check if it's correct
    console.log("Form Data:", formData);

    // Send the data to the Flask backend for prediction
    fetch('/prediction', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'  // Ensure this header is set
        },
        body: JSON.stringify(formData)  // Convert the data to JSON
    })
    .then(response => response.json())
    .then(data => {
        console.log("Prediction Response:", data.prediction);
        document.getElementById("resultText").innerText = `Predicted Price: $${data.prediction}`;
    })
    .catch(error => {
        console.error("Error:", error);
        document.getElementById("resultText").innerText = "Error in prediction. Please try again.";
    });
});
