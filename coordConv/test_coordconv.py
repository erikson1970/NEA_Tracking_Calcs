import numpy as np
import pytest

from coordinate_conversion import lla_to_ecef, ecef_to_lla, lla_to_enu, enu_to_lla

def test_lla_to_ecef():
    # Test lla_to_ecef function
    lat, lon, alt = 37.7749, -122.4194, 0  # San Francisco coordinates
    x, y, z = lla_to_ecef(lat, lon, alt)
    assert np.isclose(x, -2694711.1599, rtol=1e-3)
    assert np.isclose(y, -4263217.8384, rtol=1e-3)
    assert np.isclose(z, 3881293.4406, rtol=1e-3)

def test_ecef_to_lla():
    # Test ecef_to_lla function
    x, y, z = -2694711.1599, -4263217.8384, 3881293.4406  # San Francisco ECEF coordinates
    lat, lon, alt = ecef_to_lla(x, y, z)
    assert np.isclose(lat, 37.7749, rtol=1e-3)
    assert np.isclose(lon, -122.4194, rtol=1e-3)
    assert np.isclose(alt, 0, rtol=1e-3)

def test_lla_to_enu():
    # Test lla_to_enu function
    lat, lon, alt = 37.7749, -122.4194, 0  # San Francisco coordinates
    ref_lat, ref_lon, ref_alt = 37.7749, -122.4194, 0  # Reference point at the same location
    east, north, up = lla_to_enu(lat, lon, alt, ref_lat, ref_lon, ref_alt)
    assert np.isclose(east, 0, rtol=1e-3)
    assert np.isclose(north, 0, rtol=1e-3)
    assert np.isclose(up, 0, rtol=1e-3)

def test_enu_to_lla():
    # Test enu_to_lla function
    east, north, up = 100, -100, 50  # Example ENU coordinates
    ref_lat, ref_lon, ref_alt = 37.7749, -122.4194, 0  # Reference point at San Francisco
    lat, lon, alt = enu_to_lla(east, north, up, ref_lat, ref_lon, ref_alt)
    assert np.isclose(lat, 37.7753, rtol=1e-3)
    assert np.isclose(lon, -122.4189, rtol=1e-3)
    assert np.isclose(alt, 50, rtol=1e-3)