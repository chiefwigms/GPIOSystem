import fnmatch
import os

from modules import cbpi
from modules.core.hardware import ActorBase
from modules.core.props import Property

GPIO_PATH = '/sys/class/gpio'
GPIO_MAX  = 200
GPIO_MIN  = 0
GPIO_HIGH = '1'
GPIO_LOW  = '0'
GPIO_IN   = 'in'
GPIO_OUT  = 'out'

def listGPIO():
    #Lists any GPIO in found in /sys/class/gpio
    try:
        arr = []
        for dirname in os.listdir(GPIO_PATH):
            if fnmatch.fnmatch(dirname, 'gpio[0123456789]*'):
                arr.append(dirname[4:])
        if not arr:
            print('No active GPIO found - using default range!')
            arr = list(range(GPIO_MIN, GPIO_MAX))
        return arr
    except:
        print('Error listing GPIO!')
        return []

def setupGPIO(device, value):
    #Sets up GPIO if not defined on system boot (i.e. /etc/rc.local)
    #echo  <gpio#> > /sys/class/gpio/export
    #echo <in/out> > /sys/class/gpio/gpio<#>/direction
    try:
        if not os.path.exists(GPIO_PATH + ('/gpio%d' % device)):
            with open(GPIO_PATH + '/export', 'w') as fp:
                fp.write(str(device))
            with open( GPIO_PATH + ('/gpio%d/direction' % device), 'w') as fp:
                fp.write('out')
    except:
        print(('Error setting up GPIO%d!' % device))

def outputGPIO(device, value):
    #Outputs new GPIO value
    #echo <1/0> > /sys/class/gpio/gpio<#>/value
    try:
        with open(GPIO_PATH + ('/gpio%d/value' % device), 'w') as fp:
            fp.write(value)
    except:
        print(('Error writing to GPIO%d!' % device))


@cbpi.actor
class GPIOSystem(ActorBase):

    gpio = Property.Select("GPIO", listGPIO(), description="GPIO number to which the actor is connected")
    active = Property.Select("Active", options=["High","Low"], description="Selects if the GPIO is Active High (On = 1, Off = 0) or Low (On = 0, Off = 1)")

    def init(self):
        setupGPIO(int(self.gpio), GPIO_OUT)
        if (self.active == "High"):
            outputGPIO(int(self.gpio), GPIO_LOW)
        else:
            outputGPIO(int(self.gpio), GPIO_HIGH)

    def on(self, power=0):
        if (self.active == "High"):
            outputGPIO(int(self.gpio), GPIO_HIGH)
        else:
            outputGPIO(int(self.gpio), GPIO_LOW)

    def off(self):
        if (self.active == "High"):
            outputGPIO(int(self.gpio), GPIO_LOW)
        else:
            outputGPIO(int(self.gpio), GPIO_HIGH)
