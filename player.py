#!/usr/bin/python3.7
import os, time, random, threading, json, shutil, sys, ctypes

from PIL import Image
import stagger
import io

from pygame import mixer

from flask import Flask

from pynput.keyboard import Key, Listener

import logging
log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)

app = Flask(__name__)

@app.route('/')
def main_output():
    f = open('static/main.html', 'r')
    main_html = f.read()
    f.close()
    return main_html

@app.route('/update')
def update():
    f = open('temp/song.json', 'r')
    json_data = json.load(f)
    f.close()
    return json_data

mixer.init()

MUSIC_FOLDER = 'music'
music_extension = 'mp3'

key_log = []

album_folders = [f for f in os.listdir(MUSIC_FOLDER) if os.path.isdir(MUSIC_FOLDER + '/' + f)]

all_music = []
for f in album_folders:
    all_music += [f for f in os.listdir(MUSIC_FOLDER + '/' + f) if f.split('.')[-1] == music_extension]

all_music += [f for f in os.listdir(MUSIC_FOLDER) if f.split('.')[-1] == music_extension]

def wait_for_end():
    while 1:
        time.sleep(0.1)
        if not mixer.music.get_busy():
            break

def play_file(path):
    song_data = stagger.read_tag(path)

    json_export = {
        'title': song_data.title,
        'artist': song_data.artist,
        'album': song_data.album,
    }
    if json_export['album'] == '':
        json_export['album'] = 'single'
        
    f = open('temp/song.json', 'w')
    json.dump(json_export, f)
    f.close()

    try:
        by_data = song_data[stagger.id3.APIC][0].data
        im = io.BytesIO(by_data)
        image_file = Image.open(im)
        image_file.save('static/cover.png')
    except:
        shutil.copyfile('static/default_cover.png', 'static/cover.png')

    mixer.music.load(path)
    mixer.music.play()
    wait_for_end()

def play(path):
    try:
        if path.split('.')[-1] == music_extension:
            play_file(MUSIC_FOLDER + '/' + path)
        elif os.path.isdir(MUSIC_FOLDER + '/' + path):
            # albums
            for song in os.listdir(MUSIC_FOLDER + '/' + path):
                if song.split('.')[-1] == music_extension:
                    play_file(MUSIC_FOLDER + '/' + path + '/' + song)
    except:
        return False
    return True

def on_press(key):
    global key_log
    key_log.append([key, time.time()])
    while len(key_log) > 2:
        key_log.pop(0)
    if len(key_log) >= 2:
        if (key_log[-2][0] == Key.shift) and (key_log[-1][0] == Key.esc):
            if key_log[-1][1] - key_log[-2][1] < 0.5:
                mixer.quit()
                sys.exit()
    

def input_handler():
    with Listener(on_press=on_press) as listener:
        listener.join()

if __name__ == '__main__':
    try:
        ctypes.windll.user32.ShowWindow(ctypes.windll.kernel32.GetConsoleWindow(), 0)
    except Exception as e:
        print(e)
    server_thread = threading.Thread(target=app.run, kwargs=dict(port=55912))
    input_thread = threading.Thread(target=input_handler)
    server_thread.daemon = True
    input_thread.daemon = True
    server_thread.start()
    input_thread.start()

while 1:
    global active
    active = play(random.choice(os.listdir(MUSIC_FOLDER)))
    if not active:
        break


