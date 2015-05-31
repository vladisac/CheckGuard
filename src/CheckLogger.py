'''
 *  Copyright (C) 2015 Touch Vectron
 *
 *  Author: Cornel Punga
 *
 *  This program is free software; you can redistribute it and/or modify
 *  it under the terms of the GNU General Public License version 2 as
 *  published by the Free Software Foundation.
 *
 *  This program is distributed in the hope that it will be useful,
 *  but WITHOUT ANY WARRANTY; without even the implied warranty of
 *  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 *  GNU General Public License for more details.
 *
 *  You should have received a copy of the GNU General Public License
 *  along with this program; if not, write to the Free Software
 *  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
 *  MA 02110-1301, USA.
 *
 *	Filename: CheckLogger.py
 *	Loggind module
 *
 *
 *	Last revision: 05/31/2015
 *
'''

from logging import Logger, FileHandler, Formatter

class CheckLogger(Logger):
    def __init__(self):
        super(CheckLogger, self).__init__(name="CheckLogger", level="DEBUG")
        self.file_handler = FileHandler("{0}\{1}.log".format(r"C:\Listener", r"cg_error"))
        self.log_formatter = Formatter("%(asctime)s [%(threadName)-12.12s] [%(levelname)-5.5s]  %(message)s")
        self.file_handler.setFormatter(self.log_formatter)
        self.addHandler(self.file_handler)


check_logger = CheckLogger()