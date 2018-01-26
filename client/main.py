# -*- coding: utf-8 -*-
__author__ = 'xtwxfxk'

import time
import logging
import logging.config

from okex import OkWebSocket

logger = logging.config.fileConfig('logging.conf')
logger = logging.getLogger('verbose')


if __name__ == '__main__':

    ok = OkWebSocket(keep_data_root='/home/left5/datas/coin', channels=['ok_sub_spot_eth_usdt_kline_1min'])
    ok.start()

    # ok.ok_sub_futureusd_eth_kline_this_week_15min()
    # ok.ok_sub_spot_eth_usdt_kline_1min()
    # ok.ok_sub_spot_eth_usdt_depth()

    while not ok.stopped():
        try:
            time.sleep(1)
        except KeyboardInterrupt:
            ok.stop()
            break

