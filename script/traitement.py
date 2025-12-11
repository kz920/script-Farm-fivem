import pydirectinput
import time
import json

FICHIER_TRAJET = r"C:\Users\USER\Pictures\script fivem farm\trajet.json"

# Charger le trajet
with open(FICHIER_TRAJET, "r") as f:
    sequence = json.load(f)

print("▶️ Reproduction du trajet dans 3 secondes, mets le jeu en focus...")
time.sleep(3)

for item in sequence:
    key = item.get("key")
    action = item.get("action")
    duration = item.get("time", 0.1)  # durée entre down et up si action 'down'
    
    if action == "down":
        pydirectinput.keyDown(key)
        time.sleep(duration)
    elif action == "up":
        pydirectinput.keyUp(key)
        time.sleep(duration)
    else:
        print(f"[ERROR] Action inconnue : {action}")

print("✅ Trajet terminé")
