import os
import datetime
from html import unescape
from ftfy import fix_text
from data import *

def list_folders(path):
    dirs = []
    for entry in os.scandir(path):
        if not entry.name.startswith('.') and entry.is_dir():
            dirs.append(entry.name)
    return dirs

def list_files(path):
    files = []
    for entry in os.scandir(path):
        if not entry.name.startswith('.') and entry.is_file():
            files.append(entry.name)
    return files

def file_exists(path, file):
    return os.path.isfile(os.path.join(path, file))

def folder_exists(path, file):
    return os.path.isfile(os.path.join(path, file))

def remove_prefix(text, prefix):
    if text.startswith(prefix):
        return text[len(prefix):]
    return text

def find_normalized(node, look):
    if node.find(look) != None:
        return fix_text(unescape(node.find(look).text))
    else:
        return False

def find_float(node, look):
    if node.find(look) != None:
        return float(node.find(look).text)
    else:
        return False

def find_int(node, look):
    if node.find(look) != None:
        return int(node.find(look).text)
    else:
        return False

def find_image_path(node, look):
    if node.find(look) != None:
        return remove_prefix(node.find(look).text, "./images/")
    else:
        return False

def find_video_path(node, look):
    if node.find(look) != None:
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
    size = os.path.getsize(path)
    for unit in ["", "Ki", "Mi", "Gi", "Ti", "Pi", "Ei", "Zi"]:
        if abs(size) < 1024.0:
            return f"{size:3.1f}{unit}b"
        size /= 1024.0
    return f"{size:.1f}Yib"

def map_system_folder(system):
    if system in system_map:
        return system_map[system]
    return system

def normalize_path(path):
    return remove_prefix(path, "./")
