from sys import argv, path
from typing import Optional
import os
from threading import Thread
import socket # for hostname retrieval
import re # to split the hostname in letters and numbers

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
from queue import Subscriber

def __init__(self):
    self.moisture = 90


def __load_env_file(env_file_path=".env"):
    try:
        with open(env_file_path, "r") as file:
            for line in file:
                # Ignore lines that are empty or start with '#'
                if not line.strip() or line.startswith("#"):
                    continue

                # Split the line at the first '=' character
                key, value = line.strip().split("=", 1)

                # Set the environment variable
                os.environ[key] = value

    except FileNotFoundError:
        print(f"{env_file_path} not found. Make sure to create a .env file with your environment variables.")


def __wait_message():
    """
    Wait for a message from the broker
    """
    __load_env_file()
    url = os.getenv("URL")
    username = os.getenv("USER")
    password = os.getenv("PASS")

    # Get hostname for the queue
    hostname = socket.gethostname()
    r = re.compile("([a-zA-Z]+)([0-9]+)")
    m = r.match(hostname)
    # Match the tuple <T.i.A>
    queue_destination = "actuator.1.water"

    conn = stomp.Connection(host_and_ports=[(url, 61613)])
    conn.set_listener('', Subscriber(conn, conf, CONFIG_PATH))
    conn.connect(username, password, wait=True)
    conn.subscribe(destination=queue_destination, id=1, ack='auto')

    while 1:
        sleep(10)


def main(bucket_name: str, num_measurements: Optional[int] = 5):
    thread = Thread(target=__wait_message)
    thread.start()

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

