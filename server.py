import os
import json

from urllib.parse import unquote
from bottle import route, run, template, view, static_file, response, request
from helpers import *
from config import *

@route('/')
@view('index')
def index():
    systems = []
    es_systems = ElementTree.parse(es_systems_path).getroot()

    for system in es_systems.iter('system'):
        system_folder_path = find_normalized(system, 'path')
        systems.append({
            'fullname': find_normalized(system, 'fullname'),
            'name': find_normalized(system, 'name'),
            'path': find_normalized(system, 'path'),
            'roms': len(list_files(system_folder_path))
        })

    systems_sorted = sorted(systems, key=lambda k: (-k['roms'], k['fullname']))

    return dict(systems=json.dumps(systems_sorted))


@route('/system/<system>')
@view('system')
def view_system(system):
    es_systems = ElementTree.parse(es_systems_path).getroot()
    root = ElementTree.parse(os.path.join(roms_folder, system, 'gamelist.xml')).getroot()
    games = []
    system_info = { }

    system_ele = es_systems.findall(".//system/[name=\"%s\"]" % system)[0]

    if system_ele:
        system_info = {
            'name': find_normalized(system_ele, 'name'),
            'fullname': find_normalized(system_ele, 'fullname'),
            'manufacturer': find_image_path(system_ele, 'manufacturer'),
            'release': find_image_path(system_ele, 'release'),
            'hardware': find_normalized(system_ele, 'hardware'),
            'path': find_normalized(system_ele, 'path'),
            'extension': find_normalized(system_ele, 'extension')
        }

    for game in root.iter('game'):
        id = game.attrib.get('id')
        rom_filename = normalize_path(find_normalized(game, 'path'))
        games.append({
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

    system_name = map_system_folder(system)

    sorted_games = sorted(games, key=lambda k: (k['name']))

    return dict(system=system, system_name=system_name, games=json.dumps(sorted_games), system_info=system_info)


@route('/system/<system>/<game_ref:int>')
@route('/system/<system>/<game_ref:path>')
@view('game')
def view_game(system, game_ref):
    root = ElementTree.parse(os.path.join(roms_folder, system, 'gamelist.xml')).getroot()

    if game_ref.isdigit():
        ele = root.find(".//game[@id='%s']" % game_ref)
    else:
        ele = root.findall(".//game/[path=\"./%s\"]" % unescape(game_ref))[0]

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

    system_name = map_system_folder(system)

    return dict(system=system, system_name=system_name, game=game, game_id=game_ref, running=emu_running())


@route('/svg/<system>')
def view_svg(system):
    """Fetches a system logo SVG, or generates a simple text SVG if the logo is missing."""
    svg_dir = os.path.join(os.getcwd(), 'assets', 'svgs')
    svg = '%s.svg' % system

    response.set_header('Cache-Control', 'max-age=3600')

    if file_exists(svg_dir, svg):
        return static_file(svg, root=svg_dir)
    else:
        response.set_header('Content-Type', 'image/svg+xml')
        return template('views/empty_svg.tpl', system=map_system_folder(system).split())


@route('/image/<system>/<image>')
def view_image(system, image):
    image = os.path.join('images', unquote(image))
    path = os.path.join(roms_folder, system)
    response.set_header('Cache-Control', 'max-age=3600')
    return static_file(image, root=path)


@route('/video/<system>/<video>')
def view_video(system, video):
    video = os.path.join('videos', unquote(video))
    path = os.path.join(roms_folder, system)
    response.set_header('Cache-Control', 'max-age=3600')
    return static_file(video, root=path)


@route('/rom/<system>/<rom>')
def download_rom(system, rom):
    rom = unquote(rom)
    path = os.path.join(roms_folder, system)
    return static_file(rom, root=path, download=rom)


@route('/snapshot/<system>/<save>')
def view_snapshot(system, save):
    path = os.path.join(roms_folder, 'savestates', system)
    png = '%s%s' % (save, '.png')
    response.set_header('Cache-Control', 'max-age=3600')
    return static_file(png, root=path)


@route('/savestate/<system>/<save>')
def download_savestate(system, save):
    path = os.path.join(roms_folder, 'savestates', system)
    return static_file(save, root=path, download=save)


@route('/screenshots/<screenshot>')
def view_screenshot(screenshot):
    path = os.path.join(roms_folder, 'screenshots')
    return static_file(screenshot, root=path)


@route('/assets/<path:path>')
def assets(path):
    root = os.path.join(os.getcwd(), 'assets')
    return static_file(path, root=root)


@route('/launch/<system>/<rom>')
def assets(system, rom):
    path = os.path.join(roms_folder, system, rom)
    start_game(path)


@route('/exitemu')
def assets():
    close_game()


@route('/reloadgames')
def assets():
    reload_gameslist()


run(host=host, port=port, reloader=reloader, debug=debug)
