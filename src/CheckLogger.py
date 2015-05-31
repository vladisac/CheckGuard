from logging import Logger, FileHandler, Formatter

class CheckLogger(Logger):
    def __init__(self):
        super(CheckLogger, self).__init__(name="CheckLogger", level="DEBUG")
        self.file_handler = FileHandler("{0}\{1}.log".format(r"C:\Listener", r"cg_error"))
        self.log_formatter = Formatter("%(asctime)s [%(threadName)-12.12s] [%(levelname)-5.5s]  %(message)s")
        self.file_handler.setFormatter(self.log_formatter)
        self.addHandler(self.file_handler)


check_logger = CheckLogger()