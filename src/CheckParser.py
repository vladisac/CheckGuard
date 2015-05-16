__author__ = 'nero_luci'

import codecs
import re
from subprocess import Popen
import datetime


class CheckParser(object):
    def __init__(self, pos):
        self.check_data = []
        self.position = pos
        if pos < 0:
            raise ValueError("Initial position must be a natural number")
    
    def read_file(self):
        filename = "C:\\Vectron\\VPosPC\\files.txt"
        with codecs.open(filename, "r", encoding="latin-1") as fh:
            fh.seek(self.position)
            line = fh.readline()
            include = False
            while line:
                if re.search("\*+", line):
                    if not include:
                        include = True
                        line = fh.readline()
                    else:
                        include = False
                if include:
                    self.check_data.append(line)
                if "= Cut =" in line:
                    self.generate_new_check()
                    self.check_data = []
                line = fh.readline()
            self.position = fh.tell()

    def write_2_file(self, to_print):
        header_line = "KARAT\n"
        footer_line = "T0000010000 TOTAL\nEND KARAT\n"
        filename = "C:\\Listener\\bon.txt"
        with open(filename, "w") as fp:
            fp.write(header_line)
            for item in to_print:
                fp.write(item)
            fp.write(footer_line)

    def execute_batch_file(self):
        batch_file_path = "C:\\Listener\\start.bat"
        print_job = Popen(batch_file_path, shell=True)
        stdout, stderr = print_job.communicate()

    def generate_new_check(self):
        check_to_print = []
        time = datetime.datetime.now()
        for elem in self.check_data:
            reg_ex = re.search('\d+\,\d+', elem)
            assert reg_ex
            price = elem[reg_ex.start():reg_ex.end()]
            price = (re.sub(',', '', price)).rjust(8, '0')
            decimals = "2"
            reg_ex = re.search('\d+', elem)
            assert reg_ex
            quantity = elem[reg_ex.start():reg_ex.end()]
            quantity = (re.sub(',', '', quantity)).rjust(6, '0') + "000"
            reg_ex = re.search('\d{1,2}%', elem)
            assert reg_ex
            tva = elem[reg_ex.start():reg_ex.end()]
            tva = re.sub('%','', tva)
            if tva == "24":
                if time.hour >= 7 and time.hour < 24:
                    tva = "1"
                else:
                    tva = "2"
            else:
                tva = "4"
            subgroup = "1"
            group = "1"
            reg_ex = re.search('[a-zA-Z]{2,}[\S\s]?[a-zA-Z]*', elem)
            assert reg_ex
            prod_name = elem[reg_ex.start():reg_ex.end()]
            prod_name.strip(' ')
            final_check = '*' + prod_name + " " * (24 - len(prod_name)) + price + decimals + quantity + tva + subgroup \
                          + group + '\n'
            check_to_print.append(final_check)
        self.write_2_file(check_to_print)
        self.execute_batch_file()


    def get_file_pos(self):
        return str(self.position)


def read_init_pos():
    pos_filepath = "C:\\Vectron\\pos.txt"
    with open(pos_filepath, "r") as fp:
        init_pos = fp.readline()
        if init_pos == '':
            init_pos = 0
    return int(init_pos)


def write_init_pos(pos):
    pos_filepath = "C:\\Vectron\\pos.txt"
    with open(pos_filepath, "w") as fp:
        fp.write(pos)