"""

"""
import logging, os
import json
from datetime import datetime, timedelta

import time
import asyncio
import async_timeout
import aiohttp

import voluptuous as vol

from homeassistant.helpers.aiohttp_client import async_get_clientsession
from homeassistant.helpers.event import async_track_time_interval

from homeassistant.helpers.entity import Entity
from homeassistant.const import (ATTR_ATTRIBUTION, TEMP_CELSIUS, CONF_NAME)
from homeassistant.util import Throttle
import homeassistant.helpers.config_validation as cv
import homeassistant.util.dt as dt_util

from .const import VERSION, ROOT_PATH, TELUSERS

_LOGGER = logging.getLogger(__name__)

TIME_BETWEEN_UPDATES = timedelta(seconds=300)

DEFAULT_TIME = dt_util.now()

CONF_CITY = "city"
CONF_APPKEY_NIAOXIANG = "idniaoxiang"

ATTR_CONDITION_CN = "condition_cn"
ATTR_UPDATE_TIME = "update_time"
ATTR_AQI = "aqi"
ATTR_hourly_express = "hourly_express"
ATTR_SUGGESTION = "suggestion"
ATTR_CUSTOM_UI_MORE_INFO = "custom_ui_more_info"

ATTRIBUTION = "来自鸟箱数据"

ATTR_FORECAST_PROBABLE_PRECIPITATION = 'probable_precipitation'

# 集成安装
async def async_setup_entry(hass, config_entry, async_add_entities):
    #hass.http.register_static_path(ROOT_PATH, hass.config.path('custom_components/ti_niaoxiang/local'), False)
    #hass.components.frontend.add_extra_js_url(hass, ROOT_PATH + '/ti_niaoxiang-card/ti_niaoxiang-card.js?ver=' + VERSION)
    #hass.components.frontend.add_extra_js_url(hass, ROOT_PATH + '/ti_niaoxiang-card/ti_niaoxiang-more-info.js?ver=' + VERSION)
	
    config = config_entry.data
    name = config.get(CONF_NAME)
    expres = config.get("name")
    auth = config.get("auth")

    
    #_LOGGER.error("-----------------:%s", name)
    if epores == '鸟箱':
        data = NiaoXiangData(hass, auth)
        await data.async_update(dt_util.now())  
        async_track_time_interval(hass, data.async_update, TIME_BETWEEN_UPDATES)
        async_add_entities([ExpresNiaoXiang(data, name)], True)
    elif expres == '喜兔':
        data = XiTuData(hass, auth)
        await data.async_update(dt_util.now())  
        async_track_time_interval(hass, data.async_update, TIME_BETWEEN_UPDATES)
        async_add_entities([ExpresXiTu(data, name)], True)


class ExpresNiaoXiang(Entity):
    """Representation of a weather condition."""

    def __init__(self, roller, object_id):
        """Initialize the  weather."""
        self._object_id = object_id
        self._total = None
        self._free_hour = 0
        self._free_minute = 0
        self._roller = roller
        self._msg = ''
        self._belong = ''
        self._time_last = ''
        self._time_api_expire = ''


    @property
    def device_info(self):
        """Return information to link this entity with the correct device."""
        return {"identifiers": {(DOMAIN, self._object_id)}}

    @property
    def available(self) -> bool:
        """Return True if roller and hub is available."""
        return True
        #return self._roller.online and self._roller.hub.online

    @property
    def name(self):
        """Return the name of the sensor."""
        return self._object_id

    @property
    def should_poll(self):
        """attention No polling needed for a demo weather condition."""
        return True

    @property
    def state(self):
        """Return the weather condition."""
        return 'ok'

    @property
    def attribution(self):
        """Return the attribution."""
        return 'Powered by Home Assistant'

    @property
    def state_attributes(self):
        attributes = dict()
        """设置其它一些属性值."""
        attributes.update({
                "total": self._total,
                "free_hour": self._free_hour,
                "free_minute": self._free_minute,
                "msg": self._msg,
                "belong": self._belong,
                "cookie": self._roller._cookie,
                "time_last": self._time_last,
                "time_api_expire": self._time_api_expire
            })
        return attributes

    @property
    def total(self):
        """Return the total."""
        return self._total

    @property
    def hourly_express(self):
        """Return the express."""
        if self._total is None:
            return None
        _LOGGER.debug('hourly_express: %s', self._total)
        data_dict = {
                "total": self._total
            }
        # _LOGGER.debug('hourly_express_data: %s', data_dict)
        return data_dict

    @asyncio.coroutine
    def async_update(self):
        """update函数变成了async_update."""
        self._total = self._roller.total
        self._free_hour = self._roller._free_hour
        self._free_minute = self._roller._free_minute
        self._msg = self._roller._msg
        self._belong = self._roller._belong
        self._time_last = self._roller._time_last
        self._time_api_expire = self._roller._time_api_expire

        #_LOGGER.error("success to update informations")


class NiaoXiangData(object):
    """天气相关的数据，存储在这个类中."""

    def __init__(self, hass, auth):
        """初始化函数."""
        self._hass = hass

        self._url = "http://admin.efpost.cn/weixin/user/querydeliveryforuser.shtml"
        self._cookie = auth
        self._headers = {"Cookie": self._cookie,
                        "Host": "admin.efpost.cn"}

        self._total = None
        self._free_hour = 0
        self._free_minute = 0

        self._msg = ''
        self._belong = ''
        self._time_last = ''
        self._time_api_expire = ''

    @property
    def total(self):
        """温度."""
        return self._total

    @asyncio.coroutine
    def async_update(self, now):
        """从远程更新信息."""

        """
        # 异步模式的测试代码
        import time
        _LOGGER.info("before time.sleep")
        time.sleep(40)
        _LOGGER.info("after time.sleep and before asyncio.sleep")
        asyncio.sleep(40)
        _LOGGER.info("after asyncio.sleep and before yield from asyncio.sleep")
        yield from asyncio.sleep(40)
        _LOGGER.info("after yield from asyncio.sleep")
        """

        self._time_last = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

        # 通过HTTP访问，获取需要的信息
        # 此处使用了基于aiohttp库的async_get_clientsession
        #print(self._headers)
        try:
            session = async_get_clientsession(self._hass)
            with async_timeout.timeout(15):
                response = yield from session.post(
                    self._url, headers=self._headers)

        except(asyncio.TimeoutError, aiohttp.ClientError):
            self._total = -1
            _LOGGER.error("Error while accessing: %s", self._url)
            return

        if response.status != 200:
            self._total = -1
            _LOGGER.error("Error while accessing: %s, status=%d",
                          self._url,
                          response.status)
            return

        #result = yield from response.json()
        result = yield from response.read()
        #print(result.decode('utf-8'))
        _LOGGER.info("niaoxiang result:%s", result)
        result = json.loads(result)

        if result is None:
            self._total = -1
            _LOGGER.error("Request api Error")
            return
        elif isinstance(result, dict) and result["code"] == "0":
            self._total = -1
            self._msg = result['msg']
            self._time_api_expire = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
            _LOGGER.error("Error API return, code=%s, msg=%s",
                          result["code"],
                          result["msg"])
            return

        # 根据http返回的结果，更新数据
        self._total = int(len(result))
        self._belong = ''
        freeTimeStamp = 0
        for ent in result:
            receiverMobile = ent["receiverMobile"]
            if receiverMobile in TELUSERS:
                self._belong += TELUSERS[receiverMobile] + " "
            freeTime = ent["freeTime"]
            timeArray = time.strptime(freeTime, "%Y-%m-%d %H:%M:%S")
            timeStamp = int(time.mktime(timeArray))
            if freeTimeStamp == 0 or freeTimeStamp > timeStamp:
               freeTimeStamp = timeStamp
        self._free_hour = 0
        self._free_minute = 0
        if freeTimeStamp > 0:
            freeSec = freeTimeStamp - int(time.time())
            self._free_hour = int(freeSec / 3600)
            self._free_minute = int((freeSec - self._free_hour * 3600) / 60)



class ExpresXiTu(Entity):
    """Representation of a weather condition."""

    def __init__(self, roller, object_id):
        """Initialize the  weather."""
        self._object_id = object_id
        self._total = None
        self._time_duration = 0
        self._roller = roller
        self._codes = ''
        self._res_body = ''
        self._belong = ''
        self._time_last = ''
        self._time_api_expire = ''


    @property
    def device_info(self):
        """Return information to link this entity with the correct device."""
        return {"identifiers": {(DOMAIN, self._object_id)}}

    @property
    def available(self) -> bool:
        """Return True if roller and hub is available."""
        return True
        #return self._roller.online and self._roller.hub.online

    @property
    def name(self):
        """Return the name of the sensor."""
        return self._object_id

    @property
    def should_poll(self):
        """attention No polling needed for a demo weather condition."""
        return True

    @property
    def state(self):
        """Return the weather condition."""
        return 'ok'

    @property
    def attribution(self):
        """Return the attribution."""
        return 'Powered by Home Assistant'

    @property
    def state_attributes(self):
        attributes = dict()
        """设置其它一些属性值."""
        attributes.update({
                "total": self._total,
                "time_duration": self._time_duration,
                "codes": self._codes,
                "res_body": self._res_body,
                "belong": self._belong,
                "unionId": self._roller._unionId,
                "time_last": self._time_last,
                "time_api_expire": self._time_api_expire
            })
        return attributes

    @property
    def total(self):
        """Return the total."""
        return self._total

    @property
    def hourly_express(self):
        """Return the express."""
        if self._total is None:
            return None
        _LOGGER.debug('hourly_express: %s', self._total)
        data_dict = {
                "total": self._total
            }
        # _LOGGER.debug('hourly_express_data: %s', data_dict)
        return data_dict

    @asyncio.coroutine
    def async_update(self):
        """update函数变成了async_update."""
        self._total = self._roller.total
        self._time_duration = self._roller._time_duration
        self._codes = self._roller._codes
        self._res_body = self._roller._res_body
        self._belong = self._roller._belong
        self._time_last = self._roller._time_last
        self._time_api_expire = self._roller._time_api_expire


class XiTuData(object):
    """天气相关的数据，存储在这个类中."""

    def __init__(self, hass, auth):
        """初始化函数."""
        self._hass = hass
        self._url = "https://ztwjgateway.zto.com/gateway.do"
        self._unionId = auth
        self._headers = {"Host": "ztwjgateway.zto.com",
"X-Ca-Version": "1",
"X-Zop-Name": "getMyExpress",
"content-type": "application/json",
"User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 15_5 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 MicroMessenger/8.0.25(0x18001925) NetType/4G Language/zh_CN",
"Referer": "https://servicewechat.com/wx1da66276970981e8/63/page-frame.html"}

        self._total = None
        self._time_duration = 0
        self._codes = ''
        self._belong = ''
        self._res_body = ''
        self._time_last = ''
        self._time_api_expire = ''

    @property
    def total(self):
        return self._total

    @asyncio.coroutine
    def async_update(self, now):
        self._time_last = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

        try:
            session = async_get_clientsession(self._hass)
            with async_timeout.timeout(15):
                response = yield from session.post(
                    self._url, headers=self._headers, data='{"data":{"pageIndex":1,"pageSize":20,"unionId":"' + self._unionId + '"}}')

        except(asyncio.TimeoutError, aiohttp.ClientError):
            self._total = -1
            _LOGGER.error("Error while accessing: %s", self._url)
            return

        if response.status != 200:
            self._total = -1
            _LOGGER.error("Error while accessing: %s, status=%d",
                          self._url,
                          response.status)
            return

        result = yield from response.read()
        self._res_body = result.decode('utf-8')
        #_LOGGER.info("mitu result:%s", result)
        #print(result.decode('utf-8'))
        result = json.loads(result)

        if result is None:
            self._total = -1
            _LOGGER.error("Request api Error")
            return
        elif isinstance(result, dict) and result["statusCode"] != "404":
            self._total = -1
            _LOGGER.error("Error API return, code=%s", result["code"])
            return

        result = result['result']['items']
        self._total = int(len(result))
        self._belong = ''
        freeTimeStamp = 0
        if self._total > 0:
            _LOGGER.info("mitu result:%s", self._res_body)
        #for ent in result:
        #    receiverMobile = ent["receiverMobile"]
        #    if receiverMobile in TELUSERS:
        #        self._belong += TELUSERS[receiverMobile] + " "
        #    freeTime = ent["freeTime"]
        #    timeArray = time.strptime(freeTime, "%Y-%m-%d %H:%M:%S")
        #    timeStamp = int(time.mktime(timeArray))
        #    if freeTimeStamp == 0 or freeTimeStamp > timeStamp:
        #       freeTimeStamp = timeStamp
        #self._free_hour = 0
        #self._free_minute = 0
        #if freeTimeStamp > 0:
        #    freeSec = freeTimeStamp - int(time.time())
        #    self._free_hour = int(freeSec / 3600)
        #    self._free_minute = int((freeSec - self._free_hour * 3600) / 60)

        #print(timeStamp)

