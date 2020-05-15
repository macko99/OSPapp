from __future__ import unicode_literals

import datetime
import json
from os.path import join
from kivy.core.window import Window
from kivy.factory import Factory
from kivy.uix.button import Button
from kivy.uix.label import Label

from database import DataBase
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.properties import ObjectProperty

backg_color = (0.88, 0.98, 0.99, 1)
color_button = (0.6, 0.76, 0.85, 1)
color_dropdown = (0.75, 0.75, 0.75, 1)
color_font = (0.16, 0.2, 0.25, 1)
color_choose_btn = [(0.81, 0.81, 0.81, 1), (0.93, 0.94, 0.95, 1)]
color_yes_no = (0.93, 0.42, 0.3, 1)


class CreateReport(Screen):
    layout_content = ObjectProperty(None)

    def __init__(self, **kwargs):
        super(CreateReport, self).__init__(**kwargs)
        self.layout_content.bind(minimum_height=self.layout_content.setter('height'))
        self.asked = False

    def getYears(self):
        years = []
        for i in range(int(datetime.datetime.now().strftime("%Y")) - 2,
                       int(datetime.datetime.now().strftime("%Y")) + 3):
            years.append(str(i))
        years.append("dzisiaj")
        return years

    def on_enter(self, *args):
        self.ids.scroll_id.scroll_to(self.ids.id_number)
        self.ids.section_com.values = db.get_heroes() + json.loads('["Dowódca sekcji"]')
        self.ids.action_com.values = db.get_heroes() + json.loads('["Dowódca akcji"]')
        self.ids.driver.values = db.get_heroes() + json.loads('["Kierowca"]')
        self.dep_date_y.values = self.getYears()
        self.return_date_y.values = self.getYears()
        self.checkbox.text = "Nie"
        self.asked = False

    def on_spinner_select_depdate(self, text):
        if text == "dzisiaj":
            self.dep_date_d.text = str(datetime.datetime.now().strftime("%d"))
            self.dep_date_m.text = str(datetime.datetime.now().strftime("%m"))
            self.dep_date_y.text = str(datetime.datetime.now().strftime("%Y"))

    def on_spinner_select_returndate(self, text):
        if text == "dzisiaj":
            self.return_date_d.text = str(datetime.datetime.now().strftime("%d"))
            self.return_date_m.text = str(datetime.datetime.now().strftime("%m"))
            self.return_date_y.text = str(datetime.datetime.now().strftime("%Y"))

    def on_spinner_select_deptime(self, text):
        if text == "teraz":
            self.ids.dep_time_h.text = str(datetime.datetime.now().strftime("%H"))
            self.ids.dep_time_m.text = str(datetime.datetime.now().strftime("%M"))

    def on_spinner_select_spottime(self, text):
        if text == "teraz":
            self.ids.spot_time_h.text = str(datetime.datetime.now().strftime("%H"))
            self.ids.spot_time_m.text = str(datetime.datetime.now().strftime("%M"))

    def on_spinner_select_endtime(self, text):
        if text == "teraz":
            self.ids.end_time_h.text = str(datetime.datetime.now().strftime("%H"))
            self.ids.end_time_m.text = str(datetime.datetime.now().strftime("%M"))

    def on_spinner_select_hometime(self, text):
        if text == "teraz":
            self.ids.home_time_h.text = str(datetime.datetime.now().strftime("%H"))
            self.ids.home_time_m.text = str(datetime.datetime.now().strftime("%M"))

    def on_spinner_select(self, text):
        if text == "Tak" and not self.asked:
            Factory.readyPopout().open()
            self.asked = True

    def date_validator(self, date_str):
        day, month, year = date_str.split('.')
        try:
            datetime.datetime(int(year), int(month), int(day))
        except ValueError:
            return False
        else:
            return True

    def date_follower(self, str1, str2):
        day1, month1, year1 = str1.split('.')
        day2, month2, year2 = str2.split('.')
        try:
            date1 = datetime.datetime(int(year1), int(month1), int(day1))
            date2 = datetime.datetime(int(year2), int(month2), int(day2))
        except ValueError:
            return False
        else:
            return date1 <= date2

    def submit(self):
        if db.find_inner_id(self.id_number.text) or self.id_number.text == "Taka L.P. już istnieje!":
            Factory.IDpopout().open()
            self.id_number.text = ""
            self.ids.scroll_id.scroll_to(self.ids.id_number)
        else:
            if self.dep_date_d.text != "" and self.dep_date_m.text != "" and self.dep_date_y.text != "":
                dep_date = self.dep_date_d.text + "." + self.dep_date_m.text + "." + self.dep_date_y.text
                if not self.date_validator(dep_date):
                    Factory.datePopout().open()
                    self.ids.scroll_id.scroll_to(self.dep_date_d)
                    return
            else:
                dep_date = ""
            if self.return_date_d.text != "" and self.return_date_m.text != "" and self.return_date_y.text != "":
                return_date = self.return_date_d.text + "." + self.return_date_m.text + "." + self.return_date_y.text
                if not self.date_validator(return_date):
                    Factory.datePopout().open()
                    self.ids.scroll_id.scroll_to(self.return_date_d)
                    return
            else:
                return_date = ""
            if dep_date != "" and return_date != "":
                if not self.date_follower(dep_date, return_date):
                    Factory.date2Popout().open()
                    self.ids.scroll_id.scroll_to(self.return_date_d)
                    return
            if self.ids.dep_time_h.text != "" and self.ids.dep_time_m.text != "":
                dep_time = self.ids.dep_time_h.text + ":" + self.ids.dep_time_m.text
            else:
                dep_time = ""
            if self.ids.spot_time_h.text != "" and self.ids.spot_time_m.text != "":
                spot_time = self.ids.spot_time_h.text + ":" + self.ids.spot_time_m.text
            else:
                spot_time = ""
            if self.ids.end_time_h.text != "" and self.ids.end_time_m.text != "":
                end_time = self.ids.end_time_h.text + ":" + self.ids.end_time_m.text
            else:
                end_time = ""
            if self.ids.home_time_h.text != "" and self.ids.home_time_m.text != "":
                home_time = self.ids.home_time_h.text + ":" + self.ids.home_time_m.text
            else:
                home_time = ""
            db.put_report("", self.id_number.text, dep_date, dep_time, spot_time,
                          self.location.text, self.type_of_action.text, self.section_com.text, self.action_com.text,
                          self.driver.text, self.perpetrator.text, self.victim.text, self.section.text,
                          self.details.text, return_date, end_time, home_time, self.stan_licznika.text,
                          self.km_location.text, self.checkbox.text)
            self.clear()
            self.manager.transition.direction = "down"
            sm.current = "start"

    def clear(self):
        self.id_number.text = ""
        self.dep_date_y.text = ""
        self.dep_date_m.text = ""
        self.dep_date_d.text = ""
        self.ids.dep_time_h.text = ""
        self.ids.dep_time_m.text = ""
        self.ids.spot_time_h.text = ""
        self.ids.spot_time_m.text = ""
        self.location.text = ""
        self.type_of_action.text = ""
        self.section_com.text = "Dowódca sekcji"
        self.action_com.text = "Dowódca akcji"
        self.driver.text = "Kierowca"
        self.perpetrator.text = ""
        self.victim.text = ""
        self.section.text = ""
        self.details.text = ""
        self.return_date_d.text = ""
        self.return_date_m.text = ""
        self.return_date_y.text = ""
        self.ids.end_time_h.text = ""
        self.ids.home_time_h.text = ""
        self.ids.end_time_m.text = ""
        self.ids.home_time_m.text = ""
        self.stan_licznika.text = ""
        self.km_location.text = ""
        self.checkbox.text = ""


class EditReport(Screen):
    layout_content = ObjectProperty(None)
    input_id = ""
    tmp_id = ""
    tmp_uuid = ""
    result = []

    def __init__(self, **kwargs):
        super(EditReport, self).__init__(**kwargs)
        self.layout_content.bind(minimum_height=self.layout_content.setter('height'))
        self.asked = True

    def getYears(self):
        years = []
        for i in range(int(datetime.datetime.now().strftime("%Y")) - 2,
                       int(datetime.datetime.now().strftime("%Y")) + 3):
            years.append(str(i))
        years.append("dzisiaj")
        return years

    def start(self, input_data):
        global result
        result = db.get_report(input_data)

    def on_enter(self):
        self.ids.scroll_id.scroll_to(self.ids.id_number)
        global result
        self.uuid_num.text = "UUID: " + result[0]
        self.id_number.text = result[1]
        if result[2] != "":
            self.dep_date_d.text = str(result[2]).split(".")[0]
            self.dep_date_m.text = str(result[2]).split(".")[1]
            self.dep_date_y.text = str(result[2]).split(".")[2]
        if result[3] != "":
            self.ids.dep_time_h.text = str(result[3]).split(":")[0]
            self.ids.dep_time_m.text = str(result[3]).split(":")[1]
        if result[4] != "":
            self.ids.spot_time_h.text = str(result[4]).split(":")[0]
            self.ids.spot_time_m.text = str(result[4]).split(":")[1]
        self.location.text = result[5]
        self.type_of_action.text = result[6]
        if result[7] != "":
            self.section_com.text = result[7]
        if result[8] != "":
            self.action_com.text = result[8]
        if result[9] != "":
            self.driver.text = result[9]
        self.perpetrator.text = result[10]
        self.victim.text = result[11]
        self.section.text = result[12]
        self.details.text = result[13]
        if result[14] != "":
            self.return_date_d.text = str(result[14]).split(".")[0]
            self.return_date_m.text = str(result[14]).split(".")[1]
            self.return_date_y.text = str(result[14]).split(".")[2]
        if result[15] != "":
            self.ids.end_time_h.text = str(result[15]).split(":")[0]
            self.ids.end_time_m.text = str(result[15]).split(":")[1]
        if result[16] != "":
            self.ids.home_time_h.text = str(result[16]).split(":")[0]
            self.ids.home_time_m.text = str(result[16]).split(":")[1]
        self.stan_licznika.text = result[17]
        self.km_location.text = result[18]
        self.modDate.text = result[19][:10] + "\n" + result[19][10:]
        self.checkbox.text = result[20]
        if result[20] == "Tak":
            self.asked = True
        else:
            self.asked = False
        global tmp_id
        tmp_id = result[1]
        self.ids.action_com.values = db.get_heroes() + json.loads('["Dowódca akcji"]')
        self.ids.driver.values = db.get_heroes() + json.loads('["Kierowca"]')
        self.ids.section_com.values = db.get_heroes() + json.loads('["Dowódca sekcji"]')
        self.dep_date_y.values = self.getYears()
        self.return_date_y.values = self.getYears()

    def date_validator(self, date_str):
        day, month, year = date_str.split('.')
        try:
            datetime.datetime(int(year), int(month), int(day))
        except ValueError:
            return False
        else:
            return True

    def date_follower(self, str1, str2):
        day1, month1, year1 = str1.split('.')
        day2, month2, year2 = str2.split('.')
        try:
            date1 = datetime.datetime(int(year1), int(month1), int(day1))
            date2 = datetime.datetime(int(year2), int(month2), int(day2))
        except ValueError:
            return False
        else:
            return date1 <= date2

    def on_spinner_select_depdate(self, text):
        if text == "dzisiaj":
            self.dep_date_d.text = str(datetime.datetime.now().strftime("%d"))
            self.dep_date_m.text = str(datetime.datetime.now().strftime("%m"))
            self.dep_date_y.text = str(datetime.datetime.now().strftime("%Y"))

    def on_spinner_select_returndate(self, text):
        if text == "dzisiaj":
            self.return_date_d.text = str(datetime.datetime.now().strftime("%d"))
            self.return_date_m.text = str(datetime.datetime.now().strftime("%m"))
            self.return_date_y.text = str(datetime.datetime.now().strftime("%Y"))

    def on_spinner_select_deptime(self, text):
        if text == "teraz":
            self.ids.dep_time_h.text = str(datetime.datetime.now().strftime("%H"))
            self.ids.dep_time_m.text = str(datetime.datetime.now().strftime("%M"))

    def on_spinner_select_spottime(self, text):
        if text == "teraz":
            self.ids.spot_time_h.text = str(datetime.datetime.now().strftime("%H"))
            self.ids.spot_time_m.text = str(datetime.datetime.now().strftime("%M"))

    def on_spinner_select_endtime(self, text):
        if text == "teraz":
            self.ids.end_time_h.text = str(datetime.datetime.now().strftime("%H"))
            self.ids.end_time_m.text = str(datetime.datetime.now().strftime("%M"))

    def on_spinner_select_hometime(self, text):
        if text == "teraz":
            self.ids.home_time_h.text = str(datetime.datetime.now().strftime("%H"))
            self.ids.home_time_m.text = str(datetime.datetime.now().strftime("%M"))

    def on_spinner_select(self, text):
        if text == "Tak" and not self.asked:
            Factory.readyPopout().open()
            self.asked = True

    def submit(self):
        global tmp_id
        if (self.id_number.text != tmp_id and db.find_inner_id(
                self.id_number.text)) or self.id_number.text == "Taka L.P. już istnieje!":
            Factory.IDpopout().open()
            self.id_number.text = ""
            self.ids.scroll_id.scroll_to(self.ids.id_number)
        else:
            if self.dep_date_d.text != "" and self.dep_date_m.text != "" and self.dep_date_y.text != "":
                dep_date = self.dep_date_d.text + "." + self.dep_date_m.text + "." + self.dep_date_y.text
                if not self.date_validator(dep_date):
                    Factory.datePopout().open()
                    self.ids.scroll_id.scroll_to(self.dep_date_d)
                    return
            else:
                dep_date = ""
            if self.return_date_d.text != "" and self.return_date_m.text != "" and self.return_date_y.text != "":
                return_date = self.return_date_d.text + "." + self.return_date_m.text + "." + self.return_date_y.text
                if not self.date_validator(return_date):
                    Factory.datePopout().open()
                    self.ids.scroll_id.scroll_to(self.return_date_d)
                    return
            else:
                return_date = ""
            if dep_date != "" and return_date != "":
                if not self.date_follower(dep_date, return_date):
                    Factory.date2Popout().open()
                    self.ids.scroll_id.scroll_to(self.return_date_d)
                    return
            if self.ids.dep_time_h.text != "" and self.ids.dep_time_m.text != "":
                dep_time = self.ids.dep_time_h.text + ":" + self.ids.dep_time_m.text
            else:
                dep_time = ""
            if self.ids.spot_time_h.text != "" and self.ids.spot_time_m.text != "":
                spot_time = self.ids.spot_time_h.text + ":" + self.ids.spot_time_m.text
            else:
                spot_time = ""
            if self.ids.end_time_h.text != "" and self.ids.end_time_m.text != "":
                end_time = self.ids.end_time_h.text + ":" + self.ids.end_time_m.text
            else:
                end_time = ""
            if self.ids.home_time_h.text != "" and self.ids.home_time_m.text != "":
                home_time = self.ids.home_time_h.text + ":" + self.ids.home_time_m.text
            else:
                home_time = ""
            db.put_report(self.uuid_num.text[6:], self.id_number.text, dep_date, dep_time,
                          spot_time,
                          self.location.text, self.type_of_action.text, self.section_com.text, self.action_com.text,
                          self.driver.text, self.perpetrator.text, self.victim.text, self.section.text,
                          self.details.text,
                          return_date, end_time, home_time, self.stan_licznika.text,
                          self.km_location.text, self.checkbox.text)
            self.clear()
            self.manager.transition.direction = "right"
            sm.current = "browser"

    def clear(self):
        self.uuid_num.text = ""
        self.id_number.text = ""
        self.dep_date_y.text = ""
        self.dep_date_m.text = ""
        self.dep_date_d.text = ""
        self.ids.dep_time_h.text = ""
        self.ids.dep_time_m.text = ""
        self.ids.spot_time_h.text = ""
        self.ids.spot_time_m.text = ""
        self.location.text = ""
        self.type_of_action.text = ""
        self.section_com.text = "Dowódca sekcji"
        self.action_com.text = "Dowódca akcji"
        self.driver.text = "Kierowca"
        self.perpetrator.text = ""
        self.victim.text = ""
        self.section.text = ""
        self.details.text = ""
        self.return_date_y.text = ""
        self.return_date_m.text = ""
        self.return_date_d.text = ""
        self.ids.end_time_h.text = ""
        self.ids.home_time_h.text = ""
        self.ids.end_time_m.text = ""
        self.ids.home_time_m.text = ""
        self.stan_licznika.text = ""
        self.km_location.text = ""
        self.modDate.text = ""
        self.checkbox.text = ""

    def delete(self):
        global tmp_uuid
        db.delete_report(tmp_uuid[6:])

    def try_delete(self):
        global tmp_uuid
        tmp_uuid = self.uuid_num.text
        self.manager.transition.direction = "left"
        sm.current = "password"


class Browser(Screen):
    layout_content = ObjectProperty(None)

    def __init__(self, **kwargs):
        super(Browser, self).__init__(**kwargs)
        self.layout_content.bind(minimum_height=self.layout_content.setter('height'))

    def on_enter(self):
        self.ids.layout_content.clear_widgets()
        self.ids.layout_content.add_widget(self.ids.id1)
        reports = db.get_all_friendly()

        button_font_size_factor = 1 / 28
        button_type = 0

        for report in reports:
            button = Button(text=str(report), id=str(report).split(" ")[0],
                            color=color_font,
                            background_normal='',
                            background_color=color_choose_btn[button_type],
                            font_size=self.layout_content.width * button_font_size_factor)
            button.bind(on_release=self.on_press)
            self.ids.layout_content.add_widget(button)
            button_type = not button_type

        if reports:
            button = Button(text="Usuń wszystkie", id="del_but",
                            font_size=self.layout_content.width * button_font_size_factor,
                            background_normal='',
                            background_color=color_button,
                            color=color_font)
            button.bind(on_release=self.try_delete)
            self.ids.layout_content.add_widget(button)
        else:
            label = Label(text="Brak raportów", id="test_id", bold=True,
                          color=color_font,
                          font_size=self.layout_content.width * button_font_size_factor)
            self.ids.layout_content.add_widget(label)

        self.ids.layout_content.add_widget(self.ids.cancel_but)

    def on_press(self, instance):
        ed.start(str(instance.id))
        self.manager.transition.direction = "left"
        sm.current = "edit"

    def cancel(self):
        self.manager.transition.direction = "down"
        sm.current = "start"

    def delete_all(self):
        db.delete_all()

    def try_delete(self, instance):
        self.manager.transition.direction = "left"
        sm.current = "passwordAll"

    def clear(self):
        self.id_number.text = ""


class Password(Screen):
    layout_content = ObjectProperty(None)

    def on_enter(self):
        self.password.text = ""

    def delete(self):
        if self.password.text == db.get_passwd():
            ed.delete()
            self.password.text = ""
            self.manager.transition.direction = "right"
            sm.current = "browser"
        else:
            self.clear()
            self.ids.password.hint_text = "złe hasło!"

    def clear(self):
        self.password.text = ""


class Login(Screen):
    layout_content = ObjectProperty(None)

    def on_enter(self):
        self.clear()
        Factory.changePopout().open()

    def change(self):
        if self.password.text != "" and self.user.text != "":
            res = db.changeOSP(self.user.text, self.password.text)
            self.clear()
            if res == -1:
                Factory.userPopout().open()
            elif res == -2:
                Factory.connectionPopout().open()
                self.manager.transition.direction = "right"
                sm.current = "start"
            else:
                self.manager.transition.direction = "right"
                sm.current = "start"
        elif self.user.text == "":
            self.ids.user.hint_text = "podaj OSP!"
        else:
            self.ids.password.hint_text = "podaj hasło!"

    def clear(self):
        self.user.text = ""
        self.password.text = ""


class PasswordAll(Screen):
    layout_content = ObjectProperty(None)

    def on_enter(self):
        self.password.text = ""

    def delete(self):
        if self.password.text == db.get_passwd():
            Browser().delete_all()
            self.password.text = ""
            self.manager.transition.direction = "right"
            sm.current = "browser"
        else:
            self.clear()
            self.ids.password.hint_text = "złe hasło!"

    def clear(self):
        self.password.text = ""


class StartWindow(Screen):
    pass


class WindowManager(ScreenManager):
    pass


Builder.load_file("my.kv")
sm = WindowManager()
global db
global ed
ed = EditReport(name="edit")
screens = [StartWindow(name="start"), CreateReport(name="create"), Browser(name="browser"), Password(name="password"),
           ed, PasswordAll(name="passwordAll"), Login(name="login")]
for screen in screens:
    sm.add_widget(screen)
sm.current = "start"


def key_input(window, key, scancode, codepoint, modifier):
    if key == 27:
        if sm.current != "start":
            sm.current = "start"
        return True
    else:
        return False


class OSPApp(App):

    def build(self):
        Window.bind(on_keyboard=key_input)
        global db
        db = DataBase(App.get_running_app().storage, App.get_running_app().heroes, App.get_running_app().passwd)
        return sm

    @property
    def storage(self):
        return join(self.user_data_dir, 'storage.json')

    @property
    def heroes(self):
        return join(self.user_data_dir, 'heroes')

    @property
    def passwd(self):
        return join(self.user_data_dir, 'passwd')


if __name__ == "__main__":
    OSPApp().run()
