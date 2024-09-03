import logging


class Logger:
	def __init__(self, name: str, level: int = logging.INFO, log_file: str = None):
		"""
		Initializes a logger instance with the specified name, level, and optional log file.

		:param name: Name of the logger.
		:param level: Logging level (default is logging.INFO).
		:param log_file: Optional path to a log file. If provided, logs will be written to the file.
		"""
		self.logger = logging.getLogger(name)
		self.logger.setLevel(level)
		formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')

		# Console handler
		console_handler = logging.StreamHandler()
		console_handler.setFormatter(formatter)
		self.logger.addHandler(console_handler)

		# File handler (optional)
		if log_file:
			file_handler = logging.FileHandler(log_file)
			file_handler.setFormatter(formatter)
			self.logger.addHandler(file_handler)

	def info(self, message: str):
		self.logger.info(message)

	def warn(self, message: str):
		self.logger.warning(message)

	def error(self, message: str):
		self.logger.error(message)

	def debug(self, message: str):
		self.logger.debug(message)
