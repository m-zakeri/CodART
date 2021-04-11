# """
# This is configuration file for understand path
# You should set the path of understand installation in this script
#
# """
# import os
# import sys
#
#
# # -------------------
# # For Linux os
# LD_LIBRARY_PATH = "/home/ali/scitools/bin/linux64/"  # Put your path here
# PYTHONPATH = "/home/ali/scitools/bin/linux64/Python"  # Put your path here
#
# os.environ["LD_LIBRARY_PATH"] = LD_LIBRARY_PATH  # Put your path here
#
#
# # -------------------
# # For Windows os
# # https://scitools.com/support/python-api/
# # Python 3.8 and newer require the user add a call to os.add_dll_directory(“SciTools/bin/“  # Put your path here
# # os.add_dll_directory('C:/Program Files/SciTools/bin/pc-win64')  # Put your path here
# sys.path.insert(0, 'D:/program files/scitools/bin/pc-win64/python')  # Put your path here
#
#
# # --------------------
# # Import understand if available on the path
# try:
#     import understand as und
# except ModuleNotFoundError:
#     raise ModuleNotFoundError('Understand cannot import')
#
