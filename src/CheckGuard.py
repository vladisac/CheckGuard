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
 *	Last revision: 05/31/2015
 *
'''

import CheckParser
from CheckLogger import check_logger
try:
    from watchdog.observers import Observer
    from watchdog.events import PatternMatchingEventHandler
except ImportError:
    print("You must have watchdog module installed")
    exit()


class NewCheckHandler(PatternMatchingEventHandler):
    def __init__(self):
        super(NewCheckHandler, self).__init__(patterns=[r'C:\Vectron\VPosPC\files.txt'])
        self.start_message = "Copyright (C) 2015 Touch Vectron\n" \
                             "Check Guard version 0.1.1\n" \
                             "Check Guard started...\n" \
                             "To stop CheckGuard please hit Ctrl + C\n"
        self.end_message = "Check Guard stopped\n"
        self.user_err_msg = "*************************************\n" \
                            "**  Eroare la tiparirea bonului    **\n" \
                            "*************************************\n"
        self.bad_input = "Ai introdus informatie gresita!!!"
        self.reprint = "Exista bonuri neprintate\n" \
                       "Vrei sa le printez? Y/N"

    def on_start(self):
        print(self.start_message)

        pos_txt = CheckParser.read_init_pos()
        end_pos = CheckParser.get_file_end_pos()

        if (end_pos - pos_txt) > 0:
            print(self.reprint)
            user_ans = raw_input()
            try:
                assert isinstance(user_ans, str), "Bad user input"
            except AssertionError as e:
                check_logger.debug("{0}: {1}".format(e, user_ans))
                print(self.bad_input)

            if user_ans == 'Y' or user_ans == 'y':
                try:
                    check = CheckParser.CheckParser(pos_txt)
                    check.read_file()
                    CheckParser.write_init_pos(end_pos)
                except Exception as e:
                    print(self.user_err_msg)
                    check_logger.debug(e)
            else:
                CheckParser.write_init_pos(end_pos)
                print("Bonurile existente au fost omise")
                print("Omitere -> Status: OK")

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
            check_logger.debug(e)