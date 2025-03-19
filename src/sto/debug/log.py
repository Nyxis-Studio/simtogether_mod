import logging
import os
import sys
import traceback
from datetime import datetime
from typing import Optional
import inspect

from sto.core.singleton import SingletonMeta
from sto.utils.directory import get_sims_documents_directory


class Logger(metaclass=SingletonMeta):
    def __init__(self, log_dir: str = "logs", log_level: int = logging.DEBUG) -> None:
        """
        Initialize the Logger instance with multiple log files and production mode.

        Args:
            log_dir (str): Directory to save log files.
            log_level (int): The logging level to use.
        """
        self.log_dir = f"{get_sims_documents_directory()}/{log_dir}"
        self.log_level = log_level
        self.logger = logging.getLogger("SimtogetherLogger")
        self.logger.setLevel(self.log_level)
        self._setup_handlers()

    def _setup_handlers(self) -> None:
        """
        Setup multiple file handlers and a console handler.
        """
        if not os.path.exists(self.log_dir):
            os.makedirs(self.log_dir)

        log_filename = datetime.now().strftime("%Y-%m-%d_%H-%M-%S") + ".log"
        file_path = os.path.join(self.log_dir, log_filename)

        # File handler
        file_handler = logging.FileHandler(file_path)
        file_handler.setLevel(self.log_level)

        # Console handler
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(self.log_level)

        formatter = logging.Formatter(
            "[%(asctime)s] [%(levelname)s] [%(caller)s] %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
        )
        file_handler.setFormatter(formatter)
        console_handler.setFormatter(formatter)

        self.logger.addHandler(file_handler)
        self.logger.addHandler(console_handler)

    def _inject_caller(self, record: logging.LogRecord) -> None:
        """
        Inject caller information (file, line, function) into the log record.
        """
        frame = inspect.stack()[7]
        module = os.path.basename(frame.filename)
        record.caller = f"{module}:{frame.lineno} - {frame.function}()"

    def info(self, message: str) -> None:
        """Log an info level message."""
        self._log_with_caller(self.logger.info, message)

    def debug(self, message: str) -> None:
        """Log a debug level message."""
        self._log_with_caller(self.logger.debug, message)

    def warning(self, message: str) -> None:
        """Log a warning level message."""
        self._log_with_caller(self.logger.warning, message)

    def error(self, message: str, exc: Optional[Exception] = None) -> None:
        """
        Log an error level message, including stacktrace if exception is provided.

        Args:
            message (str): The message to log.
            exc (Optional[Exception]): The exception to log (optional).
        """
        msg = f"{message}\n{traceback.format_exc()}" if exc else message
        self._log_with_caller(self.logger.error, msg)

    def critical(self, message: str, exc: Optional[Exception] = None) -> None:
        """
        Log a critical level message, including stacktrace if exception is provided.

        Args:
            message (str): The message to log.
            exc (Optional[Exception]): The exception to log (optional).
        """
        msg = f"{message}\n{traceback.format_exc()}" if exc else message
        self._log_with_caller(self.logger.critical, msg)

    def _log_with_caller(self, log_func, message: str) -> None:
        """
        Injects the caller into the record and calls the logger function.
        """
        extra = {}
        record_factory = logging.getLogRecordFactory()

        def record_injector(*args, **kwargs):
            record = record_factory(*args, **kwargs)
            self._inject_caller(record)
            return record

        logging.setLogRecordFactory(record_injector)
        log_func(message, extra=extra)
        logging.setLogRecordFactory(record_factory)
