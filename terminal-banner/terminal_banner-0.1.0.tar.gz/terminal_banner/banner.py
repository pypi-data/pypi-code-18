import subprocess
import terminal_banner as tb


class Banner:
    def __init__(self, text):
        self.border_char = "*"
        self.text = text
        self.width = None
        self.text_box = None

    def __str__(self):
        self._reset_width()
        return self._banner_string()

    def _banner_string(self):
        output_string = self.border_char * self.width + "\n"
        for text_line in self.text_box:
            output_string += self.border_char + " " + text_line + " " + self.border_char + "\n"
        output_string += self.border_char * self.width
        return output_string

    def _reset_width(self):
        self.width = get_terminal_width()
        self.text_box = tb.TextBox(self.text, self.width - 4)


def get_terminal_width():
    return int(subprocess.check_output(['stty', 'size']).split()[1])
