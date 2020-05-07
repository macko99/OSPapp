import datetime

from kivy.factory import Factory
from kivy.storage.jsonstore import JsonStore
import uuid
import json
import requests


class DataBase:
    url = 'https://ospapp-53708.firebaseio.com/.json?auth='
    admin_passwd = ''

    def __init__(self, path, heroes_path, passwd_path):
        print("init db")
        self.path = path
        self.store = JsonStore(path)
        with open("secret", 'r') as file:
            data = file.read().split("\n")
            self.url = self.url + data[0]
        self.firebase_patch_all()
        try:
            string = str(requests.get(self.url).json()['heroes'])
            if string:
                with open(heroes_path, 'w') as file:
                    file.write(string)
        except Exception as e:
            print(str(e))
        try:
            with open(heroes_path, 'r') as file:
                self.heroes = json.loads(str(file.read()).replace("'", '"'))
        except Exception as e:
            print(str(e))
            self.heroes = ["brak strażaków w bazie"]
        try:
            string = str(requests.get(self.url).json()['passwd'])
            if string:
                with open(passwd_path, 'w') as file:
                    file.write(string)
        except Exception as e:
            print(str(e))
        try:
            with open(passwd_path, 'r') as file:
                global admin_passwd
                admin_passwd = file.readline()
        except Exception as e:
            print(str(e))

    def put_report(self, uuid_num, id_number, dep_date, dep_time, spot_time, location, type_of_action,
                   section_com, action_com, driver, perpetrator, victim, section, details,
                   return_date, end_time, home_time, stan_licznika, km_location, completed):
        if uuid_num == "":
            uuid_num = str(uuid.uuid1())
        if section_com == "Dowódca sekcji":
            section_com = ""
        if action_com == "Dowódca akcji":
            action_com = ""
        if driver == "Kierowca":
            driver = ""
        self.store.put(uuid_num, innerID=id_number, depDate=dep_date, depTime=dep_time, spotTime=spot_time,
                       location=location, type=type_of_action,
                       sectionCom=section_com, actionCom=action_com, driver=driver, perpetrator=perpetrator,
                       victim=victim, section=section, details=details,
                       returnDate=return_date, endTime=end_time, homeTime=home_time, stanLicznika=stan_licznika,
                       KM=km_location, modDate=self.get_date(), ready=completed)
        try:
            string = "{'" + uuid_num + "': " + str(self.store.get(uuid_num)) + "}"
            to_database = json.loads(string.replace("'", '"'))
            requests.patch(url=self.url, json=to_database)
        except Exception as e:
            print(str(e))

    def delete_report(self, uuid_num):
        if self.store.exists(uuid_num):
            try:
                # requests.delete(url=self.url[:-5] + id_number + ".json")
                string = '{"deleted-' + uuid_num + '": "true"}'
                to_database = json.loads(string)
                requests.patch(url=self.url, json=to_database)
            except Exception as e:
                Factory.deletePopout().open()
                print(str(e))
            else:
                self.store.delete(uuid_num)
        else:
            return -1

    def get_heroes(self):
        return self.heroes

    def firebase_patch_all(self):
        try:
            with open(self.path, 'r') as file:
                data = file.read()
                to_database = json.loads(data)
                requests.patch(url=self.url, json=to_database)
        except Exception as e:
            print(str(e))

    def delete_all(self):
        string_all = ""
        try:
            for key in self.store.keys():
                # requests.delete(url=self.url[:-5] + key + ".json")
                string = '{"deleted-' + key + '": "true"}'
                string_all = string_all + string
                to_database = json.loads(string)
                requests.patch(url=self.url, json=to_database)
        except Exception as e:
            Factory.deletePopout().open()
            print(str(e))
        else:
            self.store.clear()

    def get_report(self, id_number):
        for item in self.store.find(innerID=id_number):
            dane = self.store.get(item[0])
            id_number = dane['innerID']
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
            completed = dane['ready']
            return [item[0], id_number, dep_date, dep_time, spot_time, location, type_of_action, section_com,
                    action_com,
                    driver,
                    perpetrator, victim, section, details,
                    return_date, end_time, home_time, stan_licznika, km_location, date, completed]
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

    def get_passwd(self):
        global admin_passwd
        return admin_passwd
