from codart.refactorings.abstraction import RefactoringOperation, RefactoringModel
from codart.refactorings import extract_class, move_class, move_method, pushdown_method2, pullup_method, extract_method


class RefactoringManager:
    def __init__(self):
        self.operations = []

    def add_operation(self, operation: RefactoringOperation):
        self.operations.append(operation)

    def execute_operations(self):
        """Execute all the operations in the manager."""
        operation = self.operations.pop()
        operation.execute()
        return operation

    def get_operations(self) -> object:
        return self.operations[len(self.operations) - 1]

    def clear_operations(self):
        """Clear all operations from the list."""
        self.operations.clear()
        print("All operations have been cleared.")

    def list_operations(self):
        """List all the current operations."""
        if not self.operations or len(self.operations) == 0:
            print("No operations to display.")
        else:
            print("Current operations:")
            for i, op in enumerate(self.operations[len(self.operations) - 1]):
                print(f"{i} - {op.__class__.__name__}")

class ExtractClass(RefactoringOperation):
    def __init__(self, udb_path: str = "", moved_methods: list = None, source_class: str = "", file_path: str = "", moved_fields: list = None):
        self._udb_path = udb_path
        self._moved_methods = moved_methods if moved_methods is not None else []
        self._source_class = source_class
        self._file_path = file_path
        self._moved_fields = moved_fields if moved_fields is not None else []

    def execute(self):
        print(f"Extracting class {self._source_class} from {self._file_path}")
        extract_class.main(udb_path=self._udb_path,
                           moved_methods=self._moved_methods,
                           source_class=self._source_class,
                           file_path=self._file_path,
                           moved_fields=self._moved_fields)
    def get_refactoring(self, *args, **kwargs) -> RefactoringModel:
        return RefactoringModel(name="Extracting class", params={"moved_methods": str(self.moved_methods), "source_class": str(self.source_class), "file_path": str(self.file_path), "moved_fields": self._moved_fields})

    def is_empty(self) -> bool:
        return (not self._moved_methods or
                not self._source_class or
                not self._file_path or
                not self._moved_fields)

    @property
    def udb_path(self):
        return self._udb_path

    @udb_path.setter
    def udb_path(self, value: str):
        self._udb_path = value

    @property
    def moved_methods(self):
        return self._moved_methods

    @moved_methods.setter
    def moved_methods(self, value: list):
        self._moved_methods = value

    @property
    def source_class(self):
        return self._source_class

    @source_class.setter
    def source_class(self, value: str):
        self._source_class = value

    @property
    def file_path(self):
        return self._file_path

    @file_path.setter
    def file_path(self, value: str):
        self._file_path = value

    @property
    def moved_fields(self):
        return self._moved_fields

    @moved_fields.setter
    def moved_fields(self, value: list):
        self._moved_fields = value
class MoveClass(RefactoringOperation):
    def __init__(self, udb_path: str = "", source_package: str = "", class_name: str = "", target_package: str = ""):
        self._udb_path = udb_path
        self._source_package = source_package
        self._class_name = class_name
        self._target_package = target_package

    def execute(self):
        print(f"Moving class {self._class_name} from {self._source_package} to {self._target_package}")
        move_class.main(udb_path=self._udb_path,
                        source_package=self._source_package,
                        class_name=self._class_name,
                        target_package=self._target_package)

    def get_refactoring(self, *args, **kwargs) -> RefactoringModel:
        return RefactoringModel(name="Move class", params={
            "source_package": str(self._source_package),
            "class_name": str(self._class_name),
            "target_package": str(self._target_package),
        })

    def is_empty(self) -> bool:
        """Check if the operation has empty or default values."""
        return not (self._source_package and self._class_name and self._target_package)

    @property
    def udb_path(self):
        return self._udb_path

    @udb_path.setter
    def udb_path(self, value: str):
        self._udb_path = value

    @property
    def source_package(self):
        return self._source_package

    @source_package.setter
    def source_package(self, value: str):
        self._source_package = value

    @property
    def class_name(self):
        return self._class_name

    @class_name.setter
    def class_name(self, value: str):
        self._class_name = value

    @property
    def target_package(self):
        return self._target_package

    @target_package.setter
    def target_package(self, value: str):
        self._target_package = value


class PullupMethod(RefactoringOperation):
    def __init__(self, udb_path: str = "", method_name: str = "", children_classes: list = None):
        self._udb_path = udb_path
        self._method_name = method_name
        self._children_classes = children_classes if children_classes is not None else []

    def execute(self):
        print(f"Pulling up method {self._method_name} from {self._children_classes}")
        pullup_method.main(udb_path=self._udb_path,
                           method_name=self._method_name,
                           children_classes=self._children_classes)

    def get_refactoring(self, *args, **kwargs) -> RefactoringModel:
        return RefactoringModel(name="Pull up method", params={
            "method_name": str(self._method_name),
            "children_classes": str(self._children_classes),
        })

    def is_empty(self) -> bool:
        """Check if the method name and children classes are set."""
        return not (self._method_name and self._children_classes)

    @property
    def udb_path(self):
        return self._udb_path

    @udb_path.setter
    def udb_path(self, value: str):
        self._udb_path = value

    @property
    def method_name(self):
        return self._method_name

    @method_name.setter
    def method_name(self, value: str):
        self._method_name = value

    @property
    def children_classes(self):
        return self._children_classes

    @children_classes.setter
    def children_classes(self, value: list):
        self._children_classes = value


class PushdownMethod(RefactoringOperation):
    def __init__(self, udb_path: str = "", method_name: str = "", source_class: str = "", source_package: str = "", target_classes: list = None):
        self._udb_path = udb_path
        self._method_name = method_name
        self._source_class = source_class
        self._source_package = source_package
        self._target_classes = target_classes if target_classes is not None else []

    def execute(self):
        print(f"Pushing down method {self._method_name} from {self._source_class} to {self._target_classes}")
        pushdown_method.main(udb_path=self._udb_path,
                             method_name=self._method_name,
                             source_class=self._source_class,
                             source_package=self._source_package,
                             target_classes=self._target_classes)

    def get_refactoring(self, *args, **kwargs) -> RefactoringModel:
        return RefactoringModel(name="Push down method", params={
            "method_name": str(self._method_name),
            "source_class": str(self._source_class),
            "source_package": str(self._source_package),
            "target_classes": str(self._target_classes),
        })

    def is_empty(self) -> bool:
        return not (self._method_name and self._source_class and self._target_classes)
    @property
    def udb_path(self):
        return self._udb_path

    @udb_path.setter
    def udb_path(self, value: str):
        self._udb_path = value

    @property
    def method_name(self):
        return self._method_name

    @method_name.setter
    def method_name(self, value: str):
        self._method_name = value

    @property
    def source_class(self):
        return self._source_class

    @source_class.setter
    def source_class(self, value: str):
        self._source_class = value

    @property
    def source_package(self):
        return self._source_package

    @source_package.setter
    def source_package(self, value: str):
        self._source_package = value

    @property
    def target_classes(self):
        return self._target_classes

    @target_classes.setter
    def target_classes(self, value: list):
        self._target_classes = value


class MoveMethod(RefactoringOperation):
    def __init__(self, source_class: str = "", method_name: str = "", udb_path: str = "", source_package: str = "", target_package: str = "", target_class: str = ""):
        self._source_class = source_class
        self._method_name = method_name
        self._udb_path = udb_path
        self._source_package = source_package
        self._target_package = target_package
        self._target_class = target_class

    def execute(self):
        print(f"Moving method {self._method_name} from {self._source_class} to {self._target_class}")
        move_method.main(source_class=self._source_class,
                         method_name=self._method_name,
                         udb_path=self._udb_path,
                         source_package=self._source_package,
                         target_package=self._target_package,
                         target_class=self._target_class)

    def get_refactoring(self, *args, **kwargs) -> RefactoringModel:
        return RefactoringModel(name="Move method", params={
            "source_class": str(self._source_class),
            "method_name": str(self._method_name),
            "source_package": str(self._source_package),
            "target_class": str(self._target_class),
        })

    def is_empty(self) -> bool:
        return not (self._source_class and self._method_name and self._target_class)
    @property
    def source_class(self):
        return self._source_class

    @source_class.setter
    def source_class(self, value: str):
        self._source_class = value

    @property
    def method_name(self):
        return self._method_name

    @method_name.setter
    def method_name(self, value: str):
        self._method_name = value

    @property
    def udb_path(self):
        return self._udb_path

    @udb_path.setter
    def udb_path(self, value: str):
        self._udb_path = value

    @property
    def source_package(self):
        return self._source_package

    @source_package.setter
    def source_package(self, value: str):
        self._source_package = value

    @property
    def target_package(self):
        return self._target_package

    @target_package.setter
    def target_package(self, value: str):
        self._target_package = value

    @property
    def target_class(self):
        return self._target_class

    @target_class.setter
    def target_class(self, value: str):
        self._target_class = value


class ExtractMethod(RefactoringOperation):
    def __init__(self, file_path: str = "", lines: object = None):
        self._file_path = file_path
        self._lines = lines

    @property
    def file_path(self):
        return self._file_path

    @file_path.setter
    def file_path(self, value: str):
        self._file_path = value

    @property
    def lines(self):
        return self._lines

    @lines.setter
    def lines(self, value: list):
        self._lines = value

    def execute(self):
        print(f"Extracting method {self._file_path} to {self._lines}")
        extract_method.main(file_path=self.file_path, lines=self.lines)

    def get_refactoring(self, *args, **kwargs) -> RefactoringModel:
        return RefactoringModel(name="Extracting method", params={
            "file_path": self.file_path,
            "lines": str(self.lines),
        })

    def is_empty(self) -> bool:
        return not (self._file_path and self._lines)