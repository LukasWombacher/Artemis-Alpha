import json
import os


#load data from json

with open("pin_config.json", "r") as pin_config_file:
    pin_config_data = json.load(pin_config_file)

"""
return the GPIO pin ports for the given device as array
"""

def get_pin_ports(device):
    return pin_config_data[device]["pin_port"]

"""
return the pin names for the given device as array
"""

def get_pin_name(device):
    return pin_config_data[device]["pin_name"]

"""
return the pin status[IN or OUT] for the given device as array
"""

def get_pin_status(device):
    return pin_config_data[device]["status"]

"""
return the value of the given variable from settings.json
"""

def get_variable(variable):
    with open("settings.json", "r") as settings_file:
        settings_data = json.load(settings_file)
        return settings_data[variable]

"""
change the given variable to the new value in the settings.json file
"""

def set_variable(variable, new_value):
    with open("settings.json", "r") as settings_file:
        settings_data = json.load(settings_file)
        settings_data[variable] = new_value
    os.remove("settings.json")
    with open("settings.json", "w") as new_settings_file:
        json.dump(settings_data, new_settings_file, indent=4)
