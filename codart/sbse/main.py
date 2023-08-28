
import argparse
import configparser
# Import your refactoring modules here
from codart.refactorings import (
    make_field_non_static,
    make_field_static,
    make_method_static2,
    make_method_non_static2,
    pullup_field,
    pushdown_field2,
    pullup_method,
    pullup_constructor,
    pushdown_method,
    move_field,
    move_method,
    move_class,
    extract_class,
    extract_method,
    extract_interface2,
    increase_field_visibility,
    increase_method_visibility,
    decrease_field_visibility,
    decrease_method_visibility
)

REFACTORING_MAIN_MAP = {
    'Make Field Non-Static': make_field_non_static.main,  # RO1
    'Make Field Static': make_field_static.main,  # RO2
    'Make Method Static': make_method_static2.main,  # RO3
    'Make Method Non-Static': make_method_non_static2.main,  # RO4
    'Pull Up Field': pullup_field.main,  # RO5
    'Push Down Field': pushdown_field2.main,  # RO6, 0
    'Pull Up Method': pullup_method.main,  # RO7, 0
    'Pull Up Constructor': pullup_constructor.main,  # RO8, 0
    'Push Down Method': pushdown_method.main,  # RO9, 0
    'Move Field': move_field.main,  # RO10
    'Move Method': move_method.main,  # RO11
    'Move Class': move_class.main,  # RO12
    'Extract Class': extract_class.main,  # RO13
    'Extract Method': extract_method.main,  # RO14
    'Extract Interface': extract_interface2.main,  # RO15
    'Increase Field Visibility': increase_field_visibility.main,  # RO16
    'Increase Method Visibility': increase_method_visibility.main,  # RO17
    'Decrease Field Visibility': decrease_field_visibility.main,  # RO18
    'Decrease Method Visibility': decrease_method_visibility.main,  # RO19
}


def main():
    parser = argparse.ArgumentParser(
        description='Perform code art for dqn using command line arguments.')
    parser.add_argument('-p', '--path', help='path to the project')
    parser.add_argument('-u', '--udb', help='path to the UDB file')
    parser.add_argument('-l', '--log', help='path to the log file')
    parser.add_argument('-r', '--refactoring',
                        choices=REFACTORING_MAIN_MAP.keys(),
                        help='refactoring option')
    parser.add_argument('-j', '--jdeodorant', action='store_true',
                        help='use JDeodorant god classes')
    parser.add_argument('-jp', '--jdeodorant_path',
                        help='path to JDeodorant god classes')
    parser.add_argument('--phase', action='store_true',
                        help='choose one of two phase train or prediction using config.ini')

    args = parser.parse_args()

    # Create/configure the configparser object
    config = configparser.ConfigParser()
    config.read('config.ini')

    # Add the section if it doesn't exist
    if 'DEFAULT' not in config:
        config['DEFAULT'] = {}

    # Set project paths
    if args.path:
        config['DEFAULT']['project_path'] = args.path

    if args.udb:
        config['DEFAULT']['udb_path'] = args.udb

    if args.log:
        config['DEFAULT']['log_path'] = args.log

    # Set refactoring option
    if args.refactoring:
        config['DEFAULT']['refactoring_option'] = args.refactoring

    # Set JDeodorant god classes option
    if args.jdeodorant:
        config['DEFAULT']['jdeodorant_path'] = args.jdeodorant_path
    else:
        config['DEFAULT']['jdeodorant_path'] = None

    # Set two phase train and prediction option
    if args.phase:
        config['DEFAULT']['phase'] = 'train'
    else:
        config['DEFAULT']['phase'] = 'prediction'

    with open('config.ini', 'w') as configfile:
        config.write(configfile)

    # Perform refactoring based on selected options
    if args.refactoring:
        refactoring_function = REFACTORING_MAIN_MAP[args.refactoring]
        refactoring_function(config['DEFAULT']['project_path'],
                             config['DEFAULT']['udb_path'],
                             config['DEFAULT']['log_path'])
    else:
        print("No refactoring option selected.")

    # Print selected options for validation
    print("Project Path:", config['DEFAULT']['project_path'])
    print("UDB Path:", config['DEFAULT']['udb_path'])
    print("Log Path:", config['DEFAULT']['log_path'])
    print("Refactoring Option:", config['DEFAULT']['refactoring_option'])
    print("JDeodorant God Classes Path:", config['DEFAULT']['jdeodorant_path'])
    print("The Phase Train or Prediction:", config['DEFAULT']['phase'])


if __name__ == '__main__':
    main()