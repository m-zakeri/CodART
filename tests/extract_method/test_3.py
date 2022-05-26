"""
    extracting lines containing access to primitive local variables

    test status: pass
"""

from codart.refactorings.extract_method import extract_method
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
        'target_file': base_dir + "benchmark_projects/ganttproject/biz.ganttproject.core/src/main/java/org/w3c/util/DateParser.java",
        'output_file': base_dir + "tests/extract_method/out/benchmark_projects/ganttproject/biz.ganttproject.core/src/main/java/org/w3c/util/DateParser_test_3.java",
        'lines': [191, 192, 193, 194, 195, 196, 197, 198, 199],
        'new_method_name': 'fillBufferWithDate',
    }
    extract_method(_conf)


if __name__ == '__main__':
    main()
