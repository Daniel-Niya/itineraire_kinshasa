// static/script.js

// Coordonnées exactes (lat, lon) — duplicata ici pour le front (optionnel: fetch du backend)
const COORDS = {
    "Rond-point Victoire": { lat: -4.340787, lon: 15.313731 },
    "Gare Centrale":       { lat: -4.301203, lon: 15.317859 }, 
    "Gombe":               { lat: -4.30306, lon: 15.30333 },
    "Lingwala":            { lat: -4.32028, lon: 15.29833 },
    "Kasa-Vubu":           { lat: -4.34250, lon: 15.30528 },
    "Matonge":             { lat: -4.34022, lon: 15.31599 },
    "Barumbu":             { lat: -4.31694, lon: 15.32778 },
    "Ngaliema":            { lat: -4.37247, lon: 15.25459 },
    "Lemba":               { lat: -4.39611, lon: 15.31917 },
    "Limete":              { lat: -4.37439, lon: 15.34542 }
  };
  
  // initial view center: entre Victoire et Gare
  const center = [-4.320, 15.311];
  const map = L.map('map').setView(center, 13);
  
  L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    maxZoom: 19,
    attribution: '&copy; OpenStreetMap contributors'
  }).addTo(map);
  
  let routeLayers = []; // stocker les polylines pour suppression
  const colors = ['#2b83ba','#d7191c','#1a9641','#fdae61']; // couleurs pour itinéraires
  
  // UI éléments
  const startSelect = document.getElementById('startSelect');
  const endSelect = document.getElementById('endSelect');
  const calcBtn = document.getElementById('calcBtn');
  const swapBtn = document.getElementById('swapBtn');
  const routesInfo = document.getElementById('routesInfo');
  
  calcBtn.addEventListener('click', () => {
    const startName = startSelect.value;
    const endName = endSelect.value;
    loadRoutesByNames(startName, endName, 3);
  });
  
  swapBtn.addEventListener('click', () => {
    const tmp = startSelect.value;
    startSelect.value = endSelect.value;
    endSelect.value = tmp;
  });
  
  // Au chargement, afficher automatiquement les 3 itinéraires Victoire -> Gare Centrale
  document.addEventListener('DOMContentLoaded', () => {
    loadRoutesByNames('Rond-point Victoire', 'Gare Centrale', 3);
  });
  
  function clearRoutes() {
    routeLayers.forEach(layer => {
      if (map.hasLayer(layer)) map.removeLayer(layer);
    });
    routeLayers = [];
    routesInfo.innerHTML = '';
  }
  
  async function loadRoutesByNames(startName, endName, alternatives=3) {
    const start = COORDS[startName];
    const end = COORDS[endName];
    if (!start || !end) {
      alert('Coordonnées manquantes pour le point choisi.');
      return;
    }
    await loadRoutes(start, end, startName, endName, alternatives);
  }
  
  async function loadRoutes(start, end, startName='', endName='', alternatives=3) {
    clearRoutes();
  
    routesInfo.innerHTML = '<div class="alert alert-info">Calcul des itinéraires...</div>';
  
    try {
      const resp = await fetch('/api/routes', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          start: { lat: start.lat, lon: start.lon },
          end: { lat: end.lat, lon: end.lon },
          alternatives: alternatives
        })
      });
  
      const data = await resp.json();
      if (!resp.ok) {
        routesInfo.innerHTML = `<div class="alert alert-danger">Erreur: ${data.error || resp.statusText}</div>`;
        return;
      }
  
      if (!data.routes || data.routes.length === 0) {
        routesInfo.innerHTML = '<div class="alert alert-warning">Aucun itinéraire trouvé.</div>';
        return;
      }
  
      // Tracer chaque itinéraire
      const bounds = [];
      data.routes.forEach((r, idx) => {
        // geometry coordinates are array of [lon, lat]
        const coords = r.geometry.coordinates.map(c => [c[1], c[0]]);
        const poly = L.polyline(coords, {
          color: colors[idx % colors.length],
          weight: (idx === data.shortest_index ? 6 : 4),
          opacity: (idx === data.shortest_index ? 0.95 : 0.7),
          dashArray: (idx === data.shortest_index ? null : '6,8')
        }).addTo(map);
        routeLayers.push(poly);
        bounds.push(poly.getBounds());
  
        // popup summary
        poly.bindPopup(`<b>Itinéraire ${idx+1}</b><br>Distance: ${r.distance_km} km<br>Durée: ${r.duration_min} min`);
  
        // ajouter un marqueur au départ pour le premier route seulement
        if (idx === 0) {
          const startMarker = L.marker([start.lat, start.lon]).addTo(map).bindPopup("Départ: " + (startName || ''));
          const endMarker = L.marker([end.lat, end.lon]).addTo(map).bindPopup("Arrivée: " + (endName || ''));
          routeLayers.push(startMarker, endMarker);
        }
      });
  
      // ajuster la vue
      if (bounds.length) {
        const groupBounds = bounds.reduce((acc, b) => acc ? acc.extend(b) : b, null);
        if (groupBounds) map.fitBounds(groupBounds.pad(0.2));
      }
  
      // afficher résumé dans le sidebar
      let html = '';
      data.routes.forEach((r, idx) => {
        const isBest = idx === data.shortest_index;
        html += `
          <div class="card mb-2 ${isBest ? 'border-danger' : ''}">
            <div class="card-body p-2">
              <div class="d-flex justify-content-between">
                <div><strong>Itinéraire ${idx+1}</strong> ${isBest ? '<span class="badge bg-danger ms-2">Plus court</span>' : ''}</div>
                <div><small>${r.distance_km} km • ${r.duration_min} min</small></div>
              </div>
              <div class="mt-1">
                <button class="btn btn-sm btn-outline-primary" onclick="zoomToRoute(${idx})">Zoom</button>
              </div>
            </div>
          </div>
        `;
      });
      routesInfo.innerHTML = html;
  
    } catch (e) {
      routesInfo.innerHTML = `<div class="alert alert-danger">Erreur réseau: ${e.message}</div>`;
    }
  }
  
  function zoomToRoute(index) {
    const layer = routeLayers[index]; // note: routeLayers contains polylines then markers; ordering: poly0, poly1, ...
    if (!layer) return;
    map.fitBounds(layer.getBounds().pad(0.2));
  }
  