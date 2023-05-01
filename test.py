import json
import random
import time
import datetime

from websocket import create_connection
ws = create_connection("ws://localhost:8000/course/ws/123456789")
print("Sending 'Hello, World'...")
ws.send("Hello, World")
print("Sent")
print("Receiving...")

hour_value = 2000
count = 0
while True:
    ws.send('?')
    data = ws.recv()
    data = json.loads(data)
    # print(data, type(data))
    time.sleep(1)
    if hour_value / data['data'] > 1.01 or data['data'] / hour_value > 1.01:
        now = datetime.datetime.now()
        print("Current date and time : ", end='')
        print(data, now.strftime("%Y-%m-%d %H:%M:%S"))
    if count > 60:
        count = 0
        hour_value = data['data']
    count += 1

