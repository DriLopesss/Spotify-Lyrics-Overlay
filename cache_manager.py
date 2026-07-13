
"""
cache_manager.py

Gerencia o cache local das letras (.lrc).

- Evita baixar a mesma música diversas vezes;
- Mantém um índice em JSON;
- Remove automaticamente os arquivos menos utilizados
  quando ultrapassar o tamanho máximo definido.
"""

import json
import os
import time


class CacheManager:

    def __init__(
        self,
        cache_dir="cache",
        index_file="cache/index.json",
        max_size_mb=50
    ):

        self.cache_dir = cache_dir
        self.index_file = index_file
        self.max_size = max_size_mb * 1024 * 1024

        os.makedirs(self.cache_dir, exist_ok=True)

        self.index = {}

        self.load_index()

    # --------------------------------------------

    def load_index(self):

        if os.path.exists(self.index_file):

            try:

                with open(
                    self.index_file,
                    "r",
                    encoding="utf8"
                ) as f:

                    self.index = json.load(f)

            except Exception:

                self.index = {}

        else:

            self.index = {}

            self.save_index()

    # --------------------------------------------

    def save_index(self):

        with open(
            self.index_file,
            "w",
            encoding="utf8"
        ) as f:

            json.dump(
                self.index,
                f,
                indent=4,
                ensure_ascii=False
            )

    # --------------------------------------------

    def _music_key(self, title, artist):

        return f"{artist} - {title}"

    # --------------------------------------------

    def exists(self, title, artist):

        key = self._music_key(title, artist)

        if key not in self.index:
            return False

        path = os.path.join(
            self.cache_dir,
            self.index[key]["file"]
        )

        return os.path.exists(path)

    # --------------------------------------------

    def load(self, title, artist):

        key = self._music_key(title, artist)

        if key not in self.index:
            return None

        file_name = self.index[key]["file"]

        path = os.path.join(
            self.cache_dir,
            file_name
        )

        if not os.path.exists(path):
            return None

        self.index[key]["last_used"] = time.time()

        self.save_index()

        with open(
            path,
            "r",
            encoding="utf8"
        ) as f:

            return f.read()

    # --------------------------------------------

    def save(self, title, artist, lyrics_text):

        key = self._music_key(title, artist)

        if key in self.index:

            file_name = self.index[key]["file"]

        else:

            file_name = f"{int(time.time()*1000)}.lrc"

        path = os.path.join(
            self.cache_dir,
            file_name
        )

        with open(
            path,
            "w",
            encoding="utf8"
        ) as f:

            f.write(lyrics_text)

        self.index[key] = {

            "file": file_name,

            "last_used": time.time()

        }

        self.save_index()

        self.cleanup()

    # --------------------------------------------

    def cleanup(self):

        while self.get_cache_size() > self.max_size:

            if len(self.index) == 0:
                return

            oldest = min(
                self.index.items(),
                key=lambda x: x[1]["last_used"]
            )

            music_key = oldest[0]

            filename = oldest[1]["file"]

            path = os.path.join(
                self.cache_dir,
                filename
            )

            if os.path.exists(path):

                os.remove(path)

            del self.index[music_key]

            self.save_index()

    # --------------------------------------------

    def get_cache_size(self):

        total = 0

        for root, dirs, files in os.walk(self.cache_dir):

            for file in files:

                if file == "index.json":
                    continue

                path = os.path.join(root, file)

                total += os.path.getsize(path)

        return total

    # --------------------------------------------

    def clear(self):

        for music in list(self.index.keys()):

            filename = self.index[music]["file"]

            path = os.path.join(
                self.cache_dir,
                filename
            )

            if os.path.exists(path):

                os.remove(path)

        self.index = {}

        self.save_index()

    # --------------------------------------------

    def stats(self):

        return {

            "songs": len(self.index),

            "size_mb": round(
                self.get_cache_size() / 1024 / 1024,
                2
            )

        }