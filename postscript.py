import typing as t
import itertools as it
import functools as ft

PS_CMD = str
DEBUG = False

def DEBUG_info(function: t.Callable) -> t.Callable:
    def wrapper(*args, **kwargs) -> PS_CMD:
        dbg_info = f'% {function.__name__}({args}, {kwargs})\n\t'
        return (dbg_info if DEBUG else '') + function(*args, **kwargs)
    return wrapper


def cm_to_units(value: float) -> float:
    """
    Преобразование сантиметров в юниты
    PostScript, которые равны 1/72 дюйма
    """
    # В 1 сантиметре 0.394 дюйма
    return (value * 0.394) / (1/72)


def generic_relative(x: float,
                     y: float,
                     cmd: str,
                     absolute: bool = True):
    prefix = 'r' if not absolute else ''
    return f'{cm_to_units(x)} {cm_to_units(y)} {prefix}{cmd}'

@DEBUG_info
def moveto(x: float,
           y: float,
           absolute: bool = True) -> PS_CMD:
    return generic_relative(x, y, 'moveto', absolute)


@DEBUG_info
def lineto(x: float,
           y: float,
           absolute: bool = True) -> PS_CMD:
    return generic_relative(x, y, 'lineto', absolute)


@DEBUG_info
def stroke(save_context: bool = False) -> PS_CMD:
    if save_context:
        return 'gsave stroke grestore'
    return 'stroke'


@DEBUG_info
def closepath() -> PS_CMD:
    return 'closepath'


@DEBUG_info
def setlinewidth(width: float) -> PS_CMD:
    return f'{cm_to_units(width)} setlinewidth'


@DEBUG_info
def fill(value: float,
         grey: bool = True) -> PS_CMD:
    if grey:
        return '\n'.join((f'{value} setgray', 'fill'))
    # WIP
    return ''


@DEBUG_info
def line(x1: float,
         y1: float,
         x2: float,
         y2: float,
         width: float = 0.1,
         stroke: bool = True,
         absolute: bool = True) -> PS_CMD:
    return '\n'.join(('newpath',
                    moveto(x1, y1, absolute),
                    lineto(x2, y2, absolute),
                    setlinewidth(width),
                    stroke() if stroke else ''))


@DEBUG_info
def rect(x: float,
         y: float,
         width: float,
         height: float,
         line_width: float = 0.1,
         fill: float = 0,
         absolute: bool = True) -> PS_CMD:
    save_context = fill != 0
    return '\n'.join((moveto(x, y, absolute),
                      lineto(0, height, absolute=False),
                      lineto(width, 0,  absolute=False),
                      lineto(0, -height,absolute=False),
                      closepath(),
                      stroke(save_context)))


@DEBUG_info
def square(x: float,
           y: float,
           edge: float,
           line_width: float = 0.1,
           absolute: bool = True) -> PS_CMD:
    return rect(x, y, edge, edge, line_width, absolute)
