"""
This is configuration file for understand path
You should set the path of understand installation in this script

"""
import os
import sys
# import logging

from dotenv import load_dotenv
from codart import config

load_dotenv()

# -------------------
# For Linux os
PYTHONPATH = os.environ.get("PYTHONPATH")  # Put your path here

# -------------------
# For Windows os
# https://scitools.com/support/python-api/
# Python 3.8 and newer require the user add a call to os.add_dll_directory(“SciTools/bin/“  # Put your path here
# os.add_dll_directory('C:/Program Files/SciTools/bin/pc-win64')  # Put your path here
sys.path.insert(0, PYTHONPATH)  # Put your path here

# --------------------
# Import understand if available on the path
try:
    import understand as und
    config.logger.info(f"Loaded understand {und.version()} successfully")
except ModuleNotFoundError:
    raise ModuleNotFoundError('Understand not found.')
except ImportError:
    raise ImportError("Can not import")
