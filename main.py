from nanoleafapi import Nanoleaf, NanoleafDigitalTwin, RED, ORANGE, YELLOW, GREEN, LIGHT_BLUE, BLUE, PINK, PURPLE, WHITE
from argparse import ArgumentParser
import argparse, os, sys

# Check for environment variable
try:
   os.environ["NANOLEAF_IP"]
except KeyError: 
   print("Please set the environment variable NANOLEAF_IP")
   sys.exit(1)

if len(sys.argv) <= 1:
    sys.argv.append('--help')

nl = Nanoleaf(os.getenv("NANOLEAF_IP"))
digital_twin = NanoleafDigitalTwin(nl)

parser = argparse.ArgumentParser(
                    prog='nanoleafcli',
                    description='Control your nanoleaves with a simple CLI tool',
                    epilog='Use -h or --help for more options',
                    add_help='True',
                    exit_on_error='True')

subparsers = parser.add_subparsers(dest='command', help='Subcommand to run')

# Register all the subcommand parsers
power_parser = subparsers.add_parser('power', help='Change power state of leaves')
power_subparsers = power_parser.add_subparsers(dest='action', help='Action to take')

# Brightness parser
brightness_parser = subparsers.add_parser('brightness', help='Change brightness of leaves')
brightness_subparsers = brightness_parser.add_subparsers(dest='action', help='Action to take')

# Identify parser
identify_parser = subparsers.add_parser('identify', help='Identify a panel by providing a panel ID')
identify_subparsers = identify_parser.add_subparsers(dest='action')

# Effects parser
effects_parser = subparsers.add_parser('effects', help='View and modify information about the onboard effects of the device')
effects_subparsers = effects_parser.add_subparsers(dest='action', help='View and modify information about the onboard effects of the device')

# Color parser
colors_parser = subparsers.add_parser('color', help='View and modify information about the colors of the device')
colors_subparsers = colors_parser.add_subparsers(dest='action', help='View and modify information about the colors of the device')

# Effects options
list_parser = effects_subparsers.add_parser('list', help='List effects on the device')
current_parser = effects_subparsers.add_parser('current', help='Get current effect of device')
effect_set_parser = effects_subparsers.add_parser('set', help='List effects on the device')
effect_set_parser.add_argument('effect', help='Set device effect (use '' for effects with spaces)')

# Identify options
identify_parser = identify_subparsers.add_parser('list', help='List panel IDs')
identify_parser.add_argument('--id', help='panel ID to identify', type=int, required=False)

# Brightness options
brightness_parser = brightness_subparsers.add_parser('get', help='Get device brightness')
brightness_parser = brightness_subparsers.add_parser('set', help='Set device brightness')

# Power options
on = power_subparsers.add_parser('on', help='Turn leaves on')
off = power_subparsers.add_parser('off', help='Turn leaves off')
toggle = power_subparsers.add_parser('toggle', help='Toggle leaves power state')

args = parser.parse_args()

def power():
    if args.action == 'toggle':
        nl.toggle_power()
    elif args.action == 'on':
        nl.power_on()
    elif args.action == 'off':
        nl.power_off()
    else:
        power_parser.print_help()

def effects():
    if args.action == 'list':
        print(nl.list_effects())
    elif args.action == 'set':
        nl.set_effect(sys.argv[3])
    elif args.action == 'current':
        print("Current effect set to " + nl.get_current_effect())
    else: effects_parser.print_help()

def color(id, color):
    if args.action == 'get':
        digital_twin.get_color(id)
    elif args.action == 'set':
        digital_twin.set_color(id, color)

def identify():
    print(digital_twin.get_ids())
    digital_twin.set_all_colors((255, 255, 255))
    digital_twin.sync()
    nl.set_brightness(100)

def brightness(brightness, duration):
    if args.action == 'get':
        nl.get_brightness()
    elif args.action == 'set':
        nl.set_brightness(brightness, duration)

# Map subcommands to functions
if args.command == 'power':
    power()
elif args.command == 'effects':
    effects()
elif args.command == 'color':
    color()
elif args.command == 'identify':
    identify()
elif args.command == 'brightness':
    brightness(brightness, duration)
