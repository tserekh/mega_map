 function get_route_points(){
		if (!document.getElementById('show_route_points').checked){
			sale_points_layer.setSource(new ol.source.Vector())
			fresh_sale_points_layer.setSource(new ol.source.Vector())
		}
		param_dic = get_boarders();
		param_dic['delete_all'] = false;
		$.get(get_points_url,param_dic).then(function(response) {
			var features = get_sale_points_features(response['route_points']);
			var source = new ol.source.Vector({
				features: features,
				wrapX: false
			});
			sale_points_layer.setSource(source);
			console.log('input')
		})
	}
function delete_route_points_points()
	{	param_dic = {};
		fresh_sale_points_layer.setSource(new ol.source.Vector());
		param_dic['delete_all'] = true;
		console.log('delete all points');
		$.get(get_sale_points_url,param_dic).then(get_route_points())
		}
	function get_route_points_features(data){
		console.log('inside get_sale_points_features');

		var features = new Array(data.length);
		for (var i = 0; i < data.length; ++i){
			point = [data[i]["x"],data[i]["y"]];
			geom = new ol.geom.Point(point);
			feature = new ol.Feature({
					'geometry': geom,
					radius:11,
					'name': name,
					});
			feature.setStyle(compute_sale_point_style(feature));
			features[i] = feature;
		}
		return features
	}