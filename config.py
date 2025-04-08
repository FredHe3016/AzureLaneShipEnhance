import sys
import os

if hasattr(sys, "_MEIPASS"): 
    BASE_DIR = sys._MEIPASS
else: 
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))

SHIP_DATA_PATH = os.path.join(BASE_DIR, "data", "ship_data.xlsx")
EQUIP_DATA_PATH = os.path.join(BASE_DIR, "data", "equip_data.xlsx")
REQUISITION_PATH = os.path.join(BASE_DIR, "data", "requisition_ships.json")

ICO_PATH = os.path.join(BASE_DIR, "assets", "Akashi.ico")
