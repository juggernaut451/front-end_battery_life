from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.popup import Popup
from kivy.properties import ObjectProperty
from kivy.uix.label import Label 
import subprocess

class shellcommand(BoxLayout):
    first=ObjectProperty()
    second=ObjectProperty()
    third=ObjectProperty()

    def uname(self):
        v=subprocess.check_output("uname -a",shell=True)
        result=Popup(title="RESULT",content=Label(text="kernel is\n" + v))
        result.open()
    def date(self):
        d=subprocess.check_output("date",shell=True)
        res=Popup(title="DATE",content=Label(text="the date today is\n" + d))
        res.open()
    def last(self):
        last=subprocess.check_output("w",shell=True)
        ls=Popup(title="LOGIN",content=Label(text="logged in \n" + last))
        ls.open()


class shellApp(App):
    def build(self):
        return shellcommand()

shellApp().run()