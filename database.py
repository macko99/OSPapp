import datetime
from kivy.factory import Factory
from kivy.storage.jsonstore import JsonStore
import uuid
import json
import requests
from kivy.logger import Logger


class DataBase:
    base_url = 'https://osptest-3ddc5.firebaseio.com/'
    url = ''
    secret = ''
    admin_password = ''

    def __init__(self, path, heroes_path, password_path, trucks_path, version):
        self.version = version
        self.heroes_path = heroes_path
        self.password_path = password_path
        self.trucks_path = trucks_path
        self.path = path
        self.store = JsonStore(path)
        with open("data/login", 'r') as file:
            self.user = file.read().split("\n")[0]
        with open("data/secret", 'r') as file:
            self.secret = file.read().split("\n")[0]
        self.url = self.base_url + self.user + self.secret

        self.firebase_patch_all()
        self.update_osp_data()

    def update_osp_data(self):
        try:
            string = str(requests.get(self.url).json()['heroes'])
            if string:
                with open(self.heroes_path, 'w') as file:
                    file.write(string)
        except Exception as connection_error:
            Logger.exception(str(connection_error))
        try:
            with open(self.heroes_path, 'r') as file:
                self.heroes = json.loads(str(file.read()).replace("'", '"'))
        except Exception as no_heroes_in_db:
            Logger.exception(str(no_heroes_in_db))
            self.heroes = ["brak strażaków w bazie"]
        try:
            string = str(requests.get(self.url).json()['trucks'])
            if string:
                with open(self.trucks_path, 'w') as file:
                    file.write(string)
        except Exception as connection_error:
            Logger.exception(str(connection_error))
        try:
            with open(self.trucks_path, 'r') as file:
                self.trucks = json.loads(str(file.read()).replace("'", '"'))
        except Exception as no_trucks_in_db:
            Logger.exception(str(no_trucks_in_db))
            self.trucks = ["brak zastepów w bazie"]
        try:
            string = str(requests.get(self.url).json()['passwd'])
            if string:
                with open(self.password_path, 'w') as file:
                    file.write(string)
        except Exception as no_password_in_db:
            Logger.exception(str(no_password_in_db))
        try:
            with open(self.password_path, 'r') as file:
                # global admin_password
                self.admin_password = file.readline()
        except Exception as no_password_file:
            Logger.exception(str(no_password_file))

    def update_reports_data(self):
        result = self.firebase_patch_all()
        if result == -1:
            Factory.connectionPopout().open()
        else:
            self.update_osp_data()
            Factory.updateOK().open()

    def put_report(self, uuid_num, id_number, dep_date, dep_time, spot_time, location, type_of_action,
                   section_com, action_com, driver, perpetrator, victim, section, details,
                   return_date, end_time, home_time, meter_reading, km_location, completed, truck_num):
        if uuid_num == "":
            uuid_num = str(uuid.uuid1())
        if section_com == "Dowódca sekcji":
            section_com = ""
        if action_com == "Dowódca akcji":
            action_com = ""
        if driver == "Kierowca":
            driver = ""
        if truck_num == "Zastęp":
            truck_num = ""
        self.store.put(uuid_num, innerID=id_number, depDate=dep_date, depTime=dep_time, spotTime=spot_time,
                       location=location, type=type_of_action,
                       sectionCom=section_com, actionCom=action_com, driver=driver, perpetrator=perpetrator,
                       victim=victim, section=section, details=details,
                       returnDate=return_date, endTime=end_time, homeTime=home_time, stanLicznika=meter_reading,
                       KM=km_location, modDate=self.get_date(), ready=completed, truck=truck_num)
        try:
            string = "{'" + uuid_num + "': " + str(self.store.get(uuid_num)) + "}"
            to_database = json.loads(string.replace("'", '"'))
            requests.patch(url=self.url, json=to_database)
            return 0
        except Exception as connection_error:
            Logger.exception(str(connection_error))
            return -1

    def delete_report(self, uuid_num):
        if self.store.exists(uuid_num):
            try:
                # requests.delete(url=self.url[:-5] + id_number + ".json")
                string = '{"deleted-' + uuid_num + '": "true"}'
                to_database = json.loads(string)
                requests.patch(url=self.url, json=to_database)
                self.store.delete(uuid_num)
            except Exception as connection_error:
                Factory.deletePopout().open()
                Logger.exception(str(connection_error))
        else:
            return -1

    def get_heroes(self):
        return self.heroes.get("all")

    def get_driver(self):
        return self.heroes.get("driver")

    def get_section_comm(self):
        return self.heroes.get("section")

    def get_action_comm(self):
        return self.heroes.get("action")

    def get_trucks(self):
        return self.trucks

    def firebase_patch_all(self):
        try:
            with open(self.path, 'r') as file:
                data = file.read()
                to_database = json.loads(data)
                requests.patch(url=self.url, json=to_database)
            to_database = json.loads('{"' + self.user + '": "' + self.version + '"}')
            requests.patch(url=self.base_url + "mobileVersion/" + self.secret, json=to_database)
            return 0
        except Exception as connection_error:
            Logger.exception(str(connection_error))
            return -1

    def delete_all(self):
        string_all = ""
        try:
            for key in self.store.keys():
                # requests.delete(url=self.url[:-5] + key + ".json")
                string = '{"deleted-' + key + '": "true"}'
                string_all = string_all + string
                to_database = json.loads(string)
                requests.patch(url=self.url, json=to_database)
                self.store.clear()
        except Exception as connection_error:
            Factory.deletePopout().open()
            Logger.exception(str(connection_error))

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
            meter_reading = dane['stanLicznika']
            km_location = dane['KM']
            date = dane['modDate']
            completed = dane['ready']
            truck_num = dane['truck']
            return [item[0], id_number, dep_date, dep_time, spot_time, location, type_of_action, section_com,
                    action_com, driver, perpetrator, victim, section, details,
                    return_date, end_time, home_time, meter_reading, km_location, date, completed, truck_num]
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

    def get_user(self):
        return self.user

    def get_password(self):
        # global admin_password
        return self.admin_password

    def change_osp(self, user, password):
        with open("data/login", 'r') as file:
            old_user = file.read().split("\n")[0]
        if user != old_user:
            try:
                user_password = str(requests.get(self.base_url + "passwd/" + user + self.secret).json())
                to_database = json.loads('{"' + user + '": "' + self.version + '"}')
                requests.patch(url=self.base_url + "mobileVersion/" + self.secret, json=to_database)
            except Exception as connection_error:
                Logger.exception(str(connection_error))
                return -2  # no connection
            if user_password == "UPDATE":
                return -3  # update neeeded
            if user_password == "None" or password != user_password:
                return -1  # wrong password

            self.url = self.base_url + user + self.secret
            try:
                string = str(requests.get(self.url).json()['heroes'])
                with open(self.heroes_path, 'w') as file:
                    file.write(string)
            except Exception as connection_error:
                Logger.exception(str(connection_error))
                with open(self.heroes_path, 'w') as file:
                    file.write("")
            try:
                with open(self.heroes_path, 'r') as file:
                    self.heroes = json.loads(str(file.read()).replace("'", '"'))
            except Exception as no_heroes_in_db:
                Logger.exception(str(no_heroes_in_db))
                self.heroes = ["brak strażaków w bazie"]
            try:
                string = str(requests.get(self.url).json()['trucks'])
                with open(self.trucks_path, 'w') as file:
                    file.write(string)
            except Exception as connection_error:
                Logger.exception(str(connection_error))
            try:
                with open(self.trucks_path, 'r') as file:
                    self.trucks = json.loads(str(file.read()).replace("'", '"'))
            except Exception as no_trucks_in_db:
                Logger.exception(str(no_trucks_in_db))
                self.trucks = ["brak zastepów w bazie"]
            try:
                string = str(requests.get(self.url).json()['passwd'])
                with open(self.password_path, 'w') as file:
                    file.write(string)
            except Exception as connection_error:
                Logger.exception(str(connection_error))
                self.url = self.base_url + self.user + self.secret
                return -2
            try:
                with open(self.password_path, 'r') as file:
                    self.admin_password = file.readline()
            except Exception as no_password:
                Logger.exception(str(no_password))
            self.store.clear()
            self.user = user
            with open("data/login", 'w') as file:
                file.write(user)
        return 0
