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

function sq()
	{
		
		if (document.getElementById('square_mode').checked){
			$(document.getElementById('demand-selector')).show(200)
		}else
		{
		$(document.getElementById('demand-selector')).hide(200)
		}
		a = document.getElementById('sq_homes')
		b = document.getElementById('sq_works')
		c = document.getElementById('sq_male')
		d = document.getElementById('sq_female')
		if ((a.checked==false)&(a.checked==false)&(a.checked==false)&(a.checked==false)){

			a.checked=true;
			b.checked=true;
			c.checked=true;
			d.checked=true;
		}
	}
	
	function get_oper_squares(){
		console.log('inside get_oper_squares');
		if (!document.getElementById('square_mode').checked)
		{return}
		document.getElementById('square_mode').disabled = true;
		param_dic = get_boarders();
		param_dic['homes'] = document.getElementById('sq_homes').checked;
		param_dic['works'] = document.getElementById('sq_works').checked;
		param_dic['male'] = document.getElementById('sq_male').checked;
		param_dic['female'] = document.getElementById('sq_female').checked;

		param_dic['users_min'] = document.getElementById('sq_users').valueLow;
		param_dic['users_max'] = document.getElementById('sq_users').valueHigh;
		param_dic['income_max'] = document.getElementById('sq_income').valueHigh;
		param_dic['income_min'] = document.getElementById('sq_income').valueLow;
		param_dic['age_max'] = document.getElementById('sq_age').valueHigh;
		param_dic['age_min'] = document.getElementById('sq_age').valueLow;
		param_dic['to_mean'] = document.getElementById('pivot').value;
		console.log(param_dic);
		$.get(oper_squares_url,param_dic).then(function(response) {
			
			
			console.log(document.getElementById('heat_map').checked);
			var max_result = response['max_result'];
			geojsonfeatures = response['oper_squares'].map(function(el){
				var center = [el['x'],el['y']];
				var half_side = 445;
				list_of_coords1 = [
									[center[0]-half_side,center[1]-half_side],
									[center[0]-half_side,center[1]+half_side],
									[center[0]+half_side,center[1]+half_side],
									[center[0]+half_side,center[1]-half_side],
									[center[0]-half_side,center[1]-half_side],
								]

				return {	
						  'type': 'Feature',
						  'geometry': {
							'type': 'Polygon',
							'coordinates': [
												list_of_coords1
										   ]
						  },
						  
						  "properties": {
							'result_rate':Math.log(el['result']+1)/Math.log(max_result+1),
							'info': el['pretty_result']
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
		  console.log(geojsonfeatures[0]);
		 features = (new ol.format.GeoJSON()).readFeatures(geojsonObject);
		 
		 var oper_squares_source = new ol.source.Vector({
			features: features,
			// style: compute_oper_square_style
		  });
		oper_squares_layer.setSource(oper_squares_source);		
		document.getElementById('square_mode').disabled = false;
		console.log('end');
		})
	}
