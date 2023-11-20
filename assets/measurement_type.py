from enum import Enum

ASSET_MODEL_PREFIX = "ast:"  # Prefix for asset model measurements


class MeasurementType(Enum):
    """
    Enum containing measurement types: greenhouse, shelf, pump, pot, plant
    """

    GREENHOUSE = "greenhouse"
    SHELF = "shelf"
    PUMP = "pump"
    POT = "pot"
    PLANT = "plant"

    """
    Returns the measurement name for a given measurement type. It adds the asset model prefix to the measurement type
    """

    def get_measurement_name(self):
        # Adding the asset model prefix to the measurement type allows for easier querying
        return ASSET_MODEL_PREFIX + self.value
