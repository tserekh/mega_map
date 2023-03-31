function nFormatter(num, digits) {
  var si = [
    { value: 1, symbol: "" },
    { value: 1E3, symbol: "k" },
    { value: 1E6, symbol: "M" },
    { value: 1E9, symbol: "G" },
    { value: 1E12, symbol: "T" },
    { value: 1E15, symbol: "P" },
    { value: 1E18, symbol: "E" }
  ];
  var rx = /\.0+$|(\.[0-9]*[1-9])0+$/;
  var i;
  for (i = si.length - 1; i > 0; i--) {
    if (num >= si[i].value) {
      break;
    }
  }
  return (num / si[i].value).toFixed(digits).replace(rx, "$1") + si[i].symbol;
}

function computeRouteStyle(color) {
  var lineStyle = new ol.style.Style({
    stroke: new ol.style.Stroke({
      color: "blue",
      width: 3,
      opacity: 0.5
    })
  });
  return lineStyle;
}

function getMetroFeatures(data) {
  var features = [];
  for (var i = 0; i < data.length; ++i) {
    var point = [data[i]["lon"], data[i]["lat"]];
    point = ol.proj.fromLonLat(point);
    var geom = new ol.geom.Point(point);
    var info = data[i]["exit_name"] !== undefined ? data[i]["exit_name"] : data[i]["station_name"];
    var feature = new ol.Feature({
      "geometry": geom,
      "radius": 10,
      "info": "<br/>" + info,
      "name": ""
    });
    feature.setStyle(compute_metro_style(feature));
    features.push(feature);
  }
  return features;
}

function getMetroLayer(features) {
  var vectorSource = new ol.source.Vector({
    "features": features,
    "wrapX": false
  });
  return new ol.layer.Vector({
    "source": vectorSource
  });
}

function computeOperSquareStyle(feature) {
  var perc = feature.get("result_rate");
  perc = Math.min(1, perc);
  var color = colorFunc(perc);
  color.push(0.5);
  return new ol.style.Style({
    "fill": new ol.style.Fill({
      "color": color
    })
  });
}

function balance(x, y) {
  const elemX = document.getElementById(x);
  const elemY = document.getElementById(y);

  if (!elemX.checked && !elemY.checked) {
    elemX.checked = true;
    elemY.checked = true;
  }
}

function backBar() {
  document.getElementById("select_bar").style.display = "block";
  document.getElementById("describe_bar").style.display = "none";
}

function curtailBar() {
  const curtailBarElem = document.getElementById("curtail_bar");
  if (curtailBarElem.style.opacity === "1") {
    $(document.getElementById('bar')).show(200)
    curtailBarElem.style.backgroundImage = "url('/static/map_icons/angle-pointing-to-top.png')"
    curtailBarElem.style.opacity = "";
  } else {
    $(document.getElementById('bar')).hide(200);
    curtailBarElem.style.backgroundImage = "url('/static/map_icons/angle-pointing-to-buttom.png')";
    curtailBarElem.style.opacity = "1";
  }
}

function homesSettingsShowHide() {
  const homesElem = document.getElementById('homes');
  const homesSettingsElem = document.getElementById('homes_settings');
  if (homesElem.checked) {
    $(homesSettingsElem).show(200);
  } else {
    $(homesSettingsElem).hide(200);
  }
}

function getGroundStopFeatures(data) {
  const features = [];
  for (const item of data) {
    const point = [item.x, item.y];
    const geom = new ol.geom.Point(point);
    const feature = new ol.Feature({
      'geometry': geom,
      radius: 10,
      'info': 'Нет информации объекте',
      'count': item.count,
      'is_one': item.is_one
    });
    feature.setStyle(computeGroundStopStyle(feature));
    features.push(feature);
  }
  return features;
}

function getGroundStopLayer(features) {
  const vectorSource = new ol.source.Vector({
    features: features,
    wrapX: false
  });

  const vector = new ol.layer.Vector({
    source: vectorSource
  });
  return vector;
}

function computeNewPointStyle(feature) {
  const fill_color = 'cyan';
  const style_dic = {
    'image': new ol.style.Circle({
      radius: 10,
      fill: new ol.style.Fill({
        color: fill_color
      }),
      stroke: new ol.style.Stroke({
        color: 'black',
        width: 0
      })
    }),
    'text': new ol.style.Text({
      font: '12px helvetica,sans-serif',
      text: feature.get('revenue'),
      fill: new ol.style.Fill({
        color: '#000'
      }),
      stroke: new ol.style.Stroke({
        color: '#fff',
        width: 2
      })
    })
  };
  return new ol.style.Style(style_dic);
}

function computeGroundStopStyle(feature) {
  const fill_color = '#6D6D6D';
  const style_dic = {};

  if (!feature.get('is_one')) {
    style_dic['image'] = new ol.style.Circle({
      radius: 7 + feature.get('count').toString().length,
      fill: new ol.style.Fill({
        color: fill_color,
      }),
    });

    style_dic['text'] = new ol.style.Text({
      font: '10px helvetica,sans-serif',
      text: feature.get('count').toString(),
      fill: new ol.style.Fill({
        color: 'white',
      }),
    });
  } else {
    style_dic['image'] = new ol.style.Icon({
      radius: feature.get('radius'),
      anchor: [0.5, 0.5],
      size: [128, 128],
      offset: [0, 0],
      opacity: 1,
      scale: 0.1,
      src: decodeURIComponent('/static/map_icons/bus-stop.png'),
    });
  }

  return new ol.style.Style(style_dic);
}

function computeSearchAddressStyle(feature, fill_color) {
  const style_dic = {};

  style_dic['image'] = new ol.style.Icon({
    radius: feature.get('radius'),
    anchor: [0.5, 0.5],
    size: [200, 200],
    offset: [0, 0],
    opacity: 1,
    scale: 0.2,
    src: decodeURIComponent('/static/icons/placeholder.png'),
  });

  return new ol.style.Style(style_dic);
}

function getBoarders() {
    // Вычисляем координаты углов карты в проекции EPSG:4326
    var extent = map.getView().calculateExtent(map.getSize());
    var min_coord = ol.proj.transform([extent[0], extent[1]], 'EPSG:3857', 'EPSG:4326');
    var max_coord = ol.proj.transform([extent[2], extent[3]], 'EPSG:3857', 'EPSG:4326');

    // Создаем объект boarders_dic и добавляем в него границы карты в разных проекциях
    var boarders_dic = {
        x_min: extent[0],
        y_min: extent[1],
        x_max: extent[2],
        y_max: extent[3],
        lon_min: min_coord[0],
        lat_min: min_coord[1],
        lon_max: max_coord[0],
        lat_max: max_coord[1]
    };

    return boarders_dic;
}

