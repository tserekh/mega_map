function get_route_source(lines,  short_route_names, total_weight, info){
		geojsonObject = {
			"type": "FeatureCollection",
			"features": [
					{
						"type": "Feature",
						"properties": {
							'info': Math.round(total_weight).toString() + " минут" + "<br>" + info,

						},
						"geometry": {
							"type": "LineString",
							"coordinates": lines
						}
					}
				]
			}
	features = (new ol.format.GeoJSON()).readFeatures(geojsonObject)
    return new ol.source.Vector({
        features: features
    })
  }
function get_route_layer(line_source, color){
    linestyle = new ol.style.Style({
        stroke: new ol.style.Stroke({
            color: color,
            width: 5,
            opacity: 0.5,
        }),
    })
    return new ol.layer.Vector({
        source: line_source,
        style: linestyle

    })
  }

  function get_route() {
    let address_from = document.getElementById("searchAddressFrom").value;
    let address_to = document.getElementById("searchAddressTo").value;
    param_dic = {}
    param_dic['address_from'] = address_from
    param_dic['address_to'] = address_to
    $.get(route_url, param_dic).then(
        function (response) {
            shortest_path_coords = response['route']["shortest_path_coords"];
            short_route_names = response['route']["short_route_names"];
            total_weight = response['route']["total_weight"];
            info = response['route']["info"];
            colors = ["red", "green", "blue"]
            for (var i = 0; i < shortest_path_coords.length; ++i) {
                lines_source = get_route_source(shortest_path_coords[i], short_route_names, total_weight, info)
                line_layer = get_route_layer(lines_source, colors[i%3])
                map.addLayer(line_layer);
            }
        }
    )
}
function update_route() {
    if (document.getElementById("route").checked) {
        document.getElementById("route").disabled = true;
        get_route();
        document.getElementById("route").disabled = false;
    }
    }
