import os
import sys
from win11toast import toast
from serial.tools.list_ports_common import ListPortInfo

ICON = 'sign_16265537.png'


def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)


def add_app_to_autostart():
    this_file = sys.argv[0]
    this_file_name = os.path.basename(this_file)
    user_path = os.path.expanduser('~')

    if not os.path.exists(
            f"{user_path}\\AppData\\Roaming\\Microsoft\\Windows\\Start Menu\\Programs\\Startup\\{this_file_name}"):
        os.system(
            f'copy "{this_file}" "{user_path}\\AppData\\Roaming\\Microsoft\\Windows\\Start Menu\\Programs\\Startup"')


def notify(port: ListPortInfo, add_or_del: bool):
    cmd = "Connected" if add_or_del else "Disconnected"
    toast(cmd, f'{port.name}\n{port.description[:-7]}',
          button={'activationType': 'protocol', 'arguments': 'http:Dismiss', 'content': 'Close'},
          duration='long',
          icon={'src': resource_path(ICON),
                'placement': 'appLogoOverride'}
          )


def device_manager():
    os.system('devmgmt.msc')
