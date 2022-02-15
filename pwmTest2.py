hiC = 0
reset = 0
if(GPIO.input(19)):
    hiC+=1
time.sleep(.0001)
reset +=1
if(reset == 20):
    print(hiC)
    hiC = 0
    reset = 0


