import os
import win32gui
import win32con
import win32console
from PIL import Image
from pathlib import Path
from pystray import Icon, MenuItem, Menu
from poller import Poller
from serial.tools.list_ports_common import ListPortInfo


def update_ports(ports: list[ListPortInfo]):
    tray_app.menu = Menu(
        *[MenuItem(ports[i].name, None) for i in range(len(ports))],
        MenuItem('Диспетчер', device_manager),
        MenuItem('Выход', exit_tray),
    )
    tray_app.update_menu()


def exit_tray(app):
    app.stop()
    poller.stop()


def device_manager():
    os.system('devmgmt.msc')


poller = Poller(poll_ports_period_ms=1000, update_port_list=update_ports)

image = Image.open(Path.cwd() / "pic" / "sign_16265537.png")
tray_app = Icon('COM-viewer', image, menu=Menu(
        MenuItem('Диспетчер', device_manager),
        MenuItem('Выход', exit_tray),
    ))


def main():
    poller.start()
    win32gui.ShowWindow(win32console.GetConsoleWindow(), win32con.SW_HIDE)
    tray_app.run()


if __name__ == "__main__":
    main()
