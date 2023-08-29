import os

from geopy import distance

from src.bicing import BicingClient
from src.google_maps import Marker, get_static_map
from src.schemas import Coordinates, ResourceEnum


def read_coordinates(coords_file: str):
    with open(coords_file, 'r') as f:
        data = f.read().strip()
        coordinates = Coordinates(latitude=float(data.split(',')[0].strip()), longitude=float(data.split(',')[1].strip()))
        return coordinates


if __name__ == '__main__':
    coords = read_coordinates(os.path.join(os.getcwd(), "../coordinates.txt"))
    bc = BicingClient()
    stations = bc.find_closest(ResourceEnum.electrical_bikes, coords)

    markers = []
    for station in stations:
        markers.append(Marker(latitude=station.latitude, longitude=station.longitude, label=station.electrical_bikes))

    response = get_static_map(markers=markers)
    filename = "mapita.png"
    with open(f'{filename}', 'wb') as outfile:
        outfile.write(response)
