from twitter import Tweets, TwitterThread
from ledscroll import LedScroller
from monomepi import PressListener, Button, ButtonHandler
from time import sleep
import threading

SCROLL_SPEED = 0.07


class TwitterScroll(LedScroller):

    def __init__(self, serial_port):
        super(TwitterScroll, self).__init__(serial_port)

    def new_tweet_animation(self):
        for i in range(4):
            self.set_col('7', 'FF')
            sleep(0.05)
            self.set_col('7', '00')
            sleep(0.05)



monome = TwitterScroll('COM3')
# Declare pressable buttons
buttons = [ Button(monome, 0, 7, 'toggle', 0.04),
            Button(monome, 1, 7, 'trigger'),
            Button(monome, 2, 7, 'trigger'),
            Button(monome, 3, 7, 'trigger'),
            Button(monome, 4, 7, 'trigger'),
            Button(monome, 7, 7, 'toggle') ]
monome.open_serial()

button_thread = ButtonHandler(monome, buttons)
button_thread.start()

twitter_thread = TwitterThread()
twitter_thread.start()

while not monome.check_if_exit():
    entry = twitter_thread.twitterdb.grab_tweet()
    if entry:
        if monome.check_if_exit(): break
        monome.new_tweet_animation()
        sleep(0.5)
        monome.push_msg(entry['screen_name'] + ': ' + entry['text'])
        monome.start_scroll(SCROLL_SPEED)
        monome.flush_all_msgs()
        if monome.check_if_exit(): break
        sleep(1)

twitter_thread.call_exit()
monome.close_serial()

print 'Threads: ', threading.activeCount()

