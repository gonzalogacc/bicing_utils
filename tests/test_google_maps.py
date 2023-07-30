import pytest
from src.google_maps import Marker, MapConf, _compose_markers

def test_marker_OK():
    """ create a marker correctly
    """
    m = Marker(lat=10.0001, lon=-10.0001)
    assert(m.lat == 10.0001)
    assert(m.lon == -10.0001)

def test_marker_no_named_args_ERROR():
    """ Function is not called naming arguments
    """
    with pytest.raises(TypeError):
        Marker(1.0001, -1.0001)

def test_marker_encode_ok():
    m = Marker(lat=10.0001, lon=-10.0001)
    encoded = m.to_params()
    assert(encoded == "size%3Amid%7Ccolor%3Ared%7C10.0001%2C-10.0001")

def test_MapConf_OK():
    expected = "&center=41.380636%2C2.188023&zoom=17&size=512x512&maptype=roadmap"
    center = Marker(lat=41.380636, lon=2.188023)
    mc = MapConf(lat = center.lat, lon = center.lon, zoom = 17)
    encoded = mc.to_params()
    assert(encoded == expected)

def test__compose_markers():
    m1 = Marker(lat=10.001, lon=-10.001, label="hola")
    m2 = Marker(lat=10.001, lon=-10.001, label="hola")
    murl = _compose_markers([m1, m2])
    print(murl)

    assert(1 == 1)
