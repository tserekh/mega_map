
    function compute_polygon_style(feature) {
			return new ol.style.Style({
			  stroke: new ol.style.Stroke({
				color: 'blue',
				width: 1.5
			  }),
			  fill: new ol.style.Fill({
				color: 'rgba(0, 0, 255, 0.1)'
			  }),
			  	text: new ol.style.Text({
				font: '12px helvetica,sans-serif',
				text: feature.get('flat_num'),
				fill: new ol.style.Fill({
				color: '#000'
				}),
				stroke: new ol.style.Stroke({
					color: '#fff',
					width: 2
				})
			})
			})
      return linestyle
    }
	function get_polygon_layer(polygons, nat_class){
		console.log(polygons);
		geojsonfeatures = polygons.map(function(x){
			list_of_coords1 = x['points'];
			info_ = x['eng_name'] + '</br> Число квартир:' + Math.round(x['flat_num']).toString() + '</br>';
			info_ = info_ + 'Средняя цена кв. м:' +  Math.round(x['sale_price']).toString() + '</br>';
			info_ = info_ + '</br>Число объектов класса </br>' + nat_class + ' ';
			
			nat_class_stat = JSON.parse(x['nat_class_stat']);
			if ( ! (nat_class_stat.hasOwnProperty(nat_class))){
				nat_class_stat[nat_class] = 0;
			}
			
			info_ = info_ + nat_class_stat[nat_class]+ '</br>';
			if (nat_class_stat[nat_class]!=0){
			info_ = info_ + 'Домохозяйств на 1 объект: ' + Math.round(x['flat_num']/nat_class_stat[nat_class]).toString();}
			return {	
					  'type': 'Feature',
					  'geometry': {
						'type': 'Polygon',
						'coordinates': [
											list_of_coords1.map(function(x){return ol.proj.fromLonLat(x)})
									   ]
					  },
					  
					  "properties": {
							"name": x['eng_name'],
							'info':  info_,
							'flat_num':Math.round(x['flat_num']).toString()
									},
					}

			})
		console.log(geojsonfeatures);
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
		 var polygon_source = new ol.source.Vector({
			features: features
		  });

		 console.log(polygon_source);
		 var polygon_layer = new ol.layer.Vector({
			source: polygon_source,
			style: compute_polygon_style
		  });
		return polygon_layer
	  }
	
	const min_weight = 0; // the smallest area
	const max_weight = 1000; // the biggest area

	function perc2color(rate) {
		
		return [rate*256, (1-rate)*256,0]
	}

    function compute_line_style(feature) {
	  perc = feature.get('weight')/max_weight;
	  perc = Math.min(1, perc);
	  linestyle = new ol.style.Style({
					stroke: new ol.style.Stroke({
						color:perc2color(perc),
						width: 3,
						opacity: 0.5,
					}),
				})
      return linestyle
    }
	function get_line_layer(lines){
		console.log(lines);
		geojsonfeatures = lines.map(function(x){
		list_of_coords1 = x['line'];
			return {	
					  'type': 'Feature',
					  'geometry': {
						'type': 'LineString',
						'coordinates': list_of_coords1.map(function(x){return ol.proj.fromLonLat(x)})
					  },
					  
					  "properties": {
							"name": 'sdsd',
							'info':  Math.round(x['weight']).toString(),
							'weight':x['weight']

									},
					}

			})
		console.log(geojsonfeatures[0]);
	
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
		 console.log(line_source);
		 var line_layer = new ol.layer.Vector({
			source: line_source,
			style: compute_line_style
		  });
		return line_layer
	  }
	  
	  
		
	
	
				<!-- STYLE -->
	function compute_metro_style(feature,fill_color) {
		return new ol.style.Style({
        image: new ol.style.Icon({
          anchor: [0.5, 0.5],
          size: [200, 200],
          offset: [0, 0],
          opacity: 1,
          scale: 0.2,
          src:"{% static 'metro-moskva-logo.png' %}"
        })
		});
	}
	
	function compute_home_style(feature,fill_color) {
		return new ol.style.Style({
			image: new ol.style.Circle({
				radius: feature.get('radius'),
				fill: new ol.style.Fill({
					color: fill_color
				}),
				stroke: new ol.style.Stroke({
					color: 'black',
					width: 1
				})
			}),
			text: new ol.style.Text({
				font: '12px helvetica,sans-serif',
				text: feature.get('name'),
				fill: new ol.style.Fill({
				color: '#000'
				}),
				stroke: new ol.style.Stroke({
					color: '#fff',
					width: 2
				})
			})
		});
	}
	
	function compute_org_style(feature,fill_color) {
		have_logos = {{have_logos}};
		if (have_logos.indexOf(feature.get('chain_name')) >= 0) {
			//do something
			
			icon = feature.get('chain_name');
			console.log(decodeURIComponent('static/map_icons/' + icon + '.png'));
			return new ol.style.Style({
				image: new ol.style.Icon({
				  anchor: [0.5, 0.5],
				  size: [200, 200],
				  offset: [0, 0],
				  opacity: 1,
				  scale: 0.2,
				  src:decodeURIComponent('/static/map_icons/' + icon + '.png')
				})
			});
		}
		else
		{
			return new ol.style.Style({
					image: new ol.style.Circle({
						radius: feature.get('radius'),
						fill: new ol.style.Fill({
							color: fill_color
						}),
						stroke: new ol.style.Stroke({
							color: 'black',
							width: 1
						})
					})
				});		
		}
	}	
				<!-- GET FEATURES -->
	function get_metro_features(data){

		data = JSON.parse(data);
		console.log(data);	
		console.log(data[0]['fields']);	
		var features = [];
		point = [data[0]['fields']["lon"],data[0]['fields']["lat"]];
		for (var i = 0; i < data.length; ++i){
			point = [data[i]['fields']["lon"],data[i]['fields']["lat"]];
			point = ol.proj.fromLonLat(point);
			geom = new ol.geom.Point(point);
			
			feature = new ol.Feature({'geometry': geom, radius:10, 'info': data[i]['fields']["exit_name"], name: ''});
			feature.setStyle(compute_metro_style(feature, 'black'));
			features.push(feature);
		}
		console.log(features);
		return features	
	}

	function get_home_features(data){
		data =  JSON.parse(data);
		console.log('inside get_home_features');
		var features = new Array(data.length);
		for (var i = 0; i < data.length; ++i){
			point = [data[i]["fields"]["lon"],data[i]["fields"]["lat"]];
			point = ol.proj.fromLonLat(point);
			geom = new ol.geom.Point(point);
			
			address = data[i]["fields"]["address"];
			flat_num = data[i]["fields"]["flat_num"];
			flat_num = Math.round(flat_num);
			sale_price = data[i]["fields"]["sale_price"];
			
			feature = new ol.Feature({
					'geometry': geom, radius:10,
					'info': address + '.<br/> Квартир: ' + flat_num + '<br /> Цена кв. м.: ' + Math.round(sale_price),
					'name': flat_num.toString(),
					});
			feature.setStyle(compute_home_style(feature, 'blue'));
			features[i] = feature;
		}
		return features
	}
	
	function get_org_features(data){
		data =  JSON.parse(data);
		var features = new Array(data.length);
		for (var i = 0; i < data.length; ++i){
			point = [data[i]["fields"]["lon"],data[i]["fields"]["lat"]];
			point = ol.proj.fromLonLat(point);
			geom = new ol.geom.Point(point);
			
			feature = new ol.Feature({
					'geometry': geom, radius:8,
					'info':  data[i]["fields"]["chain_name"] + '<br/>' + data[i]["fields"]["nat_class"] + '<br/>' + data[i]["fields"]["address"],
					chain_name: data[i]["fields"]["chain_name"],
					});
			feature.setStyle(compute_org_style(feature, 'brown'));
			features[i] = feature;
		}
		return features
	}	
				<!-- GET LAYER -->
	function get_metro_layer(features, obj_color){
	var vectorSource = new ol.source.Vector({
	features: features,
	wrapX: false
      });
	  
	  
     var vector = new ol.layer.Vector({
		source: vectorSource,
		maxResolution:300,
        //minResolution:4,
	});
	
	return vector
	}

	function get_home_layer(features, obj_color){
	
		var vectorSource = new ol.source.Vector({
		features: features,
		wrapX: false
		  });
		  
		 var vector = new ol.layer.Vector({
			source: vectorSource,
			maxResolution:300,
			//minResolution:4,
		});
		
		return vector
	}
	function get_org_layer(features, obj_color){
	
		var vectorSource = new ol.source.Vector({
		features: features,
		wrapX: false
		  });
		  
		 var vector = new ol.layer.Vector({
			source: vectorSource,
			maxResolution:300,
			//minResolution:4,
		});
		
		return vector
	}

	
	var center_coord = [37.562555, 55.678045];
	center_coord = ol.proj.fromLonLat(center_coord);
	metro_url = "{% url 'main_map:get_metros'%}";
	home_url =  "{% url 'main_map:get_homes'%}";
	org_url =  "{% url 'main_map:get_orgs'%}";
	polygon_url =  "{% url 'main_map:get_polygons'%}";
	line_url =  "{% url 'main_map:get_lines'%}";
	sale_point_url =  "{% url 'main_map:cacl_sale_point'%}";
	metro_exits = {};
	
	var map_layer = new ol.layer.Tile({
            source: new ol.source.OSM()
          })
	
	var map = new ol.Map({
		layers: [map_layer],
        target: document.getElementById('map'),
        view: new ol.View({
          center: center_coord,
          zoom: 11
        })
      });
	
	function get_boarders(){
		var extent = map.getView().calculateExtent(map.getSize());
		min_coord = ol.proj.transform([extent[0],extent[1]], 'EPSG:3857', 'EPSG:4326');
		max_coord = ol.proj.transform([extent[2],extent[3]], 'EPSG:3857', 'EPSG:4326');
		
		boarders_dic = {};
		boarders_dic['lon_min'] = min_coord[0];
		boarders_dic['lat_min'] = min_coord[1];
		boarders_dic['lon_max'] = max_coord[0];
		boarders_dic['lat_max'] = max_coord[1];
		return boarders_dic
	}
	
	$('input').change(function(){
	
		param_dic = get_boarders();
		console.log(param_dic);
		param_dic['nat_class'] = document.getElementById('selected_org_type').value;
		value = $(this).val();
		console.log(value);
		if (value=='metros'){
			if (document.getElementById(value).checked){
			document.getElementById("metros").disabled = true;
				$.get(metro_url,param_dic).then(function(response) {
					console.log("Success!");
					var features = get_metro_features(response['metros']);
					metro_layer = get_metro_layer(features, 'red');
					map.addLayer(metro_layer);
					document.getElementById("metros").disabled = false;
					
					console.log('input')
				})
			}
			else{
				console.log('remove');
				
				map.removeLayer(metro_layer);
			}
		}
		if (value=='homes'){
			if (document.getElementById(value).checked){
				$.get(home_url,param_dic).then(function(response) {
					console.log("Success!");
					var features = get_home_features(response['homes']);
					home_layer = get_home_layer(features, 'blue');
					console.log('works!!!!!!!!!!!!!!!!!!!')
					map.addLayer(home_layer);

					console.log('input')
				})
			}
			else{
				console.log('remove');
				map.removeLayer(home_layer);
			}

		}
		
		if (value=='orgs'){
		
			if (document.getElementById(value).checked){
				document.getElementById("orgs").disabled = true;
				document.getElementById("selected_org_type").disabled = true;
				$.get(org_url,param_dic).then(function(response) {
					console.log("Success!");
					var features = get_org_features(response['orgs']);
					console.log(response['orgs']);
					org_layer = get_org_layer(features, 'brown');
					console.log('works!!!!!!!!!!!!!!!!!!!')
					map.addLayer(org_layer);
					document.getElementById("orgs").disabled = false;
					console.log('orgs')
				})
			}
			else{
				
				console.log('remove');
				map.removeLayer(org_layer);
				document.getElementById("selected_org_type").disabled = false;
				
			}
		}
		console.log(value);
		console.log(value=='polygons');
		if (value=='polygons'){
			param_dic['scale'] = document.getElementById('selected_polygon_type').value;
			if (document.getElementById(value).checked){
				document.getElementById("polygons").disabled = true;
				document.getElementById("selected_polygon_type").disabled = true;
				$.get(polygon_url,param_dic).then(function(response) {
					console.log("Success!");
					console.log(response['polygons'][0]['points']);
					polygons = response['polygons'];
					
					polygon_layer = get_polygon_layer(polygons, param_dic['nat_class']);
					map.addLayer(polygon_layer);
					document.getElementById("polygons").disabled = false;
					
				})
			}
			else{
				console.log('remove');
				map.removeLayer(polygon_layer);
				document.getElementById("selected_polygon_type").disabled = false;
			}

		}
		
		if (value=='lines'){
			val = document.getElementById('selected_line_type').value;
			document.getElementById("selected_line_type").disabled = true;
			param_dic['mode'] = val.split('_')[0];
			param_dic['att'] = val.split('_')[1];
			console.log(param_dic);
			if (document.getElementById(value).checked){
				document.getElementById("lines").disabled = true;
				$.get(line_url,param_dic).then(function(response) {
					lines = response['lines'];
					console.log(lines);
					
					line_layer = get_line_layer(lines);
					console.log(line_layer);
					map.addLayer(line_layer);
					document.getElementById("lines").disabled = false;

					
				})
			}
			else{
				console.log('remove');
				map.removeLayer(line_layer);
				document.getElementById("selected_line_type").disabled = false;
				
			}

		}			
		
	});

	  



	map.on('moveend', function() {
	param_dic = get_boarders();
	param_dic['nat_class'] = document.getElementById('selected_org_type').value;
		console.log(document.getElementById("metros").checked );
		console.log('move map');
		if (document.getElementById("metros").checked){
			map.removeLayer(metro_layer);

			
			$.get(metro_url,param_dic).then(function(response) {
			console.log("Success!");
			var features = get_metro_features(response['metros']);
			metro_layer = get_metro_layer(features, 'red');
			
			map.addLayer(metro_layer);
			console.log('input')
			});
		}
		console.log(document.getElementById("homes").checked );
		if (document.getElementById("homes").checked){
			map.removeLayer(home_layer);
			
			$.get(home_url,param_dic).then(function(response) {
			console.log("Success!");
			var features = get_home_features(response['homes']);
			home_layer = get_home_layer(features, 'red');
			map.addLayer(home_layer);
			console.log('input')
			});
		}
		if (document.getElementById("orgs").checked){
			map.removeLayer(org_layer);
			document.getElementById("orgs").disabled = true;
			$.get(org_url,param_dic).then(function(response) {
			console.log("Success!");
			var features = get_org_features(response['orgs']);
			org_layer = get_org_layer(features, 'brown');
			map.addLayer(org_layer);
			document.getElementById("orgs").disabled = false;
			});
		}

});

	function displayFeatureInfo(pixel) {
		var info = document.getElementById('info');
		var target = document.getElementById('map');
        info.style.left = pixel[0] + 'px';
        info.style.top = (pixel[1] - 50) + 'px';
        var feature = map.forEachFeatureAtPixel(pixel, function(feature, layer) {
            return feature;
        });
        if (feature) {
            var text = feature.get('info');
            info.style.display = 'none';
            info.innerHTML = text;
            info.style.display = 'block';
            target.style.cursor = "pointer";
        } else {
            info.style.display = 'none';
            target.style.cursor = "";
        }
    };
	
	map.on('pointermove', function(evt) {
	if (evt.dragging) {
		info.style.display = 'none';
		return;
	}
	var pixel = map.getEventPixel(evt.originalEvent);
	displayFeatureInfo(pixel);
	});

	map.on('click', function(evt) {
		lonlat = evt['coordinate'];
		lonlat = ol.proj.transform(lonlat, 'EPSG:3857', 'EPSG:4326');
		console.log(lonlat);
		coord_dic = {};
		coord_dic['lon'] = lonlat[0];
		coord_dic['lat'] = lonlat[1];
		console.log(coord_dic);
		var sale_point_info = document.getElementById('sale_point_info');
		sale_point_info.innerHTML = "Пожалуйста, подождите";
		$.get(sale_point_url,coord_dic).then(function(response) {
			console.log("Success!");
			var sale_point_info = document.getElementById('sale_point_info');
			sale_point_info.innerHTML = "Выручка: " + response['revenue']
			console.log(response['revenue']);
		})
	});
		