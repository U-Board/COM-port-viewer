import time
from common import notify
from serial.tools import list_ports
from threading import Thread, Event


def _get_time_ms():
    return int(round(time.time() * 1000))


class Poller(Thread):
    __timestamp = 0

    def __init__(self, poll_ports_period_ms: int, update_port_list: callable = None):
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
                        notify(port.name, True)

                for port in self._list_ports:
                    if port not in ports_now:
                        self._list_ports.remove(port)
                        # notify(port.name, False)
                self._update_list(self._list_ports)
            time.sleep(0.1)
