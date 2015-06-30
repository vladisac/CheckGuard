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
from re import search, sub
from inspect import stack
from subprocess import Popen
from CheckLogger import check_logger
from CheckQueue import check_queue


class CheckParser(object):
    """
    CheckParser class parses each new check from a source file,
    extracts needed information and then writes new information
    to a target file. Information written to the target file is
    generated according to a specific grammar and format required
    by the fiscal printer (check the official documentation from
    your fiscal printer vendor).
    """
    def __init__(self, position, filename=None):
        """
        :param self.check_data: holds extracted information from source file
        :param self.check_to_print: holds generated information to be written into target file
        :param self.position: starting position in source file and/or end position of last
                         read check
        :param self.filename: source file name
        :param self.cash: holds information about cash payment method
        :param self.card: holds information about card payment method
        """
        self.check_data = []
        self.check_to_print = []
        self.position = position
        self.filename = filename
        self.cash = None
        self.card = None

    @property
    def position(self):
        """
        :return: value of self.position
        """
        return self._position

    @position.setter
    def position(self, value):
        """
        :param value: initialize/change value of self.position
        :return:
        """
        if value is not None:
            if value >= 0:
                self._position = value
            else:
                raise ValueError("Initial position must be a natural number")

    @property
    def filename(self):
        """
        :return: value of self.filename
        """
        return self._filename

    @filename.setter
    def filename(self, value):
        """
        :param value: name of source file
        """
        if value is not None:
            self._filename = value
        else:
            self._filename = r"C:\Vectron\VPosPC\files.txt"

    def read_file(self):
        """
        This method extracts needed information from a check written by the POS system
        into the source file(self.filename). Extraction(selection) operation is done
        according to the check grammar, all products with information about their quantity,
        price, vat etc will be embraced by two lines containing only the '*' character.
        After the last (products) delimiter line, the payment method(s) and total amount
        information will follow.
        """
        check_logger.debug("{0}: {1}".format(stack()[0][3], "_____START_____"))
        with open(self.filename, "rb") as fh:
            check_logger.debug("{0}: {1}".format(stack()[0][3], "file.txt opened"))
            fh.seek(self.position)  # move file cursor to start position, start of source file or
            line = fh.readline()    # end of the last read check
            check_logger.debug("{0}: {1}".format(stack()[0][3], line))
            delimiter = "**************************************************"
            while line:  # Read source file lines until EOF
                if delimiter in line:
                    line = fh.readline()
                    check_logger.debug("{0}: {1}".format(stack()[0][3], line))
                    while delimiter not in line:  # Until the second delimiter line is not encountered
                        self.check_data.append(line)
                        line = fh.readline()
                        check_logger.debug("{0}: {1}".format(stack()[0][3], line))
                line = fh.readline()
                check_logger.debug("{0}: {1}".format(stack()[0][3], line))
                if "Cash" in line:  # Save the line where cash payment method is present
                    self.cash = line
                if "Plata card" in line:  # Save the line where card payment method is present
                    self.card = line
                if "= Cut =" in line and self.check_data != []:  # Got to end of current check
                    check_logger.debug("{0}: {1}".format(stack()[0][3], self.check_data))
                    self.generate_new_check()  # Use extracted information to generate new information for FP
                    check_queue.put(self.check_to_print)
                    self.check_to_print = []
                    self.check_data = []
            self.position = fh.tell()  # Save the position of the EOF
            check_logger.debug("{0}: {1}".format(stack()[0][3], "_____END_____"))

    def payment_method(self):
        """
        This method handles information about payment methods, then appends it to 'to be' written
        information for FP(fiscal printer) into target file
        """
        if self.cash:
            backup_list = list(filter(lambda x: x != '', self.cash.split(' ')))  # backup list when(if) regex fails
            price = CheckParser.get_field_value('\d+\,\d+', self.cash, backup_list, 1, ',', '', 8)
            self.check_to_print.append("RQ0CASH      " + price + "2\n")
            self.cash = None
        if self.card:
            backup_list = list(filter(lambda x: x != '', self.card.split(' ')))
            price = CheckParser.get_field_value('\d+\,\d+', self.card, backup_list, 2, ',', '', 8)
            self.check_to_print.append("RQ1CARD      " + price + "2\n")
            self.card = None

    def generate_new_check(self):
        check_logger.debug("{0}: {1}".format(stack()[0][3], "starting creation of products and payment"))
        for elem in self.check_data:
            check_logger.debug("{0}: {1}".format(stack()[0][3], elem))
            backup_list = list(filter(lambda x: x != '', elem.split(' ')))
            price = CheckParser.get_field_value('\d+\,\d+', elem, backup_list, 5, ',', '', 8)
            decimals = "2"
            quantity = CheckParser.get_field_value('\d+', elem, backup_list, 0, ',', '', 6) + "000"
            tva = CheckParser.get_field_value('\d{1,2}%', elem, backup_list, 6, '%', '')
            tva = CheckParser.tva_by_time(tva)
            subgroup = "1"
            group = "1"
            prod_name = CheckParser.get_field_value('[a-zA-Z]{2,}[\S\s]?[a-zA-Z]*[\S\s]?[a-zA-Z]*',
                                                    elem, backup_list, 3)
            # Information that is written to the target file is composed accordingly to a special grammar
            # required by the FP driver.
            # '*'<product name><padding until 26 index><price|decimals><quantity><tva><subgroup><group>
            final_check = '*' + prod_name + " " * (24 - len(prod_name)) + price + decimals + quantity + \
                          tva + subgroup + group + '\n'
            check_logger.debug("{0}: {1}".format(stack()[0][3], final_check))
            self.check_to_print.append(final_check)
        check_logger.debug("{0}: {1}".format(stack()[0][3], "finished creation of products and payment"))

    @staticmethod
    def get_field_value(regex_pattern, data_bucket, backup_data,
                        backup_index, subst_from=None, subst_to=None, padding_len=None):
        """
        This method extracts information from each product line using a regular expression,
        substitutes characters(optional, and adds padding(optional)
        :param regex_pattern: regular expression pattern used to extract information, ex: price, tva etc.
        :param data_bucket: line containing all information about a product from the check
        :param backup_data: a list containing tokens from data_bucket, used in case a regex fails
        :param backup_index: index of the needed token in the backup_list
        :param subst_from: substitute from character 'subst_form'
        :param subst_to: to character 'subst_to'
        :param padding_len: how many padding values are needed
        :return: string ; processed value of a specific token from the product line
        """
        reg_ex = search(regex_pattern, data_bucket)
        if reg_ex:
            field_value = data_bucket[reg_ex.start():reg_ex.end()]
        else:
            field_value = backup_data[backup_index]
        if subst_from and padding_len:
            field_value = (sub(subst_from, subst_to, field_value)).rjust(padding_len, '0')
        elif subst_from:
            field_value = sub(subst_from, subst_to, field_value)
        else:
            return field_value

        return field_value

    @staticmethod
    def tva_by_time(tva):
        """
        :param tva: value read from source file for a specific product
        :return: [string] ; corresponding value for FP
        """
        time = datetime.now()
        if tva == "24":  # FP tva values correspondence: 1 <-> 24%(before midnight), 2 <-> 24%(after midnight)
            if 7 <= time.hour < 24:  # 3 <-> 9%, 4 <-> 0%
                tva = "1"
            else:
                tva = "2"
        elif tva == "9":
            tva = "3"
        else:
            tva = "4"

        return tva

    @staticmethod
    def write_2_file(to_print):
        """
        This method writes selected and processed information from the source file to the target file.
        :param to_print: information to be written into the target file
        """
        header_line = "KARAT\n"  # header of the target file, needed by the FP driver
        footer_line = "T0000010000 TOTAL\nEND KARAT\n"  # footer of the target file
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
        """
        This method spawns a process that executes commands from a batch file, thus starting the FP driver.
        """
        batch_file_path = r"C:\Listener\start.bat"
        check_logger.debug("{0}: {1}".format(stack()[0][3], "execute batch file"))
        print_job = Popen(batch_file_path, shell=False)  # spawn a process that starts the FP driver
        stdout, stderr = print_job.communicate()


def read_init_pos():
    """
    This function reads initial position of the source file cursor
    """
    pos_filepath = r"C:\Vectron\pos.txt"
    with open(pos_filepath, "r") as fp:
        init_pos = fp.readline()
        check_logger.debug("{0}: {1}".format(stack()[0][3], init_pos))
        if init_pos == '':
            init_pos = 0
    return int(init_pos)


def write_init_pos(pos):
    """
    This function writes the value of the source file cursor
    :param pos: source file cursor value
    """
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
    """
    This functions tells the EOF value, used when the program starts to check if the EOF is different
    from the init position of the source file cursor. If there is a difference this means there are
    unprocessed(and unprinted) checks
    :return:
    """
    filename = r"C:\Vectron\VPosPC\files.txt"
    with open(filename, "r") as ff:
        ff.seek(0, 2)
        check_logger.debug("{0}: {1}".format(stack()[0][3], ff.tell()))
        return int(ff.tell())
