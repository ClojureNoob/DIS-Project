var mapdiv = document.getElementById('map');
var map = L.map(mapdiv).setView([42.3750997, -41.1056157], 2);

L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {attribution: 'Map data &copy; <a href="https://www.openstreetmap.org/">OpenStreetMap</a> contributors',
      maxZoom: 18,
    }).addTo(map);


var coordinates = JSON.parse(mapdiv.dataset.coordinates);
var names = mapdiv.dataset.names.split(',');
var symbols = mapdiv.dataset.symbols.split(',');


for (var i = 0; i < coordinates.length; i++) {
    var point = coordinates[i];
    var marker = L.marker([point[0], point[1]]).addTo(map);

    marker.on('click', function(e) {
        var point = e.target;
        var index = e.target.options.index;  // Add an index property to marker options

        var popup = L.popup()
          .setLatLng(point.getLatLng())
          .setContent('<b>Company:</b> ' + names[index])
          .openOn(map);
      });

      // Add an index property to marker options to store the index
      marker.options.index = i;
}



document.getElementById("parameterForm").addEventListener("submit", function(event) {
  event.preventDefault();

  // Retrieve selected parameter values
  var country = document.getElementById("country").value;
  var state = document.getElementById("state").value;
  var company = document.getElementById("company").value;
  var startDate = document.getElementById("startDate").value;
  var endDate = document.getElementById("endDate").value;

  // Use AJAX or fetch to send the form data to the server and process the response
  fetch("/query", {
    method: "POST",
    body: JSON.stringify({
      country: country,
      state: state,
      company: company,
      startDate: startDate,
      endDate: endDate,
    }),
    headers: {
      "Content-Type": "application/json"
    }
  })
    .then(response => response.json())
    .then(data => {
      // Update the relevant information based on the response data
      // Example: Update the starting and ending portfolio values
      document.getElementById("startValue").textContent = data.startValue;
      document.getElementById("endValue").textContent = data.endValue;
    })
    .catch(error => {
      console.log("An error occurred:", error);
    });
});


// Function to handle form changes
function handleFormChange() {
  // Retrieve selected parameter values
  var country = document.getElementById("country").value;
  var state = document.getElementById("state").value;
  var company = document.getElementById("company").value;
  var startDate = document.getElementById("startDate").value;
  var endDate = document.getElementById("endDate").value;

  // Create a FormData object and append the form data
  var formData = new FormData();
  formData.append("country", country);
  formData.append("state", state);
  formData.append("company", company);
  formData.append("startDate", startDate);
  formData.append("endDate", endDate);

  // Send a POST request to the server
  fetch("/update", {
    method: 'POST',
    body: formData
  })
    .then(function (response) {
      return response.json();
    })
    .then(function (data) {
      // Update the dropdown menus based on the server response
      updateDropdownMenu("country", data.countries);
      updateDropdownMenu("state", data.states);
      updateDropdownMenu("company", data.companies);
    })
    .catch(function (error) {
      console.error("Error:", error);
    });
}

// Function to update a dropdown menu with new options
function updateDropdownMenu(menuId, options) {
  var selectElement = document.getElementById(menuId);
  selectElement.innerHTML = ""; // Clear existing options

  // Add new options to the dropdown menu
  for (var i = 0; i < options.length; i++) {
    var option = options[i];
    var optionElement = document.createElement("option");
    optionElement.value = option.name;
    optionElement.textContent = option.name;

    if (option.chosen) {
      optionElement.classList.add("chosen-option");
      optionElement.selected = true;
    }

    selectElement.appendChild(optionElement);
  }
}


// Attach event listeners to the form elements
document.getElementById("country").addEventListener("change", handleFormChange);
document.getElementById("state").addEventListener("change", handleFormChange);
document.getElementById("company").addEventListener("change", handleFormChange);
document.getElementById("startDate").addEventListener("change", handleFormChange);
document.getElementById("endDate").addEventListener("change", handleFormChange);
