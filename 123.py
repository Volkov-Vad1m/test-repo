import time
import RPi.GPIO as GPIO # importiruem chob rabotalo
#
GPIO.setmode(GPIO.BCM)  # numeraziya pinov
chan_list = [10, 9, 11, 5, 6, 13, 19, 26]
GPIO.setup(chan_list, GPIO.OUT)
GPIO.setup(17, GPIO.OUT)
GPIO.setup(4, GPIO.IN)
GPIO.output(17, 1)

Vmax = 3.3

#def#
    
def GPIO_to_number(ledNumber):
    return chan_list[ledNumber]

def OffLight():
    for i in range (0, 8):
        GPIO.output(GPIO_to_number(i), 0)
    

def lightUp(ledNumber, period):
    ledNumber = GPIO_to_number(ledNumber)
    GPIO.output(ledNumber, 1)
    time.sleep(period)
    GPIO.output(ledNumber, 0)

def darkUp(ledNumber, period):
    ledNumber = GPIO_to_number(ledNumber)
    GPIO.output(ledNumber, 0)
    time.sleep(period)
    GPIO.output(ledNumber, 1)

def blink(ledNumber, blinkCount, blinkPeriod):
    for i in range (0, blinkCount):
        lightUp(ledNumber, blinkPeriod)
        time.sleep(blinkPeriod)


def runningLight(count, period):
    for i in range(0, count):
        for j in range(0, 8):
            lightUp(j, period)

def runningDark(count, period):
    for i in range(0, 8):
        GPIO.output(GPIO_to_number(i), 1)
    for i in range(0, count):
        for j in range(0, 8):
            darkUp(j, period)

def decToBinList(decNumber):
    b = 1
    a = [0, 0, 0, 0, 0, 0, 0, 0]

    for i in range(0, 8):
        if (b & (decNumber >> i) == 1):
            a[7 - i] = 1
    
    return a

def num2dac(value):
    x = decToBinList(value)
    GPIO.output(chan_list, tuple(x))

def lightNumber(number):
    bin_list = decToBinList(number)
    for i in range (0, 8):
        GPIO.output(GPIO_to_number(i), bin_list[7 - i]) 
    

def runningPattern(pattern, direction):
    lightNumber(pattern)
    if direction >= 0:
        lightNumber(pattern >> direction)
    else:
        lightNumber(pattern << abs(direction))
    OffLight()
    
    
def script1_old():

    number = 0
    while (True):
        print()
        number = int(input())
        if number == -1:
            break
        lightNumber(number)

def script2_old():
    print(111)
    repetitionsNumber = int(input())
    for i in range (0, repetitionsNumber):
        for j in range (0, 255):
            time.sleep(0.05)
            lightNumber(j)
        for j in range (255, 0, -1):
            time.sleep(0.05)
            lightNumber(j)

def script1():
    print("Enter value (-1 to exit): ")
    a = int(input())

    while(a != -1):
        b = float(float(a) / 255 * Vmax)
        b = format(b, '.2f')
        print (a, "=", b,"V")
        lightNumber(a)
        a = int(input())

def script2():
    while(True):
        for i in range(0, 255):
            lightNumber(i)
            time.sleep(0.00001)
            if(GPIO.input(4) == 0):
                b = float(float(i) / 255 * Vmax)
                b = format(b, '.2f')
                print("Digital value: ",i,", Analog value: ", b, "V")
                break

def script3():
    start = 0
    end = 255


    while(True):
        middle = (start + end) / 2
        lightNumber(int(middle))
        time.sleep(0.0001)
        if(GPIO.input(4) == 0):
            end = (start + end) / 2
        if(GPIO.input(4) == 1):
            start = (start + end) / 2
        if(int(start) == int(end)):
            b = float(float(start) / 256 * Vmax)
            b = format(b, '.2f')
            start = int(start)
            print("Digital value: ", start,", Analog value: ", b, "V")
            
            start = 0
            end = 255



#section code
try:  
    script3()
    time.sleep(1)




finally:
    OffLight()
    GPIO.cleanup()