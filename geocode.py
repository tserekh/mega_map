import os
from typing import Tuple, Union

import requests
from dotenv import load_dotenv

load_dotenv()

GEOCODE_URL = "https://geocode-maps.yandex.ru/1.x/"
BBOX = "36.498210,55.271105~38.459270,56.141082"


def geocode(address: str) -> Union[None, Tuple[float, float]]:
    api_key = os.environ.get("YANDEX_GEOCODER_API_KEY")
    if not api_key:
        raise RuntimeError(
            "Не задан YANDEX_GEOCODER_API_KEY: добавьте ключ в переменные окружения или в .env"
        )

    response = requests.get(
        GEOCODE_URL,
        params={
            "format": "json",
            "apikey": api_key,
            "box": BBOX,
            "geocode": address,
        },
        timeout=10,
    )
    response.raise_for_status()
    GeoObjectCollection = response.json()["response"]["GeoObjectCollection"]
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
