from config_manager import ConfigManager
from cache_manager import CacheManager
from spotify_controller import SpotifyController
from lyrics_manager import LyricsManager
from overlay import Overlay
import syncedlyrics

config = ConfigManager()

CLIENT_ID = ''
CLIENT_SECRET = ''
REDIRECT_URI = 'http://127.0.0.1:8888/callback'

cache = CacheManager(
    max_size_mb=config["cache_max_mb"]
)

spotify = SpotifyController(

    CLIENT_ID,

    CLIENT_SECRET,

    REDIRECT_URI,

    refresh_rate=config["spotify_refresh_rate"]

)

lyrics = LyricsManager()

overlay = Overlay(config)

# ===========================================
# CALLBACKS DO OVERLAY
# ===========================================

overlay.on_next_track = spotify.next_track

overlay.on_previous_track = spotify.previous_track

overlay.on_volume_up = spotify.volume_up

overlay.on_volume_down = spotify.volume_down




# Offset das letras

def update_offset(value):

    lyrics.set_offset(value)


overlay.on_offset_change = update_offset


# Atualização da fonte

def update_font(size):

    config["font_size"] = size


overlay.on_font_change = update_font


last_track = None


def update():

    global last_track

    spotify.update()

    if spotify.is_playing():

        track = spotify.get_track_id()

        if track != last_track:

            last_track = track

            title = spotify.get_track_name()

            artist = spotify.get_artist()

            if cache.exists(title, artist):

                lrc = cache.load(

                    title,

                    artist

                )

            else:

                lrc = syncedlyrics.search(

                    f"{title} {artist}"

                )

                if lrc:

                    cache.save(

                        title,

                        artist,

                        lrc

                    )

            if lrc:

                lyrics.load_lrc(lrc)

            else:

                lyrics.clear()

            overlay.set_music_info( spotify.get_track_name(), 
                                   
            spotify.get_artist(), 

            spotify.get_cover_url()
            )

        previous, current, next_line = (

            lyrics.get_lines(

                spotify.get_progress()

            )

        )

        overlay.update_display(

            previous,

            current,

            next_line

        )

    else:

        overlay.show_paused()

    overlay.root.after(

        int(

            config["ui_refresh_rate"] * 1000

        ),

        update

    )

update()

overlay.run()
