"""
    extracting lines containing access to primitive local variables

    test status: pass
"""

from refactorings.extract_method import extract_method
import os
import errno


def main():
    base_dir = '/mnt/d/Sajad/Uni/Spring00/Compiler/CodART/'
    if not os.path.exists(os.path.dirname(
            base_dir + "tests/extract_method/out/benchmark_projects/ganttproject/biz.ganttproject.core/src/main/java/org/w3c/util/DateParser_test_3.java")):
        try:
            os.makedirs(os.path.dirname(
                base_dir + "tests/extract_method/out/benchmark_projects/ganttproject/biz.ganttproject.core/src/main/java/org/w3c/util/DateParser_test_3.java"))
        except OSError as exc:  # Guard against race condition
            if exc.errno != errno.EEXIST:
                raise
    _conf = {
        'target_package': 'org.w3c.util',
        'target_file': base_dir + "benchmark_projects/ganttproject/biz.ganttproject.core/src/main/java/org/w3c/util/DateParser.java",
        'output_file': base_dir + "tests/extract_method/out/benchmark_projects/ganttproject/biz.ganttproject.core/src/main/java/org/w3c/util/DateParser_test_3.java",
        'target_class': 'DateParser',
        'target_method': 'getIsoDate',
        'lines': [4, 5, 6, 7, 8, 9, 10, 11, 12],
        'new_method_name': 'fillBufferWithDate',
    }
    extract_method(_conf)


if __name__ == '__main__':
    main()
