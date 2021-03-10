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
    }
	function get_polygon_layer(polygons, nat_class){
		console.log(polygons);
		geojsonfeatures = polygons.map(function(x){
			list_of_coords1 = x['points'];
			info_ = x['eng_name'] + '</br>Жителей:' + Math.round(2.7*x['flat_num']).toString() + '</br>' ;
			info_ = info_ + 'Средняя цена кв. м:' +  Math.round(x['sale_price']).toString() + '</br>';
			
			nat_class_stat = {};
			if ( ! (nat_class_stat.hasOwnProperty(nat_class))){
				nat_class_stat[nat_class] = 0;
			}
			
			if (nat_class_stat[nat_class]!=0){
			info_ = info_ + 'Домохозяйств на 1 объект: ' + Math.round(2.7*x['flat_num']/nat_class_stat[nat_class]).toString();}
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
							'flat_num':Math.round(2.7*x['flat_num']).toString()
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
	const max_weight = 2000; // the biggest area

	
function color_func(perc)

{
	if (perc > 0.5)
	{
		 return perc2rg((perc-0.5)*2)		
	}else
	{
		return perc2gb(perc*2)		
	}
}
function perc2rg(perc) {
	perc = 100*(1 - perc);
	var r, g, b = 0;
	if(perc < 50) {
		r = 255;
		g = Math.round(5.1 * perc);
	}
	else {
		g = 255;
		r = Math.round(510 - 5.10 * perc);
	}
	return [r,g,b]
}
function perc2gb(perc) {
	perc = 100*(1 - perc);
	var r, g, b = 0;
	if(perc < 50) {
		g = 255;
		b = Math.round(5.1 * perc);
	}
	else {
		b = 255;
		g = Math.round(510 - 5.10 * perc);
	}
	return [r,g,b]
}
    function compute_line_style(feature) {
	  perc = feature.get('weight')/max_weight;
	  perc = Math.min(1, perc);
	  linestyle = new ol.style.Style({
					stroke: new ol.style.Stroke({
						color:perc2rg(perc),
						width: 3,
						opacity: 0.5,
					}),
				})
      return linestyle
    }
	function get_lines_source(lines){
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
							'info': 'Домашний трафик от метро: ' + Math.round(2.7*x['weight']).toString(),
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
		return line_source
	  }
function get_line_layer(line_source){
		 var line_layer = new ol.layer.Vector({
			source: line_source,
			style: compute_line_style
		  });
		return line_layer
	  }
	  
	  
	  
	  
	function get_metro_features(data){

			data = JSON.parse(data);
			console.log(data);	
			var features = [];
			for (var i = 0; i < data.length; ++i){
				point = [data[i]['fields']["lon"],data[i]['fields']["lat"]];
				point = ol.proj.fromLonLat(point);
				geom = new ol.geom.Point(point);
				console.log(data[i]['fields']);
				if (data[i]['fields']["exit_name"]!=undefined){
					info = data[i]['fields']["exit_name"];
				}else{
					info = data[i]['fields']["station_name"];
					
				}
				
				feature = new ol.Feature({'geometry': geom, radius:10, 'info': '<br/>' + info, name: ''});
				feature.setStyle(compute_metro_style(feature, 'black'));
				features.push(feature);
			}
			console.log(features);
			return features	
		}




				//<!-- GET LAYER -->
	function get_metro_layer(features, obj_color){
		var vectorSource = new ol.source.Vector({
		features: features,
		wrapX: false
		  });
		  
		  
		 var vector = new ol.layer.Vector({
			source: vectorSource,
		});
		
		return vector
	}



