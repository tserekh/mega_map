function searchAddress() {
    var bbox = "36.498210,55.271105~38.459270,56.141082";
    var geocode_url_pattern = "https://geocode-maps.yandex.ru/1.x/?format=json&apikey=48c10c45-c431-4e27-9bd7-3ff2563f5bb9&box=" + bbox + "&geocode=";
    var search_address = document.getElementById("searchAddress").value;
    var geocode_url = geocode_url_pattern + search_address;
    $.get(geocode_url).then(function (response) {
        var info_text = '';
        var GeoObjectCollection = response['response']['GeoObjectCollection'];
        console.log(GeoObjectCollection['metaDataProperty']['GeocoderResponseMetaData']['found']);
        if (GeoObjectCollection['metaDataProperty']['GeocoderResponseMetaData']['found'] == "0") {
            console.log("Ничего не нашлось");
            info_text = 'Ничего не нашлось';
        } else {
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
            'info': info_text,
            radius: 10,
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

function compute_search_address_style(feature, fill_color) {
    var style_dic = {};
    style_dic['image'] = new ol.style.Icon({
        radius: feature.get('radius'),
        anchor: [0.5, 0.5],
        size: [200, 200],
        offset: [0, 0],
        opacity: 1,
        scale: 0.2,
        src: decodeURIComponent("/static/icons/placeholder.png")
    })
    return new ol.style.Style(style_dic);
}
