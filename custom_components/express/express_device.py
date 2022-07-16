from functools import wraps
import logging
from typing import Any, Optional, Tuple

from homeassistant.const import ATTR_BATTERY_CHARGING, ATTR_BATTERY_LEVEL
from homeassistant.core import callback
from homeassistant.helpers import entity_registry as er
from homeassistant.helpers.update_coordinator import CoordinatorEntity
from homeassistant.util import slugify
#from expressjsonpy.exceptions import IncompleteCredentials

from .const import DOMAIN, ICONS

_LOGGER = logging.getLogger(__name__)


def device_identifier(express_device) -> Tuple[str, int]:
    # Note that Home Assistant types this to be
    # tuple[str, str] but since that would involve
    # migrating, it is not changed here.
    return (DOMAIN, express_device.id())


class ExpressDevice(CoordinatorEntity):

    def __init__(self, express_device, coordinator):
        super().__init__(coordinator)
        self.express_device = express_device
        self._name: str = self.express_device.name
        self._unique_id: str = slugify(self.express_device.uniq_name)
        self._attributes: str = self.express_device.attrs.copy()
        self.config_entry_id: Optional[str] = None
        self._attr_entity_registry_enabled_default = (
            self.express_device.enabled_by_default
        )

    @property
    def name(self):
        """Return the name of the device."""
        return self._name

    @property
    def unique_id(self) -> str:
        """Return a unique ID."""
        return self._unique_id

    @property
    def icon(self):
        """Return the icon of the sensor."""
        if self.device_class:
            return None

        return ICONS.get(self.express_device.type)

    @property
    def extra_state_attributes(self):
        """Return the state attributes of the device."""
        attr = self._attributes
        if self.express_device.has_battery():
            attr[ATTR_BATTERY_LEVEL] = self.express_device.battery_level()
            attr[ATTR_BATTERY_CHARGING] = self.express_device.battery_charging()
        return attr

    @property
    def device_info(self):
        """Return the device_info of the device."""
        if hasattr(self.express_device, "car_name"):
            return {
                "identifiers": {device_identifier(self.express_device)},
                "name": self.express_device.car_name(),
                "manufacturer": "Express",
                "model": self.express_device.car_type,
                "sw_version": self.express_device.car_version,
            }
        elif hasattr(self.express_device, "site_name"):
            return {
                "identifiers": {device_identifier(self.express_device)},
                "name": self.express_device.site_name(),
                "manufacturer": "Express",
            }
        return None

    async def async_added_to_hass(self):
        """Register state update callback."""
        self.async_on_remove(self.coordinator.async_add_listener(self.refresh))
        registry = er.async_get(self.hass)
        self.config_entry_id = registry.entities.get(self.entity_id).config_entry_id

    @callback
    def refresh(self) -> None:
        """Refresh the state of the device.

        This assumes the coordinator has updated the controller.
        """
        self.express_device.refresh()
        self._attributes = self.express_device.attrs.copy()
        self.async_write_ha_state()
