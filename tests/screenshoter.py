import keyboard as kb
from time import strftime
import pyautogui as pag




while True:
        if kb.is_pressed("ctrl"):
            if kb.is_pressed("t"):
                exit(0)
        
            elif kb.is_pressed("r"):
                screenshot = pag.screenshot()
                screenshot.save(strftime("%H_%M_%S.png"))

