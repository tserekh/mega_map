function compute_metro_style(feature,fill_color) {
	return new ol.style.Style({
	image: new ol.style.Icon({
		radius: feature.get('radius'),
	  anchor: [0.5, 0.5],
	  size: [200, 200],
	  offset: [0, 0],
	  opacity: 1,
	  scale: 0.2,
	  src:decodeURIComponent("/static/map_icons/metro-moskva-logo.png")
	})
	});
}
	
function switch_metro_shop_home1()

{
	if (!document.getElementById('two_points').checked)
	{
		document.getElementById('two_points').checked = true;
		}
	document.getElementById('three_points').checked = false;
}

function switch_metro_shop_home2()

{
	if (!document.getElementById('three_points').checked)
	{
		document.getElementById('three_points').checked = true;
		}
	document.getElementById('two_points').checked = false;
}
