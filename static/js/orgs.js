// function orgs_bar_func()
// 	{
// 		if (document.getElementById('orgs_bar').checked){
// 	 		$(document.getElementById('selected_orgs')).show(200)
// 		}else
// 		{
// 		$(document.getElementById('selected_orgs')).hide(200)
// 		}
// 	}
//
// function clean_orgs()
// {
// 	var select = document.getElementById("selected_nat_class");
// 	for (var i = 0; i < select.length; i++) {
// 		select[i].selected = false;
// 			}
//
//
// 	var select = document.getElementById("selected_chain_name");
// 	for (var i = 0; i < select.length; i++) {
// 		select[i].selected = false;
// 	}
// 	orgs_layer.setSource( new ol.source.Vector())
// 	heat_map_layer.setSource( new ol.source.Vector())
//
// }

// function get_orgs(){
// 	param_dic = get_boarders();
// 	param_dic['nat_classes'] = getMultSelectbyId('selected_nat_class').join('_');
// 	param_dic['chain_name'] = getMultSelectbyId('selected_chain_name').join('_');
//
// 	$.get(org_url,param_dic).then(function(response) {
// 		console.log(response['orgs']);
// 		points = response['orgs'].map(function(coord){
// 			point = {
// 						"type": "Feature",
// 						"properties": {},
// 						"geometry": {
// 							"type": "Point",
// 							"coordinates": [coord['x'], coord['y']]
// 						}
// 					}
// 			return point
// 			}
// 		)
//
// 		geojsonObject = {
// 			  "type": "FeatureCollection",
// 			  "features": points
// 			}
// 			orgs_layer.setSource(ol.source.Vector());
// 	})
// }


// function get_org_layer(features, obj_color){
// 	var vectorSource = new ol.source.Vector({
// 	features: features,
// 	wrapX: false
// 	  });
//
// 	 var vector = new ol.layer.Vector({
// 		source: vectorSource,
// 	});
//
// 	return vector
// }
//
// function get_org_features(data){
// 	var features = new Array(data.length);
// 	for (var i = 0; i < data.length; ++i){
// 		console.log(data[i]);
// 		point = [data[i]["x"],data[i]["y"]];
// 		geom = new ol.geom.Point(point);
// 		flat_num = data[i]["flat_num"];
// 		if (flat_num===undefined)
// 		{flat_num=''}
// 		else{
// 			flat_num = '\nЧисло клиентов ' + flat_num
// 		}
// 		feature = new ol.Feature({
// 				'geometry': geom, radius:8,
// 				'info':  data[i]["chain_name"] + flat_num,
// 				'count': data[i]["count"],
// 				'chain_name': data[i]["chain_name"],
// 				'nat_class': data[i]["nat_class"],
// 				});
// 		feature.setStyle(compute_org_style(feature, 'black'));
// 		features[i] = feature;
// 	}
// 	return features
// }
//
