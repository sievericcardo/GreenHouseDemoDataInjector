from typing import Iterable, Optional, Union

from influxdb_client import Bucket, InfluxDBClient, Point
from influxdb_client.client.exceptions import InfluxDBError
from influxdb_client.client.write_api import SYNCHRONOUS

from injector.config import CONFIG_PATH


class InfluxController:
    """
    Singleton class that handles the connection to InfluxDB.
    Attributes:
        _instance: the singleton instance
        _client: the InfluxDB client used to interact with the database
    """

    # https://influxdb-client.readthedocs.io/en/latest/

    _instance = None
    _client: InfluxDBClient = InfluxDBClient.from_config_file(CONFIG_PATH)

    def __new__(cls):
        """
        Create a new instance of the class if it does not exist, otherwise return the existing one
        """
        if cls._instance is None:
            cls._instance = super(InfluxController, cls).__new__(cls)

        return cls._instance

    def delete_bucket(self, bucket_name: str) -> bool:
        """
        Delete a bucket from InfluxDB by name
        :return: True if bucket was deleted, False if bucket does not exist
        """
        bucket = self.get_bucket(bucket_name)
        if bucket is None:
            return False

        self._client.buckets_api().delete_bucket(bucket)
        return True

    def get_bucket(self, bucket_name: str) -> Optional[Bucket]:
        """
        Get a bucket from InfluxDB by name
        :return: bucket if found, None otherwise
        """
        return self._client.buckets_api().find_bucket_by_name(bucket_name)

    def create_bucket(self, bucket_name: str) -> Bucket:
        """
        Create a new bucket in InfluxDB with name bucket_name if it does not exist,
        otherwise return the existing one
        :return: the new bucket if created, the existing bucket otherwise
        """
        bucket = self.get_bucket(bucket_name)
        if bucket is not None:
            return bucket

        return self._client.buckets_api().create_bucket(bucket_name=bucket_name)

    def write_point(self, point: Union[Point, Iterable[Point]], bucket: Bucket) -> bool:
        """
        Write a Point or Iterable of Points to bucket
        :param point: measurement to write
        :param bucket: bucket to write to
        :return: True if write was successful, False otherwise
        """
        try:
            if (
                self._client.write_api(write_options=SYNCHRONOUS).write(
                    bucket=bucket.name, org=self._client.org, record=point
                )
                is None
            ):
                return True
            return False
        except InfluxDBError as e:
            print("Error while writing point in influxController.write_point: ", e)
            return False

    def close(self):
        self._client.close()
