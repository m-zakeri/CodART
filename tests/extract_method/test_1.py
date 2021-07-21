"""
    simplest test possible.

    test status: pass
"""

from refactorings.extract_method import extract_method

def main():
    base_dir = '/mnt/d/Sajad/Uni/Spring00/Compiler/CodART/'
    _conf = {
        'target_file': base_dir +"tests/extract_method/in/ExtractMethodTest.java",
        'output_file': base_dir +"tests/extract_method/out/ExtractMethodTest.java",
        'lines': [7,8 ],
        'new_method_name': 'printAllDetails',
    }
    extract_method(_conf)

if __name__ == '__main__':
    main()