import os
import datetime
import subprocess
import platform
import xml.etree.ElementTree as ElementTree

from html import unescape
from config import *

try:
    from ftfy import fix_text
except ModuleNotFoundError:
    def fix_text(text):
        return text

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

def list_files_with_extensions(path, extensions):
    files = []
    if folder_exists(path):
        for entry in os.scandir(path):
            if not entry.name.startswith('.') and entry.is_file() and os.path.splitext(entry)[1] in extensions:
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

def find_normalized_system_path(node, look):
    return remove_prefix(find_normalized(node, look), roms_folder)

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
    es_systems = ElementTree.parse(es_systems_path).getroot()
    system_ele = es_systems.findall(".//system[path=\"%s%s\"]" % (roms_folder, system))[0]
    if system_ele:
        return system_ele.find("fullname").text
    return system

def normalize_path(path):
    return remove_prefix(path, "./")

def http_post(url, body=""):
    if platform.system() == 'Darwin':
        return False
    subprocess.call(["/bin/curl", "-X", "POST", "-d", body, "http://127.0.0.1:1234/%s" % remove_prefix(url, '/')])
    return True

def http_get(url):
    if platform.system() == 'Darwin':
        return False
    subprocess.call(["/bin/curl", "-X", "GET", "http://127.0.0.1:1234/%s" % remove_prefix(url, '/')])
    return True

def start_game(rom_path):
    http_post('/launch', rom_path)

def reload_gameslist():
    http_get('/reloadgames')

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


def get_system_info(system):
    return {
        'name': find_normalized(system, 'name'),
        'fullname': find_normalized(system, 'fullname'),
        'manufacturer': find_image_path(system, 'manufacturer'),
        'release': find_image_path(system, 'release'),
        'hardware': find_normalized(system, 'hardware'),
        'path': find_normalized(system, 'path'),
        'extension': find_normalized(system, 'extension')
    }

def get_game_info(system, game_ref):
    gamelist = os.path.join(roms_folder, system, 'gamelist.xml')

    if os.path.isfile(gamelist):
        root = ElementTree.parse(gamelist).getroot()

        if game_ref.isdigit():
            ele = root.find(".//game[@id='%s']" % game_ref)
        else:
            ele = root.find(".//game/[path=\"./%s\"]" % unescape(game_ref))

        if ele != None:

            rom_filename = remove_prefix(find_normalized(ele, 'path'), './')
            rom_path = os.path.join(roms_folder, system, rom_filename)

            game = {
                'name': find_normalized(ele, 'name'),
                'desc': find_normalized(ele, 'desc'),
                'developer': find_normalized(ele, 'developer'),
                'publisher': find_normalized(ele, 'publisher'),
                'genre': find_normalized(ele, 'genre'),
                'players': find_normalized(ele, 'players'),
                'region': find_normalized(ele, 'region'),
                'lang': find_normalized(ele, 'lang'),
                'image': find_image_path(ele, 'image'),
                'thumbnail': find_image_path(ele, 'thumbnail'),
                'marquee': find_image_path(ele, 'marquee'),
                'video': find_video_path(ele, 'video'),
                'rating': find_float(ele, 'rating'),
                'path': find_normalized_path(ele, 'path'),
                'releasedate': find_date(ele, 'releasedate'),
                'lastplayed': find_date(ele, 'lastplayed'),
                'playcount': find_int(ele, 'playcount'),
                'gametime': find_int(ele, 'gametime'),
                'size': getsize_fmt(rom_path),
                'have_rom': os.path.isfile(rom_path),
                'saves': find_saves(system, rom_filename),
                'screenshots': find_screenshots(rom_filename)
            }

            return game

    rom_path = os.path.join(roms_folder, system, unescape(game_ref))
    if os.path.isfile(rom_path):
        game = {
            'name': game_ref,
            'desc': False,
            'developer': False,
            'publisher': False,
            'genre': False,
            'players': False,
            'region': False,
            'lang': False,
            'image': False,
            'thumbnail': False,
            'marquee': False,
            'video': False,
            'rating': False,
            'path': os.path.basename(rom_path),
            'releasedate': False,
            'lastplayed': False,
            'playcount': False,
            'gametime': False,
            'size': getsize_fmt(rom_path),
            'have_rom': True,
            'saves': find_saves(system, rom_path),
            'screenshots': find_screenshots(rom_path),
        }

        return game
    else:
        return False

def list_roms(system_ele):
    system = find_normalized_system_path(system_ele, 'path')
    gamelist = os.path.join(roms_folder, system, 'gamelist.xml')

    roms = []
    known_roms = []

    if os.path.isfile(gamelist):
        root = ElementTree.parse(gamelist).getroot()
        for game in root.iter('game'):
            id = game.attrib.get('id')
            rom_filename = normalize_path(find_normalized(game, 'path'))
            known_roms.append(rom_filename)
            roms.append({
                'id': id or False,
                'name': find_normalized(game, 'name'),
                'desc': find_normalized(game, 'desc'),
                'image': find_image_path(game, 'image'),
                'marquee': find_image_path(game, 'marquee'),
                'developer': find_normalized(game, 'developer'),
                'publisher': find_normalized(game, 'publisher'),
                'genre': find_normalized(game, 'genre'),
                'path': rom_filename,
            })

    rom_files = list_files(os.path.join(roms_folder, system))
    extensions = system_ele.find("extension").text.split(" ")

    for file in rom_files:
        filename, extension = os.path.splitext(file)
        if extension in extensions and file not in known_roms:
            known_roms.append(file)
            roms.append({
                'id': False,
                'name': filename,
                'desc': False,
                'image': False,
                'marquee': False,
                'developer': False,
                'publisher': False,
                'genre': False,
                'path': file,
            })

    return roms
