import time
from win10batteryoptimizer import Notifier

# #############################################################################
# ###### Stand alone program ########
# ###################################
if __name__ == "__main__":
    notifier = Notifier()
    battery_percent = notifier.get_battery_level()
    battery_line_status = notifier.get_battery_line()
    while ((int)(battery_percent>80) and (int)(battery_line_status)):
        notifier.create_plug_out_toast()
        time.sleep(600)
    while ((int)(battery_percent<40) and (int)(battery_line_status)==0):
        notifier.create_plug_in_toast()
        time.sleep(600)
    while ((int)(battery_percent)>39 and (int)(battery_percent)<81):
        time.sleep(600)