from kivy.app import App
from kivy.clock import Clock
from kivy.core.text import LabelBase
from kivy.core.window import Window
from kivy.utils import get_color_from_hex
import subprocess

from time import strftime


class ClockApp(App):
    sw_started = False
    sw_seconds = 0

    def on_start(self):
        Clock.schedule_interval(self.update, 0)

    def update(self, nap):

        try:
            a = (float(subprocess.check_output(["cat", "/sys/class/power_supply/BAT1/charge_full"]))/1000000)/(float(subprocess.check_output(["cat", "/sys/class/power_supply/BAT1/charge_full_design"]))/1000000)
            a = a*100
            b = 100.00-a
            print b
        except Exception, e:
            raise e

        self.root.ids.status.text = subprocess.check_output(["cat", "/sys/class/power_supply/BAT1/status"])
        self.root.ids.battery_type.text = subprocess.check_output(["cat", "/sys/class/power_supply/BAT1/technology"])
        self.root.ids.battery_model.text = subprocess.check_output(["cat", "/sys/class/power_supply/BAT1/model_name"])
        self.root.ids.manufacturer.text = subprocess.check_output(["cat", "/sys/class/power_supply/BAT1/manufacturer"])
        self.root.ids.percentage.text = subprocess.check_output(["cat", "/sys/class/power_supply/BAT1/capacity"]).strip()+"%"
        self.root.ids.current_now.text = str(float(subprocess.check_output(["cat", "/sys/class/power_supply/BAT1/current_now"]))/1000000).strip()+"A"
        self.root.ids.voltage_now.text = str(float(subprocess.check_output(["cat", "/sys/class/power_supply/BAT1/voltage_now"]))/1000000).strip()+"V"
        self.root.ids.charge_now.text = str(float(subprocess.check_output(["cat", "/sys/class/power_supply/BAT1/voltage_now"]))/1000000).strip()+"Ah"
        self.root.ids.design_capacity.text = str(float(subprocess.check_output(["cat", "/sys/class/power_supply/BAT1/charge_full_design"]))/1000000).strip()+"A"
        self.root.ids.last_full_capacity.text = str(float(subprocess.check_output(["cat", "/sys/class/power_supply/BAT1/charge_full"]))/1000000)+"A"
        self.root.ids.last_full_capacity_perc.text = str(a)
        self.root.ids.capacity_loss_perc.text = str(b)
        """
        if self.sw_started:
            self.sw_seconds += nap

        self.root.ids.time.text = strftime('[b]%H[/b]:%M:%S')

        m, s = divmod(self.sw_seconds, 60)
        self.root.ids.stopwatch.text = ('%02d:%02d.[size=40]%02d[/size]' %
                                        (int(m), int(s), int(s * 100 % 100)))
        """
    def start_stop(self):
        self.root.ids.start_stop.text = 'Start' if self.sw_started else 'Stop'
        self.sw_started = not self.sw_started

    def reset(self):
        if self.sw_started:
            self.root.ids.start_stop.text = 'Start'
            self.sw_started = False

        self.sw_seconds = 0

    def temp(self):
        self.root.ids.temp.text = subprocess.check_output(["echo", "Hello World!"])

if __name__ == '__main__':
    Window.clearcolor = get_color_from_hex('#101216')
    LabelBase.register(name='Roboto',
                       fn_regular='Roboto-Thin.ttf',
                       fn_bold='Roboto-Medium.ttf')
    ClockApp().run()
