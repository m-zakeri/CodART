from javalang import tokenizer
from tabulate import tabulate
import math

operand_list = [
    "Literal",
    "Integer",
    "DecimalInteger",
    "OctalInteger",
    "BinaryInteger",
    "HexInteger",
    "FloatingPoint",
    "DecimalFloatingPoint",
    "HexFloatingPoint",
    "Boolean",
    "Character",
    "String",
    "Null",
    "Annotation",
    "Identifier",
]
br_operands = ["for", "while", "if", "case"]

OPERANDS = set(operand_list)
branchOperators = set(br_operands)


def calculate_cyclomatic(operators):
    return sum(
        [
            operators[cyc_operator]
            for cyc_operator in branchOperators
            if cyc_operator in operators
        ],
        start=1,
    )


def get_operators_operands_count(tokens):
    operands = {}
    operators = {}

    for token in tokens:
        value = token.value

        if token.__class__.__name__ in OPERANDS:
            operands[value] = operands.get(value, 0) + 1
        else:
            operators[value] = operators.get(value, 0) + 1

    return operators, operands


def get_operators_operands_count(tokens):
    operands = {}
    operators = {}

    for token in tokens:
        value = token.value

        if token.__class__.__name__ in OPERANDS:
            operands[value] = operands.get(value, 0) + 1
        else:
            operators[value] = operators.get(value, 0) + 1

    return operators, operands


def calculate_halstead(n1, N1, n2, N2):
    n = n1 + n2
    N = N1 + N2

    estimated_length = n1 * math.log2(n1) + n2 * math.log2(n2)
    purity_ratio = estimated_length / N
    volume = estimated_length * math.log2(n)

    difficulty = (n1 / 2) * (N2 / n2)
    effort = difficulty * volume
    bugs = volume / 3000

    return {
        "Volume (V)": volume,
        "Difficulty (D)": difficulty,
        "Program effort (HEFF)": effort,
        "Number of delivered bugs (HNDB)": bugs,
        "Program vocabulary (HPV)": n,
        "Program length (HPL)": N,
    }


def print_table(data, headers=[], title=None):
    if title:
        print("\n", title, "\n")
    print(tabulate(data.items(), headers=headers, tablefmt="fancy_grid"))


def main_(args):

    with open(args) as file:
        code = file.read()
        tokens = list(tokenizer.tokenize(code))

        operators, operands = get_operators_operands_count(tokens)

        n1 = len(operators)
        n2 = len(operands)
        N1 = sum(operators.values())
        N2 = sum(operands.values())

        print_table(
            {
                "Number of Distinct Operators (n1)": n1,
                "Number of Distinct Operands (n2)": n2,
                "Number of Operators (N1)": N1,
                "Number of Operands (N2)": N2,
                **calculate_halstead(n1, N1, n2, N2),
            },
            ["Metric", "Value"],
            "Halstead Metrics:",
        )

        # print_table(operators, ['Operator', 'Count'], 'Operators:')
        #
        # print_table(operands, ['Operand', 'Count'], 'Operands:')
