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

"""
draw a list menu with texts and selected as selected
"""

def menu(texts, selected):
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

"""
draw the sub menu to change a displayed variable
"""

def menu_variable(menu, menu_aktual, variable):
    global last_display_info
    if str(menu[menu_aktual["sub_menu_position"]]) + str(variable) != last_display_info:
        oled.cls()
        draw.text((20, 10), menu[menu_aktual["sub_menu_position"]], fill=1)
        draw.text((45, 35), str(variable), fill=1)
        oled.display()
        last_display_info = str(menu[menu_aktual["sub_menu_position"]]) + str(variable)

def menu_rebooting():
    oled.cls()
    draw.text((30, 30), "rebooting...", fill=1)
    oled.display()

"""
draw a reboot menu with selection option
"""

def menu_reboot(selected):
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

"""
draw an icon on the display
"""

def icon(icon):
    global last_display_info
    if icon != last_display_info:
        oled.cls()
        picture = Image.open("pictures/"+icon)
        draw.bitmap((32, 0), picture, fill=1)
        oled.display()
        last_display_info = icon

def logo(icon):
    global last_display_info
    if icon != last_display_info:
        oled.cls()
        picture = Image.open("pictures/"+icon)
        picture = picture.rotate(180)
        draw.bitmap((0, 0), picture, fill=1)
        oled.display()
        last_display_info = icon
