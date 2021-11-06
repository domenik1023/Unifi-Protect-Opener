import json
import subprocess
import webbrowser
import getpass
import time
from pynput import keyboard
from pynput.keyboard import Key, Controller
from pathlib import Path

keyboard = Controller()

def Check_file():
    global config
    global username
    global password
    global ip
    global chrome_path
    settings_file = Path("config.json")
    if settings_file.is_file():
        config = json.loads(open('config.json').read())
        username = config['username']
        password = config['password']
        ip = config['ip']
        chrome_path = config['chrome_path']
    else:
        print("First start detected. Please enter credentials")
        username = input("Please enter your Username: ")
        password = getpass.getpass("Please enter your Password: ")
        ip = input("Please enter your IP for Unifi Protect (172.16.0.1): ")
        chrome_path_bool = input("Is your Chrome Path (C:/Program Files/Google/Chrome/Application/chrome.ex)? (Y/n): ")
        if (chrome_path_bool == "Y" or chrome_path_bool == "y"):
            chrome_path = "C:/Program Files/Google/Chrome/Application/chrome.exe"
        else:
            chrome_path_bool = input("Is your Chrome Path (C:/Program Files (x86)/Google/Chrome/Application/chrome.exe)? (Y/n): ")
            if(chrome_path_bool == "Y" or chrome_path_bool == "y"):
                chrome_path = "C:/Program Files (x86)/Google/Chrome/Application/chrome.exe"
            else:
                chrome_path = input("Please Input your correct Chrome Path: ")
                print(f"Your selected Chrome Path is: {chrome_path}")

def export_file():
    export_config = {
        "username": username, 
        "password": password,
        "ip": ip, 
        "chrome_path": chrome_path
    }
    with open("config.json", "w") as new_config:
        json.dump(export_config, new_config, indent=4)

def start_chrome():
    #webbrowser.get(f"{chrome_path} %s").open(f"https://{ip}/protect/liveview/", autoraise=True)
    subprocess.Popen([f"{chrome_path}", f"https://{ip}/protect/liveview/"])
    time.sleep(4)
    keyboard.type('thisisunsafe')
    keyboard.press(Key.ctrl_l)
    keyboard.press('a')
    keyboard.release('a')
    keyboard.release(Key.ctrl_l)
    keyboard.press(Key.delete)
    keyboard.release(Key.delete)
    keyboard.type(f'{username}\t{password}\n')

Check_file()
start_chrome()
export_file()


