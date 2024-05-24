document.addEventListener('DOMContentLoaded', function() {
    var map = L.map('map').setView([51.505, -0.09], 13);
    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png').addTo(map);

    var marker = L.marker([51.50735, -0.12776]).addTo(map);

    map.on('click', function (e) {
        var newMarker = L.marker(e.latlng).addTo(map);
        var algorithm = document.getElementById('algorithm').value;
        $.ajax({
            type: 'POST',
            url: '/optimize_route',
            contentType: 'application/json',
            data: JSON.stringify({ source: marker.getLatLng(), target: e.latlng, algorithm: algorithm }),
            success: function(response) {
                if (response.error) {
                    console.error(response.error);
                } else {
                    document.getElementById('result').innerHTML = `
                        <p>Chemin le plus court: ${response.shortest_path}</p>
                        <p>Longueur du chemin le plus court: ${response.shortest_path_length}</p>
                    `;
                }
            },
            error: function(xhr, status, error) {
                console.error('Error:', error);
            }
        });
    });
});
