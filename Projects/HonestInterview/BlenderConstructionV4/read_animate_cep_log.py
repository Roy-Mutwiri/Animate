import json
import urllib.request

import websocket

pages = json.load(urllib.request.urlopen("http://127.0.0.1:8089/json", timeout=3))
ws_url = pages[0]["webSocketDebuggerUrl"]
ws = websocket.create_connection(ws_url, timeout=3)
expr = '(document.getElementById("messageLog") && document.getElementById("messageLog").value) || document.body.innerText'
ws.send(json.dumps({
    "id": 1,
    "method": "Runtime.evaluate",
    "params": {
        "expression": expr,
        "returnByValue": True,
    },
}))
print(ws.recv())
ws.close()
