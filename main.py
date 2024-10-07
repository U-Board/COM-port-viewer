from PIL import Image
from pystray import Icon, MenuItem, Menu
from poller import Poller
from common import *
from serial.tools.list_ports_common import ListPortInfo


class COMViewer:
    def __init__(self):
        self.poller = Poller(poll_ports_period_ms=1000, update_port_list=self.update_ports)
        self.image = Image.open(resource_path(ICON))
        self.tray_app = Icon('COM-viewer', self.image)
        self.update_ports(None)

    def start(self):
        self.poller.start()
        self.tray_app.run()

    def update_ports(self, ports: list[ListPortInfo] | None):
        menu = []
        if ports is not None:
            for i in range(len(ports)):
                menu.append(MenuItem(ports[i].description, None))

        menu.append(MenuItem('Диспетчер устройств', device_manager))
        menu.append(MenuItem('Выход', self.exit_tray))

        self.tray_app.menu = Menu(*menu)
        self.tray_app.update_menu()

    def exit_tray(self):
        self.tray_app.stop()
        self.poller.stop()


def main():
    add_app_to_autostart()

    viewer = COMViewer()
    viewer.start()


if __name__ == "__main__":
    main()
