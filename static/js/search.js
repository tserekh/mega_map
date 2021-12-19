function geocode_coords(search_address) {
    var bbox = "36.498210,55.271105~38.459270,56.141082";
    var geocode_url_pattern = "https://geocode-maps.yandex.ru/1.x/?format=json&apikey=48c10c45-c431-4e27-9bd7-3ff2563f5bb9&box=" + bbox + "&geocode=";
    var geocode_url = geocode_url_pattern + search_address;
    console.log(geocode_url)
    response = $.getJSON(geocode_url);
    console.log(response.responseJSON)
    response.display
    var info_text = '';
    var GeoObjectCollection = response["responseJSON"]['response']['GeoObjectCollection'];
    if (GeoObjectCollection['metaDataProperty']['GeocoderResponseMetaData']['found'] === "0") {
        console.log("Ничего не нашлось");
        info_text = 'Ничего не нашлось';
    } else {
        GeoObject = GeoObjectCollection['featureMember'][0]['GeoObject'];
        info_text = GeoObject['metaDataProperty']['GeocoderMetaData']['Address']['formatted'];
        coords = GeoObject['Point']['pos'].split(' ');
        coords = coords.map(parseFloat);
        coords = ol.proj.fromLonLat(coords);
    }
    return coords
}

    function get_route() {
        let address_from = document.getElementById("searchAddressFrom").value;
        let address_to = document.getElementById("searchAddressTo").value;
        param_dic = {}
        param_dic['address_from'] = address_from
        param_dic['address_to'] = address_to
        $.get(route_url, param_dic).then(function (response) {
        coords1 = geocode_coords(search_address1)
        coords2 = geocode_coords(search_address2)
        geom1 = new ol.geom.Point(coords1)
        geom2 = new ol.geom.Point(coords2)
        view.animate({
            center: [(coords1[0] + coords2[0]) / 2, (coords1[1] + coords2[1]) / 2,],
            duration: 500,
            zoom: 15
        })

        document.getElementById("select_bar").style.display = "none";
        document.getElementById("describe_bar").style.display = "block";
        document.getElementById("bar").style.display = "block";
        document.getElementById("describe").innerHTML = info_text;

        feature = new ol.Feature({
            'geometry': geom,
            'info': info_text,
            radius: 10,
        });
        features = [
            ol.Feature({
                'geometry': geom1,
                'info': info_text,
                radius: 10,
            }),
            ol.Feature({
                'geometry': geom2,
                'info': info_text,
                radius: 10,
            }),
        ];
        var source = new ol.source.Vector({
            features: features,
            wrapX: false,
            style: compute_search_address_style
        });
        search_address_layer.setSource(source);
    }


    function compute_search_address_style(feature) {
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

