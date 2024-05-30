#!/bin/bash
cd "$( dirname "${BASH_SOURCE[0]}" )"



# Generate C++ target with visitor
antlr4 -Dlanguage=Cpp -o antlr4-runtime JavaLexer.g4
antlr4 -Dlanguage=Cpp -visitor -no-listener -o antlr4-runtime JavaLabeledParser.g4

# Generate Python target
antlr4 -Dlanguage=Python3 -o . JavaLexer.g4
antlr4 -Dlanguage=Python3 -no-visitor -no-listener -o . JavaLabeledParser.g4

# Run speedy-antlr-tool to generate parse accelerator
python3 <<EOF
from speedy_antlr_tool import generate

generate(
    py_parser_path="JavaLabeledParser.py",
    cpp_output_dir="antlr4-runtime",
)
EOF