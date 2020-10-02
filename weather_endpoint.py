import flask
import logging
import os

from flask import jsonify
from service import HtmlParser2

app = flask.Flask(__name__)
app.config["DEBUG"] = True

logging.basicConfig(level=os.environ.get("LOGLEVEL", "INFO"), format='%(asctime)s %(message)s')
logging.getLogger('schedule').propagate = False

LOGGER = logging.getLogger(__name__)


# A route to return weather for a given location
@app.route('/api/v1/weather/<location>', methods=['GET'])
def api_weather(location):
    info = HtmlParser2.call_weather_api(location)
    return jsonify(info.serialize())


# A route to return forecast for a given location
@app.route('/api/v1/weather/<location>/forecast', methods=['GET'])
def api_forecast(location):
    f_list = HtmlParser2.call_weather_forecast(location)
    serialized_list = [e.serialize() for e in f_list]
    return jsonify(serialized_list)


@app.route('/', methods=['GET'])
def home():
    return "<h1>Weather Forecast API Running</h1>"


app.run()
