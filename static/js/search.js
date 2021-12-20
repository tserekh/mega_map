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
