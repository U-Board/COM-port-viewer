import time
import queue

from serial.tools import list_ports
from threading import Thread, Event
from serial.tools.list_ports_common import ListPortInfo
from PySide6.QtCore import QObject, Signal


def _get_time_ms():
    return int(round(time.time() * 1000))


class Poller(QObject, Thread):
    __timestamp = 0

    sigDeviceConnected = Signal(ListPortInfo)
    sigDeviceDisconnected = Signal(ListPortInfo)

    sigChangeColor = Signal()

    _inbound_queue = queue.Queue(maxsize=100)

    def __init__(self, poll_ports_period_ms: int, update_port_list: callable = None, **kwargs):
        QObject.__init__(self, **kwargs)
        Thread.__init__(self, name=f'{self.__class__.__name__} thread', )

        self.__poll_ports_period_ms = poll_ports_period_ms

        self._list_ports = []

        self._stop_event = Event()
        self._update_list = update_port_list

    def stop(self):
        self._stop_event.set()

    def is_stopped(self):
        return self._stop_event.is_set()

    def run(self) -> None:
        while not self.is_stopped():
            if _get_time_ms() - self.__timestamp >= self.__poll_ports_period_ms:
                self.__timestamp = _get_time_ms()
                ports_now = list_ports.comports()
                for port in ports_now:
                    if port.vid and port.pid and port not in self._list_ports:
                        self._list_ports.append(port)
                        self._update_list(self._list_ports)
                        # print('-------------------')
                        # print(f'Found port:')
                        # print(port)
                        # print('-------------------')

                for port in self._list_ports:
                    if port not in ports_now:
                        self._list_ports.remove(port)
                        self._update_list(self._list_ports)
                        # print('-------------------')
                        # print(f'Lost port:')
                        # print(port)
                        # print('-------------------')
            time.sleep(0.001)
