# pip install playsound

import sys
from playsound import playsound
import threading
import time
import multiprocessing
import pyautogui
import cv2


class threadMusic(threading.Thread):
    def __init__(self, nameSong):
        threading.Thread.__init__(self)
        self.nameSong = nameSong

    def run(self):
        playsound(self.nameSong)
        print('have a great day!')


class threadSelfie(threading.Thread):
    def __init__(self, image):
        threading.Thread.__init__(self)
        self.image = image

    def run(self):
        print('auto selftie after 2 second')
        path = f'images/selftie-{int(time.time())}.png'
        time.sleep(2)
        cv2.imwrite(path, self.image)

        print('selftie => done, save to path: ', path)


class threadScreenShoot(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)

    def run(self):
        print('auto screen shot after 2 second')
        time.sleep(2)
        path = f'images/screenShoot-{int(time.time())}.png'

        myScreenshot = pyautogui.screenshot()
        myScreenshot.save(path)
        print('screen shoot => save to path: ', path)


def startThread(d):
    d.setDaemon(True)
    d.start()


def closeFile():
    sys.exit("close player")


if __name__ == '__main__':
    thread1 = None
    a = input('nhap 1, 2 or 3: ')
    if a == '1':
        thread1 = threadMusic('music/Lalala.mp3')
    elif a == '2':
        thread1 = threadScreenShoot()
    elif a == '3':
        # thread1 = threadSelfie(image)
        print('should not try at home')
    else:
        closeFile()

    startThread(thread1)

    input('you wanna turn off ? :')
    print('have a great day.')
