# -*- coding: utf-8 -*-
__author__ = 'xtwxfxk'

import json
import time
import thread
import threading
import queue
import websocket



X = ['btc', 'ltc', 'eth', 'etc', 'bch', ]
Y = ['this_week', 'next_week', 'quarter', ]
Z = ['1min', '3min', '5min', '15min', '30min', '1hour', '2hour', '4hour', '6hour', '12hour', 'day', '3day', 'week', ]

class Http(object):

    def __init__(self):

        pass

class OkWebSocket(object):
    contract_url = 'wss://real.okex.com:10440/websocket/okexapi' # 'wss://47.90.110.144:10440/websocket/okexapi'
    spot_url = 'wss://okexcomreal.bafang.com:10441/websocket' # 'wss://real.okex.com:10441/websocket' # 'wss://real.okcoin.cn:10441/websocket'

    def __init__(self):
        self.queue = queue.Queue(maxsize=10)


    def __getattr__(self, name):

        def wrapper(*args, **kwargs):
            def on_message(ws, message):
                m = json.loads(message)
                if 'event' in m and m['event'] == 'pong':
                    return

                print '%s - %s' % (name, m[0]['data'])
                # print message

            def on_error(ws, error):
                print('xxx %s' % error)

            def on_close(ws):
                print("### closed ###")

            def on_open(ws):
                ws.send("{'event':'addChannel','channel':'%s'}" % name)

                def run(*args):
                    while 1:
                        # ws.send("{'event':'addChannel','channel':'%s'}" % name)
                        ws.send('{"event":"ping"}')
                        time.sleep(5)

                thread.start_new_thread(run, ())

            websocket.enableTrace(False)
            ws = websocket.WebSocketApp(self.spot_url,
                                        on_open=on_open,
                                        on_message=on_message,
                                        on_error=on_error,
                                        on_close=on_close)

            ws.run_forever()

        return wrapper






if __name__ == "__main__":

    ok = OkWebSocket()

    # ok.ok_sub_futureusd_eth_kline_this_week_15min()
    ok.ok_sub_spot_eth_usdt_kline_15min()
    # ok.ok_sub_spot_eth_usdt_depth()

