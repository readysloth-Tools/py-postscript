import typing as t

from .misc import PS_CMD, DEBUG_info


def cm_to_units(value: float) -> float:
    """
    Преобразование сантиметров в юниты
    PostScript, которые равны 1/72 дюйма
    """
    # В 1 сантиметре 0.394 дюйма
    if type(value) not in (float, int):
        return value
    return (value * 0.394) / (1/72)

@DEBUG_info
def translate(x: float, y: float) -> PS_CMD:
    """
    Перемещает центр координат на заданные координаты.
    Чаще всего требуется вместе с rotate
    """
    return f'{cm_to_units(x)} {cm_to_units(y)} translate'


@DEBUG_info
def rotate(angle: float) -> PS_CMD:
    """
    Поворачивает координатные оси против часовой стрелки
    на заданный угол
    """
    return f'{angle} rotate'


def generic_relative(x: float,
                     y: float,
                     cmd: str,
                     absolute: bool = True) -> PS_CMD:
    """
    Общая функция для создания "относительных" команд
    """
    prefix = 'r' if not absolute else ''
    return f'{cm_to_units(x)} {cm_to_units(y)} {prefix}{cmd}'

@DEBUG_info
def moveto(x: float,
           y: float,
           absolute: bool = True) -> PS_CMD:
    """
    Перемещает перо на заданные координаты
    """
    return generic_relative(x, y, 'moveto', absolute)


@DEBUG_info
def lineto(x: float,
           y: float,
           absolute: bool = True) -> PS_CMD:
    """
    Создает линию из текущих координат пера до
    заданных x и y
    """
    return generic_relative(x, y, 'lineto', absolute)


@DEBUG_info
def stroke(save_context: bool = False) -> PS_CMD:
    """
    Проявляет линии. Если аргумент save_context истиннен,
    то сохраняет текущий контекст (например, чтобы фигуру
    можно было залить и обвести)
    """
    if save_context:
        return 'gsave stroke grestore'
    return 'stroke'


@DEBUG_info
def closepath() -> PS_CMD:
    """
    Корректно дорисовывает путь до его начала
    """
    return 'closepath'


@DEBUG_info
def setlinewidth(width: float) -> PS_CMD:
    """
    Задает толщину линий
    """
    return f'{cm_to_units(width)} setlinewidth'


@DEBUG_info
def setgray(value: float) -> PS_CMD:
    return f'{value} setgray'


@DEBUG_info
def fill(value: float,
         grey: bool = True,
         restore: bool = True) -> PS_CMD:
    """
    Заливает фигуру оттенками серого, где значения
    более близкие к 1.0 светлее, а к 0 темнее.
    Переменная restore по-умолчанию восстанавливает
    заливку в значение 0
    """
    if grey:
        return '\n'.join((setgray(value),
                          'fill',
                          setgray(0) if restore else ''))
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
    """
    Создает линию на документе
    """
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
         fill_value: float = 0,
         absolute: bool = True) -> PS_CMD:
    """
    Создает прямоугольник на документе
    """
    save_context = fill_value != 0
    return '\n'.join((moveto(x, y, absolute),
                      lineto(0, height, absolute=False),
                      lineto(width, 0,  absolute=False),
                      lineto(0, -height,absolute=False),
                      closepath(),
                      setlinewidth(line_width),
                      stroke(save_context),
                      fill(fill_value)))


@DEBUG_info
def square(x: float,
           y: float,
           edge: float,
           line_width: float = 0.1,
           fill_value: float = 0,
           absolute: bool = True) -> PS_CMD:
    """
    Создает квадрат на документе
    """
    return rect(x, y, edge, edge, line_width, fill_value, absolute)
