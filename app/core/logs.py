from loguru import logger


def add_debug_file_log() -> None:
    logger.add('logs/debug.log', rotation='1500mb', level='DEBUG')


def add_info_file_log() -> None:
    logger.add('logs/info.log', rotation='500mb', level='INFO')
