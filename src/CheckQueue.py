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
 *	Filename: CheckQueue.py
 *	Queue module that keeps all checks prepared for printing
 *
 *	Last revision: 07/02/2015
 *
'''

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
