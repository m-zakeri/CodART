"""
    extracting lines from methods which have been overloaded.
    for instance target method test (specified in _conf below) has been overloaded.
    we added target_method_args to our _conf object to specify arguments types of overloaded method.

    test status: failed
"""

from refactorings.extract_method import extract_method
import os
import errno

def main():
    base_dir = '/mnt/d/Sajad/Uni/Spring00/Compiler/CodART/'
    if not os.path.exists(os.path.dirname(base_dir+"tests/extract_method/out/benchmark_projects/ganttproject/biz.ganttproject.core/src/main/java/org/w3c/util/DateParser.java")):
        try:
            os.makedirs(os.path.dirname(base_dir+"tests/extract_method/out/benchmark_projects/ganttproject/biz.ganttproject.core/src/main/java/org/w3c/util/DateParser.java"))
        except OSError as exc:  # Guard against race condition
            if exc.errno != errno.EEXIST:
                raise
    _conf = {
        'target_package': 'org.w3c.util',
        'target_file': base_dir+"benchmark_projects/ganttproject/biz.ganttproject.core/src/main/java/org/w3c/util/DateParser.java",
        'output_file': base_dir+"tests/extract_method/out/benchmark_projects/ganttproject/biz.ganttproject.core/src/main/java/org/w3c/util/DateParser.java",
        'target_class': 'DateParser',
        'target_method': 'test',
        'target_method_args':['Date',],
        'lines': [2 ],
        'new_method_name': 'printDivider',
    }
    extract_method(_conf)

if __name__ == '__main__':
    main()