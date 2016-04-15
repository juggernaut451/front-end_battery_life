import subprocess
"""
a = []
a = subprocess.check_output(["acpitool", "-B"])
print a.split()
"""
a = float(subprocess.check_output(["cat", "/sys/class/power_supply/BAT1/voltage_now"]))
print a/1000000