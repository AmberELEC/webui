# full imports
import os
import json
import pam

# partial imports
from urllib.parse import unquote
from distutils import extension
from uuid import uuid4
from bottle import app, route, get, post, run, template, view, static_file, response, request, redirect, auth_basic
from beaker.middleware import SessionMiddleware
from xml.etree.ElementTree import SubElement, Element
from xml.etree.ElementTree import ElementTree as ET

# local imports
from config import *
from helpers import *

session_opts = {
    'session.key': 'amberelec-webui',
    'session.type': 'memory',
    'session.cookie_expires': 3600, # 1 hour
    'session.auto': True
}

app = SessionMiddleware(app(), session_opts)

def check_auth(username, password):
    if disable_auth:
        return True

    session = request.environ.get('beaker.session')

    if session.get('authenticated', False):
        return True
    else:
        if pam.authenticate(username, password):
            session['authenticated'] = True
            session.save()
            return True
        else:
            session['authenticated'] = False
            session.save()
            return False

    return False

@route('/')
@view('index')
@auth_basic(check_auth)
def index():
    systems = []

    for system in get_systems_list().iter('system'):
        system_folder_path = find_normalized(system, 'path')
        extensions = find_normalized(system, 'extension').split(" ")
        systems.append({
            'fullname': find_normalized(system, 'fullname'),
            'name': find_normalized(system, 'name'),
            'manufacturer': find_image_path(system, 'manufacturer'),
            'path': find_normalized(system, 'path'),
            'roms': len(list_files_and_folders_with_extensions(system_folder_path, extensions))
        })

    systems_sorted = sorted(systems, key=lambda k: (-k['roms'], k['fullname']))

    return dict(systems=json.dumps(systems_sorted))


@route('/system/<system>')
@view('system')
@auth_basic(check_auth)
def view_system(system):
    system_ele = get_system_element(system)
    system_info = get_system_info(system_ele)
    system_name = system_info["fullname"] or system
    games = list_roms(system)
    sorted_games = sorted(games, key=lambda k: (k['name']))
    return dict(system=system, system_name=system_name, games=json.dumps(sorted_games), system_info=system_info)


@route('/system/<system>/<game_ref:int>')
@route('/system/<system>/<game_ref:path>')
@view('game')
@auth_basic(check_auth)
def view_game(system, game_ref):
    game = get_game_info(system, game_ref)
    system_name = map_system_folder(system)
    return dict(system=system, system_name=system_name, game=game, game_id=game_ref, running=emu_running())


@route('/edit/<system>/<game_ref:int>')
@route('/edit/<system>/<game_ref:path>')
@auth_basic(check_auth)
def edit(system, game_ref):
    game = get_game_info(system, game_ref)
    system_ele = get_system_element(system)
    system_info = get_system_info(system_ele)
    system_name = system_info["fullname"] or system
    extensions = set([ext.lower() for ext in system_info["extension"].split(" ")])

    files = { }

    if game['path']:
        files['rom'] = json.dumps({ 'name': game['path'], 'size': game['size_raw'], 'type': 'application/binary' })

    if game['image']:
        files['image'] = json.dumps({ 'name': game['image'], 'size': game['image_size'], 'type': 'image/png' })

    if game['marquee']:
        files['marquee'] = json.dumps({ 'name': game['marquee'], 'size': game['marquee_size'], 'type': 'image/png' })

    if game['thumbnail']:
        files['thumbnail'] = json.dumps({ 'name': game['thumbnail'], 'size': game['thumbnail_size'], 'type': 'image/png' })

    if game['video']:
        files['video'] = json.dumps({ 'name': game['video'], 'size': game['video_size'], 'type': 'video/mp4' })

    return template('upload', system=system, system_name=system_name, extensions=extensions, game=game, files=files)


@route('/exists/<system>/<rom>')
@auth_basic(check_auth)
def exists(system, rom):
    gamelist = os.path.join(get_system_path(system), 'gamelist.xml')

    if os.path.isfile(gamelist):
        root = ElementTree.parse(gamelist).getroot()
        ele = root.find(".//game/[path=\"./%s\"]" % unescape(rom))
        if ele != None:
            info = get_game_info(system, rom)
            return { 'exists': True, 'as': info['id'] }

    return { 'exists': False }


@get('/upload/<system>')
@post('/upload/<system>')
@auth_basic(check_auth)
def upload_rom(system):
    if request.forms.get('submit'):
        gamelist = os.path.join(get_system_path(system), 'gamelist.xml')

        if os.path.isfile(gamelist):
            tree = ElementTree.parse(gamelist)
            root = tree.getroot()
        else:
            root = Element('gameList')

        # files
        rom = request.files.get('rom', False)
        marquee = request.files.get('marquee', False)
        screenshot = request.files.get('screenshot', False)
        boxart = request.files.get('boxart', False)
        video = request.files.get('video', False)

        # midstate
        existing_rom = request.forms.get('existing_rom', False)

        # metadata
        name = request.forms.get('name', False)
        publisher = request.forms.get('publisher', False)
        developer = request.forms.get('developer', False)
        published = request.forms.get('published', False)
        genre = request.forms.get('genre', False)
        players = request.forms.get('players', False)
        region = request.forms.get('region', False)
        rating = request.forms.get('rating', False)
        description = request.forms.get('description', False)

        # resolve rom path, look for existing entry
        if rom != False and rom.filename != 'empty':
            if root.find(".//game/[path=\"./%s\"]" % rom.raw_filename):
                game = root.find(".//game/[path=\"./%s\"]" % rom.raw_filename)
            else:
                game = SubElement(root, 'game', attrib={ 'id': str(uuid4()) })
                game.tail = "\n"
                entry = SubElement(game, 'path')
                entry.text = "./%s" % rom.raw_filename
            rom_filename = rom.raw_filename
        elif existing_rom:
            game = root.find(".//game/[path=\"./%s\"]" % existing_rom)
            rom_filename = existing_rom
            if not game:
                game = SubElement(root, 'game', attrib={ 'id': str(uuid4()) })
                game.tail = "\n"
                entry = SubElement(game, 'path')
                entry.text = "./%s" % existing_rom
        else:
            return redirect('/')

        if name:
            update_game_entry(game, 'name', name)
        else:
            update_game_entry(game, 'name', os.path.splitext(rom.raw_filename)[0])

        if publisher:
            update_game_entry(game, 'publisher', publisher)

        if developer:
            update_game_entry(game, 'developer', developer)

        if published:
            update_game_entry(game, 'releasedate', date_to_xml(published))

        if genre:
            update_game_entry(game, 'genre', genre)

        if players:
            update_game_entry(game, 'players', players)

        if region:
            update_game_entry(game, 'region', region)

        if rating:
            update_game_entry(game, 'rating', str(float(rating) / 5))

        if description:
            update_game_entry(game, 'desc', description)

        if rom and rom.filename != 'empty':
            rom.save(system_path(system, rom.raw_filename), overwrite=True)

        if marquee and marquee.filename != 'empty':
            update_game_entry(game, 'marquee', "./images/%s" % marquee.raw_filename)
            os.makedirs(system_path(system, 'images'), exist_ok=True)
            marquee.save(system_path(system, 'images', marquee.raw_filename), overwrite=True)

        if screenshot and screenshot.filename != 'empty':
            update_game_entry(game, 'image', "./images/%s" % screenshot.raw_filename)
            os.makedirs(system_path(system, 'images'), exist_ok=True)
            screenshot.save(system_path(system, 'images', screenshot.raw_filename), overwrite=True)

        if boxart and boxart.filename != 'empty':
            update_game_entry(game, 'thumbnail', "./images/%s" % boxart.raw_filename)
            os.makedirs(system_path(system, 'images'), exist_ok=True)
            boxart.save(system_path(system, 'images', boxart.raw_filename), overwrite=True)

        if video and video.filename != 'empty':
            update_game_entry(game, 'video', "./videos/%s" % boxart.raw_filename)
            os.makedirs(system_path(system, 'videos'), exist_ok=True)
            video.save(system_path(system, 'videos', boxart.raw_filename), overwrite=True)

        with open(gamelist, 'wb') as file:
            ET(root).write(file, encoding='utf-8', xml_declaration=True)

        game_id = game.attrib.get('id')

        return redirect('/system/%s/%s' % (system, game_id if game_id else rom_filename))
    else:
        system_ele = get_system_element(system)
        system_info = get_system_info(system_ele)
        system_name = system_info["fullname"] or system
        extensions = set([ext.lower() for ext in system_info["extension"].split(" ")])
        return template('upload', system=system, system_name=system_name, extensions=extensions)


@route('/svg/<system>')
@auth_basic(check_auth)
def view_svg(system):
    """Fetches a system logo SVG, or generates a simple text SVG if the logo is missing."""
    svg_dir = os.path.join(os.getcwd(), 'assets', 'svgs')
    system_ele = get_system_element(system)
    theme = system_ele.find("theme").text
    svg = '%s.svg' % theme

    response.set_header('Cache-Control', 'max-age=3600')

    if file_exists(svg_dir, svg):
        return static_file(svg, root=svg_dir)
    else:
        response.set_header('Content-Type', 'image/svg+xml')
        return template('views/empty_svg.tpl', system=map_system_folder(system).split())


@route('/svg/text/<text>')
@auth_basic(check_auth)
def view_svg(text):
    response.set_header('Content-Type', 'image/svg+xml')
    return template('views/empty_svg.tpl', system=text.split())


@route('/image/<system>/<image:path>')
@auth_basic(check_auth)
def view_image(system, image):
    image = unquote(image)
    path=get_system_path(system)
    response.set_header('Cache-Control', 'max-age=3600')
    return static_file(image, root=path)


@route('/video/<system>/<video:path>')
@auth_basic(check_auth)
def view_video(system, video):
    video = unquote(video)
    path=get_system_path(system)
    response.set_header('Cache-Control', 'max-age=3600')
    return static_file(video, root=path)


@route('/rom/<system>/<rom:path>')
@auth_basic(check_auth)
def download_rom(system, rom):
    rom = unquote(rom)
    path=get_system_path(system)
    return static_file(rom, root=path, download=rom)


@route('/snapshot/<system>/<save>')
@auth_basic(check_auth)
def view_snapshot(system, save):
    path = os.path.join(roms_folder, 'savestates', system)
    png = '%s%s' % (save, '.png')
    response.set_header('Cache-Control', 'max-age=3600')
    return static_file(png, root=path)


@route('/savestate/<system>/<save>')
@auth_basic(check_auth)
def download_savestate(system, save):
    path = os.path.join(roms_folder, 'savestates', system)
    return static_file(save, root=path, download=save)


@route('/screenshots/<screenshot>')
@auth_basic(check_auth)
def view_screenshot(screenshot):
    path = os.path.join(roms_folder, 'screenshots')
    return static_file(screenshot, root=path)


@route('/assets/<path:path>')
@auth_basic(check_auth)
def assets(path):
    root = os.path.join(os.getcwd(), 'assets')
    return static_file(path, root=root)


@route('/launch/<system>/<rom>')
@auth_basic(check_auth)
def assets(system, rom):
    path = os.path.join(get_system_path(system), rom)
    start_game(path)


@route('/exitemu')
@auth_basic(check_auth)
def assets():
    close_game()


@route('/reloadgames')
@auth_basic(check_auth)
def assets():
    reload_gameslist()


run(app=app, host=host, port=port, reloader=reloader, debug=debug)
