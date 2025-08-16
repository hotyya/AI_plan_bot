import logging
import os
import sys
from pathlib import Path
from abc import ABC, abstractmethod
from logging.handlers import RotatingFileHandler
from utils.creds import LOGS_PATH


class AbstractHandler(ABC):
    @abstractmethod
    def add(self, logger: logging.Logger) -> None:
        pass


class ConsoleHandler(AbstractHandler):
    def __init__(self, level=logging.DEBUG) -> None:
        self.level = level

    def add(self, logger: logging.Logger) -> None:
        handler = logging.StreamHandler(sys.stdout)
        handler.setLevel(self.level)

        formatter = logging.Formatter(
            fmt="%(asctime)s | %(name)s | %(levelname)s | %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S"
        )

        handler.setFormatter(formatter)
        logger.addHandler(handler)


class FileHandler(AbstractHandler):
    def __init__(
        self,
        filename: str,
        level=logging.DEBUG,
        max_bytes=10 * 1024 * 1024,
        backup_count=5,
    ) -> None:
        self.filename = filename
        self.level = level
        self.max_bytes = max_bytes
        self.backup_count = backup_count

    def add(self, logger: logging.Logger) -> None:
        logs_path: Path = LOGS_PATH

        handler = RotatingFileHandler(
            os.path.join(logs_path, self.filename),
            maxBytes=self.max_bytes,
            backupCount=self.backup_count,
            encoding="utf-8",
        )

        handler.setLevel(self.level)
        formatter = logging.Formatter(
            fmt="%(asctime)s | %(name)s | %(levelname)s | %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
        )
        handler.setFormatter(formatter)

        logger.addHandler(handler)
