import win32gui
import win32con
import win32console
from PIL import Image
from pathlib import Path
from pystray import Icon, MenuItem, Menu

ports = ['COM1', 'COM2', 'COM3']

def click(trayApp, item):
    print(trayApp, item)


def main():
    image = Image.open(Path.cwd() / "pic" / "sign_16265537.png")
    tray_app = Icon('COM-viewer', image, menu=Menu(
        MenuItem('Все порты:', Menu(*[MenuItem(ports[i], click) for i in range(len(ports))])),
        MenuItem('Диспетчер', click),
        MenuItem('Выход', click),
    ))

    # tray_app = Icon('COM-viewer', image, menu=Menu(MenuItem('Все порты:', Menu())))
    win32gui.ShowWindow(win32console.GetConsoleWindow(), win32con.SW_HIDE)
    tray_app.run()


if __name__ == "__main__":
    main()
