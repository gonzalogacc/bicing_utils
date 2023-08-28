import httpx

from src.schemas import Coordinates, BicingStationsResponse


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