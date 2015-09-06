import argparse
import json
from subprocess import Popen, PIPE, check_output
import re
import pyautogui


CONFIG_FILENAME = "beyond.config.json"
DEFAULT_APPNAME = "DEFAULT"


def get_mappings():
    with open(CONFIG_FILENAME, 'r') as config_file:
        return json.load(config_file)


def get_foreground_app():
    foregroundAppCode = Popen(["lsappinfo", "front"], stdout=PIPE).stdout.read()
    foregroundAppInfo = Popen(["lsappinfo", "info", "-only", "name", foregroundAppCode], stdout=PIPE).stdout.read()
    return foregroundAppInfo[foregroundAppInfo.index('=') + 2:-2]


def do_action(action):
    keys = action.lower().split('-')
    pyautogui.hotkey(*keys)


def on_gesture_made(gesture):
    if "up" in gesture:
        set_volume(get_volume() + 5)
    elif "down" in gesture:
        set_volume(get_volume() - 5)
    
    # First reload the config file
    app_mappings = get_mappings()

    # Then get the foreground application
    foreground_app = get_foreground_app()

    # Finally, do the action
    if foreground_app in app_mappings:
        action_mappings = app_mappings[foreground_app]
    elif DEFAULT_APPNAME in app_mappings:
        action_mappings = app_mappings[DEFAULT_APPNAME]
    else:
        # No action was specified for this app and no defaults were specified, so simply exit
        return

    if gesture in action_mappings:
        do_action(action_mappings[gesture])

def get_volume():
    regex = 'output volume:([0-9]*)'
    a = check_output(["osascript", "-e", "get volume settings"])
    vol = re.search(regex, a).group(1)
    return int(vol) 

def set_volume(volume):
    a = check_output(["osascript", "-e", "set volume output volume %i" % volume])


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("gesture")
    args = parser.parse_args()
    on_gesture_made(args.gesture)
