import datetime
from kivy.storage.jsonstore import JsonStore
import uuid
# from plyer import email


class DataBase:

    def __init__(self, path):
        self.store = JsonStore(path)

    def put_report(self, sys_id, id_number, dep_date, dep_time, spot_time, location, type_of_action,
                   section_com, action_com, driver, perpetrator, victim, section, details,
                   return_date, end_time, home_time, stan_licznika, km_location):
        if sys_id == "":
            sys_id = str(uuid.uuid1())
        self.store.put(sys_id, innerID=id_number, depDate=dep_date, depTime=dep_time, spotTime=spot_time,
                       location=location, type=type_of_action,
                       sectionCom=section_com, actionCom=action_com, driver=driver, perpetrator=perpetrator,
                       victim=victim, section=section, details=details,
                       returnDate=return_date, endTime=end_time, homeTime=home_time, stanLicznika=stan_licznika,
                       KM=km_location, modDate=self.get_date())
        # recipient = 'abc@gmail.com'
        # subject = 'Hi'
        # text = 'This is an example.'
        # create_chooser = False
        # email.send(recipient=recipient, subject=subject, text=text,
        #            create_chooser=create_chooser)

    def delete_report(self, id_number):
        if self.store.exists(id_number):
            self.store.delete(id_number)
        else:
            return -1

    def delete_all(self):
        self.store.clear()

    def if_exists(self, id_number):
        if self.store.exists(id_number):
            return True
        else:
            return False

    def get_report(self, id_number):
        for item in self.store.find(innerID=id_number):
            dane = self.store.get(item[0])
            inner_id = dane["innerID"]
            dep_date = dane['depDate']
            dep_time = dane['depTime']
            spot_time = dane['spotTime']
            location = dane['location']
            type_of_action = dane['type']
            section_com = dane['sectionCom']
            action_com = dane['actionCom']
            driver = dane['driver']
            perpetrator = dane['perpetrator']
            victim = dane['victim']
            section = dane['section']
            details = dane['details']
            return_date = dane['returnDate']
            end_time = dane['endTime']
            home_time = dane['homeTime']
            stan_licznika = dane['stanLicznika']
            km_location = dane['KM']
            date = dane['modDate']
            return [item[0], inner_id, dep_date, dep_time, spot_time, location, type_of_action, section_com, action_com,
                    driver,
                    perpetrator, victim, section, details,
                    return_date, end_time, home_time, stan_licznika, km_location, date]
        else:
            return -1

    def get_all_friendly(self):
        result = []
        for item in self.store.keys():
            data = self.store.get(item)
            result.append(data["innerID"] + " " + data["location"])
        return result

    def find_inner_id(self, id_number):
        for _ in self.store.find(innerID=id_number):
            return True
        return False

    @staticmethod
    def get_date():
        return str(datetime.datetime.now()).split(".")[0]


# class Email(object):
#
#     def send(self, recipient=None, subject=None, text=None,
#              create_chooser=None):
#         self._send(recipient=recipient, subject=subject, text=text,
#                    create_chooser=create_chooser)
#
#     # private
#
#     def _send(self, **kwargs):
#         raise NotImplementedError()
