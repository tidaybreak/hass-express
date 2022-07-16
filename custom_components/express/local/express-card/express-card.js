const locale = {
  'zh-Hans': {
    tempHi: "最高温度",
    tempLo: "最低温度",
    precip: "降水量",
    pop: "降水概率",
    uPress: "百帕",
    uSpeed: "米/秒",
    uPrecip: "毫米",
    cardinalDirections: [
      '北', '北-东北', '东北', '东-东北', '东', '东-东南', '东南', '南-东南',
      '南', '南-西南', '西南', '西-西南', '西', '西-西北', '西北', '北-西北', '北'
    ],
    aqiLevels: [
      '优', '良', '轻度污染', '中度污染', '重度污染', '严重污染'
    ]
  },
  en: {
    tempHi: "Temperature",
    tempLo: "Temperature night",
    precip: "Precipitations",
    uPress: "hPa",
    uSpeed: "m/s",
    uPrecip: "mm",
    cardinalDirections: [
      'N', 'N-NE', 'NE', 'E-NE', 'E', 'E-SE', 'SE', 'S-SE',
      'S', 'S-SW', 'SW', 'W-SW', 'W', 'W-NW', 'NW', 'N-NW', 'N'
    ]
  }
};

// 延时加载，解决每次界面显示不了的问题
; (() => {
  const timer = setInterval(() => {
    if (Polymer.Element) {
      clearInterval(timer);
      // 开始生成DOM元素
      class WeatherCardChart extends Polymer.Element {

        static get template() {
          return Polymer.html`
      <style>
        ha-icon {
          color: var(--paper-item-icon-color);
        }
        .card {
          padding: 0 18px 18px 18px;
        }
        .header {
          font-family: var(--paper-font-headline_-_font-family);
          -webkit-font-smoothing: var(
            --paper-font-headline_-_-webkit-font-smoothing
          );
          font-size: var(--paper-font-headline_-_font-size);
          font-weight: var(--paper-font-headline_-_font-weight);
          letter-spacing: var(--paper-font-headline_-_letter-spacing);
          line-height: var(--paper-font-headline_-_line-height);
          text-rendering: var(
            --paper-font-common-expensive-kerning_-_text-rendering
          );
          opacity: var(--dark-primary-opacity);
          padding: 24px 16px 5px;
          display: flex;
          justify-content: space-between;
        }
        .header div {
          display: flex;
        }
        .title {
          margin-left: 16px;
          font-size: 16px;
          color: var(--secondary-text-color);
        }
        .time {
          font-size: 16px;
          color: var(--secondary-text-color);
          align-items: center;
        }
        .now {
          display: flex;
          justify-content: space-between;
          align-items: center;
          flex-wrap: wrap;
        }
        .main {
          display: flex;
          font-size: 48px;
          align-items: center;
          line-height: 1em;
        }
        .main ha-icon {
          --iron-icon-height: 72px;
          --iron-icon-width: 72px;
          margin-right: 8px;
        }
        .main div {
          cursor: pointer;
          margin-top: -11px;
        }
        .main sup {
          font-size: 24px;
        }
        .suggestion {
          cursor: pointer;
          display: flex;
          font-size: 14px;
          color: var(--secondary-text-color);
          justify-content: space-between;
        }
        .suggestion div {
          margin-left: 15px;
        }
        .attributes {
          cursor: pointer;
          display: flex;
          justify-content: space-between;
          align-items: center;
          margin: 5px 0px 10px 0px;
        }
        .chart-title {
          font-size: 16px;
          margin: 15px 0px 5px 0px;
          text-align: center;
          font-weight: 600; 
        }
        .conditions {
          display: flex;
          justify-content: space-between;
          align-items: center;
          margin: 0px 3px 0px 16px;
        }
        .aqi,
        .alarm {
          font-size: 16px;
          border-radius: 3px;
          color: #fff;
          line-height: 20px;
          padding: 2px 5px 2px 5px;
          margin: 0px 0px 0px 10px;
          height: 20px;
        }
        .aqi_level_0_bg {
          background-color: #40c057;
        }
        .aqi_level_1_bg{
          background-color: #82c91e;
        }
        .aqi_level_2_bg {
          background-color: #f76707;
        }
        .aqi_level_3_bg {
          background-color: #e03131;
        }
        .aqi_level_4_bg {
          background-color: #841c3c;
        }
        .aqi_level_5_bg{
          background-color: #540822;
        }
        .alarm {
          background-color: rgb(21, 123, 255)
        }
        .icon.bigger {
          width: 2em;
          height: 2em;
          left: 0em;
        }

        .icon {
          width: 50px;
          height: 50px;
          display: inline-block;
          vertical-align: middle;
          background-size: contain;
          background-position: center center;
          background-repeat: no-repeat;
          text-indent: -9999px;
        }
      </style>
      <ha-card>
        <div class="header">
          <div style="align-items: baseline;">
            <div style="align-items: center;">
              [[weatherObj.attributes.condition_cn]]
              <template is="dom-if" if="[[weatherObj.attributes.aqi]]">
                <div class$ = "aqi [[aqiLevel(weatherObj.attributes.aqi.aqi)]]">[[roundNumber(weatherObj.attributes.aqi.aqi)]]</div>
              </template>
            </div>
            <div class="title">[[title]]</div>
          </div>
          <div class="time">
            <ha-icon icon="mdi:update"></ha-icon>
            <div style="margin: 0 0 0 5px">[[weatherObj.attributes.update_time]]</div>
          </div>
        </div>
        <div class="card">
          <div class="now">
            <div class="main">
              <i class="icon bigger" style="background: none, url([[getWeatherIcon(weatherObj.state)]]) no-repeat; background-size: contain;"></i>
              <template is="dom-if" if="[[tempObj]]">
                <div on-click="_tempAttr">[[roundNumber(tempObj.state)]]<sup>[[getUnit('temperature')]]</sup></div>
              </template>
              <template is="dom-if" if="[[!tempObj]]">
                <div on-click="_weatherAttr">[[roundNumber(weatherObj.attributes.temperature)]]<sup>[[getUnit('temperature')]]</sup></div>
              </template>
              <template is="dom-if" if="[[weatherObj.attributes.alarm]]">
                <div class="alarm" on-click="_weatherAttr">
                  台风预警
                </div>
              </template>
            </div>

            <div class="suggestion" on-click="_weatherAttr">
              <div>
                <span> 舒适：[[getSuggestion("comf")]]</span><br>
                <span> 穿衣：[[getSuggestion("drsg")]]</span><br>
                <span> 空气：[[getSuggestion("air")]]</span><br>
                <span> 感冒：[[getSuggestion("flu")]]	</span><br>	
              </div>
              <div>          
                <span> 紫外：[[getSuggestion("uv")]]</span><br>
                <span> 运动：[[getSuggestion("sport")]]</span><br>	
                <span> 旅游：[[getSuggestion("trav")]]</span><br>	
                <span> 洗车：[[getSuggestion("cw")]]</span><br>
              </div>
            </div>
          </div>
          <div class="attributes">
            <div on-click="_weatherAttr">
              <ha-icon icon="hass:water-percent"></ha-icon> [[roundNumber(weatherObj.attributes.humidity)]] %<br>
              <ha-icon icon="hass:gauge"></ha-icon> [[roundNumber(weatherObj.attributes.pressure)]] [[ll('uPress')]]
            </div>
            <div on-click="_sunAttr">
              <template is="dom-if" if="[[sunObj]]">
                <ha-icon icon="mdi:weather-sunset-up"></ha-icon> [[computeTime(sunObj.attributes.next_rising)]]<br>
                <ha-icon icon="mdi:weather-sunset-down"></ha-icon> [[computeTime(sunObj.attributes.next_setting)]]
              </template>
            </div>
            <div on-click="_weatherAttr">
              <ha-icon icon="hass:[[getWindDirIcon(windBearing)]]"></ha-icon> [[getWindDir(windBearing)]]<br>
              <ha-icon icon="hass:weather-windy"></ha-icon> [[computeWind(weatherObj.attributes.wind_speed)]] [[ll('uSpeed')]]
            </div>
          </div>
          <template is="dom-if" if="[[hourlyForecast]]">
          <div class="chart-title">天气预报-小时</div>
            <ha-chart-base chart-type="[[HourlyForecastChartData.type]]" data="[[HourlyForecastChartData.data]]" options="[[HourlyForecastChartData.options]]" hass="[[_hass]]"></ha-chart-base>
            <div class="conditions">
              <template is="dom-repeat" items="[[hourlyForecast]]">
                <div>
                  <i class="icon" style="background: none, url([[getWeatherIcon(item.condition)]]) no-repeat; background-size: contain;"></i>

                  <div style="text-align: center;">[[computeProbablePrecipitation(item.probable_precipitation)]]</div>
                </div>
              </template>
            </div>
          </template>
          <template is="dom-if" if="[[dailyForecast]]">
            <div class="chart-title">天气预报-天</div>
            <ha-chart-base chart-type="[[DailyForecastChartData.type]]" data="[[DailyForecastChartData.data]]" options="[[DailyForecastChartData.options]]" hass="[[_hass]]"></ha-chart-base>
            <div class="conditions">
              <template is="dom-repeat" items="[[dailyForecast]]">
                <div>
                  <i class="icon" style="background: none, url([[getWeatherIcon(item.condition)]]) no-repeat; background-size: contain;"></i>

                  <div style="text-align: center;">[[computeProbablePrecipitation(item.probable_precipitation)]]</div>
                </div>
              </template>
            </div>
          </template>
        </div>
      </ha-card>
    `;
        }

        static get properties() {
          return {
            config: Object,
            sunObj: Object,
            tempObj: Object,
            mode: String,
            weatherObj: {
              type: Object,
              observer: 'dataChanged',
            },
          };
        }

        constructor() {
          super();
          this.weatherIcons = {
            "clear-night": "hass:weather-night",
            cloudy: "hass:weather-cloudy",
            exceptional: "hass:alert-circle-outline",
            fog: "hass:weather-fog",
            hail: "hass:weather-hail",
            lightning: "hass:weather-lightning",
            "lightning-rainy": "hass:weather-lightning-rainy",
            partlycloudy: "hass:weather-partly-cloudy",
            pouring: "hass:weather-pouring",
            rainy: "hass:weather-rainy",
            snowy: "hass:weather-snowy",
            "snowy-rainy": "hass:weather-snowy-rainy",
            sunny: "hass:weather-sunny",
            windy: "hass:weather-windy",
            "windy-variant": "hass:weather-windy-variant"
          };
          this.cardinalDirectionsIcon = [
            'mdi:arrow-down', 'mdi:arrow-bottom-left', 'mdi:arrow-left',
            'mdi:arrow-top-left', 'mdi:arrow-up', 'mdi:arrow-top-right',
            'mdi:arrow-right', 'mdi:arrow-bottom-right', 'mdi:arrow-down'
          ];
          this.weatherIconsDay = {
            'clear': 'day',
            'clear-night': 'night',
            'cloudy': 'cloudy',
            'fog': 'cloudy',
            'hail': 'rainy-7',
            'lightning': 'thunder',
            'lightning-rainy': 'thunder',
            'partlycloudy': 'cloudy-day-3',
            'pouring': 'rainy-6',
            'rainy': 'rainy-5',
            'snowy': 'snowy-6',
            'snowy-rainy': 'rainy-7',
            'sunny': 'day',
            'windy': 'cloudy',
            'windy-variant': 'cloudy-day-3',
            exceptional: '!!'
          };
          this.weatherIconsNight = {
            ...this.weatherIconsDay,
            'clear': 'night',
            'sunny': 'night',
            'partlycloudy': 'cloudy-night-3',
            'windy-variant': 'cloudy-night-3'
          };
        }


        // 自定义默认配置
        static getStubConfig() {
          return { entity: "weather.express" }
        }

        setConfig(config) {
          if (!config.entity) {
            throw new Error('Please define "weather" entity in the card config');
          }
          this.config = config;
          this.mode = config.mode ? config.mode : 'both';
        }

        set hass(hass) {
          this._hass = hass;
          this.lang = this._hass.selectedLanguage || this._hass.language;
          this.weatherObj = this.config.entity in hass.states ? hass.states[this.config.entity] : null;
          this.sunObj = 'sun.sun' in hass.states ? hass.states['sun.sun'] : null;
          this.tempObj = this.config.temp in hass.states ? hass.states[this.config.temp] : null;
          this.dailyForecast = this.mode == 'hourly' ? null : this.weatherObj.attributes.forecast.slice(0, 9);
          this.hourlyForecast = this.mode == 'daily' ? null : this.weatherObj.attributes.hourly_forecast.slice(0, 9);
          this.windBearing = this.weatherObj.attributes.wind_bearing;
          this.suggestion = this.weatherObj.attributes.suggestion;
          this.title = this.config.title ? this.config.title : this.weatherObj.attributes.friendly_name;
        }

        dataChanged() {
          this.HourlyForecastChartData = this.drawChart('hourly', this.hourlyForecast);
          this.DailyForecastChartData = this.drawChart('daily', this.dailyForecast);
        }

        roundNumber(number) {
          var rounded = Math.round(number);
          return rounded;
        }

        aqiLevel(aqi) {
          return 'aqi_level_' + parseInt(aqi / 50.0) + '_bg';
        }

        getSuggestion(type) {
          for (var i = 0; i < this.suggestion.length; i++) {
            if (this.suggestion[i].title == type) {
              return this.suggestion[i].brf;
            }
          }
        }
        ll(str) {
          if (locale[this.lang] === undefined)
            return locale.en[str];
          return locale[this.lang][str];
        }

        computeTime(time) {
          const date = new Date(time);
          return date.toLocaleTimeString(this.lang,
            { hour: '2-digit', minute: '2-digit' }
          );
        }

        computeWind(speed) {
          var calcSpeed = Math.round(speed * 1000 / 3600);
          return calcSpeed;
        }

        computeProbablePrecipitation(probability) {
          return probability / 100;
        }


        getCardSize() {
          return 4;
        }

        getUnit(unit) {
          return this._hass.config.unit_system[unit] || '';
        }

        getWeatherIcon(condition) {
          return `/hf_weather-local/hf_weather-card/icons/animated/${this.sunObj.state && this.sunObj.state == "below_horizon"
            ? this.weatherIconsNight[condition]
            : this.weatherIconsDay[condition]
            }.svg`;
        }

        getWindDirIcon(degree) {
          return this.cardinalDirectionsIcon[parseInt((degree + 22.5) / 45.0)];
        }

        getWindDir(deg) {
          if (locale[this.lang] === undefined)
            return locale.en.cardinalDirections[parseInt((deg + 11.25) / 22.5)];
          return locale[this.lang]['cardinalDirections'][parseInt((deg + 11.25) / 22.5)];
        }

        getAqiLevel(aqi) {
          return locale[this.lang]['aqiLevels'][parseInt(aqi / 50.0)];
        }

        drawChart(mode, forecastData) {
          if (!forecastData) {
            return [];
          }
          var data = forecastData.slice(0, 9);
          var locale = this._hass.selectedLanguage || this._hass.language;
          var tempUnit = this._hass.config.unit_system.temperature;
          var lengthUnit = this._hass.config.unit_system.length;
          var precipUnit = lengthUnit === 'km' ? this.ll('uPrecip') : 'in';
          var i;

          var dateTime = [];
          var tempHigh = [];
          var tempLow = [];
          var precip = [];
          for (i = 0; i < data.length; i++) {
            var d = data[i];
            const dateFomart = new Date(Date.parse(d.datetime.replace(/-/g, '/')))
            dateTime.push(mode === 'daily' ? dateFomart.toLocaleDateString(locale, { weekday: 'short' }) : dateFomart.toLocaleTimeString(locale, { hour: 'numeric' }));
            tempHigh.push(d.temperature);
            tempLow.push(d.templow);
            precip.push(d.precipitation);
          }
          var style = getComputedStyle(document.body);
          var textColor = style.getPropertyValue('--primary-text-color');
          var dividerColor = style.getPropertyValue('--divider-color');
          let datasets = []
          if (mode === 'daily') {
            datasets = [
              {
                label: this.ll('tempHi'),
                type: 'line',
                data: tempHigh,
                yAxisID: 'TempAxis',
                borderWidth: 2.0,
                lineTension: 0.4,
                pointRadius: 0.0,
                pointHitRadius: 5.0,
                fill: false,
              },
              {
                label: this.ll('tempLo'),
                type: 'line',
                data: tempLow,
                yAxisID: 'TempAxis',
                borderWidth: 2.0,
                lineTension: 0.4,
                pointRadius: 0.0,
                pointHitRadius: 5.0,
                fill: false,
              },
              {
                label: this.ll('precip'),
                type: 'bar',
                data: precip,
                yAxisID: 'PrecipAxis',
              },
            ]
          } else {
            datasets = [
              {
                label: this.ll('tempHi'),
                type: 'line',
                data: tempHigh,
                yAxisID: 'TempAxis',
                borderWidth: 2.0,
                lineTension: 0.4,
                pointRadius: 0.0,
                pointHitRadius: 5.0,
                fill: false,
              },
            ]
          }
          const chartOptions = {
            type: 'bar',
            data: {
              labels: dateTime,
              datasets
            },
            options: {
              plugins: {
                animation: {
                  duration: 1000,
                  easing: 'linear',
                  onComplete: function () {
                    var _this = this
                    var ctx = this.ctx;
                    ctx.fillStyle = textColor;
                    ctx.font = "10px Roboto"
                    ctx.textAlign = 'center';
                    ctx.textBaseline = 'bottom';
                    var metaIndex = mode === 'daily' ? 2 : 0
                    var meta = this.getDatasetMeta(metaIndex);
                    meta.data.forEach(function (bar, index) {
                      var data = (Math.round((_this.data.datasets[metaIndex].data[index]) * 10) / 10).toFixed(1);
                      ctx.fillText(data, bar.x, bar.y - 5);
                    });
                  },
                }
              },
            }
          };
          return chartOptions;
        }

        _fire(type, detail, options) {
          const node = this.shadowRoot;
          options = options || {};
          detail = (detail === null || detail === undefined) ? {} : detail;
          const e = new Event(type, {
            bubbles: options.bubbles === undefined ? true : options.bubbles,
            cancelable: Boolean(options.cancelable),
            composed: options.composed === undefined ? true : options.composed
          });
          e.detail = detail;
          node.dispatchEvent(e);
          return e;
        }

        _tempAttr() {
          this._fire('hass-more-info', { entityId: this.config.temp });
        }

        _weatherAttr() {
          this._fire('hass-more-info', { entityId: this.config.entity });
        }

        _sunAttr() {
          this._fire('hass-more-info', { entityId: this.sunObj.entity_id });
        }

        _suggestionAttr() {

        }
      }

      customElements.define('hf_weather-card', WeatherCardChart);

      // 添加预览
      window.customCards = window.customCards || [];
      window.customCards.push({
        type: "hf_weather-card",
        name: "和风天气",
        preview: true,
        description: "和风天气卡片"
      });

    }
  }, 1000)
})();
