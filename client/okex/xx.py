
from websocket import create_connection

ws = create_connection("wss://real.okex.com:10440/websocket/okexapi")
print("Sending...")
ws.send("{'event':'addChannel','channel':'ok_sub_futureusd_eth_ticker_this_week'}")
print("Sent")
print("Receiving...")
result =  ws.recv()
print("Received '%s'" % result)
ws.close()