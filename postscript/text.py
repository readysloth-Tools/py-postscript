import typing

from .geometry import cm_to_units, moveto, lineto, stroke, \
                      closepath, setlinewidth, fill, line, \
                      rect, square

from .misc import DEBUG_info, PS_CMD


class Text:
    def __init__(self,
                 x: float,
                 y: float,
                 font: str,
                 size: float,
                 content: str):
         self.x = x
         self.y = y
         self.font = font
         self.size = size
         self.content = content


@DEBUG_info
def setfont(font_name: str = '/LiberationSerif',
            size: float = 11) -> PS_CMD:
    return f'{font_name} findfont {size} scalefont setfont'


def text(txt: Text,
         absolute: bool = True) -> PS_CMD:
    return '\n'.join((setfont(txt.font, txt.size),
                      moveto(txt.x, txt.y, absolute),
                      f'({txt.content})',
                      'show'))


def text_in_cell(x: float,
                 y: float,
                 width: float,
                 heigth: float,
                 txt: Text,
                 line_width: float = 0.1,
                 fill_value: float = 0,
                 absolute: bool = True) -> PS_CMD:
    return '\n'.join((rect(x, y, width, heigth,
                           line_width, fill_value, absolute),
                      text(txt, absolute)))
