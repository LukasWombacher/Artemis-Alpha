import RPi.GPIO as GPIO
from sub_display import ssd1306
from smbus import SMBus
GPIO.setmode(GPIO.BCM)
from PIL import Image

#setup display
i2cbus = SMBus(1)
oled = ssd1306(i2cbus)
draw = oled.canvas
oled.cls()
oled.display()
last_display_info = ""

def display_draw_menu_reboot(selected):
    global last_display_info
    if "you want to reboot?" + str(selected) != last_display_info:
        oled.cls()
        draw.text((10, 10), "you want to reboot?", fill=1)
        draw.rectangle((25, 35, 45, 45), outline=1, fill=not(selected))
        draw.text((30, 35), "no", fill=selected)
        draw.rectangle((68, 35, 88, 45), outline=1, fill=selected)
        draw.text((70, 35), "yes", fill=not(selected))
        oled.display()
        last_display_info = "you want to reboot?" + str(selected)

def display_draw_menu_variable(menu_settings, menu_aktual, variable):
    global last_display_info
    if str(menu_settings[menu_aktual[2]]) + str(variable) != last_display_info:
        oled.cls()
        draw.text((20, 10), menu_settings[menu_aktual[2]], fill=1)
        draw.text((45, 35), str(variable), fill=1)
        oled.display()
        last_display_info = str(menu_settings[menu_aktual[2]]) + str(variable)

def display_draw_menu(texts, selected):
    global last_display_info
    if str(selected) + str(texts) != last_display_info:
        oled.cls()
        for i in range(0, len(texts)):
            if selected != i:
                draw.text((0, i * 11), texts[i], fill=1)
            else:
                draw.rectangle((0, i * 11, 128, (i+1) * 11), outline=1, fill=1)
                draw.text((0, i * 11), texts[i], fill=0)
        oled.display()
        last_display_info = str(selected) + str(texts)

def display_draw_icon(icon):
    global last_display_info
    if icon != last_display_info:
        oled.cls()
        draw.bitmap((32, 0), Image.open("pictures/"+icon), fill=1)
        oled.display()
        last_display_info = icon