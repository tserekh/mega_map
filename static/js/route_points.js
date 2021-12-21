function get_route_source(lines,  short_route_names, total_weight){
    console.log(lines);

		geojsonObject = {
			"type": "FeatureCollection",
			// 'crs': {
			// 	'type': 'name',
			// 	'properties': {
			// 		'name': 'EPSG:3857'
			// 		},
			// 	},
			"features": [
					{
						"type": "Feature",
						"properties": {
							'info': Math.round(total_weight).toString() + "<br>" + short_route_names,

						},
						"geometry": {
							"type": "LineString",
							"coordinates": lines
						}
					}
				]
			}
console.log(geojsonObject)

	features = (new ol.format.GeoJSON()).readFeatures(geojsonObject)
	 var line_source = new ol.source.Vector({
		features: features
	  });
	return line_source
  }
function get_route_layer(line_source){
	 var line_layer = new ol.layer.Vector({
		source: line_source,
		 style: compute_route_style

	  });
	return line_layer
  }
  function get_route_points_layer(route_points_source){
	 var line_layer = new ol.layer.Vector({
		source: route_points_source,
	  });
	return line_layer
  }
      function get_route() {
        let address_from = document.getElementById("searchAddressFrom").value;
        let address_to = document.getElementById("searchAddressTo").value;
        param_dic = {}
        param_dic['address_from'] = address_from
        param_dic['address_to'] = address_to
        $.get(route_url, param_dic).then(
            function (response) {
                console.log(response)
                shortest_path_coords = response['route']["shortest_path_coords"];
                short_route_names = response['route']["short_route_names"];
                total_weight = response['route']["total_weight"];

                lines_source = get_route_source(shortest_path_coords, short_route_names, total_weight)
				line_layer = get_route_layer(lines_source)
                map.addLayer(line_layer);
                // route_points_layer = get_route_points_layer(point_source)
                // map.addLayer(route_points_layer);
            }
        )
    }
    function update_route() {
        if (document.getElementById("route").checked) {
            document.getElementById("route").disabled = true;
            get_route();
            document.getElementById("route").disabled = false;
        }
            else{
                // map.removeLayer(line_layer);
                // map.removeLayer(route_points_layer);

        }
        }
