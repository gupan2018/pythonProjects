# -*- coding:utf-8 -*-
# __author__ = 'gupan'
import xlrd
import xlwt3
from xlutils.copy import copy

class Excel:
    def __init__(self, path):
        self.path = path
        self.sheet_obj = None
        self.rb = None
        self.wb = None
        self.rows = 0
        self.cols = 0


    def get_rows(self):
        if self.sheet_obj is None:
            return None
        return self.sheet_obj.nrows

    def get_cols(self):
        if self.sheet_obj is None:
            return None
        return self.sheet_obj.ncols

    def get_sheet(self, index):
        self.rb = xlrd.open_workbook(self.path)
        #print(self.rb)
        self.sheet_obj = self.rb.sheets()[index - 1]
        #print(self.sheet_obj.name)

    def creat_sheet(self, sheet_name):
        self.wb = xlwt3.Workbook()
        self.sheet_obj = self.wb.add_sheet(sheet_name)
        return self.sheet_obj

    def read_data(self, x, y):
        if self.sheet_obj is None or x > self.sheet_obj.nrows or y > self.sheet_obj.ncols:
            return None
        return self.sheet_obj.cell_value(x - 1, y - 1)

    def write_data(self, x, y, data):
        if self.sheet_obj is None or x > self.sheet_obj.nrows or self.sheet_obj.ncols > y:
            return None
        self.sheet_obj.write(x - 1, y - 1, data)

    def write_data_when_read(self, index, x, y, data):
        if self.sheet_obj is None or index < 0:
            #print("1")
            return None

        if self.rb is None:
            return None

        wb = copy(self.rb)

        sheet_obj = wb.get_sheet(index)
        sheet_obj.write(x - 1, y - 1, data)
        wb.save(self.path)