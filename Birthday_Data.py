import datetime
import json

class Birthday_Data(object):
    # The format is the following year - month - day
    def __init__(self):
        self.data = {}

    def __repr__(self):
        if not bool(self.data):
            return "Empty dictionary"
        else:
            output = ""
            for b in self.data:
                output += f'{b} -> {self.data[b]} \n'
            return output

    def parse_file(self, file):
        try:
            with open(file) as json_file:
                j = json.load(json_file)
                for b in j['birthdays']:
                    self.data[b['name']] = datetime.datetime(
                        2000, b['month'], b['day'])
        except:
            print('unable to find the file')

    def check_if_birthday(self):
        d = datetime.datetime.now()
        all_birthdays_today = []
        for b in self.data:
            match = self.data[b].month == d.month and self.data[b].day == d.day
            if (match):
                all_birthdays_today.append(b)
        return all_birthdays_today
        

birthdays = Birthday_Data()
birthdays.parse_file("birthday_input.json")
birthdays_today = birthdays.check_if_birthday()
if (birthdays_today != []):
    print (birthdays_today)

