import time
from pynput.keyboard import Key, Controller

time.sleep(3)

print("go")

keyboard = Controller()

keyboard.press('w')
time.sleep(2)
keyboard.release('w')