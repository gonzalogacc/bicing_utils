import pytest
from src.get_station_info import BicingClient
from src.schemas import Station, BicingStationsResponse
import json

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
    response = json.loads(open("/Users/ggarcia/git_sources/bicing_utils/tests/bicing_stations_response.json").read())
    station_response = BicingStationsResponse(**response)
    assert len(response['stations']) == len(station_response.stations), "Wrong station number"

def test_get_stations():
    bc = BicingClient()
    response = bc.get_stations()
    print(response)
    assert 1 == 2