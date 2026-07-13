"""
overlay.py

Responsável apenas pela interface gráfica do Spotify Overlay.

Este módulo NÃO conhece:
- Spotify
- LyricsManager
- CacheManager

Ele apenas recebe informações e as desenha.

Autor: Projeto Spotify Overlay
"""
import keyboard
import tkinter as tk
import ctypes
from PIL import Image, ImageTk
import requests
from io import BytesIO


class Overlay:

    # ----------------------------------------------------

    def __init__(self, config): 

        keyboard.add_hotkey(
            "f12",
            lambda: self.root.after(
             0,
            self.toggle_edit_mode
         )
        )

        self.config = config

        self.edit_mode = False

        self.root = tk.Tk()

        self.root.title("Spotify Overlay")

        self.root.overrideredirect(True)

        self.root.attributes("-topmost", True)

        self.root.attributes("-transparentcolor", "black")

        self.root.configure(bg="black")

        # Callbacks externos
        self.on_next_track = None
        self.on_previous_track = None
        self.on_volume_up = None
        self.on_volume_down = None
        self.on_font_change = None
        self.on_offset_change = None

        self.offset = 0.0

        self.previous_text = ""
        self.current_text = ""
        self.next_text = ""

        self.theme_color = self.config["theme_color"]

        self.progress_value = 0.0

        self.accent_color = self.config["theme_color"]

        self.opacity = self.config["background_opacity"]

        self.shadow_enabled = self.config["shadow"]

        self.shadow_offset = self.config["shadow_offset"]

        self.draw_border = False

        

        width = self.config["window_width"]
        height = self.config["window_height"]

        x = self.config["window_x"]
        y = self.config["window_y"]

        self.root.geometry(
            f"{width}x{height}+{x}+{y}"
        )

        self.drag_x = 0
        self.drag_y = 0

        self.create_widgets()

        self.bind_events()

        self.enable_clickthrough()
        
        self.bind_keyboard()

        self.cover_photo = None

        self.cover_label = tk.Label(
            self.root,
            bg="black",
            bd=0
        )

        self.song_label = tk.Label(
            self.root,
            text="",
            bg="black",
            fg="white",
            justify="left",
            font=("Segoe UI", 10, "bold")
        )

    # ----------------------------------------------------

    def create_widgets(self):

        font_name = self.config["font_family"]
        font_size = self.config["font_size"]

        self.container = tk.Frame(
            self.root,
            bg="black"
        )

        self.container.pack(
            expand=True,
            fill="both"
        )

        # --------------------------
        # Linha anterior
        # --------------------------

        self.previous_shadow = tk.Label(
            self.container,
            text="",
            font=(font_name, int(font_size * 0.75)),
            fg="black",
            bg="black"
        )

        self.previous = tk.Label(
            self.container,
            text="",
            font=(font_name, int(font_size * 0.75)),
            fg="#909090",
            bg="black"
        )

        # --------------------------
        # Linha atual
        # --------------------------

        weight = "bold"

        if not self.config["current_line_bold"]:
            weight = "normal"

        self.current_shadow = tk.Label(
            self.container,
            text="",
            font=(font_name, font_size, weight),
            fg="black",
            bg="black"
        )

        self.current = tk.Label(
            self.container,
            text="",
            font=(font_name, font_size, weight),
            fg=self.config["theme_color"],
            bg="black"
        )

        # --------------------------
        # Próxima linha
        # --------------------------

        self.next_shadow = tk.Label(
            self.container,
            text="",
            font=(font_name, int(font_size * 0.75)),
            fg="black",
            bg="black"
        )

        self.next = tk.Label(
            self.container,
            text="",
            font=(font_name, int(font_size * 0.75)),
            fg="#909090",
            bg="black"
        )

        # --------------------------
        # Layout
        # --------------------------

        self.previous_shadow.place(
            relx=0.5,
            y=24,
            anchor="n"
        )

        self.previous.place(
            relx=0.5,
            y=22,
            anchor="n"
        )

        self.current_shadow.place(
            relx=0.5,
            y=74,
            anchor="n"
        )

        self.current.place(
            relx=0.5,
            y=72,
            anchor="n"
        )

        self.next_shadow.place(
            relx=0.5,
            y=128,
            anchor="n"
        )

        self.next.place(
            relx=0.5,
            y=126,
            anchor="n"
        )

        # --------------------------
        # Painel de edição
        # --------------------------

        self.edit_label = tk.Label(

            self.root,

            text=(
                "MODO EDIÇÃO\n\n"
                "Arraste para mover\n"
                "+/- Fonte\n"
                "← → Offset\n"
                "↑ ↓ Volume\n"
                "F12 Finalizar"
            ),

            bg="#222222",

            fg="white",

            font=("Segoe UI", 10, "bold"),

            justify="left"

        )

    # ----------------------------------------------------

    def bind_events(self):

        self.root.bind(
            "<ButtonPress-1>",
            self.start_drag
        )

        self.root.bind(
            "<B1-Motion>",
            self.drag
        )

    # ----------------------------------------------------

    def start_drag(self, event):

        if not self.edit_mode:
            return

        self.drag_x = event.x

        self.drag_y = event.y

    # ----------------------------------------------------

    def drag(self, event):

        if not self.edit_mode:
            return

        x = (
            self.root.winfo_x()
            + event.x
            - self.drag_x
        )

        y = (
            self.root.winfo_y()
            + event.y
            - self.drag_y
        )

        self.root.geometry(

            f"+{x}+{y}"

        )

        self.config["window_x"] = x

        self.config["window_y"] = y

    # ----------------------------------------------------

    def enable_clickthrough(self):

        GWL_EXSTYLE = -20

        WS_EX_LAYERED = 0x80000

        WS_EX_TRANSPARENT = 0x20

        hwnd = ctypes.windll.user32.GetParent(

            self.root.winfo_id()

        )

        style = ctypes.windll.user32.GetWindowLongW(

            hwnd,

            GWL_EXSTYLE

        )

        style |= WS_EX_LAYERED

        style |= WS_EX_TRANSPARENT

        ctypes.windll.user32.SetWindowLongW(

            hwnd,

            GWL_EXSTYLE,

            style

        )

    # ----------------------------------------------------

    def disable_clickthrough(self):

        GWL_EXSTYLE = -20

        WS_EX_TRANSPARENT = 0x20

        hwnd = ctypes.windll.user32.GetParent(

            self.root.winfo_id()

        )

        style = ctypes.windll.user32.GetWindowLongW(

            hwnd,

            GWL_EXSTYLE

        )

        style &= ~WS_EX_TRANSPARENT

        ctypes.windll.user32.SetWindowLongW(

            hwnd,

            GWL_EXSTYLE,

            style

        )

    # ----------------------------------------------------

    def set_lines(

        self,

        previous,

        current,

        next_line

    ):

        self.previous.config(

            text=previous

        )

        self.previous_shadow.config(

            text=previous

        )

        self.current.config(

            text=current

        )

        self.current_shadow.config(

            text=current

        )

        self.next.config(

            text=next_line

        )

        self.next_shadow.config(

            text=next_line

        )

    # ----------------------------------------------------

    def run(self):

        self.root.mainloop()

# MÉTODOS DE TECLADO
# ==========================================================

    def bind_keyboard(self):

        self.root.bind("<Escape>", self.exit_edit_mode)

        self.root.bind("<plus>", self.increase_font)

        self.root.bind("<minus>", self.decrease_font)

        self.root.bind("<Key-KP_Add>", self.increase_font)

        self.root.bind("<Key-KP_Subtract>", self.decrease_font)

        self.root.bind("<Left>", self.offset_left)

        self.root.bind("<Right>", self.offset_right)

        self.root.bind("<Up>", self.volume_up)

        self.root.bind("<Down>", self.volume_down)

        self.root.bind("<Prior>", self.previous_track)

        self.root.bind("<Next>", self.next_track)


# ==========================================================
# F12
# ==========================================================

    def toggle_edit_mode(self, event=None):

        self.edit_mode = not self.edit_mode

        if self.edit_mode:

            self.disable_clickthrough()

            self.root.configure(bg="#222222")

            self.container.configure(bg="#222222")

            self.previous.configure(bg="#222222")

            self.current.configure(bg="#222222")

            self.next.configure(bg="#222222")

            self.previous_shadow.configure(bg="#222222")

            self.current_shadow.configure(bg="#222222")

            self.next_shadow.configure(bg="#222222")

            self.edit_label.pack(

                side="bottom",

                fill="x"

            )
            self.cover_label.place(

                x=15,

                y=15

            )

            self.song_label.place(

                x=15,

                y=120

            )
            self.root.focus_force()

        else:

            self.exit_edit_mode()


# ==========================================================
# SAIR DO MODO EDIÇÃO
# ==========================================================

    def exit_edit_mode(self, event=None):

        self.edit_mode = False

        self.enable_clickthrough()

        self.root.configure(bg="black")

        self.container.configure(bg="black")

        self.previous.configure(bg="black")

        self.current.configure(bg="black")

        self.next.configure(bg="black")

        self.previous_shadow.configure(bg="black")

        self.current_shadow.configure(bg="black")

        self.next_shadow.configure(bg="black")

        self.edit_label.pack_forget()

        self.cover_label.place_forget()

        self.song_label.place_forget()


# ==========================================================
# TAMANHO DA FONTE
# ==========================================================

    def increase_font(self, event=None):

        if not self.edit_mode:
            return

        size = self.config["font_size"]

        size += 2

        self.config["font_size"] = size

        self.update_fonts()

        if self.on_font_change:

            self.on_font_change(size)


    def decrease_font(self, event=None):

        if not self.edit_mode:
            return

        size = self.config["font_size"]

        size = max(12, size - 2)

        self.config["font_size"] = size

        self.update_fonts()

        if self.on_font_change:

            self.on_font_change(size)


# ==========================================================
# OFFSET
# ==========================================================

    def offset_left(self, event=None):

        if not self.edit_mode:
            return

        self.offset -= 0.2

        if self.on_offset_change:

            self.on_offset_change(self.offset)


    def offset_right(self, event=None):

        if not self.edit_mode:
            return

        self.offset += 0.2

        if self.on_offset_change:

            self.on_offset_change(self.offset)


# ==========================================================
# VOLUME
# ==========================================================

    def volume_up(self, event=None):

        if not self.edit_mode:
            return

        if self.on_volume_up:

            self.on_volume_up()


    def volume_down(self, event=None):

        if not self.edit_mode:
            return

        if self.on_volume_down:

            self.on_volume_down()


# ==========================================================
# TROCAR MÚSICA
# ==========================================================

    def next_track(self, event=None):

        if not self.edit_mode:
            return

        if self.on_next_track:

            self.on_next_track()


    def previous_track(self, event=None):

        if not self.edit_mode:
            return

        if self.on_previous_track:

            self.on_previous_track()


# ==========================================================
# ATUALIZA FONTES
# ==========================================================

    def update_fonts(self):

        font_name = self.config["font_family"]

        size = self.config["font_size"]

        self.previous.configure(

            font=(font_name, int(size * 0.75))

        )

        self.previous_shadow.configure(

            font=(font_name, int(size * 0.75))

        )

        self.current.configure(

            font=(font_name, size, "bold")

        )

        self.current_shadow.configure(

            font=(font_name, size, "bold")

        )

        self.next.configure(

            font=(font_name, int(size * 0.75))

        )

        self.next_shadow.configure(

            font=(font_name, int(size * 0.75))

        )
# ==========================================================
# ATUALIZA AS LINHAS
# ==========================================================

    def update_display(

        self,

        previous="",

        current="",

        next_line=""

    ):

        if previous != self.previous_text:

            self.previous_text = previous

            self.previous.configure(

                text=previous

            )

            self.previous_shadow.configure(

                text=previous

            )

        if current != self.current_text:

            self.current_text = current

            self.current.configure(

                text=current

            )

            self.current_shadow.configure(

                text=current

            )

        if next_line != self.next_text:

            self.next_text = next_line

            self.next.configure(

                text=next_line

            )

            self.next_shadow.configure(

                text=next_line

            )


# ==========================================================
# ALTERA A COR DO TEMA
# ==========================================================

    def set_theme(

        self,

        color

    ):

        self.theme_color = color

        self.current.configure(

            fg=color

        )


# ==========================================================
# LIMPA AS LETRAS
# ==========================================================

    def clear_display(self):

        self.update_display(

            "",

            "",

            ""

        )


# ==========================================================
# MOSTRA PAUSADO
# ==========================================================

    def show_paused(self):

        self.update_display(

            "",

            "⏸ Pausado",

            ""

        )


# ==========================================================
# MOSTRA CARREGANDO
# ==========================================================

    def show_loading(self):

        self.update_display(

            "",

            "Carregando...",

            ""

        )


# ==========================================================
# MOSTRA SEM LETRA
# ==========================================================

    def show_no_lyrics(self):

        self.update_display(

            "",

            "Sem letra sincronizada",

            ""

        )


# ==========================================================
# REFRESH DA JANELA
# ==========================================================

    def refresh(self):

        self.root.update_idletasks()

        self.root.update()


# ==========================================================
# REDIMENSIONA
# ==========================================================

    def resize(

        self,

        width,

        height

    ):

        x = self.root.winfo_x()

        y = self.root.winfo_y()

        self.root.geometry(

            f"{width}x{height}+{x}+{y}"

        )

        self.config["window_width"] = width

        self.config["window_height"] = height


# ==========================================================
# MUDA OPACIDADE
# ==========================================================

    def set_opacity(

        self,

        value

    ):

        value = max(

            0,

            min(

                1,

                value

            )

        )

        self.root.attributes(

            "-alpha",

            value

        )

        self.config["background_opacity"] = value

# ==========================================================
# ATUALIZA POSIÇÃO DAS SOMBRAS
# ==========================================================

    def update_shadow_positions(self):

        offset = self.shadow_offset

        self.previous_shadow.place_configure(

            relx=0.5,

            y=22 + offset

        )

        self.current_shadow.place_configure(

            relx=0.5,

            y=72 + offset

        )

        self.next_shadow.place_configure(

            relx=0.5,

            y=126 + offset

        )


# ==========================================================
# HABILITA / DESABILITA SOMBRA
# ==========================================================

    def set_shadow(

        self,

        enabled

    ):

        self.shadow_enabled = enabled

        if enabled:

            self.previous_shadow.place(

                relx=0.5,

                y=24,

                anchor="n"

            )

            self.current_shadow.place(

                relx=0.5,

                y=74,

                anchor="n"

            )

            self.next_shadow.place(

                relx=0.5,

                y=128,

                anchor="n"

            )

        else:

            self.previous_shadow.place_forget()

            self.current_shadow.place_forget()

            self.next_shadow.place_forget()


# ==========================================================
# ALTERA COR PRINCIPAL
# ==========================================================

    def set_accent_color(

        self,

        color

    ):

        self.accent_color = color

        self.current.configure(

            fg=color

        )


# ==========================================================
# ALTERA COR DAS LINHAS SECUNDÁRIAS
# ==========================================================

    def set_secondary_color(

        self,

        color="#909090"

    ):

        self.previous.configure(

            fg=color

        )

        self.next.configure(

            fg=color

        )


# ==========================================================
# OPACIDADE GERAL
# ==========================================================

    def set_window_opacity(

        self,

        opacity

    ):

        opacity = max(

            0.2,

            min(

                1.0,

                opacity

            )

        )

        self.opacity = opacity

        self.root.attributes(

            "-alpha",

            opacity

        )


# ==========================================================
# MODO EDIÇÃO VISUAL
# ==========================================================

    def enable_edit_border(self):

        self.draw_border = True

        self.root.configure(

            bg="black"

        )

        self.container.configure(

            bg="black"

        )


# ==========================================================
# DESABILITA BORDA
# ==========================================================

    def disable_edit_border(self):

        self.draw_border = False


# ==========================================================
# DESENHA A BORDA
# ==========================================================

    def draw_edit_border(self):

        if not self.draw_border:

            return

        canvas = tk.Canvas(

            self.root,

            bg="black",

            highlightthickness=0,

            bd=0

        )

        canvas.place(

            x=0,

            y=0,

            relwidth=1,

            relheight=1

        )

        w = self.root.winfo_width()

        h = self.root.winfo_height()

        pad = 4

        canvas.create_rectangle(

            pad,

            pad,

            w - pad,

            h - pad,

            outline=self.accent_color,

            width=2

        )

        canvas.create_text(

            14,

            12,

            anchor="w",

            text="♪ Spotify Overlay",

            fill=self.accent_color,

            font=("Segoe UI", 9, "bold")

        )


# ==========================================================
# TEMA DINÂMICO
# ==========================================================

    def apply_dynamic_theme(

        self,

        color

    ):

        self.set_accent_color(

            color

        )

        self.edit_label.configure(

            fg=color

        )


# ==========================================================
# REFRESH VISUAL
# ==========================================================

    def redraw(self):

        if self.draw_border:
            self.draw_edit_border()

        self.refresh()


    def set_music_info(
        self,
        title,
        artist,
        cover_url=None
    ):

        self.song_label.config(
            text=f"{title}\n{artist}"
        )

        if cover_url is None:
            return

        try:

            response = requests.get(
                cover_url,
                timeout=5
            )

            image = Image.open(
                BytesIO(response.content)
            )

            image = image.resize((96, 96))

            self.cover_photo = ImageTk.PhotoImage(image)

            self.cover_label.config(
                image=self.cover_photo
            )

        except Exception:
            pass
    