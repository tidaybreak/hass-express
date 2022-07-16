"""Config flow for Hello World integration."""
import logging
import json
import voluptuous as vol

from homeassistant import config_entries

from .const import DOMAIN
from homeassistant.core import callback

_LOGGER = logging.getLogger(__name__)

DATA_SCHEMA = vol.Schema({
    vol.Required("name", default = ""): str,
    vol.Required("auth", default = ""): str
})


class ConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):

    VERSION = 1
    CONNECTION_CLASS = config_entries.CONN_CLASS_CLOUD_POLL

    async def async_step_user(self, user_input=None):        
        errors = {}
        # 如果输入内容不为空，则进行验证
        if user_input is not None:
            express = user_input['name']
            if express not in ["鸟箱", "喜兔"]:
                return self.async_abort(reason="not_support_express")

            return self.async_create_entry(title=user_input['name'], data=user_input)
        
        # 显示表单
        return self.async_show_form(
            step_id="info", data_schema=DATA_SCHEMA, errors=errors
        )

    @staticmethod
    @callback
    def async_get_options_flow(config_entry):
        """Get the options flow for this handler."""
        return OptionsFlowHandler(config_entry)

class OptionsFlowHandler(config_entries.OptionsFlow):
    def __init__(self, config_entry: config_entries.ConfigEntry) -> None:
        """Initialize options flow."""
        self.config_entry = config_entry
        self._all_config = config_entry.data.copy()
        self._steps = []


    async def async_step_init(self, user_input=None):
        errors = {}
        #_LOGGER.info("self._all_config:%s", self._all_config)

        if user_input is not None:
            self._all_config.update(user_input)
            self.hass.config_entries.async_update_entry(self.config_entry, data=self._all_config)
            await self.hass.config_entries.async_reload(self.config_entry.entry_id)
            return self.async_abort(reason="success")
            #return self.async_create_entry(title="", data=user_input)

        DATA_SCHEMA_UPDATE = vol.Schema({
                   vol.Required("auth", default = self._all_config['auth']): str

        })
        return self.async_show_form(
            step_id="init", data_schema=DATA_SCHEMA_UPDATE, errors=errors
        )


