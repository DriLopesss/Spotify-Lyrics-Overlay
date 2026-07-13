"""
spotify_controller.py

Controlador responsável por toda comunicação com a API do Spotify.
"""

import time
import spotipy
from spotipy.oauth2 import SpotifyOAuth


class SpotifyController:

    def __init__(
        self,
        client_id,
        client_secret,
        redirect_uri,
        refresh_rate=2.0
    ):

        scope = (
            "user-read-currently-playing "
            "user-read-playback-state "
            "user-modify-playback-state"
        )

        self.sp = spotipy.Spotify(
            auth_manager=SpotifyOAuth(
                client_id=client_id,
                client_secret=client_secret,
                redirect_uri=redirect_uri,
                scope=scope
            )
        )

        self.refresh_rate = refresh_rate

        self.last_update = 0

        self.last_progress = 0.0

        self.local_sync_time = time.time()

        self.current_state = None

        self.current_track = None

    # ---------------------------------------------------

    def update(self):

        now = time.time()

        if (now - self.last_update) < self.refresh_rate:

            return

        try:

            playback = self.sp.current_playback()

            self.last_update = now

            if playback is None:

                self.current_state = None
                self.current_track = None

                return

            self.current_state = playback

            self.current_track = playback["item"]

            self.last_progress = (
                playback["progress_ms"] / 1000.0
            )

            self.local_sync_time = now

        except Exception:

            pass

    # ---------------------------------------------------

    def get_progress(self):

        if self.current_state is None:

            return 0

        if not self.current_state["is_playing"]:

            return self.last_progress

        elapsed = time.time() - self.local_sync_time

        return self.last_progress + elapsed

    # ---------------------------------------------------

    def is_playing(self):

        if self.current_state is None:

            return False

        return self.current_state["is_playing"]

    # ---------------------------------------------------

    def get_track_id(self):

        if self.current_track is None:

            return None

        return self.current_track["id"]

    # ---------------------------------------------------

    def get_track_name(self):

        if self.current_track is None:

            return None

        return self.current_track["name"]

    # ---------------------------------------------------

    def get_artist(self):

        if self.current_track is None:

            return None

        return self.current_track["artists"][0]["name"]

    # ---------------------------------------------------

    def get_album(self):

        if self.current_track is None:

            return None

        return self.current_track["album"]["name"]

    # ---------------------------------------------------

    def get_cover_url(self):

        if self.current_track is None:

            return None

        images = self.current_track["album"]["images"]

        if len(images) == 0:

            return None

        return images[0]["url"]

    # ---------------------------------------------------

    def get_volume(self):

        if self.current_state is None:

            return 0

        return self.current_state["device"]["volume_percent"]

    # ---------------------------------------------------

    def set_volume(self, value):

        value = max(0, min(100, value))

        self.sp.volume(value)

    # ---------------------------------------------------

    def volume_up(self, amount=10):

        self.set_volume(

            self.get_volume() + amount

        )

    # ---------------------------------------------------

    def volume_down(self, amount=10):

        self.set_volume(

            self.get_volume() - amount

        )

    # ---------------------------------------------------

    def next_track(self):

        self.sp.next_track()

    # ---------------------------------------------------

    def previous_track(self):

        self.sp.previous_track()

    # ---------------------------------------------------

    def pause(self):

        self.sp.pause_playback()

    # ---------------------------------------------------

    def resume(self):

        self.sp.start_playback()

    # ---------------------------------------------------

    def toggle_play(self):

        if self.is_playing():

            self.pause()

        else:

            self.resume()

    # ---------------------------------------------------

    def has_track_changed(self, last_track_id):

        current = self.get_track_id()

        return current != last_track_id

    # ---------------------------------------------------

    def get_music_info(self):

        if self.current_track is None:

            return None

        return {

            "id": self.get_track_id(),

            "title": self.get_track_name(),

            "artist": self.get_artist(),

            "album": self.get_album(),

            "cover": self.get_cover_url(),

            "progress": self.get_progress(),

            "playing": self.is_playing(),

            "volume": self.get_volume()

        }