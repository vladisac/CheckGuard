__author__ = 'nero_luci'


import time
import CheckParser
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler, FileModifiedEvent


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
    print("Check Guard started...\n")
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