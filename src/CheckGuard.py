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
 *  and then will trigger CheckParser module
 *
 *	Last revision: 05/21/2015
 *
'''


import time
import CheckParser
try:
    from watchdog.observers import Observer
    from watchdog.events import FileSystemEventHandler
except ImportError:
    print("You must have watchdog module installed")
    exit()


class NewCheckHandler(FileSystemEventHandler):
    def on_modified(self, event):
        try:
            start_pos = CheckParser.read_init_pos()
            check = CheckParser.CheckParser(start_pos)
            check.read_file()
            CheckParser.write_init_pos(check.get_file_pos())
        except Exception as e:
            print(e)

if __name__ == "__main__":
    print("Check Guard started...\nTo stop CheckGuard please hit Ctrl + C\n")
    event_handler = NewCheckHandler()
    observer = Observer()
    observer.schedule(event_handler, path="C:\\Vectron\\VPosPC", recursive=False)
    observer.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()

    observer.join()

    print("Check Guard stopped\n")
    time.sleep(1)
