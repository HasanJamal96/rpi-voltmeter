import RPi.GPIO as GPIO
import time

CLK = 11
MISO = 9
MOSI = 10
CS = 8


def init():
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(MOSI, GPIO.OUT)
    GPIO.setup(MISO, GPIO.IN)
    GPIO.setup(CLK, GPIO.OUT)
    GPIO.setup(CS, GPIO.OUT)
    pass


# read SPI data from MCP3008(or MCP3204) chip,8 possible adc's (0 thru 7)
def readadc(adcnum, clockpin, mosipin, misopin, cspin):
    if ((adcnum > 7) or (adcnum < 0)):
        return -1
    GPIO.output(cspin, True)

    GPIO.output(clockpin, False)  # start clock low
    GPIO.output(cspin, False)  # bring CS low

    commandout = adcnum
    commandout |= 0x18
    commandout <<= 3
    for i in range(5):
        if (commandout & 0x80):
            GPIO.output(mosipin, True)
        else:
            GPIO.output(mosipin, False)
        commandout <<= 1
        GPIO.output(clockpin, True)
        GPIO.output(clockpin, False)

    adcout = 0
    for i in range(12):
        GPIO.output(clockpin, True)
        GPIO.output(clockpin, False)
        adcout <<= 1
        if(GPIO.input(misopin)):
            adcout |= 0x1

    GPIO.output(cspin, True)

    adcout >>= 1
    return adcout


def main():
    init()
    time.sleep(2)
    while True:
        for i in range(3):
            ad_value = readadc(i, CLK, MOSI, MISO, CS)
            voltage = ad_value * (3.3 / 1024) * 5
            print("***********")
            print("Voltage at channel " + str(i) + " is " + str("%.2f" % voltage) + "V")
            print("***********")
            print(' ')
            time.sleep(0.5)


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        pass
GPIO.cleanup()

