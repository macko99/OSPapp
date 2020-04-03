from __future__ import unicode_literals
from kivy.clock import mainthread
from kivy.uix.label import Label
from kivy.core.window import Window
from kivy.uix.button import Button
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

    def submit(self):
        if self.id_number.text == "" or self.id_number.text == "Pole wymagane" or self.id_number.text == "Taka L.P. już istnieje!":
            self.id_number.text = "Pole wymagane"
        elif db.if_exists(self.id_number.text):
            self.id_number.text = "Taka L.P. już istnieje!"
        else:
            db.put_report(self.id_number.text, self.dep_date.text, self.dep_time.text, self.spot_time.text,
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

    data = ""

    def __init__(self, **kwargs):
        super(EditReport, self).__init__(**kwargs)
        self.layout_content.bind(minimum_height=self.layout_content.setter('height'))

    def start(self, input_data):
        global data
        data = input_data

    def on_enter(self):
        result = db.get_report(data)
        self.id_number.text = result[0]
        self.dep_date.text = result[1]
        self.dep_time.text = result[2]
        self.spot_time.text = result[3]
        self.location.text = result[4]
        self.type_of_action.text = result[5]
        self.section_com.text = result[6]
        self.action_com.text = result[7]
        self.driver.text = result[8]
        self.perpetrator.text = result[9]
        self.victim.text = result[10]
        self.section.text = result[11]
        self.details.text = result[12]
        self.return_date.text = result[13]
        self.end_time.text = result[14]
        self.home_time.text = result[15]
        self.stan_licznika.text = result[16]
        self.km_location.text = result[17]
        self.modDate.text = result[18]

    def submit(self):
        db.put_report(self.id_number.text, self.dep_date.text, self.dep_time.text, self.spot_time.text,
                      self.location.text, self.type_of_action.text, self.section_com.text, self.action_com.text,
                      self.driver.text, self.perpetrator.text, self.victim.text, self.section.text, self.details.text,
                      self.return_date.text, self.end_time.text, self.home_time.text, self.stan_licznika.text,
                      self.km_location.text)
        EditReport.clear(self)
        self.manager.transition.direction = "right"
        sm.current = "browser"

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
        self.modDate.text = ""


class Browser(Screen):
    layout_content = ObjectProperty(None)

    def __init__(self, **kwargs):
        super(Browser, self).__init__(**kwargs)
        self.layout_content.bind(minimum_height=self.layout_content.setter('height'))

    @mainthread
    def on_enter(self):
        self.ids.layout_content.clear_widgets()
        label = Label(text="Wybierz raport do edycji:")
        self.ids.layout_content.add_widget(label)
        reports = db.get_all_array()
        for report in reports:
            button = Button(text="L.P. = " + str(report), id=str(report))
            button.bind(on_press=self.on_press)
            self.ids.layout_content.add_widget(button)

        if reports:
            label = Label(text="Wybierz raport do usunięcia poniżej:")
            self.ids.layout_content.add_widget(label)
            self.ids.layout_content.add_widget(self.ids.id_number)
            button = Button(text="Usuń")
            button.bind(on_press=self.try_delete)
            self.ids.layout_content.add_widget(button)
        else:
            label = Label(text="Brak raportów")
            self.ids.layout_content.add_widget(label)
            self.ids.layout_content.add_widget(self.ids.id_number)
        button = Button(text="Anuluj")
        button.bind(on_press=self.cancel)
        self.ids.layout_content.add_widget(button)

    def on_press(self, instance):
        EditReport().start(str(instance.id))
        self.manager.transition.direction = "left"
        sm.current = "edit"

    def cancel(self, instance):
        self.clear()
        self.manager.transition.direction = "down"
        sm.current = "start"

    id_number = ObjectProperty(None)
    tmp_id_number = ""

    #
    # def load(self):
    #     if not db.if_exists(self.id_number.text):
    #         self.id_number.text = "brak takiego raportu"
    #     else:
    #         EditReport().start(self.id_number.text)
    #         self.manager.transition.direction = "left"
    #         self.id_number.text = ""
    #         sm.current = "edit"

    def delete(self):
        global tmp_id_number
        db.delete_report(tmp_id_number)

    def try_delete(self, instance):
        if not db.if_exists(self.id_number.text):
            self.id_number.text = "brak takiego raportu"
        else:
            global tmp_id_number
            tmp_id_number = self.id_number.text
            self.id_number.text = ""
            self.manager.transition.direction = "left"
            sm.current = "password"

    def clear(self):
        self.id_number.text = ""


class Password(Screen):
    layout_content = ObjectProperty(None)
    password = ObjectProperty(None)

    def count(self):
        self.password.text = db.count_reports()

    def delete(self):
        if self.password.text == "admin":
            OSPApp.test.delete()
            self.password.text = ""
            self.manager.transition.direction = "right"
            sm.current = "browser"
        else:
            self.password.text = "złe hasło"

    def clear(self):
        self.password.text = ""


class StartWindow(Screen):
    pass


class WindowManager(ScreenManager):
    pass


Builder.load_file("my.kv")
sm = WindowManager()
db = DataBase()

screens = [StartWindow(name="start"), CreateReport(name="create"), Browser(name="browser"), Password(name="password"),
           EditReport(name="edit")]
for screen in screens:
    sm.add_widget(screen)

sm.current = "start"


class OSPApp(App):
    test = Browser()
    test2 = EditReport()

    def build(self):
        Window.bind(on_keyboard=self.key_input)
        return sm

    def key_input(self, window, key, scancode, codepoint, modifier):
        if key == 27:
            if sm.current != "start":
                sm.current = "start"
            return True
        else:
            return False


if __name__ == "__main__":
    OSPApp().run()
