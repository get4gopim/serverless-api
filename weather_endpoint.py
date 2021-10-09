import flask
import logging
import os

from flask import jsonify
from service import HtmlParser2

app = flask.Flask(__name__)
app.config["DEBUG"] = True

logging.basicConfig(level=os.environ.get("LOGLEVEL", "INFO"), format='%(asctime)s %(message)s')

LOGGER = logging.getLogger(__name__)


# A route to return weather for a given location
@app.route('/api/v1/weather/<location>', methods=['GET'])
def api_weather(location):
    LOGGER.info("weather.location" + location)
    info = HtmlParser2.call_weather_api(location)
    return jsonify(info.serialize())


# A route to return forecast for a given location
@app.route('/api/v1/weather/<location>/forecast', methods=['GET'])
def api_forecast(location):
    LOGGER.info("weather.forecast.location" + location)
    f_list = HtmlParser2.call_weather_forecast(location)
    serialized_list = [e.serialize() for e in f_list]
    return jsonify(serialized_list)


# A route to return current gold rate in [chennai]
@app.route('/api/v1/gold', methods=['GET'])
def api_gold():
    info = HtmlParser2.call_gold_api()
    return jsonify(info.serialize())


# A route to return current fuel rate in [chennai]
@app.route('/api/v1/fuel', methods=['GET'])
def api_fuel():
    info = HtmlParser2.call_fuel_api()
    return jsonify(info.serialize())


# A route to return current HDFC Bond fund growth
@app.route('/api/v1/hdfcbond', methods=['GET'])
def api_hdfc_bond():
    LOGGER.info("hdfc bond fund growth api call")
    info = HtmlParser2.call_hdfc_api()
    return jsonify(info.serialize())


@app.route('/', methods=['GET'])
def home():
    return "<h1>Weather Forecast API Running</h1>"

