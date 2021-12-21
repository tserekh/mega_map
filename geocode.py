import json
from typing import Tuple, Union

import requests
from pyproj import Transformer


def geocode(address: str) -> Union[None, Tuple[float, float]]:
    bbox = "36.498210,55.271105~38.459270,56.141082"
    geocode_url_pattern = (
        "https://geocode-maps.yandex.ru/1.x/?format=json&apikey=48c10c45-c431-4e27-9bd7-3ff2563f5bb9&box="
        + bbox
        + "&geocode="
    )
    geocode_url = geocode_url_pattern + address
    response = json.loads(requests.get(geocode_url).content)
    GeoObjectCollection = response["response"]["GeoObjectCollection"]
    if (
        GeoObjectCollection["metaDataProperty"]["GeocoderResponseMetaData"]["found"]
        == "0"
    ):
        return None

    GeoObject = GeoObjectCollection["featureMember"][0]["GeoObject"]
    coords = GeoObject["Point"]["pos"].split(" ")
    lon = coords[0]
    lat = coords[1]
    return float(lat), float(lon)
