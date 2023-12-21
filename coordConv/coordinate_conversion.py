import numpy as np

def lla_to_ecef(latitude, longitude, altitude):
    a = 6378137.0  # Semi-major axis of the Earth
    f = 1/298.257223563  # Flattening factor of the Earth

    e_squared = 2*f - f**2  # Eccentricity squared

    lat_rad = np.radians(latitude)
    lon_rad = np.radians(longitude)

    N = a / np.sqrt(1 - e_squared * np.sin(lat_rad)**2)

    x = (N + altitude) * np.cos(lat_rad) * np.cos(lon_rad)
    y = (N + altitude) * np.cos(lat_rad) * np.sin(lon_rad)
    z = (N * (1 - e_squared) + altitude) * np.sin(lat_rad)

    return x, y, z

def ecef_to_lla(x, y, z):
    a = 6378137.0  # Semi-major axis of the Earth
    f = 1/298.257223563  # Flattening factor of the Earth

    e_squared = 2*f - f**2  # Eccentricity squared
    e_prime_squared = e_squared / (1 - e_squared)  # Eccentricity prime squared

    lon_rad = np.arctan2(y, x)

    p = np.sqrt(x**2 + y**2)

    lat_rad = np.arctan2(z, p * (1 - f) + e_prime_squared * a)

    for _ in range(5):
        N = a / np.sqrt(1 - e_squared * np.sin(lat_rad)**2)
        new_lat_rad = np.arctan2(z + e_prime_squared * N * np.sin(lat_rad), p)
        if np.abs(new_lat_rad - lat_rad) < 1e-10:
            break
        lat_rad = new_lat_rad

    alt = p / np.cos(lat_rad) - N

    lat_deg = np.degrees(lat_rad)
    lon_deg = np.degrees(lon_rad)

    return lat_deg, lon_deg, alt

def lla_to_enu(latitude, longitude, altitude, ref_latitude, ref_longitude, ref_altitude):
    x, y, z = lla_to_ecef(latitude, longitude, altitude)
    ref_x, ref_y, ref_z = lla_to_ecef(ref_latitude, ref_longitude, ref_altitude)
    ref_longitude_rad,ref_latitude_rad=np.radians([ref_longitude,ref_latitude])

    sin_lon, cos_lon = np.sin(ref_longitude_rad), np.cos(ref_longitude_rad)
    sin_lat, cos_lat = np.sin(ref_latitude_rad), np.cos(ref_latitude_rad)

    r = np.array([
        [-sin_lon, cos_lon, 0],
        [-sin_lat * cos_lon, -sin_lat * sin_lon, cos_lat],
        [cos_lat * cos_lon, cos_lat * sin_lon, sin_lat]
    ])

    enu_coords = np.dot(r, np.array([x - ref_x, y - ref_y, z - ref_z]))

    return enu_coords

def lla_to_enu_flat(lat, lon, alt, ref_lat, ref_lon, ref_alt):
    lat_rad = np.radians(lat)
    lon_rad = np.radians(lon)
    ref_lat_rad = np.radians(ref_lat)
    ref_lon_rad = np.radians(ref_lon)

    # Constants for conversion
    meters_per_degree = 111319.9  # Meters per degree of latitude at the equator

    # Calculate ENU coordinates assuming a flat Earth
    east = (lon_rad - ref_lon_rad) * np.cos(lat_rad) * meters_per_degree
    north = (lat_rad - ref_lat_rad) * meters_per_degree
    up = alt - ref_alt

    return east, north, up


def enu_to_lla(east, north, up, ref_latitude, ref_longitude, ref_altitude):
    ref_x, ref_y, ref_z = lla_to_ecef(ref_latitude, ref_longitude, ref_altitude)

    delta_lon = ref_longitude
    sin_lon, cos_lon = np.sin(delta_lon), np.cos(delta_lon)
    sin_lat, cos_lat = np.sin(ref_latitude), np.cos(ref_latitude)

    r = np.array([
        [-sin_lon, cos_lon, 0],
        [-sin_lat * cos_lon, -sin_lat * sin_lon, cos_lat],
        [cos_lat * cos_lon, cos_lat * sin_lon, sin_lat]
    ])

    ecef_coords = np.dot(np.linalg.inv(r), np.array([east, north, up])) + np.array([ref_x, ref_y, ref_z])

    return ecef_to_lla(*ecef_coords)