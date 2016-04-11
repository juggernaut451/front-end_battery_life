import time,os,fnmatch
import numpy as np
import matplotlib.pyplot as plt
"""
plt.axis([0, 120, 30, 105])
plt.ion()
plt.show()

for i in range(100):
 y = 55
 plt.scatter(i, y)
 plt.draw()
 time.sleep(1) 
"""
found = 0
y = 0
for file in os.listdir('/sys/class/power_supply/'):
     if fnmatch.fnmatch(file, 'BAT*'):
      print file+" contains all the battery information"
      found += 1
if found == 0 :
  print "no battery information file found"

while 1:
  with open('/sys/class/power_supply/'+file+'/capacity', 'r') as f:
    plt.axis([0, y, 0, 100])
    plt.ion()
    plt.show()
    percentage = int(f.readlines()[0])
    #print percentage
    plt.scatter(y, percentage)
    plt.draw()
    time.sleep(1) 
    y = y+1
     


