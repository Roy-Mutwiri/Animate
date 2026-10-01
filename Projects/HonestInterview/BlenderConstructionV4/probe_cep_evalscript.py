import json
import time
import urllib.request

import websocket

pages = json.load(urllib.request.urlopen("http://127.0.0.1:8089/json", timeout=3))
ws = websocket.create_connection(pages[0]["webSocketDebuggerUrl"], timeout=3)


def send(method, params=None):
    send.counter += 1
    ws.send(json.dumps({"id": send.counter, "method": method, "params": params or {}}))
    while True:
        msg = json.loads(ws.recv())
        if msg.get("id") == send.counter:
            return msg


send.counter = 0

expr = """
window.__codexEvalResult = "pending";
try {
  var csi = new CSInterface();
  csi.evalScript("1+1", function(result) {
    window.__codexEvalResult = String(result);
  });
  "sent";
} catch (e) {
  window.__codexEvalResult = "error:" + e.message;
  window.__codexEvalResult;
}
"""
print(send("Runtime.evaluate", {"expression": expr, "returnByValue": True}))
for _ in range(10):
    time.sleep(0.5)
    out = send("Runtime.evaluate", {"expression": "window.__codexEvalResult", "returnByValue": True})
    print(out)
    value = out.get("result", {}).get("result", {}).get("value")
    if value and value != "pending":
        break
ws.close()
