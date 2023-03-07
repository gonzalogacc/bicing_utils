from get_station_info import get_stations
from geopy import distance

def read_coordinates(coords_file: str):
    with open(coords_file, 'r') as f:
        data = f.read().strip()
        return data.split(',')

def get_station_dict():
    stations = get_stations()
    station_dict = {}
    for station in stations['stations']:
        station_dict[station['id']] = station
    return station_dict

def get_closer_station(stations: {}, lat: float, lon: float):
    
    sation_distances = []
    for id, station in stations.items():
        dd = distance.distance((lat, lon), (station['latitude'], station['longitude'])).m
        sation_distances.append((station['id'], dd))

    station_distances = sorted(sation_distances, key=lambda x: x[1])
    return station_distances

if __name__ == '__main__':
    lat, lon = read_coordinates("./coordinates.txt")
    stations = get_station_dict()
    close_stations = get_closer_station(stations, lat, lon)

    for id, dist in close_stations[:5]:
        if stations[id]['electrical_bikes'] == 0:
            continue
        print(f"La estación {id} está a {dist:.1f} metros y tiene {stations[id]['electrical_bikes']} bicis eléctricas, Direccion: {stations[id]['streetName']}")
