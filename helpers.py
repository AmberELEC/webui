import os
import datetime
import subprocess
import platform
import xml.etree.ElementTree as ElementTree

from html import unescape
from config import *
from xml.etree.ElementTree import SubElement, Element
from uuid import UUID

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

def list_files_and_folders(path):
    files = []
    if folder_exists(path):
        for entry in os.scandir(path):
            if not entry.name.startswith('.'):
                files.append(entry.name)
    return files

def list_files_and_folders_with_extensions(path, extensions):
    files = []
    if folder_exists(path):
        for entry in os.scandir(path):
            if not entry.name.startswith('.') and os.path.splitext(entry)[1] in extensions:
                files.append(entry.name)
    return files

def file_exists(path, file):
    return os.path.isfile(os.path.join(path, file))

def file_get_size(file):
    if os.path.isfile(file):
        return os.path.getsize(file)

def folder_exists(path):
    return os.path.isdir(path)

def remove_prefix(text, prefix):
    if text.startswith(prefix):
        return text[len(prefix):]
    return text

def find(node, look):
    if node.find(look) != None and node.find(look).text != None:
        return node.find(look).text
    else:
        return False

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
        return node.find(look).text
    else:
        return False

def find_video_path(node, look):
    if node.find(look) != None and node.find(look).text != None:
        return node.find(look).text
    else:
        return False

def find_normalized_path(node, look):
    return remove_prefix(find_normalized(node, look), "./")

def system_path(system, *paths):
    return os.path.join(os.path.abspath(get_system_path(system)), *paths)

def find_date(node, look):
    if find_normalized(node, look):
        return format_xml_date(find_normalized(node, look))
    else:
        return False

def find_date_form(node, look):
    if find_normalized(node, look):
        return format_xml_date_form(find_normalized(node, look))
    else:
        return False

def format_xml_date(date):
    try:
      return datetime.datetime.strptime(date, '%Y%m%dT%H%M%S').strftime('%d %B %Y')
    except ValueError:
      return date

def format_xml_date_form(date):
    try:
      return datetime.datetime.strptime(date, '%Y%m%dT%H%M%S').strftime('%Y-%m-%d')
    except ValueError:
      return date
def date_to_xml(date):
    return datetime.datetime.strptime(date, '%Y-%m-%d').strftime('%Y%m%dT%H%M%S')

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

    if os.path.isdir(path):
        return ""
    else:
        return "0b"

def map_system_folder(system):
    system_ele = get_system_element(system)
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

es_systems = None

# This lazy caches the ES systems list (from es_systems.cfg)
# - the file is read only - so caching is ok
# - caching does trade a bit of memory usage for not having to reload from file.
#   I think this is necessary to figure out the non-standard system paths. 
#   - Another option to limit memory would be to refactor to just cache the system paths in a dictionary, etc.
def get_systems_list():
    global es_systems
    
    if not es_systems:
        es_systems = ElementTree.parse(es_systems_path).getroot()

    return es_systems

def get_system_element(system_name):
    return get_systems_list().findall(".//system/[name=\"%s\"]" % ( system_name))[0]

def get_system_path(system_name):
    return find_normalized(get_system_element(system_name),'path')

def get_game_info(system, game_ref):
    system_folder_path = get_system_path(system)
    gamelist = os.path.join(system_folder_path, 'gamelist.xml')

    if os.path.isfile(gamelist):
        root = ElementTree.parse(gamelist).getroot()

        if game_ref.isdigit():
            ele = root.find(".//game[@id='%s']" % game_ref)
        elif is_valid_uuid(game_ref):
            ele = root.find(".//game[@id='%s']" % game_ref)
        else:
            ele = root.find(".//game/[path=\"./%s\"]" % unescape(game_ref))

        if ele != None:

            #NOTE: is it important the rom_filename is not 'normalized' as it will mess up loading from file system in cases like: é
            rom_filename = remove_prefix(find(ele, 'path'), './')
            rom_path = os.path.join(system_folder_path, rom_filename)

            game = {
                'id': ele.attrib.get('id', False) or rom_filename,
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
                'path': rom_filename,
                'releasedate': find_date(ele, 'releasedate'),
                'releasedate_form': find_date_form(ele, 'releasedate'),
                'lastplayed': find_date(ele, 'lastplayed'),
                'playcount': find_int(ele, 'playcount'),
                'gametime': find_int(ele, 'gametime'),
                'size': getsize_fmt(rom_path),
                'size_raw': file_get_size(rom_path),
                'have_rom': os.path.exists(rom_path),
                'can_download': os.path.isfile(rom_path),
                'saves': find_saves(system, rom_filename),
                'screenshots': find_screenshots(rom_filename)
            }

            if game["image"]:
                game["image_size"] = file_get_size(os.path.join(system_folder_path, find_image_path(ele, 'image')))

            if game["thumbnail"]:
                game["thumbnail_size"] = file_get_size(os.path.join(system_folder_path, find_image_path(ele, 'thumbnail')))

            if game["marquee"]:
                game["marquee_size"] = file_get_size(os.path.join(system_folder_path, find_image_path(ele, 'marquee')))

            if game["video"]:
                game["video_size"] = file_get_size(os.path.join(system_folder_path, find_image_path(ele, 'video')))

            return game

    rom_path = os.path.join(system_folder_path, unescape(game_ref))
    if os.path.exists(rom_path):
        game = {
            'id': game_ref,
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
            'image_size': 0,
            'thumbnail_size': 0,
            'marquee_size': 0,
            'video_size': 0,
            'rating': False,
            'path': os.path.basename(rom_path),
            'releasedate': False,
            'releasedate_form': False,
            'lastplayed': False,
            'playcount': False,
            'gametime': False,
            'size': getsize_fmt(rom_path),
            'size_raw': file_get_size(rom_path),
            'have_rom': True,
            'can_download': os.path.isfile(rom_path),
            'saves': find_saves(system, rom_path),
            'screenshots': find_screenshots(rom_path),
        }

        return game
    else:
        return False

def list_roms(system):
    system_ele = get_system_element(system)
    gamelist = os.path.join(get_system_path(system), 'gamelist.xml')

    roms = []
    known_roms = []

    if os.path.isfile(gamelist):
        root = ElementTree.parse(gamelist).getroot()
        for game in root.iter('game'):
            id = game.attrib.get('id')

            # NOTE: it is important the filename is not normalized using 'find_normalized' or it will mess up loading from file system
            rom_filename = remove_prefix(find(game, 'path'), './')

            # Hide any entries where files don't exist
            if not os.path.exists(os.path.join(get_system_path(system),rom_filename)):
                continue

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

    rom_files = list_files_and_folders(get_system_path(system))
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

def update_game_entry(game, name, value):
    if value != False and value != None:
        if game.find(name) != None:
            game.find(name).text = value
        else:
            entry = SubElement(game, name)
            entry.text = value

def is_valid_uuid(val):
    try:
        UUID(str(val))
        return True
    except ValueError:
        return False
