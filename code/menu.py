import time
import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)
import os
import display
import eroeffnungsrennen
import hindernisrennen
import test

#setup rotary encoder
sw_Pin = 5
dt_Pin = 6
clk_Pin = 12
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
menu_settings = ["<--      back", "led brightness", "led speed", "led effekte", "led matrix", "engine speed", "sound", "data view"]
menu_informations = ["<--      back", "rotary encoder", "ultrasonic sensor"]
menu_aktual = [0, False, 0, 0, False]

#setup settings
led_brightness = 100
led_speed = 100
led_effekte = False
led_matrix = True
engine_speed = 100
sound = 100
data_view = True

def main_menu():
    global encoder_val, encoder_pressed, led_brightness, led_speed, led_effekte, led_matrix, engine_speed, sound, data_view
    rotary_Change(0.2)
    menu_aktual[0] = encoder_val % len(menu_main)
    display.display_draw_icon(menu_icon[menu_aktual[0]])
    if encoder_pressed:
        menu_aktual[1] = True
        if menu_aktual[0] == 0: #programs
            encoder_val = 0
            time.sleep(0.5)
            while(menu_aktual[1]):
                rotary_Change(0.1)
                menu_aktual[2] = encoder_val % len(menu_programs)
                menu_scrolling(menu_programs)
                display.display_draw_menu(menu_programs[menu_aktual[3]:menu_aktual[3]+6], menu_aktual[2]-menu_aktual[3])
                if encoder_pressed:
                    if menu_aktual[2] == 0:
                        menu_aktual[1] = False
                    elif menu_aktual[2] == 1:
                        eroeffnungsrennen
                    elif menu_aktual[2] == 2:
                        hindernisrennen
                    elif menu_aktual[2] == 3:
                        test
            menu_aktual[2] = 0
            encoder_val = menu_aktual[0]
            time.sleep(0.5)
            pass
        elif menu_aktual[0] == 1: #settings
            encoder_val = 0
            time.sleep(0.5)
            while(menu_aktual[1]):
                rotary_Change(0.1)
                menu_aktual[2] = encoder_val % len(menu_settings)
                menu_scrolling(menu_settings)
                display.display_draw_menu(menu_settings[menu_aktual[3]:menu_aktual[3]+6], menu_aktual[2]-menu_aktual[3])
                if encoder_pressed:
                    if menu_aktual[2] == 0:
                        menu_aktual[1] = False
                    elif menu_aktual[2] == 1:
                        led_brightness = change_variable_percent(led_brightness)
                    elif menu_aktual[2] == 2:
                        led_speed = change_variable_percent(led_speed)
                    elif menu_aktual[2] == 3:
                        led_effekte = change_variable_bool(led_effekte)
                    elif menu_aktual[2] == 4:
                        led_matrix = change_variable_bool(led_matrix)
                    elif menu_aktual[2] == 5:
                        engine_speed = change_variable_percent(engine_speed)
                    elif menu_aktual[2] == 6:
                        sound = change_variable_percent(sound)
                    elif menu_aktual[2] == 7:
                        data_view = change_variable_bool(data_view)
            menu_aktual[2] = 0
            encoder_val = menu_aktual[0]
            time.sleep(0.5)
            pass
        elif menu_aktual[0] == 2: #informations
            encoder_val = 0
            time.sleep(0.5)
            while(menu_aktual[1]):
                rotary_Change(0.1)
                menu_aktual[2] = encoder_val % len(menu_informations)
                menu_scrolling(menu_informations)
                display.display_draw_menu(menu_informations[menu_aktual[3]:menu_aktual[3]+6], menu_aktual[2]-menu_aktual[3])
                if encoder_pressed:
                    if menu_aktual[2] == 0:
                        menu_aktual[1] = False
            menu_aktual[2] = 0
            encoder_val = menu_aktual[0]
            time.sleep(0.5)
            pass
        elif menu_aktual[0] == 3: #reboot
            encoder_val = 0
            time.sleep(0.5)
            while(menu_aktual[1]):
                rotary_Change(0.1)
                if encoder_val >= 1:
                    encoder_val = 1
                elif encoder_val <= 0:
                    encoder_val = 0
                display.display_draw_menu_reboot(encoder_val)
                if encoder_pressed:
                    if encoder_val == 0:
                        encoder_pressed = False
                        menu_aktual[1] = False
                        encoder_val = menu_aktual[0]
                    elif encoder_val == 1:
                        os.system("sudo reboot")
                    time.sleep(0.5)
            pass

def change_variable_bool(variable):
    global encoder_pressed, encoder_val
    menu_aktual[4] = True
    encoder_val = 0
    time.sleep(0.5)
    while(menu_aktual[4]):
        rotary_Change(0.1)
        variable += encoder_val
        if variable >= 1:
            variable = True
            variable_show = "on"
        elif variable <= 0:
            variable = False
            variable_show = "off"
        encoder_val = False 
        display.display_draw_menu_variable(menu_settings, menu_aktual, variable_show)
        if encoder_pressed:
            menu_aktual[4] = False
            encoder_pressed = False
            encoder_val = menu_aktual[2]
            time.sleep(0.5)
            return variable

def change_variable_percent(variable):
    global encoder_pressed, encoder_val
    menu_aktual[4] = True
    encoder_val = 0
    time.sleep(0.5)
    while(menu_aktual[4]):
        rotary_Change(0.1)
        variable += encoder_val * 10
        if variable > 100:
            variable = 100
        elif variable < 0:
            variable = 0
        encoder_val = 0 
        display.display_draw_menu_variable(menu_settings, menu_aktual, str(variable) + "%")
        if encoder_pressed:
            menu_aktual[4] = False
            encoder_pressed = False
            encoder_val = menu_aktual[2]
            time.sleep(0.5)
            return variable

def menu_scrolling(menu_selected):
    global menu_aktual
    if len(menu_selected) >= 6:
        if menu_aktual[2] == 0:
            menu_aktual[3] = 0
        elif menu_aktual[2] == len(menu_selected)-1:
            menu_aktual[3] = len(menu_selected) - 6
        elif menu_aktual[2] > menu_aktual[3] + 5:
            menu_aktual[3] += 1
        elif menu_aktual[2] < menu_aktual[3]:
            menu_aktual[3] -= 1

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
