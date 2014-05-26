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


tests = m.Monome('COM6', 115200)
tests.open_serial()

print "Ahoy"
time.sleep(3)
#simpleTrigger(tests)
#while True:
#    tests.read_keys()
#    tests.toggle()

tests.close_serial()
