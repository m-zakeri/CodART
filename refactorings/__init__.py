# from refactorings import collapse_hierarchy
from . import make_field_static, make_field_non_static

refactoring_map = {
    'make_field_static': make_field_static,
    'make_field_non_static': make_field_non_static
}
