from __future__ import unicode_literals
from os.path import join
from kivy.core.window import Window
from kivy.uix.button import Button
from kivy.uix.label import Label

from database import DataBase
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.properties import ObjectProperty


class CreateReport(Screen):
    layout_content = ObjectProperty(None)

    def __init__(self, **kwargs):
        super(CreateReport, self).__init__(**kwargs)
        self.layout_content.bind(minimum_height=self.layout_content.setter('height'))

    def on_enter(self, *args):
        self.ids.scroll_id.scroll_to(self.ids.id_number)

    def submit(self):
        if db.find_inner_id(self.id_number.text) or self.id_number.text == "Taka L.P. już istnieje!":
            self.id_number.text = "Taka L.P. już istnieje!"
        else:
            db.put_report("", self.id_number.text, self.dep_date.text, self.dep_time.text, self.spot_time.text,
                          self.location.text, self.type_of_action.text, self.section_com.text, self.action_com.text,
                          self.driver.text, self.perpetrator.text, self.victim.text, self.section.text,
                          self.details.text,
                          self.return_date.text, self.end_time.text, self.home_time.text, self.stan_licznika.text,
                          self.km_location.text)
            CreateReport.clear(self)
            self.manager.transition.direction = "down"
            sm.current = "start"

    def clear(self):
        self.id_number.text = ""
        self.dep_date.text = ""
        self.dep_time.text = ""
        self.spot_time.text = ""
        self.location.text = ""
        self.type_of_action.text = ""
        self.section_com.text = ""
        self.action_com.text = ""
        self.driver.text = ""
        self.perpetrator.text = ""
        self.victim.text = ""
        self.section.text = ""
        self.details.text = ""
        self.return_date.text = ""
        self.end_time.text = ""
        self.home_time.text = ""
        self.stan_licznika.text = ""
        self.km_location.text = ""


class EditReport(Screen):
    layout_content = ObjectProperty(None)
    input_id = ""
    tmp_id = ""
    tmp_uuid = ""

    def __init__(self, **kwargs):
        super(EditReport, self).__init__(**kwargs)
        self.layout_content.bind(minimum_height=self.layout_content.setter('height'))

    def start(self, input_data):
        global input_id
        input_id = input_data

    def on_enter(self):
        self.ids.scroll_id.scroll_to(self.ids.uuid_num)
        global input_id
        result = db.get_report(input_id)
        self.uuid_num.text = result[0]
        self.id_number.text = result[1]
        self.dep_date.text = result[2]
        self.dep_time.text = result[3]
        self.spot_time.text = result[4]
        self.location.text = result[5]
        self.type_of_action.text = result[6]
        self.section_com.text = result[7]
        self.action_com.text = result[8]
        self.driver.text = result[9]
        self.perpetrator.text = result[10]
        self.victim.text = result[11]
        self.section.text = result[12]
        self.details.text = result[13]
        self.return_date.text = result[14]
        self.end_time.text = result[15]
        self.home_time.text = result[16]
        self.stan_licznika.text = result[17]
        self.km_location.text = result[18]
        self.modDate.text = result[19]
        global tmp_id
        tmp_id = result[1]

    def submit(self):
        global tmp_id
        if (self.id_number.text != tmp_id and db.find_inner_id(self.id_number.text)) or self.id_number.text == "Taka L.P. już istnieje!":
            self.id_number.text = "Taka L.P. już istnieje!"
        else:
            db.put_report(self.uuid_num.text, self.id_number.text, self.dep_date.text, self.dep_time.text,
                          self.spot_time.text,
                          self.location.text, self.type_of_action.text, self.section_com.text, self.action_com.text,
                          self.driver.text, self.perpetrator.text, self.victim.text, self.section.text,
                          self.details.text,
                          self.return_date.text, self.end_time.text, self.home_time.text, self.stan_licznika.text,
                          self.km_location.text)
            EditReport.clear(self)
            self.manager.transition.direction = "right"
            sm.current = "browser"

    def clear(self):
        self.uuid_num.text = ""
        self.id_number.text = ""
        self.dep_date.text = ""
        self.dep_time.text = ""
        self.spot_time.text = ""
        self.location.text = ""
        self.type_of_action.text = ""
        self.section_com.text = ""
        self.action_com.text = ""
        self.driver.text = ""
        self.perpetrator.text = ""
        self.victim.text = ""
        self.section.text = ""
        self.details.text = ""
        self.return_date.text = ""
        self.end_time.text = ""
        self.home_time.text = ""
        self.stan_licznika.text = ""
        self.km_location.text = ""
        self.modDate.text = ""

    def delete(self):
        global tmp_uuid
        db.delete_report(tmp_uuid)

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

        button_colors = [[1.75, 1.75, 1.75, 1], [2.01, 2.01, 2.01, 1]]
        button_type = 0

        for report in reports:
            button = Button(text=str(report), id=str(report).split(" ")[0], color=[0.29, 0.29, 0.29, 1], background_color=button_colors[button_type])
            button.bind(on_press=self.on_press)
            self.ids.layout_content.add_widget(button)
            button_type = not button_type

        if reports:
            self.ids.layout_content.add_widget(self.ids.del_but)
        else:
            label = Label(text="Brak raportów", id="test_id", bold=True, color=[0.29, 0.29, 0.29, 1], font_size=60)
            self.ids.layout_content.add_widget(label)

        self.ids.layout_content.add_widget(self.ids.cancel_but)

    def on_press(self, instance):
        EditReport().start(str(instance.id))
        self.manager.transition.direction = "left"
        sm.current = "edit"

    def cancel(self):
        self.manager.transition.direction = "down"
        sm.current = "start"

    def delete_all(self):
        db.delete_all()

    def try_delete(self):
        self.manager.transition.direction = "left"
        sm.current = "passwordAll"

    def clear(self):
        self.id_number.text = ""


class Password(Screen):
    layout_content = ObjectProperty(None)

    def delete(self):
        if self.password.text == "admin":
            EditReport().delete()
            self.password.text = ""
            self.manager.transition.direction = "right"
            sm.current = "browser"
        else:
            self.clear()
            self.ids.password.hint_text = "złe hasło!"

    def clear(self):
        self.password.text = ""


class PasswordAll(Screen):
    layout_content = ObjectProperty(None)

    def delete(self):
        if self.password.text == "admin":
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
screens = [StartWindow(name="start"), CreateReport(name="create"), Browser(name="browser"), Password(name="password"),
           EditReport(name="edit"), PasswordAll(name="passwordAll")]
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
        db = DataBase(App.get_running_app().storage)
        return sm

    @property
    def storage(self):
        return join(self.user_data_dir, 'storage.json')


if __name__ == "__main__":
    OSPApp().run()
