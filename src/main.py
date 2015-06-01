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
 *	Filename: main.py
 *	Main module, handles shell arguments, watchdog observer and CheckGuard instance
 *
 *
 *	Last revision: 05/31/2015
 *
'''

from time import sleep
from argparse import ArgumentParser
from CheckGuard import *


def main():
    parser = ArgumentParser(description="CheckGuard command line argument parser")
    parser.add_argument('--log', help="level of logging", default=None, type=str)
    arg_level = parser.parse_args()
    if arg_level.log:
        check_logger.disabled = False
    else:
        check_logger.disabled = True

    check_logger.info("{}".format("----- Program start -----"))
    event_handler = NewCheckHandler()
    event_handler.on_start()
    observer = Observer()
    observer.schedule(event_handler, path=r"C:\Vectron\VPosPC", recursive=False)
    observer.start()
    check_logger.info("{}".format("----- Observer start -----"))
    try:
        while True:
            sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    check_logger.info("{}".format("----- Observer join -----"))
    observer.join()

    event_handler.on_end()
    sleep(1)


if __name__ == "__main__":
    main()
