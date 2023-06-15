import menu
import logging
from datetime import datetime
import drive_motor
import stepper_motor
import time
import edit_json

main_on = True

#config logger

logging.basicConfig(level=logging.INFO, filename="/home/pi/Artemis-Alpha/Code/log/log_" + str(datetime.now().strftime("%Y-%m-%d %H:%M:%S")) + ".log", filemode="w", format="%(asctime)s - %(levelname)s - %(filename)s/%(funcName)s  - %(message)s")
logging.info("main.py started")

"""
main function of the program
"""

def main():
    menu.main_menu()

"""
start main function
"""

while(edit_json.get_variable("on") == True):
    main()
    print("main")

