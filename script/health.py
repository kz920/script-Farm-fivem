import pyautogui
import pydirectinput
import time
import os

class Action:
     def __init__(self):
        self.x = 'x'
        self.k = 'k'
        self.e = 'e'
        self.Drink = '4'
        self.Eat = '5'

        self.delay = 1
        self.close_menu_delay = 0.5
        self.detection_interval = 0.1
        self.cooldown = 3

        self.Image_Health = r"C:\Users\USER\Desktop\script fivem farm\images\health_gris.png"
        self.Image_Health2 = r"C:\Users\USER\Desktop\script fivem farm\images\health_blue.png"
        self.Image_message = r"C:\Users\USER\Pictures\script fivem farm\images\recolte.png"
        self.Image_Boeuf = r"C:\Users\USER\Desktop\script\images\boeuf.png"
        self.Image_Steak = r"C:\Users\USER\Desktop\script\images\steak.png"

        DISCORD_WEBHOOK = "https://discord.com/api/webhooks/1441016778829467648/sMw059jkWiZgOV-v5MSlBPSMCMegglsuvElUuLypBPCTv1WPttIUHzCsnTudvl9oJabQ"
if not os.path.exists(Action.Image_Health):
    print(f"[ERROR] Image non trouvée : {Action.Image_Health}, {Action.Image_Health2}, {Action.Image_message}, {Action.Image_Boeuf}, {Action.Image_Steak}")
    exit()

def Heath_check():
    pos_health = pyautogui.locateCenterOnScreen(Action.Image_Health, confidence=0.7)
    pos_health = pyautogui.locateCenterOnScreen(Action.Image_Health2, confidence=0.7)
    if pos_health:
        if Action.Image_Health:
            print(f"[DEBUG] Santé en gris trouvée. ({Action.Image_Health.x},({Action.Image_Health.y}))")
            return "gray"
    elif Action.Image_Health2:
            print(f"[DEBUG] Santé en bleu trouvée. ({Action.Image_Health2.x},({Action.Image_Health2.y})")
            return "blue"
    else:
            print("[DEBUG] Santé non trouvée.")
            return "unknown"

while True:
    health = Heath_check()
    if health == "gray":
        print("Santé en gris, je fais l'action.")
        pydirectinput.press(Action.action_x)
        time.sleep(0.1)
        pydirectinput.press(Action.action_x)
        time.sleep(0.1)
        pydirectinput.press(Action.action_Drink)
        time.sleep(Action.delay)
        pydirectinput.press(Action.action_Eat)
    elif health == "blue":
        pass
    else:
        pass
    time.sleep(Action.cooldown)
