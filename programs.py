import monomepi as m
import time



def simpleTrigger(instance):
    while True:
        key = instance.read_keys()
        instance.set_led(m.translate(key['c']), key['x'], key['y'])
        if key['x'] == '7' and key['y'] == '7':
            print 'exit!'
            break


def simpleToggle(instance):
    while True:
        key = instance.read_keys()
        if key['c'] == m.KEY_DN:
            if instance.get_led(key['x'], key['y']) == '0':
                instance.set_led(m.LED_ON_CMD, key['x'], key['y'])
            else:
                instance.set_led(m.LED_OFF_CMD, key['x'], key['y'])
        if key['x'] == '7' and key['y'] == '7':
            print 'exit!'
            break


                
        


tests = m.Monome('COM3', 115200, 5)
tests.open_serial()
tests.set_all(0)

simpleTrigger(tests)
#simpleToggle(tests)

tests.set_all(0)
tests.close_serial()
