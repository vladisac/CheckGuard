from time import sleep
from Queue import Queue
from threading import Thread
from CheckLogger import check_logger

check_queue = Queue()


def run_queue_threads(num_threads=1):
    for _ in range(num_threads):
        thread = Thread(target=queue_worker)
        thread.daemon = True
        check_logger.info("{}".format("----- Queue thread starting -----"))
        thread.start()
        thread.join()
        check_logger.info("{}".format("----- Queue thread joined -----"))


def queue_worker():
    from CheckParser import CheckParser
    check_logger.info("{}".format("----- Queue worker -----"))
    while not check_queue.empty():
        check = check_queue.get()
        check_logger.info("Unqueue: {}".format(check))
        CheckParser.write_2_file(check)
        sleep(0.5)
        CheckParser.execute_batch_file()
        sleep(0.5)
        check_queue.task_done()
        check_logger.info("{}".format("Task done"))


check_queue.join()
