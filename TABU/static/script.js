let ciudades = [];
let markers = [];
let rutaPolyline = null;

const map = L.map('map').setView([0, 0], 2);
L.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png').addTo(map);

map.on('click', e => {
  const latlng = [e.latlng.lat, e.latlng.lng];
  ciudades.push(latlng);
  const marker = L.marker(latlng).addTo(map);
  markers.push(marker);
});

function resolver() {
  if (ciudades.length < 3) {
    alert("Agrega al menos 3 ciudades.");
    return;
  }

  fetch('/api/tabu', {
    method: 'POST',
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify({
      ciudades: ciudades,
      iteraciones: document.getElementById('iteraciones').value,
      memoria: document.getElementById('memoria').value
    })
  })
  .then(res => res.json())
  .then(data => {
    const ruta = data.ruta.map(i => ciudades[i]);
    ruta.push(ruta[0]);  // Cerrar el ciclo

    if (rutaPolyline) map.removeLayer(rutaPolyline);
    rutaPolyline = L.polyline(ruta, {color: 'yellow', weight: 4}).addTo(map);

    document.getElementById('resultado').innerText = `Ruta óptima encontrada con distancia total: ${data.distancia}`;
  });
}
