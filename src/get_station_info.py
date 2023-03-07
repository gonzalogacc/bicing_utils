import requests

def get_stations():
    #url = 'https://gbfs.urbansharing.com/oslobysykkel.no/station_information.json'
    url  = "https://www.bicing.barcelona/es/get-stations"
    response = requests.post(url)
    if response.status_code == 200:
        return response.json()
    else:
        return None
