import argparse
from pathlib import Path
from refactorings.extract_class import main
from configparser import ConfigParser
import git
import os

def save_config(
        refactor_types: str = None,
        sys_path_object: str = None,
        sys_path_index: int = None,
        os_environs_key: str = None,
        os_environs_value: str = None,
        core_option: int = None,
) -> None:
    config = ConfigParser()
    config.read("config.ini")

    # Update or create the 'REFACTORING' section if refactor_types is not None
    if refactor_types is not None:
        if not config.has_section("REFACTORING"):
            config.add_section("REFACTORING")
        config.set("REFACTORING", "types", refactor_types)

    # Update or create the 'UNDERSTAND' section if sys_path_object is not None
    if sys_path_object is not None:
        if not config.has_section("UNDERSTAND"):
            config.add_section("UNDERSTAND")
        config.set("UNDERSTAND", "sys_path_object", sys_path_object)

    if sys_path_index is not None:  # Update sys_path_index
        if not config.has_section("UNDERSTAND"):
            config.add_section("UNDERSTAND")
        config.set("UNDERSTAND", "sys_path_index", str(sys_path_index))

    if os_environs_key is not None:  # Update os_environs_key
        if not config.has_section("UNDERSTAND"):
            config.add_section("UNDERSTAND")
        config.set("UNDERSTAND", "os_environs_key", os_environs_key)

    if os_environs_value is not None:  # Update os_environs_value
        if not config.has_section("UNDERSTAND"):
            config.add_section("UNDERSTAND")
        config.set("UNDERSTAND", "os_environs_value", os_environs_value)

    # Update or create the 'CORE' section if core_option is not None
    if core_option is not None:
        if not config.has_section("CORE"):
            config.add_section("CORE")
        config.set("CORE", "option", str(core_option))

    with open("../config.ini", "w") as configfile:
        config.write(configfile)
def main_cli():
    parser = argparse.ArgumentParser(
        description='CLI for Extract Class Refactoring')
    parser.add_argument('--udb_path', type=str, help='Path to the UDB file')
    parser.add_argument('--file_path', type=str,
                        help='Path to the Java source file')
    parser.add_argument('--source_class', type=str,
                        help='Name of the source class')
    parser.add_argument('--moved_fields', nargs='+',
                        help='List of fields to be moved')
    parser.add_argument('--moved_methods', nargs='+',
                        help='List of methods to be moved')
    parser.add_argument('--core', nargs='+', type=int,
                        help='understand or openunderstand (0\\1)')
    parser.add_argument('--project-path', type=str, nargs='+',
                        help='project path ')
    args = parser.parse_args()
    repo_path = args.project_path[0]
    assert os.path.isdir(repo_path)
    print('Reverted back to the original state successfully.')
    new_class = f"{args.source_class}Extracted"
    new_file_path = Path(args.file_path).parent / f"{new_class}.java"
    core_option = args.core[0]
    save_config(core_option=core_option)
    result = main(
        udb_path=args.udb_path,
        file_path=args.file_path,
        source_class=args.source_class,
        moved_fields=args.moved_fields,
        moved_methods=args.moved_methods,
        new_file_path=str(new_file_path)
    )

    if result:
        print(
            f"The refactoring process was successful. The new class file is created at: {new_file_path}")
    else:
        print("The refactoring process encountered an error.")


if __name__ == "__main__":
    main_cli()