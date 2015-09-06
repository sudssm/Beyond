# Beyond

## Inspiration
TV remotes are ubiquitous. Even more than smartphones, they live in all of our homes, but have largely been abandoned due to the advent of Wifi and Bluetooth.

We challenged ourselves to build a hardware hack that anyone would be able use at home using just off-the-shelf parts and without tinkering experience.  Bringing TV remotes into the 21st century fit that goal perfectly.

## What it does
Control anything on your laptop by pointing a TV remote at it!

Our app translates gestures into common actions.  These actions are context-aware and specific to whatever app you're using.  We've added support for many common apps, but extending this to your favorite app takes just seconds using our [configuration system](#configuration).

## How we built it
We took advantage of the fact that laptop webcams can detect infrared (IR) light in addition to the visible light spectrum.  We use OpenCV to identify the IR light coming from TV remotes and apply gesture recognition to this data to turn movements into human-understandable gestures.

## Configuration

Configuration is done via a file called `beyond.config.json`.
This file maps gestures to keyboard shortcuts at a per-app level, as shown in the following example:
```json
{
	"DEFAULT" : {
		"down" : "command-q"
	},
	"Firefox" : {
		"left" : "delete"
	}
}
```
The DEFAULT app lists the keyboard shortcuts to be applied when the foreground app is not listed in the config file.

### Shortcuts

Shortcuts are taken from standard characters and the following list:

'\t', '\n', '\r', ' ', '!', '"', '#', '$', '%', '&', "'", '(',
')', '*', '+', ',', '-', '.', '/', '0', '1', '2', '3', '4', '5', '6', '7',
'8', '9', ':', ';', '<', '=', '>', '?', '@', '[', '\\', ']', '^', '_', '`',
'a', 'b', 'c', 'd', 'e','f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o',
'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', '{', '|', '}', '~',
'accept', 'add', 'alt', 'altleft', 'altright', 'apps', 'backspace',
'browserback', 'browserfavorites', 'browserforward', 'browserhome',
'browserrefresh', 'browsersearch', 'browserstop', 'capslock', 'clear',
'convert', 'ctrl', 'ctrlleft', 'ctrlright', 'decimal', 'del', 'delete',
'divide', 'down', 'end', 'enter', 'esc', 'escape', 'execute', 'f1', 'f10',
'f11', 'f12', 'f13', 'f14', 'f15', 'f16', 'f17', 'f18', 'f19', 'f2', 'f20',
'f21', 'f22', 'f23', 'f24', 'f3', 'f4', 'f5', 'f6', 'f7', 'f8', 'f9',
'final', 'fn', 'hanguel', 'hangul', 'hanja', 'help', 'home', 'insert', 'junja',
'kana', 'kanji', 'launchapp1', 'launchapp2', 'launchmail',
'launchmediaselect', 'left', 'modechange', 'multiply', 'nexttrack',
'nonconvert', 'num0', 'num1', 'num2', 'num3', 'num4', 'num5', 'num6',
'num7', 'num8', 'num9', 'numlock', 'pagedown', 'pageup', 'pause', 'pgdn',
'pgup', 'playpause', 'prevtrack', 'print', 'printscreen', 'prntscrn',
'prtsc', 'prtscr', 'return', 'right', 'scrolllock', 'select', 'separator',
'shift', 'shiftleft', 'shiftright', 'sleep', 'stop', 'subtract', 'tab',
'up', 'volumedown', 'volumemute', 'volumeup', 'win', 'winleft', 'winright', 'yen',
'command', 'option', 'optionleft', 'optionright'

See our base config file at https://github.com/sudssm/Beyond/blob/master/beyond.config.json
