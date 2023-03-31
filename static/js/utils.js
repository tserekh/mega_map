function nFormatter(num, digits) {
    var si = [
        {value: 1, symbol: ""},
        {value: 1E3, symbol: "k"},
        {value: 1E6, symbol: "M"},
        {value: 1E9, symbol: "G"},
        {value: 1E12, symbol: "T"},
        {value: 1E15, symbol: "P"},
        {value: 1E18, symbol: "E"}
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


function compute_route_style(color) {
    linestyle = new ol.style.Style({
        stroke: new ol.style.Stroke({
            color: "blue",
            width: 3,
            opacity: 0.5,
        }),
    })
    return linestyle
}

function get_metro_features(data) {
    var features = [];
    for (var i = 0; i < data.length; ++i) {
        point = [data[i]["lon"], data[i]["lat"]];
        point = ol.proj.fromLonLat(point);
        geom = new ol.geom.Point(point);
        if (data[i]["exit_name"] !== undefined) {
            info = data[i]["exit_name"];
        } else {
            info = data[i]["station_name"];
        }

        feature = new ol.Feature({'geometry': geom, radius: 10, 'info': '<br/>' + info, name: ''});
        feature.setStyle(compute_metro_style(feature));
        features.push(feature);
    }
    return features;
}


//<!-- GET LAYER -->
function get_metro_layer(features) {
    var vectorSource = new ol.source.Vector({
        features: features,
        wrapX: false
    });


    return new ol.layer.Vector({
        source: vectorSource,
    });
}

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
    function balance(x, y) {
        if ((document.getElementById(x).checked === false) && (document.getElementById(y).checked === false)) {
            document.getElementById(x).checked = true;
            document.getElementById(y).checked = true;
        }
    }



    function back_bar() {
        document.getElementById("select_bar").style.display = "block";
        document.getElementById("describe_bar").style.display = "none";
    }

    function curtail_bar() {

        if (document.getElementById("curtail_bar").style.opacity === 1) {
            $(document.getElementById('bar')).show(200)
            document.getElementById("curtail_bar").style.backgroundImage = "url('/static/map_icons/angle-pointing-to-top.png')"
            document.getElementById("curtail_bar").style.opacity = ""
        } else {
            $(document.getElementById('bar')).hide(200);
            document.getElementById("curtail_bar").style.backgroundImage = "url('/static/map_icons/angle-pointing-to-buttom.png')";
            document.getElementById("curtail_bar").style.opacity = 1;
        }
    }

    function homes_settings_show_hide() {
        if (document.getElementById('homes').checked) {
            $(document.getElementById('homes_settings')).show(200);
        } else {
            $(document.getElementById('homes_settings')).hide(200);
        }
    }

    var vector = new ol.layer.Vector({
        source: new ol.source.Vector(),
        style: compute_new_point_style,
    });

    var ground_stop_layer = new ol.layer.Vector({
        source: new ol.source.Vector(),
        style: compute_oper_square_style
    });

    function get_ground_stop_features(data) {
        var features = [];
        for (var i = 0; i < data.length; ++i) {
            point = [data[i]["x"], data[i]["y"]];
            geom = new ol.geom.Point(point);
            feature = new ol.Feature(
                {
                    'geometry': geom,
                    radius: 10, 'info': 'Нет информации объекте',
                    'count': data[i]["count"],
                    'is_one': data[i]["is_one"]
                },);
            feature.setStyle(compute_ground_stop_style(feature));

            features.push(feature);
        }
        return features
    }

    function get_ground_stop_layer(features) {
        let vectorSource = new ol.source.Vector({
            features: features,
            wrapX: false
        });

        let vector = new ol.layer.Vector({
            source: vectorSource,
        });
        return vector
    }


    function compute_new_point_style(feature) {
        var fill_color = 'cyan';
        var style_dic = {}
        style_dic['image'] = new ol.style.Circle({
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
        if (feature.get('is_one') !== true) {
            style_dic['image'] = new ol.style.Circle({
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
        } else {
            style_dic['image'] = new ol.style.Icon({
                radius: feature.get('radius'),
                anchor: [0.5, 0.5],
                size: [128, 128],
                offset: [0, 0],
                opacity: 1,
                scale: 0.1,
                src: decodeURIComponent("/static/map_icons/bus-stop.png")
            })
        }
        return new ol.style.Style(style_dic);
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

    have_logos = {{have_logos}};
    metro_url = "{{ url_for('get_metros') }}"
    ground_stop_url = "{{ url_for('get_ground_stops') }}"
    home_url = "{{ url_for('get_homes') }}"
    route_url = "{{ url_for('get_route') }}"
    document.getElementById("search").addEventListener("keyup", function (event) {
        event.preventDefault();
        if (event.keyCode === 13) {
            get_route();
        }
    });

    let center_coord = [37.622504, 55.753215];
    center_coord = ol.proj.fromLonLat(center_coord);

    let map_layer = new ol.layer.Tile({
        source: new ol.source.OSM()
    })

    var view = new ol.View({
        center: center_coord,
        zoom: 11
    });

    sale_points_layer = new ol.layer.Vector({
        source: new ol.source.Vector()
    });

    fresh_sale_points_layer = new ol.layer.Vector({
        source: new ol.source.Vector()
    });
    search_address_layer = new ol.layer.Vector({
        source: new ol.source.Vector()
    });
    home_layer = new ol.layer.Vector({
        source: new ol.source.Vector()
    });

    var map = new ol.Map({
        layers: [
            map_layer,
            // home_layer,
            // orgs_layer,
            search_address_layer,
            {#ground_stop_layer#}
        ],
        target: document.getElementById('map'),
        view: view
    });

    function get_boarders() {
        var extent = map.getView().calculateExtent(map.getSize());
        min_coord = ol.proj.transform([extent[0], extent[1]], 'EPSG:3857', 'EPSG:4326');
        max_coord = ol.proj.transform([extent[2], extent[3]], 'EPSG:3857', 'EPSG:4326');

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

    $('input').change(function () {
        param_dic = get_boarders();
        value = $(this).val();
        if (value === 'metros') {
            if (document.getElementById(value).checked) {
                document.getElementById("metros").disabled = true;
                    $.get(metro_url, param_dic).then(function (response) {
                        var features = get_metro_features(response['metros']);
                        metro_layer = get_metro_layer(features);
                        map.addLayer(metro_layer);
                        document.getElementById("metros").disabled = false;
                    })
            } else {
                map.removeLayer(metro_layer);
            }
        }
        if (value === 'homes') {
            get_homes();
            document.getElementById("homes").disabled = false;
        }
        if (value === 'ground_stops') {
            if (document.getElementById(value).checked) {
                document.getElementById("ground_stops").disabled = true;
                $.get(ground_stop_url, param_dic).then(function (response) {
                    var features = get_ground_stop_features(response['ground_stops']);
                    ground_stop_layer = get_ground_stop_layer(features);
                    map.addLayer(ground_stop_layer);
                    document.getElementById("ground_stops").disabled = false;
                })
            } else {
                map.removeLayer(ground_stop_layer);
            }
        }


    });
    document.getElementsByClassName("ol-attribution")[0].style.display = 'none'
    map.on('moveend', function () {
        param_dic = get_boarders();
        param_dic['delete_all'] = false;
        if (document.getElementById("metros").checked) {
            $.get(metro_url, param_dic).then(function (response) {
                var features = get_metro_features(response['metros']);
                var source = new ol.source.Vector({
                    features: features,
                    wrapX: false
                });
                metro_layer.setSource(source);
            });
        }
        if (document.getElementById("homes").checked) {
            get_homes();
            document.getElementById("homes").disabled = false;
        }
        if (document.getElementById("ground_stops").checked) {
            document.getElementById("ground_stops").disabled = true;
            $.get(ground_stop_url, param_dic).then(function (response) {
                var features = get_ground_stop_features(response['ground_stops']);
                source = new ol.source.Vector({
                    features: features,
                    wrapX: false
                });

                ground_stop_layer.setSource(source)
                document.getElementById("ground_stops").disabled = false;
            });
        }
    });

    map.on('click', function (evt) {
        var feature = map.forEachFeatureAtPixel(evt.pixel,
        function (feature) {
            info = feature.get('info');
            if (feature.get('info') === undefined) {
                info = 'Нет информации об объекте';
            }
            document.getElementById("select_bar").style.display = "none";
            document.getElementById("describe_bar").style.display = "block";
            document.getElementById("bar").style.display = "block";
            document.getElementById("describe").innerHTML = info;
        });
    });