function getRouteSource(lines, shortRouteNames, totalWeight, info) {
  const geojsonObject = {
    type: 'FeatureCollection',
    features: [
      {
        type: 'Feature',
        properties: {
          info: `${Math.round(totalWeight)} минут<br>${info}`,
        },
        geometry: {
          type: 'LineString',
          coordinates: lines,
        },
      },
    ],
  };
  const features = new ol.format.GeoJSON().readFeatures(geojsonObject);
  return new ol.source.Vector({ features });
}

function getRouteLayer(lineSource, color) {
  const linestyle = new ol.style.Style({
    stroke: new ol.style.Stroke({
      color,
      width: 5,
      opacity: 0.5,
    }),
  });
  return new ol.layer.Vector({
    source: lineSource,
    style: linestyle,
  });
}

function getRoute() {
  const addressFrom = document.getElementById('searchAddressFrom').value;
  const addressTo = document.getElementById('searchAddressTo').value;
  const paramDic = { address_from: addressFrom, address_to: addressTo };
  $.get(routeUrl, paramDic).then(response => {
    const shortestPathCoords = response.route.shortest_path_coords;
    const shortRouteNames = response.route.short_route_names;
    const totalWeight = response.route.total_weight;
    const info = response.route.info;
    const colors = ['red', 'green', 'blue'];
    for (let i = 0; i < shortestPathCoords.length; i++) {
      const linesSource = getRouteSource(shortestPathCoords[i], shortRouteNames, totalWeight, info);
      const lineLayer = getRouteLayer(linesSource, colors[i % 3]);
      map.addLayer(lineLayer);
    }
  });
}

function updateRoute() {
  if (document.getElementById('route').checked) {
    document.getElementById('route').disabled = true;
    getRoute();
    document.getElementById('route').disabled = false;
  }
}