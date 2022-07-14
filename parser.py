import requests
import json
import xmltodict
import threading
from mcstatus import JavaServer
from time import sleep

maxthreads = 25
filename = "minecraftservers.xml" #xml export from masscan
webhookurl = "discordwebhookhere"

threads = []

def make_json(file):
    with open(file, "r") as fd:
        doc = xmltodict.parse(fd.read())
        jds = json.loads(json.dumps(doc, indent=2))
        return jds

def try_server(serverip):
    try:
        #server = JavaServer.lookup(serverip)
        print(serverip)
        server =  JavaServer(serverip, 25565)
        status = server.status()
        plrsonline = status.players.online
        pingvar = status.latency
    except Exception as exce:
        print(exce)
    else:
        print(serverip, plrsonline, pingvar)
        webhookdata = {
            "embeds": [{
                "title": "New Minecraft Server Found!",
                "color": 16032255,
                "fields": [
                    {
                    "name": "Server IP:",
                    "value": str(serverip)
                    },
                    {
                    "name": "Players online:",
                    "value": str(plrsonline),
                    "inline": "true"
                    },
                    {
                    "name": "Ping:",
                    "value": str(pingvar) + "ms",
                    "inline": "true"
                    }
                ]
            }],
        }
        
        q = requests.post(webhookurl, json=webhookdata)
        print(q)
    return

if __name__ == '__main__':
    j = make_json("internetscan.xml")
    for v in j["nmaprun"]["host"]:
        while len(threads) >= maxthreads:
            sleep(0.4)
            threads = threading.enumerate()
        # print(json.dumps(v, indent=1))
        if v["ports"]["port"]["state"]["@state"] == "open": 
            serverip = v["address"]["@addr"]
            hh = threading.Thread(target=try_server, args=(serverip,))
            threads.append(hh)
            hh.start()
