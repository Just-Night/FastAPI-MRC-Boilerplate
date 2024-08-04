import logging
import sys
from pathlib import Path
from loguru import logger
import json
from core import Config


class InterceptHandler(logging.Handler):
    """
    A logging handler that intercepts log messages and forwards them to Loguru.
    """
    loglevel_mapping = {
        logging.CRITICAL: 'CRITICAL',
        logging.ERROR: 'ERROR',
        logging.WARNING: 'WARNING',
        logging.INFO: 'INFO',
        logging.DEBUG: 'DEBUG',
        logging.NOTSET: 'NOTSET',
    }

    def emit(self, record):
        level = self.loglevel_mapping.get(record.levelno, 'INFO')

        frame, depth = logging.currentframe(), 2
        while frame and frame.f_code.co_filename == logging.__file__:
            frame = frame.f_back
            depth += 1

        log = logger.bind(request_id='app')
        log.opt(depth=depth, exception=record.exc_info).log(level, record.getMessage())


class CustomizeLogger:
    """
    A class to customize and configure Loguru logging with configuration file.
    """

    @classmethod
    def make_logger(cls, config_path: Path):
        """
        Create and configure the logger using the provided configuration file.
        """
        config = cls.load_logging_config(config_path)
        logging_config = config.get('logger')

        return cls.customize_logging(
            filepath=logging_config.get('path'),
            level=Config.LOG_LEVEL,
            retention=logging_config.get('retention'),
            rotation=logging_config.get('rotation'),
            format=logging_config.get('format')
        )

    @classmethod
    def customize_logging(cls, filepath: Path, level: str, rotation: str, retention: str, format: str):
        """
        Customize logging settings for Loguru.
        """
        # Remove all handlers associated with the root logger.
        logging.getLogger().handlers = []

        logger.remove()

        # Filter out logs below the set level
        def filter_logs(record):
            return record["level"].name >= level.upper()

        logger.add(
            sys.stdout,
            enqueue=True,
            backtrace=True,
            level=level.upper(),
            format=format,
            filter=filter_logs
        )
        logger.add(
            str(filepath),
            rotation=rotation,
            retention=retention,
            enqueue=True,
            backtrace=True,
            level=level.upper(),
            format=format,
            filter=filter_logs
        )

        # Set InterceptHandler as the only handler for the root logger.
        logging.basicConfig(handlers=[InterceptHandler()], level=logging.NOTSET)

        # Configure uvicorn and fastapi loggers to use InterceptHandler and set levels
        # uvicorn & uvicorn.error logs are set to INFO level, while fastapi logs are set to ERROR level.
        for log_name in ['uvicorn.access', 'fastapi']:
            log = logging.getLogger(log_name)
            log.handlers = [InterceptHandler()]
            log.propagate = False
            if level.upper() in ["INFO", "DEBUG"]:
                log.setLevel(logging.INFO)
            else:
                log.setLevel(logging.ERROR)

        return logger.bind(request_id=None, method=None)

    @staticmethod
    def load_logging_config(config_path: Path):
        """
        Load logging configuration from a JSON file.
        """
        with open(config_path, 'r') as config_file:
            return json.load(config_file)
