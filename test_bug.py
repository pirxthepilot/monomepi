from monomepi import Monome, PressListener, Button, ButtonHandler
from time import sleep


def pause(sec):
    for i in range(sec+1):
        sleep(1)
        print str(i) + '..'

monome = Monome('COM3')
# Declare pressable buttons
##buttons = [ Button(monome, 0, 1, 'toggle'),
##            Button(monome, 0, 2, 'trigger'),
##            Button(monome, 0, 3, 'trigger'),
##            Button(monome, 0, 4, 'trigger'),
##            Button(monome, 0, 5, 'trigger'),
##            Button(monome, 0, 6, 'toggle') ]
buttons = [ Button(monome, 7, 7, 'toggle') ]
monome.open_serial()

button_thread = ButtonHandler(monome, buttons)
button_thread.start()

col = '42'
setval = '4'
monome.set_col('0', col)
monome.set_col('1', col)
pause(1)
monome.set_led('20', '0', setval)
monome.set_led('20', '2', setval)
#pause()
##monome.set_led('20', '0', '2')
##pause()
while monome.get_led('7', '7') != '1':
    pass


monome.call_exit()
monome.close_serial()


