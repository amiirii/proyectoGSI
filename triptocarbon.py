import json
import requests
from enum import Enum

class FuelType(Enum):
    motorGasoline = "motorGasoline"
    diesel = "diesel"
    aviationGasoline = "aviationGasoline"
    jetFuel = "jetFuel"

class Mode(Enum):
    dieselCar = "dieselCar"
    petrolCar = "petrolCar"
    anyCar = "anyCar"
    taxi = "taxi"
    economyFlight = "economyFlight"
    businessFlight = "businessFlight"
    firstclassFlight = "firstclassFlight"
    anyFlight = "anyFlight"
    motorbike = "motorbike"
    bus = "bus"
    transitRail = "transitRail"

class TTCException(Exception):
    pass

class TripToCarbon:

    litres_gallon = 4.54609
    km_mile = 1.609344

    def __init__(self, api_key=None, url="https://api.triptocarbon.xyz/v1/footprint"):
        self.api_key = api_key
        self.url = url

    def _request(self, **kwargs):
        req_url = self.url + '?' + '&'.join(['{}={}'.format(k, v) for k, v in kwargs.items()])
        response = requests.get(req_url)

        response_obj = json.loads(response.text)

        if response.status_code == 200:
            if 'carbonFootprint' in response_obj:
                return response_obj['carbonFootprint']
            else:
                raise TTCException()

        elif response.status_code == 400:
            if 'errorMessage' in response_obj:
                if 'invalidParameters' in response_obj:
                    raise TTCException('{}. Parameters: {}'.format(response_obj['errorMessage'], response_obj['invalidParameters']))
                else:
                    raise TTCException(response_obj['errorMessage'])
        
    def huella_consumo_combustible(self, litros, combustible, cod_pais="def"):
        return self._request(activity=litros / TripToCarbon.litres_gallon, activityType="fuel", country=cod_pais, fuelType=combustible.value)

    def huella_km_recorridos(self, km, combustible, vehiculo, cod_pais="def"):
        return self._request(activity=km / TripToCarbon.km_mile, activityType="miles", country=cod_pais, fuelType=combustible.value, mode=vehiculo.value)

if __name__ == '__main__':
    ttc = TripToCarbon()
    print(ttc.huella_consumo_combustible(54, FuelType.jetFuel))
    print(ttc.huella_km_recorridos(50, FuelType.diesel, Mode.dieselCar))
