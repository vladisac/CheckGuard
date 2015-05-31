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
            check_logger.debug("{}".format("----- while loop -----"))
            sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    check_logger.info("{}".format("----- Observer join -----"))
    observer.join()

    event_handler.on_end()
    sleep(1)


if __name__ == "__main__":
    main()
