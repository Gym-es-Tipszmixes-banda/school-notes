import pyautogui
import time

while True:
    newmsg = pyautogui.locateCenterOnScreen('newmsg.png')
    pyautogui.moveTo(newmsg)
    pyautogui.moveRel(100, 0)
    pyautogui.click()
    time.sleep(1)
    btnback = pyautogui.locateCenterOnScreen('btnback.png', confidence = .8)
    pyautogui.moveTo(btnback)
    pyautogui.click()
    time.sleep(1)
