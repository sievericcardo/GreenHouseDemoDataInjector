"""
Used to initialize dummy measurements for testing purposes.
"""

from datetime import datetime
from typing import List

import numpy as np
from assets.measurement_type import MeasurementType
from influxdb_client import Point

start_time = datetime.now() - timedelta(days=30)
end_time = datetime.now()

time_data = np.linspace(start_time.timestamp(), end_time.timestamp(), 100)
light_data = np.linspace(0, 1, 100)
temp_data = np.linspace(20, 30, 100)
humidity_data = np.linspace(0, 100, 100)
pumpd_water_data = np.linspace(0, 100, 100)
# For moist data we want to start from 90, then go down to 50, then go up to 90 again using a linear function of -10/3x + 90 (x is the time that passes) with noise that will not make it perfectly linear
# The function is given by empirical observation of the data
moist_data = np.concatenate(
    (
        np.linspace(90, 50, 50),
        np.linspace(50, 90, 50),
    )
)
# moist_data = np.linspace(0, 100, 100)
ndvi_data = np.linspace(-1, 1, 100)
growth_data = np.linspace(0, 100, 100)

np.random.seed(42)
ones_and_twos = np.random.choice([1, 2], size=100, replace=True)
left_and_right = np.random.choice(["left", "right"], size=100, replace=True)

GREENHOUSE_MEASUREMENTS: List[Point] = [
    Point(MeasurementType.GREENHOUSE.get_measurement_name())
    .field("light", light)
    .time(datetime.fromtimestamp(ts))
    for light, ts in zip(light_data, time_data)
]

SHELF_MEASUREMENTS: List[Point] = [
    Point(MeasurementType.SHELF.get_measurement_name())
    .tag("shelf_floor", floor)
    .field("temperature", temp)
    .field("humidity", humidity)
    .time(datetime.fromtimestamp(ts))
    for floor, temp, humidity, ts in zip(
        ones_and_twos, temp_data, humidity_data, time_data
    )
]

PUMP_MEASUREMENTS: List[Point] = [
    Point(MeasurementType.PUMP.get_measurement_name())
    .tag("shelf_floor", shelf)
    .tag("group_position", group)
    .field("pumped_water", water)
    .time(datetime.fromtimestamp(ts))
    for shelf, group, water, ts in zip(
        ones_and_twos, left_and_right, pumpd_water_data, time_data
    )
]

POT_MEASUREMENTS: List[Point] = [
    Point(MeasurementType.POT.get_measurement_name())
    .tag("shelf_floor", shelf)
    .tag("group_position", group)
    .tag("pot_position", pot)
    .tag("plant_id", plant)
    .field("moisture", moist)
    .time(datetime.fromtimestamp(ts))
    for shelf, group, pot, plant, moist, ts in zip(
        ones_and_twos,
        left_and_right,
        left_and_right,
        ones_and_twos,
        moist_data,
        time_data,
    )
]

PLANT_MEASUREMENTS: List[Point] = [
    Point(MeasurementType.PLANT.get_measurement_name())
    .tag("plant_id", plant)
    .field("ndvi", ndvi)
    .time(datetime.fromtimestamp(ts))
    for plant, ndvi, growth, ts in zip(ones_and_twos, ndvi_data, time_data)
]
