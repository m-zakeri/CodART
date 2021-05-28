"""
    simplest test possible.

    test status: pass
"""

from refactorings.extract_method import extract_method

def main():
    _conf = {
        'target_package': None,
        'target_file': "/mnt/d/Sajad/Uni/Spring00/Compiler/CodART/tests/extract_method/in/ExtractMethodTest.java",
        'output_file': "/mnt/d/Sajad/Uni/Spring00/Compiler/CodART/tests/extract_method/out/ExtractMethodTest.java",
        'target_class': 'ExtractMethodTest',
        'target_method': 'printOwing',
        'lines': [4, 5 ],
        'new_method_name': 'printDetails',
    }
    extract_method(_conf)

if __name__ == '__main__':
    main()