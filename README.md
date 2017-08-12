# GPIOSystem
GPIO Plugin for Craftbeerpi 3.0

This plugin writes to native system files to control GPIO output (rather than relying on RPi.GPIO), allowing it to be used on non-Pi based setups.

The "Active" parameter allows the user to specify if the GPIO pin is Active High or Low.

On init, the plugin will configure/setup each GPIO. For persistent GPIO (if you don't auto run CraftbeerPi), add the following lines to /etc/rc.local for each GPIO 

    echo  <gpio#> > /sys/class/gpio/export
    echo <in/out> > /sys/class/gpio/gpio<#>/direction
    echo  <1/0> > /sys/class/gpio/gpio<#>/value

Known Issues:
The plugin will query any GPIO at /sys/class/gpio, and use these values as the only GPIO.  If nothing is found, it will default to a range of 0-200 (updated each run).
