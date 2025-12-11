import pyautogui
import pydirectinput
import time
import os
import requests

# ================= CONFIG =================
DISCORD_WEBHOOK = "https://discord.com/api/webhooks/1441016778829467648/sMw059jkWiZgOV-v5MSlBPSMCMegglsuvElUuLypBPCTv1WPttIUHzCsnTudvl9oJabQ"
image_message = r"C:\Users\USER\Pictures\script fivem farm\images\recolte.png"
image_health = r"C:\Users\USER\Pictures\script fivem farm\images\recolte.png"

# Positions fixes (source → target)
objects_positions = [
    {"source": (510, 580), "target": (1468, 450)},  # boeuf
    # Ajouter d'autres objets ici plus tard
]

menu_key = 'k'
extra_key = 'e'
menu_delay = 1       # attendre que le menu apparaisse
close_menu_delay = 0.5
drag_duration = 1 # plus rapide
detection_interval = 0.1
action_cooldown = 3  # secondes minimum entre deux actions
action_eat = '4'
action_drink = '5'
stop_action = 'x'

# Vérification image
if not os.path.exists(image_message):
    print(f"[ERROR] Image non trouvée : {image_message}")
    exit()

def send_discord(msg):
    try:
        requests.post(DISCORD_WEBHOOK, json={"content": msg})
        print(f"[DEBUG] Discord : {msg}")
    except:
        print("[ERROR] Impossible d'envoyer Discord")

send_discord("🟢Script Lancé Récolte en cour ...")

def health_check():
    pos_health = pyautogui.locateCenterOnScreen(image_health, confidence=0.5)
    if pos_health:
        print(f"[DEBUG] Health OK détecté en ({pos_health.x},{pos_health.y})")
        return True
    else:
        print("[WARNING] Health NON détecté")
        return False

print("=== Script démarré ===")

last_action_time = 0

while True:
    try:
        # Vérification du message récolte
        pos_msg = pyautogui.locateCenterOnScreen(image_message, confidence=0.5)
        if not pos_msg:
            print("[DEBUG] Message NON détecté")
            time.sleep(detection_interval)
            continue

        print(f"[DEBUG] Message récolte détecté en ({pos_msg.x},{pos_msg.y})")
        now = time.time()
        if now - last_action_time < action_cooldown:
            print("[DEBUG] Cooldown actif")
            time.sleep(detection_interval)
            continue



        # ----------- OUVERTURE MENU -----------
        try:
            pydirectinput.press(menu_key)
            print(f"[DEBUG] Touche '{menu_key}' pressée (ouvrir menu)")
            time.sleep(menu_delay)
        except Exception as e:
            print(f"[ERROR] Impossible d'ouvrir le menu : {e}")

        # ----------- VIDER LES OBJETS -----------
        for obj in objects_positions:
            try:
                sx, sy = obj["source"]
                tx, ty = obj["target"]
                pyautogui.moveTo(sx, sy)
                pyautogui.mouseDown()
                pyautogui.dragTo(tx, ty, duration=drag_duration)
                pyautogui.mouseUp()
                print(f"[DEBUG] Drag-déposé de ({sx},{sy}) vers ({tx},{ty})")
            except Exception as e:
                print(f"[ERROR] Problème drag-déposé : {e}")

        # ----------- FERMER LE MENU -----------
        try:
            time.sleep(close_menu_delay)
            pydirectinput.press(menu_key)
            print("[DEBUG] Menu fermé")
        except Exception as e:
            print(f"[ERROR] Impossible de fermer le menu : {e}")

        # ----------- REPRISE RÉCOLTE -----------
        try:
            pydirectinput.press(extra_key)
            print(f"[DEBUG] Touche '{extra_key}' pressée (reprise récolte)")
        except Exception as e:
            print(f"[ERROR] Impossible de reprendre la récolte : {e}")

        last_action_time = now
        time.sleep(detection_interval)

    except Exception as e:
        print(f"[ERROR] Exception globale : {e}")
        time.sleep(1)
