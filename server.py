import os
import xml.etree.ElementTree as ElementTree
import json

from urllib.parse import unquote
from bottle import route, run, template, view, static_file, response
from helpers import *
from data import *
from config import *

@route('/')
@view('index')
def index():
    systems = { }
    system_folders = list_folders(roms_folder)

    for system_folder in system_folders:
        if not system_folder.lower() in ignored_systems:
            system_folder_path = os.path.join(roms_folder, system_folder)
            systems[system_folder] = {
                'name': map_system_folder(system_folder),
                'folder': system_folder,
                'path': system_folder_path,
                'roms': len(list_files(system_folder_path))
            }

    systems_sorted = sorted(systems, key = lambda k: (-systems[k]['roms'], systems[k]['name']))
    sorted_dict = { k: systems[k] for k in systems_sorted }

    return dict(systems=json.dumps(sorted_dict))


@route('/system/<system>')
@view('system')
def view_system(system):
    root = ElementTree.parse(os.path.join(roms_folder, system, 'gamelist.xml')).getroot()
    games = { }

    for game in root.iter('game'):
        id = game.attrib.get('id')
        rom_filename = normalize_path(find_normalized(game, 'path'))
        games[id] = {
            'id': id,
            'name': find_normalized(game, 'name'),
            'desc': find_normalized(game, 'desc'),
            'image': find_image_path(game, 'image'),
            'marquee': find_image_path(game, 'marquee'),
            'developer': find_normalized(game, 'developer'),
            'publisher': find_normalized(game, 'publisher'),
            'genre': find_normalized(game, 'genre'),
            'path': rom_filename,
        }

    system_name = system
    if system in system_map:
        system_name = system_map[system]

    sorted_games = sorted(games, key = lambda k: (games[k]['name']))
    sorted_dict = { k: games[k] for k in sorted_games }

    return dict(system=system, system_name=system_name, games=json.dumps(sorted_dict))


@route('/system/<system>/<game_id>')
@view('game')
def view_game(system, game_id):
    root = ElementTree.parse(os.path.join(roms_folder, system, 'gamelist.xml')).getroot()
    ele = root.find(".//game[@id='%s']" % game_id)

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
        'saves': find_saves(system, rom_filename),
        'screenshots': find_screenshots(rom_filename)
    }

    system_name = system
    if system in system_map:
        system_name = system_map[system]

    return dict(system=system, system_name=system_name, game=game, game_id=game_id)


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


run(host=host, port=port, reloader=reloader, debug=debug)
