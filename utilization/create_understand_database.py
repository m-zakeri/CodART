import understand as und
from statistics import mean
import os
# from tkinter import *
# import main_metrics
import sys
# import Qf_numpy
import time
# import tkinter as tk
# import tkinter
# from tkinter import filedialog
import os


class create_udb_databace:
    path = ""

    def main(self):

        # {{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{
        # root = tkinter.Tk()
        # root.withdraw()  # use to hide tkinter window
        #
        # def search_for_file_path():
        #     currdir = os.getcwd()
        #     tempdir = filedialog.askdirectory(parent=root, initialdir=currdir, title='Please select a directory')
        #     if len(tempdir) > 0:
        #         print("You chose: %s" % tempdir)
        #     return tempdir

        file_path_variable = "D:/archive/uni/CD/project"
        print("\nfile_path_variable = ", file_path_variable)
        # {{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{
        rootpath = file_path_variable + "/"
        obj = create_udb_databace()
        obj.create_understand_database_from_project(rootpath)

    def create_understand_database_from_project(cls, root_path):
        STRNAME = "project"
        count = 1
        # {0}: understand_db_directory, {1}: understand_db_name, {2}: project_root_directory
        cmd = 'und create -db {0}{1}.udb -languages C# java python add {2} analyze -all'
        # projects = [x[0] for x in os.walk(root_path)]
        projects = [name for name in os.listdir(root_path) if os.path.isdir(os.path.join(root_path, name))]
        # print("list :",projects)
        for project_ in projects:
            command = cmd.format(root_path, project_, root_path + project_)
            count += 1
            print('executing ... ', command)
            os.system(cmd)
            print("finished ", project_)


obj2 = create_udb_databace()
obj2.main()
