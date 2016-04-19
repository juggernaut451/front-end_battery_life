from kivy.app import App
from kivy.clock import Clock
from kivy.core.text import LabelBase
from kivy.core.window import Window
from kivy.utils import get_color_from_hex
import subprocess
import fnmatch,os
import re,time
from pyfirmata import *
from serial.tools.list_ports import comports
from kivy.garden.graph import Graph

from time import strftime


class ClockApp(App):
    sw_started = False
    sw_seconds = 0
    file = ""
    charge = "charge"
    unit = "A"
    current = "current"



    def on_start(self):
        self.battery_file()
        Clock.schedule_interval(self.update, 0)

    def update(self, nap):

        try:
            a = (float(subprocess.check_output(["cat", "/sys/class/power_supply/"+self.file+"/"+self.charge+"_full"]))/1000000)/(float(subprocess.check_output(["cat", "/sys/class/power_supply/"+self.file+"/"+self.charge+"_full_design"]))/1000000)
            a = a*100
            b = 100.00-a

        except Exception, e:
            raise e


        self.root.ids.status.text = subprocess.check_output(["cat", "/sys/class/power_supply/"+self.file+"/status"])
        self.root.ids.battery_type.text = subprocess.check_output(["cat", "/sys/class/power_supply/"+self.file+"/technology"])
        self.root.ids.battery_model.text = subprocess.check_output(["cat", "/sys/class/power_supply/"+self.file+"/model_name"])
        self.root.ids.manufacturer.text = subprocess.check_output(["cat", "/sys/class/power_supply/"+self.file+"/manufacturer"])
        self.root.ids.percentage.text = subprocess.check_output(["cat", "/sys/class/power_supply/"+self.file+"/capacity"]).strip()+"%"
        self.root.ids.current_now.text = str(float(subprocess.check_output(["cat", "/sys/class/power_supply/"+self.file+"/"+self.current+"_now"]))/1000000).strip()+self.unit
        self.root.ids.voltage_now.text = str(float(subprocess.check_output(["cat", "/sys/class/power_supply/"+self.file+"/voltage_now"]))/1000000).strip()+"V"
        self.root.ids.charge_now.text = str(float(subprocess.check_output(["cat", "/sys/class/power_supply/"+self.file+"/voltage_now"]))/1000000).strip()+"Ah"
        self.root.ids.design_capacity.text = str(float(subprocess.check_output(["cat", "/sys/class/power_supply/"+self.file+"/"+self.charge+"_full_design"]))/1000000).strip()+self.unit
        self.root.ids.last_full_capacity.text = str(float(subprocess.check_output(["cat", "/sys/class/power_supply/"+self.file+"/"+self.charge+"_full"]))/1000000)+self.unit
        self.root.ids.last_full_capacity_perc.text = str(a)
        self.root.ids.capacity_loss_perc.text = str(b)
        #self.root.ids.reset.text = "aoeu"
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

    def battery_file(self):
        for file in os.listdir('/sys/class/power_supply/'):
             if fnmatch.fnmatch(file, 'BAT*'):
              print file+" contains all the battery information"
              #found += 1
        self.file = file     
        try:
            a = (float(subprocess.check_output(["cat", "/sys/class/power_supply/"+file+"/"+self.charge+"_full"]))/1000000)/(float(subprocess.check_output(["cat", "/sys/class/power_supply/"+self.file+"/"+self.charge+"_full_design"]))/1000000)
        except Exception, e:
            self.charge = "energy"
            self.current = "energy"
            self.unit = "Wh"
            self.root.ids.text_last_full_capacity.text = "Last Full Energy"
            self.root.ids.text_capacity_loss_perc.text = "Energy Loss %"


    def temp(self):
        self.root.ids.temp.text = subprocess.check_output(["echo", "Hello World!"])

    def board(self):
        boards_file = open('./boards.txt', 'r')
        boards_lines = boards_file.readlines()

        model = {}

        for line in boards_lines:
            match = re.search(r'(^[a-z]*)\.name=(.*)', line)
            if match:
                model[match.group(1)] = [match.group(2), [], []] # the two empty lists are the vid and pid lists

        for line in boards_lines:
            for k in model.keys():
                match_vid = re.search(r'^' + k + r'\.vid\.[0-9]*=0x([a-fA-F0-9]{4})', line)
                match_pid = re.search(r'^' + k + r'\.pid\.[0-9]*=0x([a-fA-F0-9]{4})', line)
                if match_vid:
                    model[k][1].append(match_vid.group(1).upper())
                elif match_pid:
                    model[k][2].append(match_pid.group(1).upper())

        prods = {'0001':'Arduino Uno'      , '0043':'Arduino Uno R3',
                 '0010':'Arduino Mega 2560', '0042':'Arduino Mega 2560 R3',
                 '003F':'Arduino Mega ADK' , '0044':'Arduino Mega ADK R3'}

        #Arduino vendor ID: 0x2341
        #Old Arduinos use the FTDI VID/PID (VID=0x0403)
        VIDs  = ['2341', '0403']

        sdevs = comports()
        intdev = []
        for dev in sdevs:
            if dev[2]!= 'n/a':
                intdev.append(dev)

        ptn = 'USB VID:PID=([A-F0-9]{4}):([A-F0-9]{4}) '
        arduinos = []
        for dev in intdev:
            match = re.search(ptn,dev[2])
            if match and match.group(1) == VIDs[0]:
                if match.group(2) in prods:
                    data = (prods[match.group(2)], dev[0])
                else:
                    data = ('Arduino', dev[0])
            elif match and match.group(1) == VIDs[1]:
                    data = ('FTDI', dev[0])
            else:
                data = ('Unknown', dev[0])
            arduinos.append(data)

        if not arduinos:
            self.root.ids.start_stop.text = 'No hardware connected !!!'
        else:
            print 'Connected Arduino device(s):'
            for ard in arduinos:
                self.root.ids.start_stop.text = ard[0], ' at ', ard[1] 
        
        

if __name__ == '__main__':
    Window.clearcolor = get_color_from_hex('#101216')
    LabelBase.register(name='Roboto',
                       fn_regular='Roboto-Thin.ttf',
                       fn_bold='Roboto-Medium.ttf')
    ClockApp().run()
