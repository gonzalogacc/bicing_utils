import os

import pytest

from src.bicing import BicingClient
from src.schemas import Station, BicingStationsResponse, Coordinates
import json
from tests.test_fixtures import bicing_test_API


def test_Station_object():
    estacion = {
        "id": "519",
        "type": "BIKE",
        "latitude": 41.4246548,
        "longitude": 2.166289,
        "streetName": "C/ PEDRELL, 52",
        "streetNumber": "",
        "slots": 18,
        "bikes": 5,
        "type_bicing": 2,
        "electrical_bikes": 5,
        "mechanical_bikes": 0,
        "status": 1,
        "disponibilidad": 25,
        "icon": "/modules/custom/mapa_disponibilitat/assets/icons/ubicacio-25.png",
        "transition_start": "",
        "transition_end": ""
    }

    station = Station(**estacion)
    assert station.id == 519


def test_Station_object_no_coordinates():
    estacion = {
        "id": "519",
        "type": "BIKE",
        "latitude": "",
        "longitude": "",
        "streetName": "C/ PEDRELL, 52",
        "streetNumber": "",
        "slots": 18,
        "bikes": 5,
        "type_bicing": 2,
        "electrical_bikes": 5,
        "mechanical_bikes": 0,
        "status": 1,
        "disponibilidad": 25,
        "icon": "/modules/custom/mapa_disponibilitat/assets/icons/ubicacio-25.png",
        "transition_start": "",
        "transition_end": ""
    }

    station = Station(**estacion)
    assert station.id == 519
    assert station.longitude == 0
    assert station.latitude == 0


def test_BicingStationsResponse():
    response = json.loads(open(os.path.join(os.getcwd(), "bicing_stations_response.json")).read())
    station_response = BicingStationsResponse(**response)
    assert len(response['stations']) == len(station_response.stations), "Wrong station number"
    assert int(response['stations'][0]['id']) == station_response.stations[0].id
    assert float(response['stations'][0]['latitude']) == station_response.stations[0].latitude
    assert float(response['stations'][0]['longitude']) == station_response.stations[0].longitude


def test_get_sort_station_distance(bicing_test_API):
    bc = BicingClient()
    bc._httpx_client = bicing_test_API  ## Replace the real client for the fixture (to avoid the http request)
    my_location = Coordinates(latitude=41.3842634, longitude=2.1692556)  ## station 51
    stations = bc.get_sort_station_distance(my_location)
    assert stations[0].id == 51
    ## Distance always increases
    assert all(x.distance <= y.distance for x, y in zip(stations, stations[1:])), "Distance is not ever increasing"


def test_get_stations():
    bc = BicingClient()
    response = bc.get_stations()
    print(response)
    assert 1 == 2
