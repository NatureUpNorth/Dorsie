const latlon = document.getElementById("latlon");
const resultsSidebar = document.getElementById("resultsSidebar");
var map = L.map('map').setView([44.597, -75.168], 10);

L.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png', {
    maxZoom: 19,
    attribution: '&copy; <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a>'
}).addTo(map);

var marker = L.marker();
var lat;
var lan;
var currentSearchResults = [];
var selectedResultIndex = -1;

// Nominatim Search Bar Setup
function searchAddress() {
    const searchInput = document.getElementById("searchInput").value;

    if (searchInput.trim() === "") {
        alert("Please enter an address");
        return;
    }

    // Clear previous search status
    let check = document.getElementById("check");
    check.textContent = '';
    let save = document.getElementById("save");
    save.textContent = " not saved";
    save.style.color = "black";

    // Call Nominatim API
    fetch('https://nominatim.openstreetmap.org/search?format=json&q=' + encodeURIComponent(searchInput) + '&limit=8')
        .then(response => response.json())
        .then(data => {
            if (data && data.length > 0) {
                // Store results
                currentSearchResults = data;
                selectedResultIndex = -1;

                // Display results in sidebar
                displaySearchResults(data);

                // Auto-zoom to first result bounds
                const firstResult = data[0];
                const bounds = [
                    [parseFloat(firstResult.boundingbox[0]), parseFloat(firstResult.boundingbox[2])],
                    [parseFloat(firstResult.boundingbox[1]), parseFloat(firstResult.boundingbox[3])]
                ];
                map.fitBounds(bounds);
            } else {
                alert("Address not found. Please try another search.");
                resultsSidebar.classList.remove('active');
                resultsSidebar.innerHTML = '';
            }
        })
        .catch(error => {
            console.error('Error:', error);
            alert("Error searching address. Please try again.");
        });
}

// Display search results in sidebar
function displaySearchResults(results) {
    resultsSidebar.innerHTML = '';
    resultsSidebar.classList.add('active');

    results.forEach((result, index) => {
        const resultItem = document.createElement('div');
        resultItem.className = 'result-item';
        resultItem.innerHTML = `
            <div class="result-name">${result.name}</div>
            <div class="result-address">${result.display_name}</div>
        `;
        resultItem.addEventListener('click', () => selectResult(index, result));
        resultsSidebar.appendChild(resultItem);
    });
}

// Handle result selection
function selectResult(index, result) {
    const latitude = parseFloat(result.lat);
    const longitude = parseFloat(result.lon);

    // Update selected state
    selectedResultIndex = index;
    updateSelectedResultUI();

     // Update map view
    map.setView([latitude, longitude], 14);

    // Update marker
    marker.setLatLng([latitude, longitude]);
    marker.addTo(map);

    // Update coordinates
    lat = latitude;
    lan = longitude;
    latlon.textContent = 'Latitude: ' + latitude.toString() + ' Longitude: ' + longitude.toString();

    // Clear unsaved status
    let check = document.getElementById("check");
    check.textContent = '';
    let save = document.getElementById("save");
    save.textContent = " not saved";
    save.style.color = "black";
}

// Update UI to show selected result
function updateSelectedResultUI() {
    const resultItems = resultsSidebar.querySelectorAll('.result-item');
    resultItems.forEach((item, index) => {
        if (index === selectedResultIndex) {
            item.classList.add('selected');
        } else {
            item.classList.remove('selected');
        }
    });
}

// Allow Enter key to trigger search (no longer moves marker automatically)
document.getElementById("searchInput").addEventListener('keypress', function(event) {
    if (event.key === 'Enter') {
        event.preventDefault(); // prevent form submit on enter
        searchAddress();
    }
});

function onMapClick(e) {
    // new coordinates not yet saved
    let check = document.getElementById("check");
    check.textContent = '';
    let save = document.getElementById("save");
    save.textContent = " not saved";
    save.style.color = "black";

    marker.setLatLng(e.latlng);
    marker.addTo(map);
    lat = e.latlng.lat;
    lan = e.latlng.lng;
    latlon.textContent = 'Latitude: ' + e.latlng.lat.toString() + ' Longitude: ' + e.latlng.lng.toString();

    // Clear search input when clicking map
    document.getElementById("searchInput").value = '';

    // Close results sidebar and clear selection
    resultsSidebar.classList.remove('active');
    resultsSidebar.innerHTML = '';
    selectedResultIndex = -1;
    currentSearchResults = [];
}

var button = document.getElementById('saveCoordinates');

// show green check and "saved"
function saveLocation() {
    let check = document.getElementById("check");
    check.textContent = '✓';
    let save = document.getElementById("save");
    save.textContent = "saved";
    save.style.color = "green";

    // Set hidden HTML inputs for backup form submission
    document.getElementById("latitude_input").value = lat;
    document.getElementById("longitude_input").value = lan;

    // Using Fetch API
    fetch('/save_coordinates', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ latitude: lat, longitude: lan})
    })
    .then(response => response.json())
    .then(data => console.log(data))
    .catch(error => console.error('Error:', error));
}

map.on('click', onMapClick);
button.addEventListener('click', saveLocation);
