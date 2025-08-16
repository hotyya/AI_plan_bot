from __future__ import annotations
import logging
from utils.logger.handlers import AbstractHandler, ConsoleHandler, FileHandler

HANDLER_REGISTRY = {
    "console": ConsoleHandler,
    "file": FileHandler,
}


class BaseLoggerBuilder:
    """
    A logger builder that allows flexible composition of logging handlers.

    Usage:
        builder = BaseLoggerBuilder("my_logger")
        builder.add(SomeHandler()).add(AnotherHandler())
        logger = builder.build()

    Handlers must inherit from `AbstractHandler` and implement the `.add(logger)` method.
    """

    def __init__(self, name: str, level=logging.DEBUG) -> None:
        self.logger = logging.getLogger(name)
        self.logger.setLevel(level)
        self.logger.handlers.clear()

    def add(self, handler: str | AbstractHandler, **kwargs) -> BaseLoggerBuilder:
        if isinstance(handler, str):
            handler_cls = HANDLER_REGISTRY.get(handler)
            if handler_cls is None:
                raise ValueError(f"Unknown handler: {handler}")
            handler = handler_cls(**kwargs)

        handler.add(self.logger)
        return self

    def build(self) -> logging.Logger:
        return self.logger
