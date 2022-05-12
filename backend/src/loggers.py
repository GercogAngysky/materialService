import logging


_format = '%(asctime)s - %(levelname)s:  %(name)s.%(message)s'
_datefmt='%Y-%m-%d %H:%M:%S'
_filename='./materials.log'


def _get_file_handler():
    file_handler = logging.FileHandler(_filename)
    file_handler.setLevel(logging.WARNING)
    file_handler.setFormatter(
        logging.Formatter(
            fmt=_format,
            datefmt=_datefmt
        )
    )
    return file_handler


def _get_stream_handler():
    stream_handler = logging.StreamHandler()
    stream_handler.setLevel(logging.INFO)
    stream_handler.setFormatter(
        logging.Formatter(
            fmt=_format,
            datefmt=_datefmt
        )
    )
    return stream_handler


def get_logger(name):
    logger = logging.getLogger(name)
    logger.setLevel(logging.ERROR)
    logger.addHandler(_get_file_handler())
    logger.addHandler(_get_stream_handler())
    return logger
