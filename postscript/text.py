import typing

from .geometry import cm_to_units, moveto, lineto, stroke, \
                      closepath, setlinewidth, fill, line, \
                      rect, square

from .misc import DEBUG_info, PS_CMD

@DEBUG_info
def set_font(font_name: str = '/Liberation-Serif',
             size: float = 11) -> PS_CMD:
    return f'{font_name} findfont {size} scalefont setfont'
