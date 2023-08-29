from geopy import distance

from src.bicing import BicingClient
from src.google_maps import Marker, get_static_map
from src.schemas import Coordinates

def read_coordinates(coords_file: str):
    with open(coords_file, 'r') as f:
        data = f.read().strip()
        coordinates = Coordinates(lat=data.split(',')[0], lon=data.split(',')[1])
        return coordinates

def get_station_dict():
    bc = BicingClient()
    stations = bc.get_stations()
    station_dict = {}
    for station in stations['stations']:
        station_dict[station['id']] = station
    return station_dict

def get_closer_station(stations: {}, lat: float, lon: float):
    
    sation_distances = []
    for id, station in stations.items():
        dd = distance.distance((lat, lon), (station['latitude'], station['longitude']))
        sation_distances.append((station['id'], dd))

    station_distances = sorted(sation_distances, key=lambda x: x[1])
    return station_distances

def find_bikes(lat, lon):
    stations = get_station_dict()
    close_stations = get_closer_station(stations, lat, lon)
    
    markers = []
    for id, dist in close_stations[:20]:
        if stations[id]['electrical_bikes'] == 0:
            continue
        ##print(f"La estación {id} está a {dist:.1f} metros y tiene {stations[id]['electrical_bikes']} bicis eléctricas, Direccion: {stations[id]['streetName']}")
        marker = Marker(
                lat = stations[id]["latitude"], 
                lon=stations[id]["longitude"], 
                label=stations[id]["electrical_bikes"]
        )
        markers.append(marker)
    map = get_static_map(markers)
    return map

if __name__ == '__main__':
    lat, lon = read_coordinates("./coordinates.txt")
    bikes = find_bikes(lat, lon)

    filename = "mapita.png"
    with open(f'{filename}', 'wb') as outfile:
       outfile.write(bikes)

