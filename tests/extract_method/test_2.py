"""
    extracting lines from methods which have been overloaded.

    test status: pass
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
        'target_file': base_dir+"benchmark_projects/ganttproject/biz.ganttproject.core/src/main/java/org/w3c/util/DateParser.java",
        'output_file': base_dir+"tests/extract_method/out/benchmark_projects/ganttproject/biz.ganttproject.core/src/main/java/org/w3c/util/DateParser_test_2.java",
        'lines': [255,256,257,258 ],
        'new_method_name': 'printDivider',
    }
    extract_method(_conf)

if __name__ == '__main__':
    main()