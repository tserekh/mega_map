function nFormatter(num, digits) {
    var si = [
        {value: 1, symbol: ""},
        {value: 1E3, symbol: "k"},
        {value: 1E6, symbol: "M"},
        {value: 1E9, symbol: "G"},
        {value: 1E12, symbol: "T"},
        {value: 1E15, symbol: "P"},
        {value: 1E18, symbol: "E"}
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


function compute_route_style(color) {
    linestyle = new ol.style.Style({
        stroke: new ol.style.Stroke({
            color: color,
            width: 3,
            opacity: 0.5,
        }),
    })
    return linestyle
}

function get_metro_features(data) {
    var features = [];
    for (var i = 0; i < data.length; ++i) {
        point = [data[i]["lon"], data[i]["lat"]];
        point = ol.proj.fromLonLat(point);
        geom = new ol.geom.Point(point);
        if (data[i]["exit_name"] !== undefined) {
            info = data[i]["exit_name"];
        } else {
            info = data[i]["station_name"];
        }

        feature = new ol.Feature({'geometry': geom, radius: 10, 'info': '<br/>' + info, name: ''});
        feature.setStyle(compute_metro_style(feature));
        features.push(feature);
    }
    return features;
}


//<!-- GET LAYER -->
function get_metro_layer(features) {
    var vectorSource = new ol.source.Vector({
        features: features,
        wrapX: false
    });


    return new ol.layer.Vector({
        source: vectorSource,
    });
}

 function compute_oper_square_style(feature) {

	perc = feature.get('result_rate');

	perc = Math.min(1, perc);
	color = color_func(perc);
	color.push(0.5);
		return new ol.style.Style({
		  fill: new ol.style.Fill({
			color: color,
		  }),
		})
}
