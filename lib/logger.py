import colorlog, sys, os
from dotenv import load_dotenv

load_dotenv()


def createLogger(name, level=os.environ.get("WS_LOGLEVEL", "info")):
    levels = {
        "debug": colorlog.DEBUG,
        "info": colorlog.INFO,
        "warning": colorlog.WARNING,
        "error": colorlog.ERROR,
        "critical": colorlog.CRITICAL,
    }
    handler = colorlog.StreamHandler(sys.stdout)
    formatter = colorlog.ColoredFormatter(
        "%(log_color)s%(levelname)-8s%(name)-25s%(reset)s%(blue)s%(message)s",
        datefmt=None,
        reset=True,
        log_colors={
            'DEBUG': 'cyan',
            'INFO': 'green',
            'WARNING': 'yellow',
            'ERROR': 'red',
            'CRITICAL': 'red,bg_white',
        },
        secondary_log_colors={},
        style='%'
    )
    handler.setFormatter(formatter)
    logger = colorlog.getLogger(name)
    logger.addHandler(handler)
    logger.setLevel(levels[level])
    return logger
