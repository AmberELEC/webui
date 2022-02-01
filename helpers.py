import os
import datetime
import http.client
import subprocess
import platform

from html import unescape
from config import *

try:
    from ftfy import fix_text
except ModuleNotFoundError:
    def fix_text(text):
        return text

from data import *

def list_folders(path):
    dirs = []
    for entry in os.scandir(path):
        if not entry.name.startswith('.') and entry.is_dir():
            dirs.append(entry.name)
    return dirs

def list_files(path):
    files = []
    if folder_exists(path):
        for entry in os.scandir(path):
            if not entry.name.startswith('.') and entry.is_file():
                files.append(entry.name)
    return files

def file_exists(path, file):
    return os.path.isfile(os.path.join(path, file))

def folder_exists(path):
    return os.path.isdir(path)

def remove_prefix(text, prefix):
    if text.startswith(prefix):
        return text[len(prefix):]
    return text

def find_normalized(node, look):
    if node.find(look) != None and node.find(look).text != None:
        return fix_text(unescape(node.find(look).text))
    else:
        return False

def find_float(node, look):
    if node.find(look) != None and node.find(look).text != None:
        return float(node.find(look).text)
    else:
        return False

def find_int(node, look):
    if node.find(look) != None and node.find(look).text != None:
        return int(node.find(look).text)
    else:
        return False

def find_image_path(node, look):
    if node.find(look) != None and node.find(look).text != None:
        return remove_prefix(node.find(look).text, "./images/")
    else:
        return False

def find_video_path(node, look):
    if node.find(look) != None and node.find(look).text != None:
        return remove_prefix(node.find(look).text, "./videos/")
    else:
        return False

def find_normalized_path(node, look):
    return remove_prefix(find_normalized(node, look), "./")

def find_date(node, look):
    if find_normalized(node, look):
        return format_xml_date(find_normalized(node, look))
    else:
        return False

def format_xml_date(date):
    return datetime.datetime.strptime(date, '%Y%m%dT%H%M%S').strftime('%d %B %Y')

def find_saves(system, rom):
    saves = []
    rom_name = os.path.splitext(rom)[0]
    path = os.path.join(roms_folder, 'savestates', system)

    if not os.path.isdir(path):
        return saves

    for file in os.listdir(path):
        if file.startswith(rom_name) and not file.endswith('.png'):
            saves.append(file)

    return saves

def find_screenshots(rom):
    screenshots = []
    rom_name = os.path.splitext(rom)[0]
    path = os.path.join(roms_folder, 'screenshots')

    if not os.path.isdir(path):
        return screenshots

    for file in os.listdir(path):
        if file.startswith(rom_name) and file.endswith('.png'):
            screenshots.append(file)

    return screenshots

def getsize_fmt(path):
    if os.path.isfile(path):
        size = os.path.getsize(path)
        for unit in ["", "Ki", "Mi", "Gi", "Ti", "Pi", "Ei", "Zi"]:
            if abs(size) < 1024.0:
                return f"{size:3.1f}{unit}b"
            size /= 1024.0
        return f"{size:.1f}Yib"
    else:
        return "0b"

def map_system_folder(system):
    if system in system_map:
        return system_map[system]
    return system

def normalize_path(path):
    return remove_prefix(path, "./")

def http_post(path, body=""):
    headers = { 'Content-type': 'text/plain', 'Accept': 'text/plain' }
    conn = http.client.HTTPConnection('127.0.0.1', 1234)
    conn.request('POST', path, body, headers)
    response = conn.getresponse()
    data = response.read()
    conn.close()
    return data

def http_get(path, body=""):
    headers = { 'Content-type': 'text/plain', 'Accept': 'text/plain' }
    conn = http.client.HTTPConnection('127.0.0.1', 1234)
    conn.request('GET', path, body, headers)
    response = conn.getresponse()
    data = response.read()
    conn.close()
    return data

def start_game(rom_path):
    http_post('/launch', rom_path)

def close_game():
    emu_kill()

def emu_kill():
    if platform.system() == 'Darwin':
        return True
    path = os.path.join(os.getcwd(), 'helpers.sh')
    return subprocess.call(["/bin/bash", path, "--emukill"]) == 0

def emu_running():
    if platform.system() == 'Darwin':
        return False
    path = os.path.join(os.getcwd(), 'helpers.sh')
    return subprocess.call(["/bin/bash", path, "--emupid"]) == 0
