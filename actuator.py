import argparse
import json
from subprocess import Popen, PIPE
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

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("gesture")
    args = parser.parse_args()
    on_gesture_made(args.gesture)
