# Run speedy-antlr-tool to generate parse accelerator
from speedy_antlr_tool import generate

generate(
    py_parser_path='Java9_v2Parser.py',
    cpp_output_dir='cpp_src',
)