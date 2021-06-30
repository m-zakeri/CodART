"""
    extracting lines containing static variables.

    test status: pass
"""

from refactorings.extract_method import extract_method
import os
import errno

def main():
    base_dir = '/mnt/d/Sajad/Uni/Spring00/Compiler/CodART/'
    if not os.path.exists(os.path.dirname(
            base_dir + "tests/extract_method/out/benchmark_projects/ganttproject/biz.ganttproject.core/src/main/java/biz/ganttproject/core/chart/render/Style.java")):
        try:
            os.makedirs(os.path.dirname(
                base_dir + "tests/extract_method/out/benchmark_projects/ganttproject/biz.ganttproject.core/src/main/java/biz/ganttproject/core/chart/render/Style.java"))
        except OSError as exc:  # Guard against race condition
            if exc.errno != errno.EEXIST:
                raise
    _conf = {
        'target_package': 'biz.ganttproject.core.chart.render',
        'target_file': base_dir + "benchmark_projects/ganttproject/biz.ganttproject.core/src/main/java/biz/ganttproject/core/chart/render/Style.java",
        'output_file': base_dir + "tests/extract_method/out/benchmark_projects/ganttproject/biz.ganttproject.core/src/main/java/biz/ganttproject/core/chart/render/Style.java",
        'lines': [108,109,110,111,112,113,114,115,116,117,118,119],
        'new_method_name': 'checkResult',
    }
    extract_method(_conf)


if __name__ == '__main__':
    main()
