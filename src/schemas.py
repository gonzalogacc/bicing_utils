from enum import Enum
from typing import Optional, List, Any, Annotated

from pydantic import BaseModel, BeforeValidator
from pydantic_core.core_schema import ValidationInfo


class Coordinates(BaseModel):
    latitude: float
    longitude: float


def make_validator(label: str):
    def validator(v: Any, info: ValidationInfo) -> Any:
        if v == "":
            v = 0
        return v

    return validator


## Not set latlong values are converted to 0
Latitude = Annotated[float, BeforeValidator(make_validator('check-float'))]
Longitude = Annotated[float, BeforeValidator(make_validator('check-float'))]


class ResourceEnum(str, Enum):
    electrical_bikes = 'electrical_bikes'
    mechanical_bikes = 'mechanical_bikes'
    disponibilidad = 'disponibilidad'


class Station(BaseModel):
    id: int
    type: str
    latitude: Optional[Latitude]
    longitude: Optional[Longitude]
    streetName: Optional[str] = None
    streetNumber: Optional[str] = None
    slots: int
    bikes: int
    type_bicing: int
    electrical_bikes: int
    mechanical_bikes: int
    status: int
    disponibilidad: int
    icon: str
    transition_start: str
    transition_end: str
    distance: Optional[float] = None


class BicingStationsResponse(BaseModel):
    url_icon: Optional[str] = None
    url_icon2: Optional[str] = None
    url_icon3: Optional[str] = None
    url_icon4: Optional[str] = None
    url_icon5: Optional[str] = None
    url_icon6: Optional[str] = None
    url_icon7: Optional[str] = None

    estacions_icon: Optional[str] = None
    parametros_filtro: Optional[List] = []

    stations: List[Station]
