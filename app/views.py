import sys
sys.path.append(r"C:\Users\Anikat dogra\Desktop\SolarChain")
from subprocess import call
import datetime
import json
import requests
from flask import render_template, redirect, request,Flask
from app import app
import time
import serial


app = Flask(__name__)

#app = Flask(__name__)
# The node with which our application interacts, there can be multiple
# such nodes as well.
CONNECTED_NODE_ADDRESS = "http://127.0.0.1:8000"

posts = []

def run(runfile):
  with open(runfile,"r") as rnf:
    exec(rnf.read())

def fetch_posts():
    """
    Function to fetch the chain from a blockchain node, parse the
    data and store it locally.
    """
    get_chain_address = "{}/chain".format(CONNECTED_NODE_ADDRESS)
    response = requests.get(get_chain_address)
    if response.status_code == 200:
        content = []
        chain = json.loads(response.content)
        for block in chain["chain"]:
            for tx in block["transactions"]:
                tx["index"] = block["index"]
                tx["hash"] = block["previous_hash"]
                content.append(tx)

        global posts
        posts = sorted(content, key=lambda k: k['timestamp'],
                       reverse=True)

@app.route('/send1')
def send1():
    arduino = serial.Serial('COM5', 90000)

    def onOffFunction():
        command = 'on'
        if command == 'on':
        	print("The LED is on...")
        	time.sleep(1)
        	arduino.write(True)
        	onOffFunction()
        elif command =="off":
        	print("The LED is off...")
        	time.sleep(1)
        	arduino.write(False)
        	onOffFunction()
        elif command =="bye":
        	print("See You!...")
        	time.sleep(1)
        	arduino.close()
        else:
        	print("Sorry..type another thing..!")
        	onOffFunction()

        time.sleep(2) #waiting the initialization...

    onOffFunction()

    return render_template('index.html')

@app.route('/')
def index():
    fetch_posts()
    return render_template('index.html',
                           title = 'Solar Chain',
                           posts=posts,
                           node_address=CONNECTED_NODE_ADDRESS,
                           readable_time=timestamp_to_string)

@app.route('/submit', methods=['POST'])
def submit_textarea():
    """
    Endpoint to create a new transaction via our application.
    """
    post_content = request.form["content"]
    seller = request.form["seller"]
    buyer = request.form["buyer"]
    post_object = {
        'seller': seller,
        'content': post_content,
        'buyer' : buyer,
    }

    # Submit a transaction
    new_tx_address = "{}/new_transaction".format(CONNECTED_NODE_ADDRESS)

    requests.post(new_tx_address,
                  json=post_object,
                  headers={'Content-type': 'application/json'})

    return redirect('/')

@app.route('/send', methods=['POST'])
def send():



    arduino = serial.Serial('COM5', 90000)

    def onOffFunction():
        command = 'on'
        if command == 'on':
            print("The LED is on...")
            time.sleep(1)
            arduino.write(True)
            onOffFunction()
        elif command =="off":
            print("The LED is off...")
            time.sleep(1)
            arduino.write(False)
            onOffFunction()
        elif command =="bye":
            print("See You!...")
            time.sleep(1)
            arduino.close()
        else:
            print("Sorry..type another thing..!")
            onOffFunction()

        time.sleep(2) #waiting the initialization...

    onOffFunction()

    return redirect('/')



def timestamp_to_string(epoch_time):
    return datetime.datetime.fromtimestamp(epoch_time).strftime('%H:%M')

app.run(debug=True, port=4000)
