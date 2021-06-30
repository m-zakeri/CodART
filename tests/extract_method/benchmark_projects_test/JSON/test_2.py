from refactorings.extract_method import extract_method
from tests.extract_method.candidate_reader import CandidateReader
import os
import errno

def main():
    base_dir = '/mnt/d/Sajad/Uni/Spring00/Compiler/CodART/'
    project_root = 'benchmark_projects/JSON/src/main/java/'
    csv_addr = '/mnt/d/Sajad/Uni/Spring00/Compiler/CodART/tests/extract_method/benchmark_projects_test/JSON/Long-Method.csv'
    cr = CandidateReader(csv_addr)
    _conf = cr.get_conf(4)
    if not os.path.exists(os.path.dirname(
            base_dir + 'tests/extract_method/out/' +project_root + str(_conf['target_file']).replace(".","/") + '.java')):
        try:
            os.makedirs(os.path.dirname(
                base_dir + 'tests/extract_method/out/' +project_root + str(_conf['target_file']).replace(".","/") + '.java'))
        except OSError as exc:  # Guard against race condition
            if exc.errno != errno.EEXIST:
                raise
    target_file = _conf['target_file']
    _conf['target_file'] = base_dir + project_root + str(target_file).replace(".","/") + '.java'
    _conf['output_file'] = base_dir + 'tests/extract_method/out/' +project_root + str(target_file).replace(".","/") + '_test_2.java'
    _conf['new_method_name'] = 'checkCondition'
    print('conf:',_conf)
    extract_method(_conf)

if __name__ == '__main__':
    main()