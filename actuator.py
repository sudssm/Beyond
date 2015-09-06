import argparse
import json
from subprocess import Popen, PIPE, check_output
import re
import pyautogui
from test import HIDPostAuxKey


# hidsystem/ev_keymap.h
NX_KEYTYPE_SOUND_UP = 0
NX_KEYTYPE_SOUND_DOWN = 1
NX_KEYTYPE_PLAY = 16
NX_KEYTYPE_MUTE = 7

NX_KEYTYPE_FAST = 19
NX_KEYTYPE_REWIND = 20


CONFIG_FILENAME = "beyond.config.json"
DEFAULT_APPNAME = "DEFAULT"


def get_mappings():
    with open(CONFIG_FILENAME, 'r') as config_file:
        j = json.load(config_file)
        # return dict((k.lower(), v) for k, v in j.iteritems())
        return j 

def get_foreground_app():
    foregroundAppCode = Popen(["lsappinfo", "front"], stdout=PIPE).stdout.read()
    foregroundAppInfo = Popen(["lsappinfo", "info", "-only", "name", foregroundAppCode], stdout=PIPE).stdout.read()
    return foregroundAppInfo[foregroundAppInfo.index('=') + 2:-2]

def handle_media_keys(action): 
    if action=="volumeup":
        HIDPostAuxKey(NX_KEYTYPE_SOUND_UP)
    if action == "volumedown":
        HIDPostAuxKey(NX_KEYTYPE_SOUND_DOWN)
    elif action == "volumemute":
        HIDPostAuxKey(NX_KEYTYPE_MUTE)
    if action == "media_playpause":
        HIDPostAuxKey(NX_KEYTYPE_PLAY)
    if action == "media_nexttrack":
        HIDPostAuxKey(NX_KEYTYPE_FAST)
    if action == "media_prevtrack":
        HIDPostAuxKey(NX_KEYTYPE_REWIND)

# def handle_brightness(action):
    


    


def set_volume(volume):
    a = check_output(["osascript", "-e", "set volume output volume %i" % volume])


def do_action(action):
    print action 
    if "media" in action or "volume" in action: 
        handle_media_keys(action)
    keys = action.lower().split('_')
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
