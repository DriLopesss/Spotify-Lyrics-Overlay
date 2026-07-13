"""
config_manager.py
Gerencia todas as configurações persistentes do Spotify Overlay.

Autor: Projeto Spotify Overlay
"""

import json
import os
from copy import deepcopy


class ConfigManager:

    DEFAULT_CONFIG = {

        # ----------------------------
        # Janela
        # ----------------------------

        "window_x": 50,
        "window_y": 50,

        "window_width": 800,
        "window_height": 200,

        "always_on_top": True,

        # ----------------------------
        # Fonte
        # ----------------------------

        "font_family": "Segoe UI",
        "font_size": 26,

        "current_line_bold": True,

        # ----------------------------
        # Aparência
        # ----------------------------

        "theme_color": "#1DB954",

        "background_color": "#000000",

        "background_opacity": 0.0,

        "shadow": True,

        "shadow_offset": 2,

        # ----------------------------
        # Letras
        # ----------------------------

        "show_previous": True,

        "show_next": True,

        "global_offset": 0.0,

        "line_spacing": 8,

        # ----------------------------
        # Atualização
        # ----------------------------

        "spotify_refresh_rate": 2.0,

        "ui_refresh_rate": 0.03,

        # ----------------------------
        # Cache
        # ----------------------------

        "cache_max_mb": 50,

        # ----------------------------
        # Interface
        # ----------------------------

        "compact_mode": False,

        "edit_mode": False

    }

    def __init__(self, filename="config.json"):

        self.filename = filename

        self.data = deepcopy(self.DEFAULT_CONFIG)

        self.load()

    # --------------------------------

    def load(self):

        if not os.path.exists(self.filename):

            self.save()

            return

        try:

            with open(
                self.filename,
                "r",
                encoding="utf8"
            ) as f:

                loaded = json.load(f)

            # Mantém compatibilidade com versões futuras
            for key, value in self.DEFAULT_CONFIG.items():

                if key not in loaded:

                    loaded[key] = value

            self.data = loaded

        except Exception:

            # Caso o arquivo corrompa
            self.data = deepcopy(self.DEFAULT_CONFIG)

            self.save()

    # --------------------------------

    def save(self):

        with open(
            self.filename,
            "w",
            encoding="utf8"
        ) as f:

            json.dump(
                self.data,
                f,
                indent=4,
                ensure_ascii=False
            )

    # --------------------------------

    def get(self, key):

        return self.data.get(key)

    # --------------------------------

    def set(self, key, value):

        self.data[key] = value

        self.save()

    # --------------------------------

    def update(self, dictionary):

        self.data.update(dictionary)

        self.save()

    # --------------------------------

    def reset(self):

        self.data = deepcopy(self.DEFAULT_CONFIG)

        self.save()

    # --------------------------------

    def __getitem__(self, key):

        return self.get(key)

    # --------------------------------

    def __setitem__(self, key, value):

        self.set(key, value)

    # --------------------------------

    def __contains__(self, key):

        return key in self.data

    # --------------------------------

    def __str__(self):

        return str(self.data)
