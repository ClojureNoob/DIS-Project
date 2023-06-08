var mapdiv = document.getElementById('map');
var map = L.map(mapdiv).setView([42.3750997, -41.1056157], 2);

L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
  attribution: 'Map data &copy; <a href="https://www.openstreetmap.org/">OpenStreetMap</a> contributors',
  maxZoom: 18,
}).addTo(map);

console.log(mapdiv.dataset.coordinates);

var coordinates = JSON.parse(mapdiv.dataset.coordinates);
var names = mapdiv.dataset.names;


for (var i = 0; i < coordinates.length; i++) {
  var point = coordinates[i];
  var marker = L.marker([point[0], point[1]]).addTo(map);

  marker.on('click', function(e) {
    var point = e.target;
    var index = e.target.options.index;

    var popup = L.popup()
      .setLatLng(point.getLatLng())
      .setContent('<b>Company:</b> ' + names[index])
      .openOn(map);
  });

  marker.options.index = i;
}

// This code implements the time period slider, and updates the page when a new range is chosen

const slider = document.getElementById('slider');
const startDot = document.createElement('div');
const endDot = document.createElement('div');

startDot.classList.add('dot');
startDot.id = 'startDot';
startDot.style.left = '0%';

endDot.classList.add('dot');
endDot.id = 'endDot';
endDot.style.left = '100%';

slider.parentNode.insertBefore(startDot, slider);
slider.parentNode.insertBefore(endDot, slider);

slider.addEventListener('input', function() {
  const range = this.max - this.min;
  const left = ((this.value - this.min) / range) * 100 + '%';
  const dot = this.id === 'slider' ? 'startDot' : 'endDot';
  document.getElementById(dot).style.left = left;
});


// Updating of values
document.getElementById("slider").addEventListener("input", function() {
    document.getElementById("sliderValue").textContent = this.value;
});

document.getElementById("parameterForm").addEventListener("submit", function(event) {
    event.preventDefault();
  
    // Retrieve selected parameter values
    var country = document.getElementById("country").value;
    var state = document.getElementById("state").value;
    var company = document.getElementById("company").value;
    var startDate = document.getElementById("startDate").value;
    var endDate = document.getElementById("endDate").value;
    var timeFrame = document.getElementById("slider").value;
  
    // Perform necessary calculations and update the displayed values
  
    // Example: Update the starting and ending portfolio values
    document.getElementById("startValue").textContent = "1000";
    document.getElementById("endValue").textContent = "1200";
  
    // Use AJAX or fetch to send the form data to the server and process the response
    // Example using fetch:
    fetch("/api/endpoint", {
      method: "POST",
      body: JSON.stringify({
        country: country,
        state: state,
        company: company,
        startDate: startDate,
        endDate: endDate,
        timeFrame: timeFrame
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
})})
