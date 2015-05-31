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
 *	Filename: CheckParser.py
 *	This module will parse files.txt (this is where the check from POS is written)
 *      and then will output related information to bon.txt (file from where the printer
 *      reads the check)
 *
 *	Last revision: 05/31/2015
 *
'''

from datetime import datetime
from codecs import open as copen
from re import search, sub
from inspect import stack
from subprocess import Popen
from CheckLogger import check_logger


class CheckParser(object):
    def __init__(self, position, filename=None):
        self.check_data = []
        self.position = position
        self.filename = filename

    @property
    def position(self):
        return self._position

    @position.setter
    def position(self, value):
        if value is not None:
            if value >= 0:
                self._position = value
            else:
                raise ValueError("Initial position must be a natural number")

    @property
    def filename(self):
        return self._filename

    @filename.setter
    def filename(self, value):
        if value is not None:
            self._filename = value
        else:
            self._filename = r"C:\Vectron\VPosPC\files.txt"

    def read_file(self):
        check_logger.debug("{0}: {1}".format(stack()[0][3], "_____START_____"))
        with copen(self.filename, "r", encoding="latin-1") as fh:
            fh.seek(self.position)
            line = fh.readline()
            include = False
            while line:
                if search("\*{2,}", line):
                    if not include:
                        include = True
                        line = fh.readline()
                        if search("\*{2,}", line):
                            include = False
                    else:
                        include = False
                if include:
                    self.check_data.append(line)
                if "= Cut =" in line and self.check_data != []:
                    check_logger.debug("{0}: {1}".format(stack()[0][3], self.check_data))
                    self.generate_new_check()
                    self.check_data = []
                line = fh.readline()
            self.position = fh.tell()
            check_logger.debug("{0}: {1}".format(stack()[0][3], "_____END_____"))

    @staticmethod
    def write_2_file(to_print):
        header_line = "KARAT\n"
        footer_line = "T0000010000 TOTAL\nEND KARAT\n"
        file_bon = r"C:\Listener\bon.txt"
        check_logger.debug("{0}: {1}".format(stack()[0][3], to_print))
        with open(file_bon, "w") as fp:
            fp.write(header_line)
            for item in to_print:
                fp.write(item)
            fp.write(footer_line)
        print("Tiparire -> Status: OK!")

    @staticmethod
    def execute_batch_file():
        batch_file_path = r"C:\Listener\start.bat"
        print_job = Popen(batch_file_path, shell=False)
        stdout, stderr = print_job.communicate()

    def generate_new_check(self):
        check_to_print = []
        time = datetime.now()
        for elem in self.check_data:
            check_logger.debug("{0}: {1}".format(stack()[0][3], elem))
            backup_list = list(filter(lambda x: x != '', elem.split(' ')))
            reg_ex = search('\d+\,\d+', elem)
            if reg_ex:
                price = elem[reg_ex.start():reg_ex.end()]
            else:
                price = backup_list[5]
            price = (sub(',', '', price)).rjust(8, '0')
            decimals = "2"
            reg_ex = search('\d+', elem)
            if reg_ex:
                quantity = elem[reg_ex.start():reg_ex.end()]
            else:
                quantity = backup_list[0]
            quantity = (sub(',', '', quantity)).rjust(6, '0') + "000"
            reg_ex = search('\d{1,2}%', elem)
            if reg_ex:
                tva = elem[reg_ex.start():reg_ex.end()]
                tva = sub('%', '', tva)
                if tva == "24":
                    if 7 <= time.hour < 24:
                        tva = "1"
                    else:
                        tva = "2"
                elif tva == "9":
                    tva = "3"
                else:
                    tva = "4"
            else:
                tva = backup_list[6]
            subgroup = "1"
            group = "1"
            reg_ex = search('[a-zA-Z]{2,}[\S\s]?[a-zA-Z]*[\S\s]?[a-zA-Z]*', elem)
            if reg_ex:
                prod_name = elem[reg_ex.start():reg_ex.end()]
                prod_name.strip(' ')
            else:
                prod_name = backup_list[3]
            final_check = '*' + prod_name + " " * (24 - len(prod_name)) + price + decimals + quantity + tva + subgroup \
                          + group + '\n'
            check_logger.debug("{0}: {1}".format(stack()[0][3], final_check))
            check_to_print.append(final_check)
        CheckParser.write_2_file(check_to_print)
        CheckParser.execute_batch_file()


def read_init_pos():
    pos_filepath = r"C:\Vectron\pos.txt"
    with open(pos_filepath, "r") as fp:
        init_pos = fp.readline()
        check_logger.debug("{0}: {1}".format(stack()[0][3], init_pos))
        if init_pos == '':
            init_pos = 0
    return int(init_pos)


def write_init_pos(pos):
    if not isinstance(pos, str):
        try:
            pos = str(pos)
        except (ValueError, TypeError):
            pos = "0"

    pos_filepath = r"C:\Vectron\pos.txt"
    check_logger.debug("{0}: {1}".format(stack()[0][3], pos))
    with open(pos_filepath, "w") as fp:
        fp.write(pos)


def get_file_end_pos():
        filename = r"C:\Vectron\VPosPC\files.txt"
        with open(filename, "r") as ff:
            ff.seek(0, 2)
            check_logger.debug("{0}: {1}".format(stack()[0][3], ff.tell()))
            return int(ff.tell())