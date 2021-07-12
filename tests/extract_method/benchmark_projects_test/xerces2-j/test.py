import unittest


from refactorings.extract_method import extract_method
from tests.extract_method.candidate_reader import CandidateReader
from tests.extract_method.java_file_equality_checker import is_equal


class MyTestCase(unittest.TestCase):

    def setUp(self):
        self.base_dir = '/mnt/d/Sajad/Uni/Spring00/Compiler/CodART/'
        self.benchmark_project_root = 'benchmark_projects/xerces2-j/src/'
        csv_addr = self.base_dir + 'tests/extract_method/benchmark_projects_test/xerces2-j/Long-Method.csv'
        self.cr = CandidateReader(csv_addr)

    def assert__(self,test_index,new_method_name):
        _conf = self.cr.get_conf(test_index)
        target_file = _conf['target_file']
        _conf['target_file'] = self.base_dir + self.benchmark_project_root + str(target_file).replace(".",
                                                                                                      "/") + '.java'
        _conf['output_file'] = self.base_dir + 'tests/extract_method/benchmark_projects_test/xerces2-j/testdata/test_' + \
                               str(test_index) + '_CodART.java'
        _conf['new_method_name'] = new_method_name
        extract_method(_conf)
        self.assertTrue(is_equal(_conf['output_file'], _conf['output_file'].replace('_CodART', '_JDeodorant')))

    # def test_0(self):                 # correct but different
    #     test_index = 0
    #     new_method_name = 'getString'
    #     self.assert__(test_index,new_method_name)


    def test_128(self):               # pass
        test_index = 128
        new_method_name = 'refactored'
        self.assert__(test_index,new_method_name)

    def test_323(self):               # pass
        test_index = 323
        new_method_name = 'getXsWildcardDecl'
        self.assert__(test_index,new_method_name)

    # def test_338(self):               # correct but different
    #     test_index = 338
    #     new_method_name = 'getAttributePSV'
    #     self.assert__(test_index,new_method_name)

    def test_372(self):               # pass
        test_index = 372
        new_method_name = 'getSymbolHash'
        self.assert__(test_index,new_method_name)

    def test_634(self):               # correct but different
        test_index = 634
        new_method_name = 'dwdw'
        self.assert__(test_index,new_method_name)

    def test_630(self):               # pass
        test_index = 630
        new_method_name = 'setBool'
        self.assert__(test_index,new_method_name)

    def test_628(self):               # correct but different
        test_index = 628
        new_method_name = 'test'
        self.assert__(test_index,new_method_name)

    def test_625(self):               # pass
        test_index = 625
        new_method_name = 'test'
        self.assert__(test_index,new_method_name)

    def test_624(self):               # pass
        test_index = 624
        new_method_name = 'getString'
        self.assert__(test_index,new_method_name)

    def test_622(self):               # pass
        test_index = 622
        new_method_name = 'getIndent'
        self.assert__(test_index,new_method_name)

    def test_619(self):               # pass
        test_index = 619
        new_method_name = 'test'
        self.assert__(test_index,new_method_name)

    def test_616(self):               # correct but different
        test_index = 616
        new_method_name = 'test'
        self.assert__(test_index,new_method_name)

    def test_614(self):               # pass
        test_index = 614
        new_method_name = 'getString'
        self.assert__(test_index,new_method_name)

    def test_613(self):               # pass
        test_index = 613
        new_method_name = 'getString'
        self.assert__(test_index,new_method_name)


if __name__ == '__main__':
    unittest.main()
