# Weather Info Class file

class WeatherForecast:

    def __init__(self, next_day, temp, low, condition, preciption):
        self.__next_day = next_day
        self.__temp = temp
        self.__low = low
        self.__condition = condition
        self.__preciption = preciption
        self.__humidity = None
        self.error = None

    def set_humidity(self, humidity):
        self.__humidity = humidity

    def get_humidity(self):
        return self.__humidity

    def get_next_day(self):
        return self.__next_day

    def get_error(self):
        return self.error

    def set_error(self, error):
        self.error = error

    def get_temp(self):
        return self.__temp

    def get_low(self):
        return self.__low

    def get_condition(self):
        return self.__condition

    def get_preciption(self):
        return self.__preciption

    def __str__(self):
        return "WeatherInfo: [next_day: " + str(self.__next_day) + ", temp: " + str(self.__temp) + ", low: " + str(self.__low) + ", condition: " + str(self.__condition) + ", preciption: " + str(self.__preciption) + ", humidity: " + str(self.__humidity) + "]"

    def serialize(self):
        return {
            'next_day': self.__next_day,
            'temperature': self.__temp,
            'humidity': self.__humidity,
            'condition': self.__condition,
            'low': self.__low,
            'preciption': self.__preciption,
        }