# Test script to verify that the Understand Python API is setup correctly

import sys
import struct
import shutil
import re
from utilization.setup_understand import *

# Verify Python 3

if (sys.version_info >= (3, 0)):
    print("Checking for Python Version >= 3.0 : Pass")
    print("  Python Version: " + str(sys.version_info.major) + "." + str(sys.version_info.minor) + "." + str(
        sys.version_info.micro))
else:
    print("Checking for Python Version >= 3.0 : Fail")
    print("  Error: The Understand API requires Python 3.0 or later")
    print("  Python Version: " + str(sys.version_info.major) + "." + str(sys.version_info.minor) + "." + str(
        sys.version_info.micro))
    quit()

# Check that Understand is in the PATH
undPath = shutil.which("und")
if not undPath:
    print("Checking for Understand in PATH: Fail")
    print("  Error: Add scitools/bin/[SYSTEM] to PATH and restart your session")
    quit()
undPath = os.path.normcase(re.sub(r'und(\.exe)*$', '', undPath, flags=re.IGNORECASE))
if (undPath):
    print("Checking for Understand in PATH: Pass")
    print("  found at ", undPath)
else:
    print("Checking for Understand in PATH: Fail")
    print("  Error: Add scitools/bin/[SYSTEM] to PATH and restart your session")
    quit()

# Check that Understand is the same bitness as python
understandBit = 0
caseSensitive = True
ldTest = False
if 'pc-win32' in undPath:
    understandBit = 32
    caseSensitive = False
elif 'pc-win64' in undPath:
    understandBit = 64
    caseSensitive = False
elif 'linux32' in undPath:
    understandBit = 32
    ldTest = True
elif 'linux64' in undPath:
    understandBit = 64
    ldTest = True
elif 'MacOS' in undPath:
    understandBit = 64
else:
    print('  Error: Unexpected Directory Structure, the Understand install directory should not be modified. ', undPath)
    quit()
pythonBit = (struct.calcsize("P") * 8)
if (pythonBit != understandBit):
    print("Checking that Bit versions match: Fail")
    print("  Error: Python is", pythonBit, "bit and Understand is", understandBit, "bit. They need to match")
    quit()
print("Checking that Bit versions match: Pass")

# If Linux, check if LD_LIBRARY_PATH is set. Otherwise graphing won't work
if ldTest:
    try:
        LD_LIBRARY_PATH = os.environ['LD_LIBRARY_PATH']
        if LD_LIBRARY_PATH == undPath:
            print("Checking that LD_LIBRARY_PATH is set correctly: Pass")
        else:
            print("Checking that LD_LIBRARY_PATH is set correctly: Fail")
            print("  Warning: LD_LIBRARY_PATH set to ", LD_LIBRARY_PATH, ". Draw function may not work.")
            print("  If draw function does not work, set LD_LIBRARY_PATH to ", undPath,
                  ". If it is already set you may need to restart your session.")
    except Exception as e:
        print("Checking that LD_LIBRARY_PATH is set correctly: Fail")
        print("  Warning: LD_LIBRARY_PATH not set. Draw function may not work.")
        print("  Set LD_LIBRARY_PATH to ", undPath, ". If it is set you may need to restart your session.")

# Check that PYTHONPATH can find the understand.pyd
inPythonPath = False
pythonDir = os.path.normcase(undPath + "Python")
pythonPath = sys.path
for testDir in pythonPath:
    cleanDir = os.path.normcase(testDir)
    if cleanDir == pythonDir:
        inPythonPath = True
    if (cleanDir.find('\"') > 0):
        print("  Illegal Quote characters were found in PYTHONPATH: " + cleanDir)
if (not inPythonPath):
    print("Checking that PYTHONPATH includes API: Fail")
    print("  Error: Add", pythonDir, "to PYTHONPATH. If it is set you may need to restart your session.")
    quit()
print("Checking that PYTHONPATH includes API: Pass")

# Try actually loading the API
try:
    import understand
except ModuleNotFoundError:
    print("Checking that API Loads: Fail")
    pydDebugPath = os.path.normcase((pythonDir + "/understand_d.pyd"))
    if os.path.exists(pydDebugPath):
        print("  Error: Running Python API from debug build not currently supported")
        quit()
    pydPath = os.path.normcase(pythonDir + "/understand.pyd")
    print("  Error: Module Not Found: ", pydPath)
    print("  Unexpected Directory Structure, the Understand install directory should not be modified.")
    quit()
except ImportError as e:
    print("Checking that API Loads: Fail")
    qtPaths = []
    for path in os.environ['PATH'].split(os.pathsep):
        candidate = os.path.join(path, 'qt.conf')
        if os.path.exists(candidate):
            qtPaths.append(path)
    if (len(qtPaths) == 0):
        print("  Error: QtFiles are missing from the PATH even though", undPath, "was found")
        print("  Unexpected Directory Structure, the Understand install directory should not be modified.")
        quit()
    if (len(qtPaths) > 1):
        print("  Error: Multiple Qt Installations in the PATH.")
        print("  Try moving the sti\\bin directory earlier in the path.")
        for path in qtPaths:
            print("    Qt installed at", path)
        quit()
    print("  Error importing API:", e)
    quit()
except Exception as e:
    print("Checking that API Loads: Fail")
    print("  Error loading API:", e)
    quit()

print("Checking that API Loads: Pass")

print("\nSuccess! The Python API is setup correctly and ready to use!")
