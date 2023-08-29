from typing import List

import httpx
from geopy import distance

from src.schemas import Coordinates, BicingStationsResponse, Station


class BicingClient:

    def __init__(self):
        self._httpx_client = httpx.Client(
            base_url="https://www.bicing.barcelona",
            headers={}
        )

    def get_stations(self):
        response = self._httpx_client.get("/es/get-stations")
        print(response)
        assert response.status_code == 200
        return BicingStationsResponse(**response.json())

    def get_sort_station_distance(self, coordinates: Coordinates) -> List[Station]:
        stations = self.get_stations().stations
        for station in stations:
            dd = distance.distance(
                (coordinates.latitude, coordinates.longitude),
                (station.latitude, station.longitude)
            )
            station.distance = dd
        return sorted(stations, key=lambda x: x.distance)