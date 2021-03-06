
function get_homes() {
    if (document.getElementById("homes").checked) {
        document.getElementById("homes").disabled = true;
        $.get(home_url, param_dic).then(function (response) {
            let features = get_home_features(response['homes']);
            let source = new ol.source.Vector({
                    features: features,
                    wrapX: false
                });
                home_layer.setSource(source);
                map.addLayer(home_layer);
                document.getElementById("homes").disabled = false;
            }
        )
    } else {
        map.removeLayer(home_layer);
    }
}

function get_home_features(data) {
    var features = new Array(data.length);
    for (var i = 0; i < data.length; ++i) {
        point = [data[i]["x"], data[i]["y"]];
        geom = new ol.geom.Point(point);
        address = data[i]["address"];
        flat_num = data[i]["flat_num"];
        flat_num = Math.round(2.7 * flat_num);
        sale_price = data[i]["sale_price"];
        min_distance = data[i]["min_distance"];
        min_distance_metro = data[i]["min_distance_metro"];
        chain_name = data[i]["chain_name"];


        feature = new ol.Feature({
            'geometry': geom,
            radius: 10,
            'info': 'Жителей: ' + flat_num + '<br/>' + chain_name,
            'chain_name': chain_name,
            'name': nFormatter(flat_num),
            'min_distance': parseFloat(min_distance),
            'min_distance_metro': min_distance_metro
        });
        feature.setStyle(compute_home_style(feature));
        features[i] = feature;
    }
    return features
}

function compute_home_style(feature) {

    chain_name = ''
    min_distance = feature.get('min_distance')
    var fill_color = 'green';
    stroke = null;

    style_dic = {}
    style_dic['image'] = new ol.style.Circle({
        radius: 7 + feature.get('name').toString().length,
        fill: new ol.style.Fill({
            color: fill_color
        }),
    })

    style_dic['text'] = new ol.style.Text({
        font: '10px helvetica,sans-serif',
        text: feature.get('name') + chain_name,
        fill: new ol.style.Fill({
            color: 'white',
        }),
        'stroke': stroke,

    })
    return new ol.style.Style(style_dic);
}
