import get_orgs from './orgs'
import get_homes from './homes'
map.on('moveend', function() {
	get_orgs();
	get_sale_points()
	if (document.getElementById('square_mode').checked)
	{get_oper_squares()}
	fresh_sale_points_layer.setSource(new ol.source.Vector());
	param_dic = get_boarders();
	param_dic['delete_all'] = false;
	param_dic['nat_class'] = document.getElementById('selected_nat_class').value;
		console.log('move map');
		if (document.getElementById("metros").checked){
			$.get(metro_url,param_dic).then(function(response) {
				var features = get_metro_features(response['metros']);
				source = new ol.source.Vector({
					features: features,
					wrapX: false
					});
				metro_layer.setSource(source);
			});
		}
		if (document.getElementById("homes").checked){
			get_homes()
		}

		if (document.getElementById("ground_stops").checked){
			document.getElementById("ground_stops").disabled = true;
			$.get(ground_stop_url,param_dic).then(function(response) {
				var features = get_ground_stop_features(response['ground_stops']);
				source = new ol.source.Vector({
					features: features,
					wrapX: false
				});

				ground_stop_layer.setSource(source)
				document.getElementById("ground_stops").disabled = false;
			});
		}
		if (document.getElementById("lines").checked){
			document.getElementById("lines").disabled = true;

			$.get(line_url, param_dic).then(function(response) {
				console.log(response);
				var source = get_lines_source(response['lines']);
				line_layer.setSource(source);
				document.getElementById("lines").disabled = false;
			});
		}
});

map.on('click', function(evt){
    var feature = map.forEachFeatureAtPixel(evt.pixel,
        function(feature, layer) {
			console.log('click event');
            console.log(feature.get('info'));
			info = feature.get('info');
			if (feature.get('info')==undefined){
				info = 'Нет информации об объекте';
			}
			console.log(feature);
			document.getElementById("select_bar").style.display = "none";
			document.getElementById("describe_bar").style.display = "block";
			document.getElementById("bar").style.display = "block";
			document.getElementById("describe").innerHTML = info;
    });
});