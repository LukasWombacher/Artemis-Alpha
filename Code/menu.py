import time
import RPi.GPIO as GPIO
import os
import display
import eroeffnungsrennen
import hindernisrennen
import test
import edit_json
import ultrasonic

GPIO.setmode(GPIO.BCM)

#setup rotary encoder

pins_rotary_encoder = edit_json.get_pin_ports("rotary_encoder")
sw_Pin = pins_rotary_encoder[0]
dt_Pin = pins_rotary_encoder[1]
clk_Pin = pins_rotary_encoder[2]
GPIO.setup(dt_Pin, GPIO.IN)
GPIO.setup(clk_Pin, GPIO.IN)
GPIO.setup(sw_Pin, GPIO.IN)
last_status = (GPIO.input(dt_Pin) << 2) | (GPIO.input(clk_Pin) << 1) | GPIO.input(sw_Pin)
encoder_val = 0
encoder_pressed = False

#setup menu

menu_main = ["programs", "settings", "informations", "reboot"]
menu_icon = ["icon_programs.png", "icon_settings.png", "icon_informations.png", "icon_reboot.png"]
menu_programs = ["<--      back", "Eröffnungsrennen", "Hindernisrennen", "Test"]
menu_settings = ["<--      back", "led brightness", "led speed", "led effekte", "led matrix", "engine speed", "sound", "temperature", "data view"]
menu_informations = ["<--      back", "ultrasonic_front", "ultrasonic_left", "ultrasonic_right"]
menu_aktual = {"menu_position": 0, "menu_selected": False, "sub_menu_position": 0, "sub_menu_display_position": 0, "sub_menu_selected": False}

"""
The menu connects the other program parts and subprograms.
It is graphically represented and operated with the rotary encoder.
It is used to start programs, configure settings, read sensor data, log files and control system processes.
"""

def main_menu():
    global encoder_val, encoder_pressed, led_brightness, led_speed, led_effekte, led_matrix, engine_speed, sound, data_view
    rotary_Change(0.2)
    menu_aktual["menu_position"] = encoder_val % len(menu_main)
    display.icon(menu_icon[menu_aktual["menu_position"]])
    if encoder_pressed:
        menu_aktual["menu_selected"] = True
        if menu_aktual["menu_position"] == 0: #programs
            encoder_val = 0
            time.sleep(0.2)
            while(menu_aktual["menu_selected"]):
                rotary_Change(0.1)
                menu_aktual["sub_menu_position"] = encoder_val % len(menu_programs)
                menu_scrolling(menu_programs)
                display.menu(menu_programs[menu_aktual["sub_menu_display_position"]:menu_aktual["sub_menu_display_position"]+6], menu_aktual["sub_menu_position"]-menu_aktual["sub_menu_display_position"])
                if encoder_pressed:
                    if menu_aktual["sub_menu_position"] == 0:
                        menu_aktual["menu_selected"] = False
                    elif menu_aktual["sub_menu_position"] == 1:
                        eroeffnungsrennen.main()
                        menu_aktual["sub_menu_position"] = 0
                        menu_aktual["menu_selected"] = False
                    elif menu_aktual["sub_menu_position"] == 2:
                        hindernisrennen.main()
                        menu_aktual["sub_menu_position"] = 0
                        menu_aktual["menu_selected"] = False
                    elif menu_aktual["sub_menu_position"] == 3:
                        test.main()
                        menu_aktual["sub_menu_position"] = 0
                        menu_aktual["menu_selected"] = False
            menu_aktual["sub_menu_position"] = 0
            encoder_val = menu_aktual["menu_position"]
            time.sleep(0.2)
            pass
        elif menu_aktual["menu_position"] == 1: #settings
            encoder_val = 0
            time.sleep(0.2)
            while(menu_aktual["menu_selected"]):
                rotary_Change(0.1)
                menu_aktual["sub_menu_position"] = encoder_val % len(menu_settings)
                menu_scrolling(menu_settings)
                display.menu(menu_settings[menu_aktual["sub_menu_display_position"]:menu_aktual["sub_menu_display_position"]+6], menu_aktual["sub_menu_position"]-menu_aktual["sub_menu_display_position"])
                if encoder_pressed:
                    if menu_aktual["sub_menu_position"] == 0:
                        menu_aktual["menu_selected"] = False
                    elif menu_aktual["sub_menu_position"] == 1:
                        edit_json.set_variable("led_brightness",  change_variable_percent(edit_json.get_variable("led_brightness")))
                    elif menu_aktual["sub_menu_position"] == 2:
                        edit_json.set_variable("led_speed",  change_variable_percent(edit_json.get_variable("led_speed")))
                    elif menu_aktual["sub_menu_position"] == 3:
                        edit_json.set_variable("led_effekte",  change_variable_bool(edit_json.get_variable("led_effekte")))
                    elif menu_aktual["sub_menu_position"] == 4:
                        edit_json.set_variable("led_matrix",  change_variable_bool(edit_json.get_variable("led_matrix")))
                    elif menu_aktual["sub_menu_position"] == 5:
                        edit_json.set_variable("engine_speed",  change_variable_percent(edit_json.get_variable("engine_speed")))
                    elif menu_aktual["sub_menu_position"] == 6:
                        edit_json.set_variable("sound",  change_variable_percent(edit_json.get_variable("sound")))
                    elif menu_aktual["sub_menu_position"] == 7:
                        edit_json.set_variable("temperature",  change_variable_percent(edit_json.get_variable("temperature")))
                    elif menu_aktual["sub_menu_position"] == 8:
                        edit_json.set_variable("data_view",  change_variable_bool(edit_json.get_variable("data_view")))
            menu_aktual["sub_menu_position"] = 0
            encoder_val = menu_aktual["menu_position"]
            time.sleep(0.2)
        elif menu_aktual["menu_position"] == 2: #informations
            encoder_val = 0
            time.sleep(0.2)
            while(menu_aktual["menu_selected"]):
                rotary_Change(0.1)
                menu_aktual["sub_menu_position"] = encoder_val % len(menu_informations)
                menu_scrolling(menu_informations)
                display.menu(menu_informations[menu_aktual["sub_menu_display_position"]:menu_aktual["sub_menu_display_position"]+6], menu_aktual["sub_menu_position"]-menu_aktual["sub_menu_display_position"])
                if encoder_pressed:
                    if menu_aktual["sub_menu_position"] == 0:
                        menu_aktual["menu_selected"] = False
                    else:
                        encoder_pressed = False
                        menu_aktual["sub_menu_selected"] = True
                        time.sleep(0.2)
                        while(menu_aktual["sub_menu_selected"]):
                            rotary_Change(0.2)
                            display.menu_variable(menu_informations, menu_aktual, str(ultrasonic.get_distance(menu_informations[menu_aktual["sub_menu_position"]])) + " cm")
                            time.sleep(0.4)
                            if encoder_pressed:
                                menu_aktual["sub_menu_selected"] = False
                                encoder_pressed = False
                                encoder_val = menu_aktual["sub_menu_position"]
            menu_aktual["sub_menu_position"] = 0
            encoder_val = menu_aktual["menu_position"]
            time.sleep(0.2)
        elif menu_aktual["menu_position"] == 3: #reboot
            encoder_val = 0
            time.sleep(0.2)
            while(menu_aktual["menu_selected"]):
                rotary_Change(0.1)
                if encoder_val >= 1:
                    encoder_val = 1
                elif encoder_val <= 0:
                    encoder_val = 0
                display.menu_reboot(encoder_val)
                if encoder_pressed:
                    if encoder_val == 0:
                        encoder_pressed = False
                        menu_aktual["menu_selected"] = False
                        encoder_val = menu_aktual["menu_position"]
                    elif encoder_val == 1:
                        display.menu_rebooting()
                        GPIO.cleanup()
                        os.system("sudo reboot")

"""
change a bool type variable menu
"""

def change_variable_bool(variable):
    global encoder_pressed, encoder_val
    menu_aktual["sub_menu_selected"] = True
    encoder_val = 0
    time.sleep(0.2)
    while(menu_aktual["sub_menu_selected"]):
        rotary_Change(0.1)
        variable += encoder_val
        if variable >= 1:
            variable = True
            variable_show = "on"
        elif variable <= 0:
            variable = False
            variable_show = "off"
        encoder_val = False 
        display.menu_variable(menu_settings, menu_aktual, variable_show)
        if encoder_pressed:
            menu_aktual["sub_menu_selected"] = False
            encoder_pressed = False
            encoder_val = menu_aktual["sub_menu_position"]
            return variable

"""
change a int type variable in percent
"""

def change_variable_percent(variable):
    global encoder_pressed, encoder_val
    menu_aktual["sub_menu_selected"] = True
    encoder_val = 0
    time.sleep(0.2)
    while(menu_aktual["sub_menu_selected"]):
        rotary_Change(0.1)
        variable += encoder_val * 10
        if variable > 100:
            variable = 100
        elif variable < 0:
            variable = 0
        encoder_val = 0 
        display.menu_variable(menu_settings, menu_aktual, str(variable) + "%")
        if encoder_pressed:
            menu_aktual["sub_menu_selected"] = False
            encoder_pressed = False
            encoder_val = menu_aktual["sub_menu_position"]
            return variable

"""
calculate the shown part of sub menus and the selected position
"""

def menu_scrolling(menu_selected):
    global menu_aktual
    if len(menu_selected) >= 6:
        if menu_aktual["sub_menu_position"] == 0:
            menu_aktual["sub_menu_display_position"] = 0
        elif menu_aktual["sub_menu_position"] == len(menu_selected)-1:
            menu_aktual["sub_menu_display_position"] = len(menu_selected) - 6
        elif menu_aktual["sub_menu_position"] > menu_aktual["sub_menu_display_position"] + 5:
            menu_aktual["sub_menu_display_position"] += 1
        elif menu_aktual["sub_menu_position"] < menu_aktual["sub_menu_display_position"]:
            menu_aktual["sub_menu_display_position"] -= 1

"""
detect status changes of the rotary encoder
"""

def rotary_Change(wait_time):
    global last_status, encoder_val, encoder_pressed
    new_status = (GPIO.input(dt_Pin) << 2) | (GPIO.input(clk_Pin) << 1) | GPIO.input(sw_Pin)
    if new_status == last_status:
        return
    if new_status == 5:
        encoder_val += 1
    elif new_status == 3:
        encoder_val -= 1
    elif new_status == 6:
        encoder_pressed = True
    else:
        encoder_pressed = False
    last_status = new_status
    time.sleep(wait_time)

#while True:
#    print((GPIO.input(dt_Pin) << 2) | (GPIO.input(clk_Pin) << 1) | GPIO.input(sw_Pin))
