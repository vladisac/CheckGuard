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
 *	Filename: CheckGuard.py
 *	This module will monitor files.txt for changes(for new checks)
 *      and then will trigger CheckParser module
 *
 *	Last revision: 05/21/2015
 *
'''


import time
import CheckParser
import logging
import argparse
try:
    from watchdog.observers import Observer
    from watchdog.events import FileSystemEventHandler
except ImportError:
    print("You must have watchdog module installed")
    exit()


class NewCheckHandler(FileSystemEventHandler):
    def __init__(self):
        self.start_message = "Copyright (C) 2015 Touch Vectron\n" \
                             "Check Guard version 0.1.1\n" \
                             "Check Guard started...\n" \
                             "To stop CheckGuard please hit Ctrl + C\n"
        self.end_message = "Check Guard stopped\n"
        self.user_err_msg = "*************************************\n" \
                            "**  Eroare la retiparirea bonului  **\n" \
                            "*************************************\n"

    def on_start(self):
        print(self.start_message)

        pos_txt = CheckParser.read_init_pos()
        end_pos = CheckParser.get_file_end_pos()

        if (end_pos - pos_txt) > 0:
            print("Exista bonuri neprintate")
            print("Vrei sa le printez? Y/N")
            user_ans = raw_input()
            try:
                assert isinstance(user_ans, str), "Bad user input"
            except AssertionError as e:
                logger.debug("{0}: {1}".format(e, user_ans))

            if user_ans == 'Y' or user_ans == 'y':
                try:
                    check = CheckParser.CheckParser(pos_txt)
                    check.read_file()
                    CheckParser.write_init_pos(end_pos)
                except Exception as e:
                    print(self.user_err_msg)
                    logger.debug(e)
            else:
                CheckParser.write_init_pos(end_pos)

    def on_end(self):
        print(self.end_message)

    def on_modified(self, event):
        try:
            start_pos = CheckParser.read_init_pos()
            check = CheckParser.CheckParser(start_pos)
            check.read_file()
            CheckParser.write_init_pos(check.position)
        except Exception as e:
            print(self.user_err_msg)
            logger.debug(e)

if __name__ == "__main__":
    # Command line arguments
    parser = argparse.ArgumentParser(description="CheckGuard command line argument parser")
    parser.add_argument('--log', help="level of logging", default="DEBUG", type=str)
    arg_level = parser.parse_args()
    # Setup for logger
    log_level = getattr(logging, arg_level.log.upper(), None)
    logger = logging.getLogger()
    logger.setLevel(level=log_level)
    file_handler = logging.FileHandler("{0}\{1}.log".format(r"C:\Listener", r"cg_error"))
    log_formatter = logging.Formatter("%(asctime)s [%(threadName)-12.12s] [%(levelname)-5.5s]  %(message)s")
    file_handler.setFormatter(log_formatter)
    logger.addHandler(file_handler)

    event_handler = NewCheckHandler()
    event_handler.on_start()
    observer = Observer()
    observer.schedule(event_handler, path=r"C:\Vectron\VPosPC", recursive=False)
    observer.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()

    observer.join()

    event_handler.on_end()
    time.sleep(1)
