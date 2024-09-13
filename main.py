import sys
import os
import win32gui
import win32con
import win32console
from PIL import Image
from pathlib import Path
from pystray import Icon, MenuItem, Menu
from win11toast import toast

ports = ['COM1', 'COM2', 'COM3']


def notify(tray_app, item):
    icon = {'src': f'{Path.cwd() / "pic" / "sign_16265537.png"}',
            'placement': 'appLogoOverride'
            }
    toast("Новое устройство", f'{item}',
          button={'activationType': 'protocol', 'arguments': 'http:Dismiss', 'content': 'Закрыть'},
          icon=icon,
          duration='long'
          )


def click(tray_app, item):
    print(tray_app, item)


def exit_tray(tray_app, item):
    tray_app.stop()


def device_manager(tray_app, item):
    os.system('devmgmt.msc')


def main():
    image = Image.open(Path.cwd() / "pic" / "sign_16265537.png")
    tray_app = Icon('COM-viewer', image, menu=Menu(
        *[MenuItem(ports[i], notify) for i in range(len(ports))],
        MenuItem('Диспетчер', device_manager),
        MenuItem('Выход', exit_tray),
    ))

    # tray_app = Icon('COM-viewer', image, menu=Menu(MenuItem('Все порты:', Menu())))
    win32gui.ShowWindow(win32console.GetConsoleWindow(), win32con.SW_HIDE)
    tray_app.run()


if __name__ == "__main__":
    main()
