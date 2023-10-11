from flask import Flask, jsonify, render_template
import requests
import base64
from getpass import getpass
import time  # <-- Added for timing

app = Flask(__name__)

BASE_URL = "http://192.168.100.1/api"
HEADERS = {
    'Accept': 'application/json, text/plain, */*',
    'Accept-Language': 'en-US,en;q=0.9',
    'Connection': 'keep-alive',
    'Origin': 'http://192.168.100.1',
    'Referer': 'http://192.168.100.1/',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36',
    'content-type': 'application/json'
}

PASSWORD = getpass("Enter your password: ")
ENCODED_PASSWORD = base64.b64encode(PASSWORD.encode()).decode()

sid = None
DEBUG_MODE = True

def login():
    global sid
    if sid:
        if DEBUG_MODE:
            print("[DEBUG] Using existing SID:", sid)
        return sid
    
    if DEBUG_MODE:
        print("[DEBUG] Logging in to retrieve a new SID...")
    payload = {
        "version": "1.0",
        "sid": "00000000000000000000000000000000",
        "mid": 0,
        "module": "login",
        "api": "login",
        "param": {
            "password": ENCODED_PASSWORD
        }
    }
    response = requests.post(BASE_URL, headers=HEADERS, json=payload)
    data = response.json()
    sid = data.get('result', {}).get('sid')
    return sid

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/data', methods=['GET'])
def get_signal_data():
    start_time = time.time()  # <-- Record start time
    
    sid_value = login()
    if not sid_value:
        return jsonify({"error": "Failed to log in."}), 500

    data = {
        "version": "1.0",
        "sid": sid_value,
        "mid": 0,
        "module": "lte",
        "api": "at_cmd",
        "param": {
            "cmd": 'AT+QENG="servingcell"'
        }
    }

    response = requests.post(BASE_URL, headers=HEADERS, json=data, verify=False)
    response_data = response.json()

    lines = response_data["result"]["result"].split("\r\n")
    lte_data = []
    nr5g_data = []
    
    for line in lines:
        if "\"LTE\"," in line:
            lte_data = line.split(",")
        if "\"NR5G-NSA\"," in line:
            nr5g_data = line.split(",")

    # Calculate and print the elapsed time
    elapsed_time = time.time() - start_time
    if DEBUG_MODE:
        print(f"[DEBUG] Request took {elapsed_time:.4f} seconds")

    return jsonify({
        "LTE": {
            "rsrp": int(lte_data[11]) if lte_data else None,
            "rsrq": int(lte_data[13]) if lte_data else None,
            "sinr": int(lte_data[12]) if lte_data else None
        },
        "5G": {
            "mcc": int(nr5g_data[2]) if nr5g_data else None,
            "mnc": int(nr5g_data[3]) if nr5g_data else None,
            "rsrp": int(nr5g_data[4]) if nr5g_data else None,
            "sinr": int(nr5g_data[5]) if nr5g_data else None,
            "rsrq": int(nr5g_data[6]) if nr5g_data else None,
            "band": int(nr5g_data[8]) if nr5g_data else None
        }
    })

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000, use_reloader=False)
