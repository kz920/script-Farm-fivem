
                
import pyautogui
import pydirectinput
import time
import os
import requests


class Action:
    DISCORD_WEBHOOK = "https://discord.com/api/webhooks/1441016778829467648/sMw059jkWiZgOV-v5MSlBPSMCMegglsuvElUuLypBPCTv1WPttIUHzCsnTudvl9oJabQ"

    Image_Health = r"C:\Users\USER\Desktop\script\images\health.png"
    Image_Health2 = r"C:\Users\USER\Desktop\script\images\health.png"
    Image_message = r"C:\Users\USER\Desktop\script\images\recolte.png"
    Image_Boeuf = r"C:\Users\USER\Desktop\script\images\boeuf.png"
    Image_Steak = r"C:\Users\USER\Desktop\script\images\steak.png"

    def __init__(self):
        self.x = 'x'
        self.k = 'k'
        self.e = 'e'
        self.Drink = '4'
        self.Eat = '5'

        self.drag_duration = 1 # plus rapide
        self.last_action_time = 0

        self.delay = 1
        self.close_menu_delay = 0.5
        self.detection_interval = 0.1
        self.cooldown = 3
        
action = Action()
images = [
    action.Image_Health,
    action.Image_Health2,
    action.Image_message,
    action.Image_Boeuf,
    action.Image_Steak
]

if not all(os.path.exists(path) for path in images):
    print(f"[ERROR] Certaines images sont manquantes : {', '.join([path for path in images if not os.path.exists(path)])}")
    exit()

# Positions fixes (source → target)
objects_positions = [
    {"source": (510, 580), "target": (1468, 450)},  # boeuf
    # Ajouter d'autres objets ici plus tard
]

def send_discord(msg):
    try:
        requests.post(Action.DISCORD_WEBHOOK, json={"content": msg})
        print(f"[DEBUG] Discord : {msg}")
    except:
        print("[ERROR] Impossible d'envoyer Discord")
send_discord("🟢Script Lancé Récolte en cour ...")

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
    try:
        # Vérification du message récolte
        pos_msg = pyautogui.locateCenterOnScreen(Action.Image_message, confidence=0.5)
        if not pos_msg:
            print("[DEBUG] Message NON détecté")
            time.sleep(Action.detection_interval)
            continue

        print(f"[DEBUG] Message récolte détecté en ({pos_msg.x},{pos_msg.y})")
        now = time.time()
        if now - Action.last_action_time < Action.cooldown:
            print("[DEBUG] Cooldown actif")
            time.sleep(Action.detection_interval)
            continue
        # ----------- HEAL CHECK -----------
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
        # ----------- OUVERTURE MENU -----------
        try:
            pydirectinput.press(Action.k)
            print(f"[DEBUG] Touche '{Action.k}' pressée (ouvrir menu)")
            time.sleep(Action.delay)
        except Exception as e:
            print(f"[ERROR] Impossible d'ouvrir le menu : {e}")

        # ----------- VIDER LES OBJETS -----------
        for obj in objects_positions:
            try:
                sx, sy = obj["source"]
                tx, ty = obj["target"]
                pyautogui.moveTo(sx, sy)
                pyautogui.mouseDown()
                pyautogui.dragTo(tx, ty, duration=Action.drag_duration)
                pyautogui.mouseUp()
                print(f"[DEBUG] Drag-déposé de ({sx},{sy}) vers ({tx},{ty})")
            except Exception as e:
                print(f"[ERROR] Problème drag-déposé : {e}")

        # ----------- FERMER LE MENU -----------
        try:
            time.sleep(Action.close_menu_delay)
            pydirectinput.press(Action.k)
            print("[DEBUG] Menu fermé")
        except Exception as e:
            print(f"[ERROR] Impossible de fermer le menu : {e}")

        # ----------- REPRISE RÉCOLTE -----------
        try:
            pydirectinput.press(Action.e)
            print(f"[DEBUG] Touche '{Action.e}' pressée (reprise récolte)")
        except Exception as e:
            print(f"[ERROR] Impossible de reprendre la récolte : {e}")

        Action.last_action_time = now
        time.sleep(Action.detection_interval)

    except Exception as e:
        print(f"[ERROR] Exception globale : {e}")
        time.sleep(1)
