from .logger import BaseLoggerBuilder
from .handlers import ConsoleHandler, FileHandler

logger_builder = BaseLoggerBuilder(name='bot_logger')
logger_builder.add(ConsoleHandler()).add(FileHandler(filename='bot_log'))
bot_logger = logger_builder.build()