#!/usr/bin/env python3
import sys
import os
import understand


def check_for_classes(db_path):
    """
    Check if an Understand database contains any classes.

    Args:
        db_path (str): Path to the .und database file

    Returns:
        bool: True if classes exist, False otherwise
    """
    try:
        # Open the database
        db = understand.open(db_path)

        # Get all entities of kind "class"
        classes = db.ents("class")

        # Print the number of classes found
        print(f"Found {len(classes)} classes in the database.")

        # Print each class if any exist
        if classes:
            print("\nClasses found:")
            for cls in classes:
                print(f" - {cls.longname()} [{cls.language()}]")
            return True
        else:
            print("No classes found in the database.")
            return False

    except understand.UnderstandError as e:
        print(f"Error: {e}")
        return False
    finally:
        # Close the database if it was opened
        if 'db' in locals() and db:
            db.close()


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print(f"Usage: {sys.argv[0]} <path_to_und_file>")
        sys.exit(1)

    db_path = sys.argv[1]

    # Check if the file exists and is a .und file
    if not os.path.exists(db_path):
        print(f"Error: File {db_path} does not exist.")
        sys.exit(1)

    if not db_path.endswith('.und'):
        print(f"Warning: File {db_path} does not have a .und extension.")

    check_for_classes(db_path)