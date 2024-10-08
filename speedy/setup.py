"""
`java8speedy` module setup

Adding support for Java 8 labeled grammar

"""
__version__ = '0.5.0'
__author__ = 'Morteza'

import sys
import os
import platform
import fnmatch
import setuptools

target = platform.system().lower()
PLATFORMS = {'windows', 'linux', 'darwin', 'cygwin'}
for known in PLATFORMS:
    if target.startswith(known):
        target = known


def run_setup(with_binary):
    if with_binary:

        extra_compile_args = {
            'windows': ['/DANTLR4CPP_STATIC', '/Zc:__cplusplus'],
            'linux': ['-std=c++11'],
            'darwin': ['-std=c++11'],
            'cygwin': ['-std=c++11'],
        }

        # Define an Extension object that describes the Antlr accelerator
        parser_ext = setuptools.Extension(
            # Extension name shall be at the same level as the sa_java8_parser.py module
            name='java8speedy.parser.sa_javalabeled_cpp_parser',

            # Add the Antlr runtime source directory to the include search path
            include_dirs=["src/java8speedy/parser/cpp_src/antlr4_cpp_runtime"],

            # Rather than listing each C++ file (Antlr has a lot!), discover them automatically
            sources=get_files("src/java8speedy/parser/cpp_src", "*.cpp"),
            depends=get_files("src/java8speedy/parser/cpp_src", "*.h"),

            extra_compile_args=extra_compile_args.get(target, [])
        )
        ext_modules = [parser_ext]
    else:
        ext_modules = []

    # Define a package
    setuptools.setup(
        name='java8speedy',
        version='1.2.0',
        description='Java Speedup Parser',
        packages=setuptools.find_packages("src"),
        package_dir={"": "src"},
        include_package_data=True,
        install_requires=[
            "antlr4-python3-runtime >= 4.9.2",
        ],
        ext_modules=ext_modules,
        cmdclass={"build_ext": ve_build_ext},
    )


# ===============================================================================
from setuptools.command.build_ext import build_ext
from distutils.errors import CCompilerError, DistutilsExecError, DistutilsPlatformError


def get_files(path, pattern):
    """
    Recursive file search that is compatible with python3.4 and older
    """
    matches = []
    for root, _, filenames in os.walk(path):
        for filename in fnmatch.filter(filenames, pattern):
            matches.append(os.path.join(root, filename))
    return matches


class BuildFailed(Exception):
    pass


class ve_build_ext(build_ext):
    """
    This class extends setuptools to fail with a common BuildFailed exception
    if a build fails
    """

    def run(self):
        try:
            build_ext.run(self)
        except DistutilsPlatformError:
            raise BuildFailed()

    def build_extension(self, ext):
        try:
            build_ext.build_extension(self, ext)
        except (CCompilerError, DistutilsExecError, DistutilsPlatformError):
            raise BuildFailed()
        except ValueError:
            # this can happen on Windows 64 bit, see Python issue 7511
            if "'path'" in str(sys.exc_info()[1]):  # works with Python 2 and 3
                raise BuildFailed()
            raise


# Detect if an alternate interpreter is being used
is_jython = "java" in sys.platform
is_pypy = hasattr(sys, "pypy_version_info")

# Force using fallback if using an alternate interpreter
using_fallback = is_jython or is_pypy

if not using_fallback:
    try:
        run_setup(with_binary=True)
    except BuildFailed:
        if 'SPAM_EXAMPLE_REQUIRE_CI_BINARY_BUILD' in os.environ:
            # Require build to pass if running in travis-ci
            raise
        else:
            using_fallback = True

if using_fallback:
    run_setup(with_binary=False)
