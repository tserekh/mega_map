function get_sale_points() {
    return
    // if (!document.getElementById('show_sale_points').checked){
    // sale_points_layer.setSource(new ol.source.Vector())
    // fresh_sale_points_layer.setSource(new ol.source.Vector())
    // return
    // }
    param_dic = get_boarders();
    param_dic['delete_all'] = false;
    $.get(get_sale_points_url, param_dic).then(function (response) {
        console.log("Success!");
        console.log(response['sale_points']);
        var features = get_sale_points_features(response['sale_points']);
        var source = new ol.source.Vector({
            features: features,
            wrapX: false
        });
        sale_points_layer.setSource(source);
        console.log('input')
    })
}

function delete_all_sale_points() {
    param_dic = {};
    fresh_sale_points_layer.setSource(new ol.source.Vector());
    param_dic['delete_all'] = true;
    console.log('delete all points');
    $.get(get_sale_points_url, param_dic).then(get_sale_points())
}

function get_sale_points_features(data) {
    console.log('inside get_sale_points_features');

    var features = new Array(data.length);
    for (var i = 0; i < data.length; ++i) {
        point = [data[i]["x"], data[i]["y"]];
        geom = new ol.geom.Point(point);
        if (document.getElementById('sale_point1').checked) {
            var name = (Math.round(data[i]['revenue_pred_model1'] / 1000)).toString() + 'k';
        } else {
            var name = (Math.round(data[i]['revenue_pred_model2'] / 1000)).toString() + 'k';

        }
        feature = new ol.Feature({
            'geometry': geom,
            radius: 11,
            'info': 'М.Видео:' + data[i]['revenue_pred_model1'] + '</br>' + 'Эльдорадо:' + data[i]['revenue_pred_model2'] + '</br>' + data[i]['cann'],
            'name': name,
        });
        feature.setStyle(compute_sale_point_style(feature));
        features[i] = feature;
    }
    return features
}
