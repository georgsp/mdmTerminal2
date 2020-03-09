#!/usr/bin/env python3

import queue
import threading
import time

import logger
from lib.api.api import API
from lib.api.misc import api_commands
from lib.subscriptions_worker import SubscriptionsWorker
from owner import Owner


def make_dict_reply(cmd: str or None) -> dict:
    if cmd:
        return {'result': 'ok', 'id': cmd}
    else:
        return {'method': 'ping', 'params': [str(time.time())], 'id': 'pong'}


class DuplexMode(API):
    UPGRADE_DUPLEX = 'upgrade duplex'

    def __init__(self, cfg, log, owner: Owner):
        super().__init__(cfg, log, owner, name='DuplexMode')
        self._queue = queue.Queue()
        self.own.subscribe(self.UPGRADE_DUPLEX, self._handle_upgrade_duplex, self.UPGRADE_DUPLEX)
        self._notify_worker = SubscriptionsWorker(owner)
        self._has_started = False
        self.duplex = False
        self._notify_duplex = self.own.registration('duplex_mode')
        self._upgrade_duplex_lock = threading.Lock()

    def start(self):
        self._has_started = True
        super().start()

    def join(self, timeout=30):
        self._queue.put_nowait(None)
        self._notify_worker.join()
        super().join(timeout=timeout)

    def off(self):
        if self.duplex:
            self._api_close()

    def _handle_upgrade_duplex(self, _, cmd, lock, conn):
        try:
            # Забираем сокет у сервера
            conn_ = conn.extract()
            if conn_:
                self.own.messenger(self._handle_upgrade_duplex_safe, None, conn_, cmd)
        finally:
            lock()

    def _handle_upgrade_duplex_safe(self, conn, cmd):
        with self._upgrade_duplex_lock:
            conn.settimeout(None)
            self._api_close()
            self._queue.put_nowait((conn, cmd))
            if not self._has_started:
                self.start()

    def _api_close(self):
        self.duplex = False
        self._notify_worker.disconnect()
        self._conn.close()

    @api_commands('subscribe', pure_json=True)
    def _api_subscribe(self, _, data: list):
        return self._notify_worker.subscribe(data)

    @api_commands('unsubscribe', pure_json=True)
    def _api_unsubscribe(self, _, data: list):
        return self._notify_worker.unsubscribe(data)

    def _conn_open(self):
        self.duplex = True
        self._notify_duplex('open')
        self._notify_worker.connect(self._conn)

    def _conn_close(self):
        self._api_close()
        self._notify_duplex('close')

    def do_ws_allow(self, *args, **kwargs):
        return False

    def run(self):
        while self.work:
            conn = self._queue.get()
            if not conn:
                break

            self._conn, cmd = conn

            self._conn_open()
            try:
                self._processing(make_dict_reply(cmd))
            finally:
                self._conn_close()
        self._api_close()

    def _processing(self, cmd: dict):
        info = self._conn.info
        if self._testing(info, cmd):
            self.log('OPEN {}::{}:{}'.format(*info), logger.INFO)
            for line in self._conn.read():
                self.parse(line)
            self.log('CLOSE {}::{}:{}'.format(*info), logger.INFO)

    def _testing(self, info: tuple, cmd: dict) -> bool:
        try:
            self._conn.write(cmd)
        except RuntimeError as e:
            self.log('OPEN ERROR {}::{}:{}: {}'.format(*info, e), logger.ERROR)
            return False
        return True
