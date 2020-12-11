import typing as t


PS_CMD = str
DEBUG = False


def DEBUG_info(function: t.Callable) -> t.Callable:
    def wrapper(*args, **kwargs) -> PS_CMD:
        dbg_info = f'% {function.__name__}({args}, {kwargs})\n\t'
        return (dbg_info if DEBUG else '') + function(*args, **kwargs)
    return wrapper


@DEBUG_info
def times(times: int,
          cmd: t.Callable[..., PS_CMD],
          *args, **kwargs) -> PS_CMD:
    return cmd(*args, **kwargs) * times


@DEBUG_info
def for_loop(start: float,
             step: float,
             end: float,
             cmd: t.Callable[..., PS_CMD],
             index: t.Dict[str, t.Any],
             **kwargs) -> PS_CMD:
    if index is not None:
        kwargs = {**kwargs, **index}
    return f'{start} {step} {end} {{ /index exch def {cmd(**kwargs)} }} for'
