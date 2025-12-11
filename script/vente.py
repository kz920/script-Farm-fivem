import pyautogui
import pydirectinput
import time
import os
import requests
import json

# ================= CONFIG =================
DISCORD_WEBHOOK = "https://discord.com/api/webhooks/1441016778829467648/sMw059jkWiZgOV-v5MSlBPSMCMegglsuvElUuLypBPCTv1WPttIUHzCsnTudvl9oJabQ"
image_message = r"C:\Users\USER\Pictures\script fivem farm\images\recolte.png"

# Positions exactes
steak_pos = (1468, 450)     # position du steak dans le coffre
drag_target = (510, 580)    # position d'arrivée du steak

# Menu et touches
menu_key = 'k'
extra_key = 'e'
menu_delay = 0.6
close_menu_delay = 0.4
drag_duration = 0.3
detection_interval = 0.1
action_cooldown = 3

# ================= FONCTIONS =================
def send_discord(embed_title, embed_description, screenshot_path=None):
    """Envoie un embed Discord avec screenshot en pièce jointe."""
    data = {"embeds":[{"title": embed_title, "description": embed_description, "color": 65280}]}
    files = {}
    if screenshot_path and os.path.exists(screenshot_path):
        files["file"] = open(screenshot_path, "rb")
        data["embeds"][0]["image"] = {"url": "attachment://screenshot.png"}
    try:
        if files:
            requests.post(DISCORD_WEBHOOK, data={"payload_json": json.dumps(data)}, files=files)
        else:
            requests.post(DISCORD_WEBHOOK, json=data)
        print(f"[DEBUG] Discord envoyé : {embed_title}")
    except Exception as e:
        print(f"[ERROR] Impossible d'envoyer Discord : {e}")

def steak_present():
    """Vérifie si un steak est présent à la position connue."""
    try:
        screenshot = pyautogui.screenshot()
        pixel_color = screenshot.getpixel(steak_pos)
        # On peut ajuster la condition selon la couleur exacte du steak
        if pixel_color != (0,0,0):  # exemple : noir = vide
            print(f"[DEBUG] Steak détecté en {steak_pos}")
            return True
        else:
            print(f"[INFO] Pas de steak détecté")
            return False
    except Exception as e:
        print(f"[ERROR] Problème détection steak : {e}")
        return False

# ================= MAIN LOOP =================
print("=== Script démarré ===")
send_discord("🟢 Script lancé", "Vente en cour ...")

last_action_time = 0

while True:
    try:
        # Vérification du message de récolte
        pos_msg = pyautogui.locateCenterOnScreen(image_message, confidence=0.7)
        if not pos_msg:
            time.sleep(detection_interval)
            continue

        print(f"[DEBUG] Message récolte détecté en ({pos_msg.x},{pos_msg.y})")
        now = time.time()
        if now - last_action_time < action_cooldown:
            time.sleep(detection_interval)
            continue

        # Vérification steak
        if not steak_present():
            screenshot_path = r"C:\Users\USER\Pictures\sale_end.png"
            pyautogui.screenshot(screenshot_path)
            send_discord("🛑 Vente terminée", "Plus de steak détecté à la position connue.", screenshot_path)
            break

        # Ouvrir menu et drag-déposer
        pydirectinput.press(menu_key)
        time.sleep(menu_delay)
        pyautogui.moveTo(*steak_pos)
        pyautogui.mouseDown()
        pyautogui.dragTo(*drag_target, duration=drag_duration)
        pyautogui.mouseUp()
        pydirectinput.press(menu_key)
        time.sleep(close_menu_delay)

        # Reprendre récolte
        pydirectinput.press(extra_key)
        print(f"[DEBUG] '{extra_key}' pressée pour reprise")

        last_action_time = now
        time.sleep(detection_interval)

    except Exception as e:
        print(f"[ERROR] Exception globale : {e}")
        time.sleep(0.5)
