"""Support for Express binary sensor."""

from homeassistant.components.binary_sensor import DEVICE_CLASSES, BinarySensorEntity

from .const import DOMAIN
from .express_device import ExpressDevice


async def async_setup_entry(hass, config_entry, async_add_entities):
    """Set up the Express binary_sensors by config_entry."""
    async_add_entities(
        [
            ExpressBinarySensor(
                device,
                hass.data[DOMAIN][config_entry.entry_id]["coordinator"],
            )
            for device in hass.data[DOMAIN][config_entry.entry_id]["devices"][
                "binary_sensor"
            ]
        ],
        True,
    )


class ExpressBinarySensor(ExpressDevice, BinarySensorEntity):
    """Implement an Express binary sensor for parking and charger."""

    @property
    def device_class(self):
        """Return the class of this binary sensor."""
        return (
            self.express_device.sensor_type
            if self.express_device.sensor_type in DEVICE_CLASSES
            else None
        )

    @property
    def is_on(self):
        """Return the state of the binary sensor."""
        return self.express_device.get_value()
