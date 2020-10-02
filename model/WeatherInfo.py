# Weather Info Class file

class WeatherInfo:

    def __init__(self, temp, low, high, asof, condition, location, preciption):
        self.__temp = temp
        self.__low = low
        self.__high = high
        self.__asof = asof
        self.__condition = condition
        self.__location = location
        self.__preciption = preciption
        self.__humidity = None
        self.error = None

    def set_humidity(self, humidity):
        self.__humidity = humidity

    def get_humidity(self):
        return self.__humidity

    def get_error(self):
        return self.error

    def set_error(self, error):
        self.error = error

    def get_temp(self):
        return self.__temp

    def get_low(self):
        return self.__low

    def get_high(self):
        return self.__high

    def get_as_of(self):
        return self.__asof

    def get_condition(self):
        return self.__condition

    def get_location(self):
        return self.__location

    def get_preciption(self):
        return self.__preciption

    def __str__(self):
        return "WeatherInfo: [location: " + str(self.__location) + ", temp: " + str(self.__temp) + ", low: " + str(self.__low) + ", high: " + str(self.__high) + ", condition: " + str(self.__condition) + ", preciption: " + str(self.__preciption) + ", humidity: " + str(self.__humidity) + ", asof: " + str(self.__asof) + "]"

    def serialize(self):
        return {
            'location': self.__location,
            'temperature': self.__temp,
            'low': self.__low,
            'high': self.__high,
            'humidity': self.__humidity,
            'condition': self.__condition,
            'asof': self.__asof,
            'preciption': self.__preciption,
        }