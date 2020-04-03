import datetime
from kivy.storage.jsonstore import JsonStore


class DataBase:
    store = JsonStore("reports" + ".json")

    def put_report(self, id_number, dep_date, dep_time, spot_time, location, type_of_action,
                   section_com, action_com, driver, perpetrator, victim, section, details,
                   return_date, end_time, home_time, stan_licznika, km_location):
        self.store.put(id_number, depDate=dep_date, depTime=dep_time, spotTime=spot_time, location=location,
                       type=type_of_action,
                       sectionCom=section_com, actionCom=action_com, driver=driver, perpetrator=perpetrator,
                       victim=victim, section=section, details=details,
                       returnDate=return_date, endTime=end_time, homeTime=home_time, stanLicznika=stan_licznika,
                       KM=km_location, modDate=self.get_date())

    def delete_report(self, id_number):
        if self.store.exists(id_number):
            self.store.delete(id_number)
        else:
            return -1

    def if_exists(self, id_number):
        if self.store.exists(id_number):
            return True
        else:
            return False

    def get_report(self, id_number):
        if self.store.exists(id_number):
            global dep_date, dep_time, spot_time, location, type_of_action, section_com, action_com, driver, perpetrator, victim, section, details
            global return_date, end_time, home_time, stan_licznika, km_location, date
            dane = self.store.get(id_number)
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
            return [id_number, dep_date, dep_time, spot_time, location, type_of_action, section_com, action_com, driver,
                    perpetrator, victim, section, details,
                    return_date, end_time, home_time, stan_licznika, km_location, date]
        else:
            return -1

    def count_reports(self):
        return str(self.store.count())

    def get_all(self):
        res = ""
        for key in self.store.keys():
            res = res + str(key) + ", "
        res = res[:-2]
        return res

    def get_all_array(self):
        return self.store.keys()

    @staticmethod
    def get_date():
        return str(datetime.datetime.now()).split(".")[0]
