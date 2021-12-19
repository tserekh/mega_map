function compute_metro_style(feature, fill_color) {
    return new ol.style.Style({
        image: new ol.style.Icon({
            radius: feature.get('radius'),
            anchor: [0.5, 0.5],
            size: [200, 200],
            offset: [0, 0],
            opacity: 1,
            scale: 0.2,
            src: decodeURIComponent("/static/map_icons/metro-moskva-logo.png")
        })
    });
}
