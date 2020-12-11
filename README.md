# dfp-music-overlay
a local music player for streaming

the title, artist, album, and cover are extracted from the sound file.

might release an executable later...

![](https://ibb.co/Z169Y5K)

## Dependencies

This script uses Python3 and the following dependencies. Install with the following (`pip3` may be `pip` on some installs):

`pip3 install Pillow flask pygame stagger pynput`

## Setup

This script runs off of local music. Create a `music` folder in the same directory as `player.py`. Then dump all your music in there. Sub-folders are considered albums and will be played as a group. It's worth noting that the expected file type is `.mp3`, but `.wav` and a few other types may work if you switch the `music_extension` variable in `player.py`.

An album layout example:
```
player.py
music/
├─ my_album/
│  ├─ album_song_1.mp3
│  ├─ album_song_2.mp3
├─ my_single_1.mp3
├─ my_single_2.mp3
```

If you're using OBS, you'll want to add a `Browser` source.

![](https://i.imgur.com/exBu426.png)

Right click your new source and go to `Properties`. I recommend the following configuration (the URL is the most important part):

![](https://i.imgur.com/FduOGuN.png)

Hiding the source and reloading it will refresh the webpage the overlay is sourced from if my settings are used. Until you've started the music player for the first time, you probably won't see anything other than some leftover values I had.

## Running

If you have Python3 and all of the dependencies installed, you should just have to double click `player.py`. You'll briefly see a console pop up and disappear. You should start hearing music. If you hear the music, the overlay should be functioning as well (you may need to get OBS to reload the webpage). To stop it, just press shift+esc. If for some reason that isn't working, just kill the python process in task manager. The music is selected randomly with songs in albums grouped.

## Customization

Since the overlay is rendered as a webpage, you can easily modify the website by modifying the `main.css` and the `main.html` under the `static` folder. Just make sure that all of the `id=`s are kept since the JS script expects those.
