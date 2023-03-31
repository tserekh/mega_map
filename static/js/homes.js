function getHomes() {
  const homesCheckbox = document.getElementById("homes");
  if (homesCheckbox.checked) {
    homesCheckbox.disabled = true;
    $.get(homeUrl, paramDic).then((response) => {
      const features = getHomeFeatures(response.homes);
      const source = new ol.source.Vector({
        features: features,
        wrapX: false
      });
      homeLayer.setSource(source);
      map.addLayer(homeLayer);
      homesCheckbox.disabled = false;
    });
  } else {
    map.removeLayer(homeLayer);
  }
}

function getHomeFeatures(data) {
  const features = [];
  data.forEach((item) => {
    const point = [item.x, item.y];
    const geom = new ol.geom.Point(point);
    const flatNum = Math.round(2.7 * item.flat_num);
    const feature = new ol.Feature({
      geometry: geom,
      radius: 10,
      info: `Жителей: ${flatNum}<br/>${item.chain_name}`,
      chain_name: item.chain_name,
      name: nFormatter(flatNum),
      min_distance: parseFloat(item.min_distance),
      min_distance_metro: item.min_distance_metro
    });
    feature.setStyle(computeHomeStyle(feature));
    features.push(feature);
  });
  return features;
}

function computeHomeStyle(feature) {
  const fill_color = "green";
  const name = feature.get("name");
  const chain_name = feature.get("chain_name");
  const stroke = null;

  const styleDic = {
    image: new ol.style.Circle({
      radius: 7 + name.toString().length,
      fill: new ol.style.Fill({
        color: fill_color
      })
    }),
    text: new ol.style.Text({
      font: "10px helvetica,sans-serif",
      text: `${name}${chain_name}`,
      fill: new ol.style.Fill({
        color: "white"
      }),
      stroke: stroke
    })
  };
  return new ol.style.Style(styleDic);
}