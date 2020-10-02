# Rate Info Class file


class FuelInfo:

    def __init__(self, petrol, diesel, date, last_updated_time):
        self.__petrol = petrol
        self.__diesel = diesel
        self.__date = date
        self.__last_updated_time = last_updated_time
        self.error = None

    def get_error(self):
        return self.error

    def set_error(self, error):
        self.error = error

    def get_petrol(self):
        return self.__petrol

    def get_diesel(self):
        return self.__diesel

    def get_date(self):
        return self.__date

    def get_last_updated_time(self):
        return self.__last_updated_time

    def __str__(self):
        return "FuelInfo: [date: " + str(self.__date) + ", petrol: " + str(self.__petrol) + ", diesel: " + str(self.__diesel) + ", lastUpdated: " + str(self.__last_updated_time) + "]"