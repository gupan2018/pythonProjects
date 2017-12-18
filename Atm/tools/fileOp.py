# -*- coding:utf-8 -*-
# __author__ = 'gupan'
class File:
    def __init__(self, path):
        self.path = path
        self.file_instance = None

    def openFile(self, mode = 'r'):
        if self.file_instance == None or self.file_instance.closed == True:
            self.file_instance = open(self.path, mode)

    def closeFile(self):
        if self.file_instance != None and self.file_instance.closed == False:
            self.file_instance.close()
            self.file_instance = None

    def getFile_instance(self):
        if self.file_instance != None:
            return self.file_instance
        else:
            return None

    def write_in_file(self, words):
        if self.file_instance != None:
            self.file_instance.write(words)

    def writeline_in_file(self, line):
        if self.file_instance != None:
            self.file_instance.writelines(line)

    def readFile(self, count = 0):
        if self.file_instance != None:
            if count == 0:
                return self.file_instance.read()
            else:
                return self.file_instance.read(count)