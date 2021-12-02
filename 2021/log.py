import logging
from rich.logging import RichHandler


logging.basicConfig(
    level=logging.INFO,
    format='{levelname}: {message}',
    style='{', handlers=[RichHandler(
        rich_tracebacks = True,
        show_time = False,
    )]
)

log = logging.getLogger('Advent of Code')
