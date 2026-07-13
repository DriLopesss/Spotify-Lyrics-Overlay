"""
lyrics_manager.py

Gerencia sincronização das letras.
Não faz download das letras.
Recebe apenas o conteúdo do arquivo LRC.
"""

import re

from streamlit import progress


class LyricsManager:

    def __init__(self):

        self.lyrics = []

        self.current_index = 0

        self.offset = 0.0

    # ---------------------------------------------

    def clear(self):

        self.lyrics = []

    # ---------------------------------------------

    def set_offset(self, seconds):

        self.offset = seconds

    # ---------------------------------------------

    def load_lrc(self, lrc_text):

        self.lyrics = []

        pattern = r"\[(\d+):(\d+\.\d+)\](.*)"

        for line in lrc_text.splitlines():

            match = re.match(pattern, line)

            if not match:
                continue

            minute = int(match.group(1))

            second = float(match.group(2))

            text = match.group(3).strip()

            timestamp = minute * 60 + second

            self.lyrics.append(

                (timestamp, text)

            )

        self.lyrics.sort(key=lambda x: x[0]) 

        # Reinicia o cursor 
        self.current_index = 0

    # ---------------------------------------------

    def has_lyrics(self):

        return len(self.lyrics) > 0

    # ---------------------------------------------

    def get_lines(self, progress):

        self.update_progress(progress)

        return self.get_current_lines()

    # ---------------------------------------------

    def get_current_index(self, progress):

        progress += self.offset

        current = 0

        for i in range(len(self.lyrics)):

            if progress >= self.lyrics[i][0]:

                current = i

            else:

                break

        return current

    # ---------------------------------------------

    def time_until_next_line(self, progress):

        if len(self.lyrics) == 0:

            return None

        progress += self.offset

        index = self.get_current_index(progress)

        if index >= len(self.lyrics) - 1:

            return None

        next_time = self.lyrics[

            index + 1

        ][0]

        return max(

            0,

            next_time - progress

        )

    # ---------------------------------------------

    def get_progress_between_lines(

        self,

        progress

    ):

        if len(self.lyrics) == 0:

            return 0

        progress += self.offset

        index = self.get_current_index(

            progress

        )

        if index >= len(self.lyrics) - 1:

            return 1

        start = self.lyrics[index][0]

        end = self.lyrics[

            index + 1

        ][0]

        if end == start:

            return 1

        return (

            progress - start

        ) / (

            end - start

        )

    # ---------------------------------------------

    def get_all(self):

        return self.lyrics

    def update_progress(self, progress):

        if not self.lyrics:
            return

        progress += self.offset

        while (
            self.current_index < len(self.lyrics)-1
         and
         progress >= self.lyrics[self.current_index + 1][0]
        ):
            self.current_index += 1

        while (
            self.current_index > 0
        and
            progress < self.lyrics[self.current_index][0]
        ):
            self.current_index -= 1

    def get_current_lines(self):

        if not self.lyrics:

            return "", "Sem letra", ""

        previous = ""

        current = self.lyrics[
            self.current_index
        ][1]

        next_line = ""

        if self.current_index > 0:

            previous = self.lyrics[
                self.current_index-1
            ][1]

        if self.current_index < len(self.lyrics)-1:

            next_line = self.lyrics[
                self.current_index+1
            ][1]

        return (

            previous,

            current,

            next_line

        )