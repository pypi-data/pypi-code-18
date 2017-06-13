import u3

d = u3.U3()
d.configIO(NumberOfTimersEnabled = 1)
#d.configIO(NumberOfTimersEnabled = 2)
d.getFeedback(u3.Timer0Config(TimerMode = 5))
while True:
    input("press enter to see the counter value")
    print("----------- \n ",d.getFeedback(u3.Timer0(UpdateReset = False, Value = 0, Mode = None)))
d.close()