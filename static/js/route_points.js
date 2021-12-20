
function get_route_source(lines){
    console.log(lines);
	geojsonfeatures = lines.map(function(x){
	list_of_coords1 = x['line'];
		return {
				  'type': 'Feature',
				  'geometry': {
					'type': 'LineString',
					'coordinates': lines
				  },
				}

		})
	var geojsonObject = {
		'type': 'FeatureCollection',
		'crs': {
		  'type': 'name',
		  'properties': {
			'name': 'EPSG:3857'
		  }
		},
		'features': geojsonfeatures
	  };

	 features = (new ol.format.GeoJSON()).readFeatures(geojsonObject);

	 var line_source = new ol.source.Vector({
		features: features
	  });
	return line_source
  }
function get_route_layer(line_source){
	 var line_layer = new ol.layer.Vector({
		source: line_source,
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
                // coords1 = response['route']["start_coords_xy"];
                // coords2 = response['route']["end_coords_xy"];
                // geom1 = new ol.geom.Point(coords1)
                // console.log(coords1)
                // geom2 = new ol.geom.Point(coords2)
                // console.log(coords2)
                // view.animate({
                //     center: [(coords1[0] + coords2[0]) / 2, (coords1[1] + coords2[1]) / 2,],
                //     duration: 500,
                //     zoom: 15
                // })
                //
                // feature1 = ol.Feature({
                //         'geometry': geom1,
                //         'info': 'no info',
                //         radius: 10,
                //     })
                // feature2 = ol.Feature({
                //         'geometry': geom2,
                //         'info': 'no info',
                //         radius: 10,
                //     })

                // var point_source = new ol.source.Vector({
                //     features: features,
                //     wrapX: false,
                //     style: compute_search_address_style
                // });

                lines_source = get_route_source(shortest_path_coords)
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
