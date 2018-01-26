# -*- coding: utf-8 -*-
__author__ = 'xtwxfxk'

import os
import json
import time
import thread
import threading
import queue
import websocket
import traceback
import logging
import csv

logger = logging.getLogger('verbose')


# X = ['btc', 'ltc', 'eth', 'etc', 'bch', ]
# Y = ['this_week', 'next_week', 'quarter', ]
# Z = ['1min', '3min', '5min', '15min', '30min', '1hour', '2hour', '4hour', '6hour', '12hour', 'day', '3day', 'week', ]

class Http(object):

    def __init__(self):

        pass

class OkWebSocket(threading.Thread):
    contract_url = 'wss://real.okex.com:10440/websocket/okexapi' # 'wss://47.90.110.144:10440/websocket/okexapi'
    spot_url = 'wss://okexcomreal.bafang.com:10441/websocket' # 'wss://real.okex.com:10441/websocket' # 'wss://real.okcoin.cn:10441/websocket'

    def __init__(self, keep_data_root=None, channels=None):
        super(OkWebSocket, self).__init__()
        self._stop_event = threading.Event()

        self.queue = queue.Queue(maxsize=10)

        self.keep_data_root = keep_data_root

        self.channels = channels if channels is not None else []

    def stop(self):
        self._stop_event.set()

    def stopped(self):
        return self._stop_event.is_set()

    def on_message(self, ws, message):
        try:
            m = json.loads(message)
            if 'event' in m and m['event'] == 'pong':
                # logger.info('pong')
                return

            # logger.info('%s' % (m))
            if self.keep_data_root is not None and m[0]['channel'] not in [u'addChannel']:
                for data in m[0]['data']:
                    file_path = os.path.join(self.keep_data_root, m[0]['channel'])
                    with open(file_path, 'a+') as f:
                        _d = json.dumps(data)[1:-1]
                        f.write('%s\n' % _d)
                        logger.info('write data: %s' % _d)

        except Exception as e:
            logger.error(e)
            logger.error(traceback.format_exc())
            logger.error('Error Message: %s' % message)


    def on_error(self, ws, error):
        logger.error(error)

    def on_close(self, ws):
        logger.info('### close ###')
        ws.close()

    def on_open(self, ws):
        def run(*args):
            while not self.stopped():
                try:
                    try:
                        name = self.queue.get(timeout=1)
                        logger.info('Register: %s' % name)
                        msg = "{'event':'addChannel','channel':'%s'}" % name
                        ws.send(msg)
                    except queue.Empty:
                        pass
                    ws.send('{"event":"ping"}')
                    time.sleep(5)
                except websocket.WebSocketConnectionClosedException as e:
                    break

            # ws.close()

        thread.start_new_thread(run, ())

    def connection(self):

        self.put_channel()

        websocket.enableTrace(False)
        ws = websocket.WebSocketApp(self.spot_url,
                                    on_open=self.on_open,
                                    on_message=self.on_message,
                                    on_error=self.on_error,
                                    on_close=self.on_close)

        ws.run_forever()

    def run(self):
        while not self.stopped():
            self.connection()
            logger.info('Wait Reconnection...')
            time.sleep(5)

    def put_channel(self):

        for channel in self.channels:
            self.queue.put(channel)


    def __getattr__(self, name):
        def wrapper(*args, **kwargs):

            self.queue.put(name)

        return wrapper


    def __del__(self):

        self.stop()





