document.getElementById("search").addEventListener("keyup", function(event) {
    event.preventDefault();
    if (event.keyCode === 13) {
	
        searchAddress();
    }
});
function balance(x,y)
{	
	console.log('balance');
	console.log(console.log(document.getElementById(x).checked));
	console.log(console.log(document.getElementById(y).checked));
	if ((document.getElementById(x).checked==false)&(document.getElementById(y).checked==false)){
		document.getElementById(x).checked=true;
		document.getElementById(y).checked=true;
	}
}
function update_heat_map_radius(){
	radius = document.getElementById('radius')
	heat_map_layer.setRadius( parseInt(radius.value, 10))
	}
function update_heat_map_blur(){
blur = document.getElementById('blur')
	heat_map_layer.setBlur( parseInt(blur.value, 10))
	}
function back_bar(){
	document.getElementById("select_bar").style.display = "block";
	document.getElementById("describe_bar").style.display = "none";
			}
function curtail_bar(){
	
	if (document.getElementById("curtail_bar").style.opacity == 1){
		$(document.getElementById('bar')).show(200)
		document.getElementById("curtail_bar").style.backgroundImage = "url('/static/map_icons/angle-pointing-to-top.png')"
		document.getElementById("curtail_bar").style.opacity = ""
	}else{
		$(document.getElementById('bar')).hide(200);
		document.getElementById("curtail_bar").style.backgroundImage = "url('/static/map_icons/angle-pointing-to-buttom.png')";
		document.getElementById("curtail_bar").style.opacity = 1;
	}	
}
function homes_settings_show_hide(){
	if (document.getElementById('homes').checked){
		$(document.getElementById('homes_settings')).show(200);
	}else{
	$(document.getElementById('homes_settings')).hide(200);
	}
}
			
		
			
function searchAddress(){
	var bbox = "36.498210,55.271105~38.459270,56.141082";
	var geocode_url_pattern = "https://geocode-maps.yandex.ru/1.x/?format=json&bbox=" + bbox +"&geocode=";
	var search_address = document.getElementById("searchAddress").value;
	var geocode_url = geocode_url_pattern + search_address;
	$.get(geocode_url).then(function(response, geocode_url) {
		var info_text  = '';
		var GeoObjectCollection = response['response']['GeoObjectCollection'];
		console.log(GeoObjectCollection['metaDataProperty']['GeocoderResponseMetaData']['found']);
		if (GeoObjectCollection['metaDataProperty']['GeocoderResponseMetaData']['found']=="0"){
			console.log("Ничего не нашлось");
			info_text = 'Ничего не нашлось';
		}else{
			GeoObject = GeoObjectCollection['featureMember'][0]['GeoObject'];
			info_text = GeoObject['metaDataProperty']['GeocoderMetaData']['Address']['formatted'];
			coords = GeoObject['Point']['pos'].split(' ');
			coords = coords.map(parseFloat);
			console.log(coords);
			
			coords = ol.proj.fromLonLat(coords);
			geom = new ol.geom.Point(coords)
			view.animate({
				center: coords,
				duration: 500,
				zoom: 15
			})
			
		}
		
		document.getElementById("select_bar").style.display = "none";
		document.getElementById("describe_bar").style.display = "block";
		document.getElementById("bar").style.display = "block";
		document.getElementById("describe").innerHTML = info_text;
		
			feature = new ol.Feature({
			'geometry': geom,
			'info':info_text,
			radius:10,
			});
			feature.setStyle(compute_search_address_style(feature, '#FC00C3'));
			features = [feature];
						
				var source = new ol.source.Vector({
					features: features,
					wrapX: false
				});
				
				search_address_layer.setSource(source);
		
	})
}
      var vector = new ol.layer.Vector({
        source: new ol.source.Vector(),
		style:compute_new_point_style,
      });
	  
	  var orgs_layer = new ol.layer.Vector({
        source: new ol.source.Vector(),
		style:compute_new_point_style,
      });
	  
	  var heat_map_layer = new ol.layer.Heatmap({
       source: new ol.source.Vector(),
	   radius:10
	  });
	  
	 var oper_squares_layer = new ol.layer.Vector({
		source: new ol.source.Vector(),
		style: compute_oper_square_style
	  });
	 var pred_squares_layer = new ol.layer.Vector({
		source: new ol.source.Vector(),
		style: compute_pred_square_style
	  });
function get_ground_stop_features(data){
		console.log(data);	
		console.log(data[0]);	
		var features = [];
		for (var i = 0; i < data.length; ++i){
			point = [data[i]["x"],data[i]["y"]];
			geom = new ol.geom.Point(point);
			
			feature = new ol.Feature(
				{
					'geometry': geom,
					radius:10,'info': 'Нет информации объекте',
					'n_ground_stops':data[i]["n_ground_stops"],
					'is_one':data[i]["is_one"]
					}, );
			feature.setStyle(compute_ground_stop_style(feature));
			features.push(feature);
		}
		console.log(features);
		return features	
	}
	function get_ground_stop_layer(features, obj_color){
		var vectorSource = new ol.source.Vector({
		features: features,
		wrapX: false
		  });
		  
		  
		 var vector = new ol.layer.Vector({
			source: vectorSource,
		});
		
		return vector
	}
function compute_new_point_style(feature) {
	var fill_color = 'cyan';
	
	
	var style_dic = {}
		style_dic['image'] =  new ol.style.Circle({
					radius: 10,
					fill: new ol.style.Fill({
						color: fill_color
					}),
					stroke: new ol.style.Stroke({
						color: 'black',
						width: 0
					})
				})
		style_dic['text'] = new ol.style.Text({
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
	return new ol.style.Style(style_dic);
	}
function compute_ground_stop_style(feature) {
	var fill_color = '#6D6D6D';
	
	
	var style_dic = {}
	console.log(feature);
	if (feature.get('is_one')!=true){
		style_dic['image'] =  new ol.style.Circle({
					radius: 7 + feature.get('n_ground_stops').toString().length,
					fill: new ol.style.Fill({
						color: fill_color
					}),
				})
		style_dic['text'] = new ol.style.Text({
			font: '10px helvetica,sans-serif',
			text: feature.get('n_ground_stops').toString(),
			fill: new ol.style.Fill({
			color: 'white'
			}),
		})
	}else{
		style_dic['image'] = new ol.style.Icon({
		radius: feature.get('radius'),
          anchor: [0.5, 0.5],
          size: [128, 128],
          offset: [0, 0],
          opacity: 1,
          scale: 0.1,
          src:decodeURIComponent("/static/map_icons/bus-stop.png")
        })
		
		
		
	}
	return new ol.style.Style(style_dic);
}
	
	
	function compute_search_address_style(feature,fill_color) {
		var style_dic = {};
		style_dic['image'] =  new ol.style.Icon({
			radius: feature.get('radius'),
          anchor: [0.5, 0.5],
          size: [200, 200],
          offset: [0, 0],
          opacity: 1,
          scale: 0.2,
          src:decodeURIComponent("/static/icons/placeholder.png")
        })
	return new ol.style.Style(style_dic);
}
	
	
	function compute_sale_point_style(feature) {
		fill_color='#3498db';
		style_dic = {}
		style_dic['image'] =  new ol.style.Circle({
				radius: feature.get('radius'),
				fill: new ol.style.Fill({
					color: fill_color
				}),
			})
	
	
		style_dic['text'] = new ol.style.Text({
			font: '10px helvetica,sans-serif',
			text: feature.get('name'),
			fill: new ol.style.Fill({
				color: 'white',
			}),
		})
		return new ol.style.Style(style_dic);	
	}
	function compute_org_style(feature,fill_color) {
		have_logos = {{have_logos}};
		var fill_color = 'brown';
		var style_dic = {}
		if (feature.get('count')!=1){
			style_dic['image'] =  new ol.style.Circle({
						radius: 7 + feature.get('count').toString().length,
						fill: new ol.style.Fill({
							color: fill_color
						}),
					})
			style_dic['text'] = new ol.style.Text({
				font: '10px helvetica,sans-serif',
				text: feature.get('count').toString(),
				fill: new ol.style.Fill({
				color: 'white'
				}),
			})
		}else{
			chain_name = feature.get('chain_name');
			
			if (have_logos[chain_name] != undefined){
				style_dic['image'] = new ol.style.Icon({
				radius: feature.get('radius'),
				  scale: 25/have_logos[chain_name] ,
	
				  src:decodeURIComponent('/static/map_icons/' + chain_name + '.png')
				})
			}else{
					style_dic['image'] =  new ol.style.Circle({
					radius: 6,
					fill: new ol.style.Fill({
						color: fill_color
					}),
				})
			}
		}
		return new ol.style.Style(style_dic);	
	}	

	var center_coord = [37.622504, 55.753215];
	center_coord = ol.proj.fromLonLat(center_coord);

	
	var map_layer = new ol.layer.Tile({
        source: new ol.source.XYZ({
			url: 'https://api.mapbox.com/v4/mapbox.streets/{z}/{x}/{y}.png?access_token=pk.eyJ1Ijoia3ZlcnRlYSIsImEiOiJjamp5aTdiMnUxMGE5M3ZuNmQ5eXoyOWQ4In0.UkitlLx2XQzHq8A8kNyAEw',
			attributions: []
			})
          })
	
	
      var view = new ol.View({
        center: center_coord,
        zoom: 11
      });
	
	sale_points_layer = new ol.layer.Vector({
		source:new ol.source.Vector()
	});
	
	fresh_sale_points_layer = new ol.layer.Vector({
		source:new ol.source.Vector()
	});
	search_address_layer = new ol.layer.Vector({
		source:new ol.source.Vector()
	});
	home_layer = new ol.layer.Vector({
		source:new ol.source.Vector()
	});
	
	var map = new ol.Map({
		layers: [
					map_layer, vector,heat_map_layer, home_layer, orgs_layer,
					search_address_layer, fresh_sale_points_layer,
					sale_points_layer, oper_squares_layer, pred_squares_layer ],
        target: document.getElementById('map'),
        view: view
      });
	function get_boarders(){
		var extent = map.getView().calculateExtent(map.getSize());
		min_coord = ol.proj.transform([extent[0],extent[1]], 'EPSG:3857', 'EPSG:4326');
		max_coord = ol.proj.transform([extent[2],extent[3]], 'EPSG:3857', 'EPSG:4326');
		
		boarders_dic = {};
		
		boarders_dic['x_min'] = extent[0];
		boarders_dic['y_min'] = extent[1];
		boarders_dic['x_max'] = extent[2];
		boarders_dic['y_max'] = extent[3];
		
		boarders_dic['lon_min'] = min_coord[0];
		boarders_dic['lat_min'] = min_coord[1];
		boarders_dic['lon_max'] = max_coord[0];
		boarders_dic['lat_max'] = max_coord[1];
		return boarders_dic
	}
	
	
	function getMultSelectbyId(id_)
	
	{
		var select = document.getElementById(id_);
		var selected = [];
		for (var i = 0; i < select.length; i++) {
			if (select[i].selected) selected.push(select[i].value);
				}
		return selected
	}
	
		
	
	$('input').change(function(){
	
		
		param_dic = get_boarders();
		console.log(param_dic);
		
		param_dic['nat_class'] = document.getElementById('selected_nat_class').value;
		
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
			get_homes()
		}
		
		
		if (value=='lines'){
			console.log(param_dic);
			if (document.getElementById(value).checked){
				document.getElementById("lines").disabled = true;
				$.get(line_url,param_dic).then(function(response) {
					lines = response['lines'];
					console.log(lines);
					source = get_lines_source(lines);
					line_layer = get_line_layer(source);
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
		if (value=='ground_stops'){
			if (document.getElementById(value).checked){
			document.getElementById("ground_stops").disabled = true;
				$.get(ground_stop_url,param_dic).then(function(response) {
					console.log("Success!");
					var features = get_ground_stop_features(response['ground_stops']);
					ground_stop_layer = get_ground_stop_layer(features, 'red');
					map.addLayer(ground_stop_layer);
					document.getElementById("ground_stops").disabled = false;
					
					console.log('input')
				})
			}
			else{
				console.log('remove');
				
				map.removeLayer(ground_stop_layer);
			}
		}
		
		
	});
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
	
	function addRevenues(vector){
		features = vector.getSource().getFeatures();
		console.log(features);
		var revenue_;
		lonlatOnMap = [];
		for (var i = 0; i < features.length; ++i){
			geometry = features[i].getGeometry();
			
			if (geometry.getType() == 'Point'){
				lonlat3857= geometry['A'];
				lonlat = ol.proj.transform(lonlat3857, 'EPSG:3857', 'EPSG:4326');
				coord_dic = {};
				coord_dic['lon'] = lonlat[0];
				coord_dic['lat'] = lonlat[1];
				lonlat = ol.proj.fromLonLat(lonlat);
				 
				a = Math.round(lonlat[0]).toString().slice(-3,)
				b = Math.round(lonlat[1]).toString().slice(-3,);
				revenue_ = 2*a*b+1200000
				revenue_ = parseFloat(revenue_);
				features[i]['N']['info']  = "Прогноз выручки " + revenue_;
				features[i]['N']['revenue']  = (Math.round(revenue_/10000)/100).toString()+'M';
	
			}
		}
	}
document.getElementsByClassName("ol-attribution")[0].style.display='none'
	