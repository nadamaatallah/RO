document.addEventListener('DOMContentLoaded', function() {
    // Initialiser la carte (par exemple, avec Leaflet.js)
    var map = L.map('map').setView([51.505, -0.09], 13);
    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png').addTo(map);

    // Soumettre le formulaire
    document.getElementById('route-form').addEventListener('submit', function(event) {
        event.preventDefault();
        var formData = new FormData(this);
        fetch('/optimize_route', {
            method: 'POST',
            body: formData
        })
        .then(response => response.json())
        .then(data => {
            // Afficher les résultats sur la page
            document.getElementById('result').innerHTML = `
                <p>Chemin le plus court: ${data.shortest_path}</p>
                <p>Longueur du chemin le plus court: ${data.shortest_path_length}</p>
            `;
        })
        .catch(error => console.error('Erreur:', error));
    });
});
