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
        extensions = find_normalized(system, 'extension').split(" ")
        systems.append({
            'fullname': find_normalized(system, 'fullname'),
            'name': find_normalized(system, 'name'),
            'manufacturer': find_image_path(system, 'manufacturer'),
            'folder': find_normalized_system_path(system, 'path'),
            'path': find_normalized(system, 'path'),
            'roms': len(list_files_with_extensions(system_folder_path, extensions))
        })

    systems_sorted = sorted(systems, key=lambda k: (-k['roms'], k['fullname']))

    return dict(systems=json.dumps(systems_sorted))


@route('/system/<system>')
@view('system')
def view_system(system):
    es_systems = ElementTree.parse(es_systems_path).getroot()
    system_ele = es_systems.findall(".//system/[path=\"%s%s\"]" % (roms_folder, system))[0]
    system_info = get_system_info(system_ele)
    system_name = system_info["fullname"] or system
    games = list_roms(system_ele)
    sorted_games = sorted(games, key=lambda k: (k['name']))
    return dict(system=system, system_name=system_name, games=json.dumps(sorted_games), system_info=system_info)


@route('/system/<system>/<game_ref:int>')
@route('/system/<system>/<game_ref:path>')
@view('game')
def view_game(system, game_ref):
    game = get_game_info(system, game_ref)
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


@route('/svg/text/<text>')
def view_svg(text):
    response.set_header('Content-Type', 'image/svg+xml')
    return template('views/empty_svg.tpl', system=text.split())


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
