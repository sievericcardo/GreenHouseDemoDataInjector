from sys import argv, path
from typing import Optional

from influxdb_client import Bucket

from pathlib import Path
# path.append("..")
path.append(str(Path(__file__).resolve().parent.parent))  # add parent directory to system path


from influx.influx_controller import InfluxController
from test.random_measurements import (
    GREENHOUSE_MEASUREMENTS,
    PLANT_MEASUREMENTS,
    POT_MEASUREMENTS,
    PUMP_MEASUREMENTS,
    SHELF_MEASUREMENTS,
)


def main(bucket_name: str, num_measurements: Optional[int] = 5):
    influx_controller = InfluxController()
    # if bucket does not exist create it
    bucket: Bucket = influx_controller.get_bucket(
        bucket_name
    ) or influx_controller.create_bucket(bucket_name)

    # get dummy measurement for each asset
    greenhouse_measurements = GREENHOUSE_MEASUREMENTS[:num_measurements]
    shelf_measurements = SHELF_MEASUREMENTS[:num_measurements]
    pump_measurements = PUMP_MEASUREMENTS[:num_measurements]
    pot_measurements = POT_MEASUREMENTS[:num_measurements]
    plant_measurements = PLANT_MEASUREMENTS[:num_measurements]

    # write measurements to influx
    influx_controller.write_point(greenhouse_measurements, bucket)
    influx_controller.write_point(shelf_measurements, bucket)
    influx_controller.write_point(pump_measurements, bucket)
    influx_controller.write_point(pot_measurements, bucket)
    influx_controller.write_point(plant_measurements, bucket)


if __name__ == "__main__":
    """
    Loads random data into the specified bucket.
    Usage: python load_random_data.py <bucket_name>
        or python load_random_data.py <bucket_name> <num_measurements>
    """
    if len(argv) == 2:
        print("Loading 5 measurements per asset...")
        main(argv[1])
    elif len(argv) == 3:
        print(f"Loading {argv[2]} measurements per asset...")
        main(argv[1], int(argv[2]))
    else:
        print(
            "Usage: python load_random_data.py <bucket_name> or python load_random_data.py <bucket_name> "
            "<num_measurements>"
        )
        exit(1)

    exit()
