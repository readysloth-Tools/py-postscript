import typing as t


PS_CMD = str
DEBUG = False


def DEBUG_info(function: t.Callable) -> t.Callable:
    """
    Декоратор для вывода дебажной информации
    """
    def wrapper(*args, **kwargs) -> PS_CMD:
        dbg_info = f'% {function.__name__}({args}, {kwargs})\n\t'
        return (dbg_info if DEBUG else '') + function(*args, **kwargs)
    return wrapper


@DEBUG_info
def times(times: int,
          cmd: t.Callable[..., PS_CMD],
          *args, **kwargs) -> PS_CMD:
    """
    Дублирует команду times раз
    """
    return cmd(*args, **kwargs) * times


@DEBUG_info
def for_loop(start: float,
             step: float,
             end: float,
             cmd: t.Callable[..., PS_CMD],
             index: t.Dict[str, t.Any],
             **kwargs) -> PS_CMD:
    """
    Создает нативный for-цикл, в котором cmd -- функция
    данного API, а index -- словарь с аргументами для cmd,
    в котором аргументы, необходимые для итерирования указываются
    как ключи, а их значениями являются PostScript выражения,
    используюЩие неявную переменную index. В kwargs помещаются
    аргументы для cmd, независящие от цикла

    Пример:
    print(postscript.for_loop(0, 1, 10,
                              postscript.square,
                              {'x' : 'index 10 mul',
                              'fill_value' : '1 index 10 div sub',
                              'line_width': 'index 2 mul' },
                              y=10,
                              edge=10)

    Напечатает в документе 10 чернеющих квадратов,
    которые сдвигаются вправо и у которых увеличивается
    размер обводки
    """
    if index is not None:
        kwargs = {**kwargs, **index}
    return f'{start} {step} {end} {{ /index exch def {cmd(**kwargs)} }} for'
