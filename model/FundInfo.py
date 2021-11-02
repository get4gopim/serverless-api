# Fund Info Class file


class FundInfo:

    def __init__(self, scheme, nav, purchase_value, change_value, last_updated_time):
        self.__scheme = scheme
        self.__nav = nav
        self.__purchase_value = purchase_value
        self.__change_value = change_value
        self.__last_updated_time = last_updated_time
        self.error = None

    def get_error(self):
        return self.error

    def set_error(self, error):
        self.error = error

    def get_scheme(self):
        return self.__scheme

    def get_nav(self):
        return self.__nav

    def get_purchase_value(self):
        return self.__purchase_value

    def get_change_value(self):
        return self.__change_value

    def get_last_updated_time(self):
        return self.__last_updated_time

    def __str__(self):
        return "FundInfo: [scheme: " + str(self.__scheme) + ", change_value: " + str(self.__change_value) + ", nav: " + str(self.__nav) + ", purchase_value: " + str(self.__purchase_value) + ", lastUpdated: " + str(self.__last_updated_time) + "]"

    def serialize(self):
        return {
            'scheme': self.__scheme,
            'change_value': self.__change_value,
            'nav': self.__nav,
            'purchase_value': self.__purchase_value,
            'lastUpdated': self.__last_updated_time
        }