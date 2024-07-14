#!/usr/bin/env python3

import subprocess
import platform
from flask import Flask, render_template, request

app = Flask(__name__)

def ping(host):
    param = '-n' if platform.system().lower() == 'windows' else '-c'
    command = ['ping', param, '1', host]
    return subprocess.call(command) == 0

def read_hosts_from_file(filename):
    hosts_data = []
    try:
        with open(filename, 'r') as file:
            for line in file:
                try:
                    ip, pc_name, mac_address = line.strip().split(',')
                except:
                    ip, pc_name = line.strip().split(',')
                    mac_address = False
                hosts_data.append({"name": pc_name, "ip": ip, "mac": mac_address})
    except FileNotFoundError:
        print(f"Error: {filename} not found.")
    return hosts_data

@app.route("/")
def home():
    hosts_data = read_hosts_from_file('Setup/hosts.txt')
    online_hosts = []
    offline_hosts = []

    for host in hosts_data:
        if ping(host["ip"]):
            online_hosts.append(host)
        else:
            offline_hosts.append(host)

    return render_template("index.html", online=online_hosts, offline=offline_hosts)

@app.route("/start/<mac_address>")
def start_wake_on_lan(mac_address):
    # Execute the Wake-on-LAN command
    subprocess.run(["wakeonlan", "-i", "192.168.0.255", mac_address])
    return "Magic packet sent!"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=80, debug=False)