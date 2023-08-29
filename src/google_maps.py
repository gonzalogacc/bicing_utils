import requests
from dataclasses import dataclass
from typing import List
import os
from dotenv import load_dotenv
import urllib
from urllib.parse import quote

load_dotenv()

## Get API key from env
## Do some self testing to check the api key
GMAP_API_KEY = os.getenv("GMAP_API_KEY", None)
if GMAP_API_KEY is None:
    raise Exception("No api key")


class Marker:
    def __init__(self, *, latitude, longitude, **kwargs):
        self.latitude = latitude
        self.longitude = longitude

        ## Set default values for markers
        self.style = {"size": "mid", "color": "red"}
        valid_args = ["size", "color", "label"]
        for k, v in kwargs.items():
            if k not in valid_args:
                continue
            self.style[k] = v

    def to_params(self):
        marker_style = "|".join([f"{k}:{v}" for k, v in self.style.items()])
        return quote(f"{marker_style}|{self.latitude},{self.longitude}")


def _compose_markers(markers: List[Marker]):
    marker_string = ""
    for m in markers:
        marker_string += f"&markers={m.to_params()}"
    return marker_string


class MapConf:

    def __init__(self, *, latitude: float, longitude: float, zoom: int = 15, size: int = 512, maptype: str = "roadmap"):
        self.params_dict = {"center": f"{latitude},{longitude}", "zoom": zoom, "size": f"{size}x{size}", "maptype": maptype}

    def to_params(self):
        return f"&{urllib.parse.urlencode(self.params_dict)}"


def get_static_map(markers=[]):
    base_url = "https://maps.googleapis.com"
    url_path = "/maps/api/staticmap"

    ## Compute map center
    min_lat = min([m.latitude for m in markers])
    max_lat = max([m.latitude for m in markers])
    center_lat = (max_lat + min_lat) / 2.0
    min_lon = min([m.longitude for m in markers])
    max_lon = max([m.longitude for m in markers])
    center_lon = (max_lon + min_lon) / 2.0

    map_conf = MapConf(latitude=center_lat, longitude=center_lon).to_params()

    marker_conf = _compose_markers(markers)
    params = f"key={GMAP_API_KEY}{map_conf}{marker_conf}"

    map_url = urllib.parse.urljoin(base_url, url_path)
    map_url += f"?{params}"
    print(map_url)
    response = requests.get(map_url, stream=True)
    response.raw.decode_content = True

    # filename = "mapita.png"
    # with open(f'{filename}', 'wb') as outfile:
    #   outfile.write(response.content)
    return response.content


if __name__ == "__main__":
    response = get_static_map(
        markers=[
            Marker(latitude=41.38, longitude=2.18, label="2"),
            Marker(latitude=41.3805, longitude=2.1805, label="3")
        ])

    filename = "mapita.png"
    with open(f'{filename}', 'wb') as outfile:
        outfile.write(response)
