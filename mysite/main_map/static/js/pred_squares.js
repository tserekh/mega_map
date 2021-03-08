 function compute_pred_square_style(feature) {

	console.log(feature);
	var perc_ = 1
	

	perc_ = Math.min(1, perc_);
	console.log(perc_);
	color_ = perc2rg(perc_);
	color_.push(0.5);
		return new ol.style.Style({

		  fill: new ol.style.Fill({
			color: color_,
			
		  }),

		})
}
function update_pred_square_style(){
	pred_squares_layer.setStyle(compute_pred_square_style);
	
}
function get_pred_squares(){
	console.log(document.getElementById('pred_squares').checked)
	if (!document.getElementById('pred_squares').checked){	
		pred_squares_layer.setSource(ol.source.Vector({}))
		return
		}
		param_dic = get_boarders();
		param_dic['cafe'] = document.getElementById("sale_point2").checked;
		$.get(pred_squares_url,param_dic).then(function(response) {
			
				
			console.log(response);


			geojsonfeatures = response.map(function(el){

				console.log(el);
				return {	
						  'type': 'Feature',
						  'geometry': {
							'type': 'Polygon',
							'coordinates': el
						  },
						  
						  "properties": {
							// 'driving':el['driving'],
							// 'foot':el['foot'],
							// 'info': 'Авто' + el['driving'] + '</br>' + 'Пешеходный' + el['foot']
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
			 
			 var pred_squares_source = new ol.source.Vector({
				features: features,
				style: compute_pred_square_style
			  });
			pred_squares_layer.setSource(pred_squares_source);		
			console.log('end');
		})

}
function pred_squares_show_hide()
	{
		
		if (document.getElementById('pred_squares').checked){
			$(document.getElementById('pred_squares_selecter')).show(200)
		}else
		{
			$(document.getElementById('pred_squares_selecter')).hide(200)
		}

	}
	
function switch_sale_point1()

{
	if (!document.getElementById('sale_point1').checked)
	{
		document.getElementById('sale_point1').checked = true;
		}
	document.getElementById('sale_point2').checked = false;
}

function switch_sale_point2()

{
	if (!document.getElementById('sale_point2').checked)
	{
		document.getElementById('sale_point2').checked = true;
		}
	document.getElementById('sale_point1').checked = false;
}