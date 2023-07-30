import requests
from dataclasses import dataclass
from typing import List
import os
from dotenv import load_dotenv
import urllib

load_dotenv()

## Get API key from env
## Do some self testing to check the api key
GMAP_API_KEY = os.getenv("GMAP_API_KEY", None)
if GMAP_API_KEY is None:
    raise Exception("No api key")

class Marker:
    def __init__(self, *, 
                 lat, 
                 lon,
                 **kwargs
        ):
        self.lat = lat
        self.lon = lon
    
        self.style = {}
        self.style["size"] = "mid"
        self.style["color"] = "red"
        valid_args = ["size", "color", "label"]
        for k, v in kwargs.items():
            if k not in valid_args:
                continue
            self.style[k] = v     

    def to_params(self):
        marker_style = "|".join([f"{k}:{v}" for k, v in self.style.items()])
        return urllib.parse.quote(f"{marker_style}|{self.lat},{self.lon}")


def _compose_markers(markers: List[Marker]):
    marker_string=""
    for m in markers:
        marker_string += f"&markers={m.to_params()}"
    return marker_string


class MapConf:

    def __init__(self, *, 
                 lat: float,
                 lon: float,
                 zoom: int = 15, 
                 size: int = 512, 
                 maptype: str = "roadmap"
        ):
        self.params_dict = {}
        self.params_dict["center"] = f"{lat},{lon}"
        self.params_dict["zoom"] = zoom
        self.params_dict["size"] = f"{size}x{size}"
        self.params_dict["maptype"] = maptype


    def to_params(self):
        return f"&{urllib.parse.urlencode(self.params_dict)}"


def get_static_map(markers=[]):
    

    base_url = "https://maps.googleapis.com"
    url_path = "/maps/api/staticmap"
    
    ## Compute map center
    min_lat = min([m.lat for m in markers])
    max_lat = max([m.lat for m in markers])
    center_lat = (max_lat + min_lat) / 2.0
    min_lon = min([m.lon for m in markers])
    max_lon = max([m.lon for m in markers])
    center_lon = (max_lon + min_lon) / 2.0

    map_conf = MapConf(lat=center_lat, lon=center_lon).to_params()

    marker_conf = _compose_markers(markers)
    params = f"key={GMAP_API_KEY}{map_conf}{marker_conf}"

    map_url = urllib.parse.urljoin(base_url, url_path)
    map_url += f"?{params}"
    print(map_url)
    response = requests.get(map_url, stream=True)
    filename = "mapita.png"
    response.raw.decode_content = True

    with open(f'{filename}', 'wb') as outfile:
       outfile.write(response.content)
       
    return None

if __name__ == "__main__":
    response = get_static_map(markers = [Marker(lat = 41.38, lon = 2.18, label="2"), Marker(lat = 41.3805, lon=2.1805, label="3")])
    print(response)


