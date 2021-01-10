import datetime

class Birthday_Data(object):
    def __init__(self, data):
        self.data = data

    def __rep__(self):
        return "nop"

    def parse_file(self, file):
        pass

    def check_if_birthday(self):
        for b in self.data:
            if (self.data[b].month == datetime.datetime.now().month):
                print("match the month")
                if (self.data[b].day == datetime.datetime.now().day):
                    print(birthday_data_dictionary[b])
                    print(f'Is {b} fucking birhtday')
                    return True
        return False


# The format is the following year - month - day
birthday_data_dictionary = {
    "Jara": datetime.datetime(1997, 5, 15),
    "Ruben": datetime.datetime(1997, 5, 15),
    "Paquito": datetime.datetime(1997, 1, 10),
    "Alicia ": datetime.datetime(1997, 6, 8)
}

birthdays = Birthday_Data(birthday_data_dictionary)
birthdays.check_if_birthday()
