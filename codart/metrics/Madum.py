import os
import sys
from graphviz import Digraph
import json
from codart.utility.directory_utils import create_understand_database
os.add_dll_directory("C:\\Program Files\\SciTools\\bin\\pc-win64\\")
sys.path.append("C:\\Program Files\\SciTools\\bin\\pc-win64\\python")
import understand as und
import pandas as pd
from collections import defaultdict
import json
import copy

# Open the "Understand" project
def open_udb(udb_path):
    try:
        db = und.open(udb_path)
        return db
    except und.UnderstandError as e:
        print(f"Error opening Understand database: {e}")
        return None


# Extract methods and fields of a class
def extract_class_members(class_entity):
    methods = []
    fields = []

    for member in class_entity.ents("Define", "Java Variable"):
        fields.append(member)
    for member in class_entity.ents("Define", "Java Method"):
        method_identifier = f"{member.longname()}({member.parameters()})"
        methods.append((member, method_identifier))  # Include parameter details
        # print("..", member, "..", member.kind(), "..", member.ref() )
    #     for mem in (member.ents("Set, Use, Define, Modify", "Java Variable") +
    #                 member.ents("Define, Use, Set", "Java Parameter")):
    #         fields.append(mem)
        for mem in member.ents("Override", "Java Method"):
            method_identifier = f"{mem.longname()}({mem.parameters()})"
            methods.append((mem, method_identifier))
            # override_methods = []
            # override_methods.append(mem, method_identifier)
            for mem2 in mem.ents("Set, Modify", "Java Variable"):
                fields.append(mem2)
        for mem in member.ents("Set, Modify", "Protected Java Variable"):
            # print("....", mem.kind(), mem.ref())
            fields.append(mem)
    # for member in class_entity.ents("Define, Use", "Java Variable"):
    #     fields.append(member)
    return methods, list(set(fields))


# Extract Enhanced Call Graph (ECG) with categorization
def extract_ecg_with_categories(db):
    ecg = {}

    for class_entity in db.ents("Class"):
        # Ignore external classes (Java SDK, third-party libraries)
        if class_entity.library():
            continue  # Skip classes like java.lang.RuntimeException

        # Ensure the class is defined within the project
        file_ref = class_entity.ref("Definein")
        if not file_ref or not file_ref.file():
            continue  # Skip if there's no valid file reference

        # Get the file path of the class definition
        file_path = file_ref.file().longname()

        print(f"Processing class: {class_entity.longname()} in {file_path}")
        methods_with_identifiers, fields = extract_class_members(class_entity)

        # Build M(C) and F(C)
        M_C = [method_id for _, method_id in methods_with_identifiers]
        F_C = [field.longname() for field in fields]
        # Build Emf and Emm
        Emf = set()
        Emm = set()

        for method, method_id in methods_with_identifiers:
            # Emf: Method -> Field accesses
            method_refs = method.refs()
            return_refs = method.refs("Return")
            for field in fields:
                for ref in method_refs:
                    if ref.ent().longname() == field.longname():
                        ref_kind = ref.kind().name()
                        if method.kind().check("Constructor"):
                            relation = "c"
                        elif ref_kind in ["Set", "Modify", "Write"]:
                            relation = "t"
                        elif any(ref.ent().longname() == field.longname() for ref in return_refs):
                            relation = "r"
                        else:
                            relation = "o"
                        Emf.add((method_id, field.longname(), relation))

            # Emm: Method -> Method calls
            for ref in method.refs("Call, Extend, Define, Override", "Method"):
                callee = ref.ent()
                callee_identifier = f"{callee.longname()}({callee.parameters()})"
                if callee in [m for m, _ in methods_with_identifiers]:
                    Emm.add((method_id, callee_identifier))

        ecg[class_entity.longname()] = {
            "M(C)": M_C,
            "F(C)": F_C,
            # "Method Categories": method_categories,  # Add categories
            "Emf": list(Emf),
            "Emm": list(Emm)
        }

    return ecg


# Visualize or save ECG
def save_ecg_to_file(ecg, output_file):
    with open(output_file, "w") as f:
        json.dump(ecg, f, indent=4)
    print(f"ECG saved to {output_file}")


def visualize_ecg(ecg, output_folder):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    for class_name, data in ecg.items():
        graph = Digraph(format="png", engine="dot")

        # Create individual subgraphs for methods and their accessed fields
        for method in data["M(C)"]:
            subgraph = Digraph(name=f"cluster_{method}")
            subgraph.attr(style="dashed", label=method.split(".")[-1])

            # Add the method node
            subgraph.node(
                method,
                shape="circle",
                style="filled",
                fillcolor="lightblue",
                label="",
                fixedsize="true",
                width="1",
                height="1",
            )

            # Add duplicated field nodes accessed by this method
            for ref_method, field, label in data["Emf"]:
                if ref_method == method:  # Add only the fields accessed by this method
                    field_label = field.split(".")[-1]  # Shorten field name
                    field_node_id = f"{method}_{field}"  # Unique ID for each field duplication
                    subgraph.node(
                        field_node_id,
                        shape="box",
                        style="filled",
                        fillcolor="lightgreen",
                        label=field_label,
                        fixedsize="true",
                        width="1.2",
                        height="1.2",
                        fontsize="10"
                    )
                    subgraph.edge(method, field_node_id, color="orange", style="solid")  # Link method to field

            # Add methods called by this method
            for caller, callee in data["Emm"]:
                if caller == method:
                    callee_label = callee.split(".")[-1]
                    subgraph.node(
                        callee,
                        shape="circle",
                        style="filled",
                        fillcolor="lightblue",
                        label=callee_label,
                        fixedsize="true",
                        width="2",
                        height="2",
                        fontsize="10"
                    )
                    subgraph.edge(method, callee, color="blue", style="solid")  # Link caller to callee

            # Add the subgraph for the method to the main graph
            graph.subgraph(subgraph)

        # Save the graph for the class
        output_file = os.path.join(output_folder, f"{class_name}_ecg")
        graph.render(output_file)
        print(f"Graph for class {class_name} saved to {output_file}.png")

def process_json_and_create_matrices_with_inheritance(json_data):
    data = json.loads(json_data)
    # Create a map to store inheritance relationships
    inheritance_map = defaultdict(list)

    # Detect inheritance relationships between classes
    for class_name, class_data in data.items():
        if "M(C)" in class_data:
            for entry in class_data["M(C)"]:
                # Extract the prefix of the method (class name)
                method_prefix = entry.split(".")[0]
                # If the method belongs to another class, add it to the inheritance map
                if method_prefix != class_name:
                    inheritance_map[class_name].append(method_prefix)

    inherited_classes, non_inherited_classes = {}, {}
    # Dictionary to store matrices for each class
    class_matrices = {}

    # Build base matrices (without inheritance)
    for class_name, class_data in data.items():
        if "M(C)" in class_data:
            columns = []
            # Track seen methods to handle duplicates
            seen_methods = defaultdict(list)

            for method in class_data["M(C)"]:
                # Split method into class and method name
                method_parts = method.split(".")
                method_class = method_parts[0]
                method_name = method_parts[1]

                # Add class name to method name if it's a duplicate
                if method_name in seen_methods:
                    method_name = f"{method_name}'"

                # Track the method and its class
                seen_methods[method_parts[1]].append(method_class)
                columns.append(method_name)

            # Extract rows from "F(C)" entries that belong to the current class
            rows = [entry.split(".", 1)[1].split(".")[-1] for entry in class_data.get("F(C)", []) if class_name + "." in entry]
            # Create the matrix with columns and rows
            matrix = {"columns": columns, "rows": sorted(set(rows))}

            # Store the matrix for the current class
            class_matrices[class_name] = matrix

    # Process classes to identify inherited and non-inherited classes
    for class_name in class_matrices:
        if class_name in inheritance_map:
            # Mark the class as inherited (initialize empty structure)
            inherited_classes[class_name] = {"columns": [], "rows": []}
        else:
            # Add the class to non-inherited classes
            non_inherited_classes[class_name] = class_matrices[class_name]

    # Add parent class rows and columns to inherited classes
    for class_name, parents in inheritance_map.items():
        inherited_matrix = class_matrices[class_name]

        # Collect columns and rows from parent classes
        parent_columns = []
        parent_rows = []
        for parent in parents:
            if parent in class_matrices:
                parent_columns.extend(class_matrices[parent]["columns"])
                parent_rows.extend(class_matrices[parent]["rows"])

        # Remove duplicates while preserving order
        parent_columns = list(dict.fromkeys(parent_columns))
        parent_rows = list(dict.fromkeys(parent_rows))

        # Add parent columns and rows to the beginning of the matrix
        inherited_matrix["columns"] = parent_columns + [col for col in inherited_matrix["columns"] if col not in parent_columns]
        inherited_matrix["rows"] = parent_rows + [row for row in inherited_matrix["rows"] if row not in parent_rows]

        # Store the updated matrix for the inherited class
        inherited_classes[class_name] = inherited_matrix

    # Return the results
    return inherited_classes, non_inherited_classes, inheritance_map

def extract_emf_data(json_data):
    data = json.loads(json_data)
    emf_data = [emf for class_data in data.values() for emf in class_data.get("Emf", [])]
    return emf_data

def create_empty_matrix_for_all_classes(non_inherited_classes, inherited_classes):
    empty_matrices = {}

    # Process non-inherited classes
    for class_name, matrix in non_inherited_classes.items():
        rows, columns = matrix["rows"], matrix["columns"]
        empty_matrix = [[0 for _ in range(len(columns))] for _ in range(len(rows))]
        empty_matrices[class_name] = {"rows": rows, "columns": columns, "matrix": empty_matrix}

    # Process inherited classes
    for class_name, matrix in inherited_classes.items():
        rows, columns = matrix["rows"], matrix["columns"]
        empty_matrix = [[0 for _ in range(len(columns))] for _ in range(len(rows))]
        empty_matrices[class_name] = {"rows": rows, "columns": columns, "matrix": empty_matrix}

    return empty_matrices

def match_emf_data_with_non_inherited(non_inherited_classes, emf_data, empty_matrices):
    emf_matches = []
    # Set to track seen matches and avoid duplicates
    seen_matches = set()

    # Iterate over non-inherited classes and their matrices
    for class_name, matrix in non_inherited_classes.items():
        # Iterate over rows in the matrix
        for row in matrix["rows"]:
            # Iterate over columns in the matrix
            for column in matrix["columns"]:
                # Iterate over EMF data entries
                for emf_entry in emf_data:
                    # Match rows
                    row_match = row == emf_entry[1].split(".")[-1]

                    # Extract method name and parameters from the matrix column
                    column_name = column.split("(")[0]
                    column_params = column.split("(")[1].split(")")[0] if "(" in column else ""

                    # Extract method name and parameters from the EMF entry
                    emf_method_full = emf_entry[0]
                    emf_method_name = emf_method_full.split("(")[0].split(".")[-1]
                    emf_params = emf_method_full.split("(")[1].split(")")[0] if "(" in emf_method_full else ""

                    # Match method names and parameters
                    method_match = column_name == emf_method_name
                    params_match = column_params == emf_params

                    # Match class names
                    class_match = emf_method_full.split(".")[0] == class_name

                    # If all conditions are met
                    if row_match and method_match and params_match and class_match:
                        # Create a unique key for the match
                        match_key = (class_name, row, column, tuple(emf_entry))

                        # Check if the match has already been processed
                        if match_key not in seen_matches:
                            # Add the match to the seen set
                            seen_matches.add(match_key)
                            # Add the match to the results list
                            emf_matches.append({
                                "class": class_name,
                                "row": row,
                                "column": column,
                                "emf_entry": emf_entry
                            })

                            # Update the matrix with EMF data
                            row_idx = matrix["rows"].index(row)
                            col_idx = matrix["columns"].index(column)
                            type_value = emf_entry[2] if len(emf_entry) > 2 else "Unknown"
                            empty_matrices[class_name]["matrix"][row_idx][col_idx] = type_value

    return emf_matches

def process_method_category(method_category):
    return method_category.split(".", 1)[1]

def extract_column_and_type(method_categories):
    return [{"column_name": process_method_category(method), "type": method_type} for method, method_type in method_categories.items()]

def update_matrix(empty_matrices):
    for class_name, matrix_data in empty_matrices.items():
        for i, row in enumerate(matrix_data["rows"]):
            for j, column in enumerate(matrix_data["columns"]):
                if isinstance(matrix_data["matrix"][i][j], str):
                    matrix_data["matrix"][i][j] = f"{matrix_data['matrix'][i][j]}"  # No subscript added here
    return empty_matrices


def draw_matrices_with_pandas(matrices, title):
    print(f"\n{title}:\n" + "="*50)
    for class_name, matrix_data in matrices.items():
        columns_with_params = []
        for col in matrix_data["columns"]:
            if "(" in col:
                columns_with_params.append(col)
            else:
                columns_with_params.append(col)

        df = pd.DataFrame(matrix_data["matrix"], index=matrix_data["rows"], columns=columns_with_params)
        print(f"\nMatrix for class: {class_name}")
        print(df)
        print("-" * 50)



json_file_path = 'ecg_output_with_categories.json'
with open(json_file_path, 'r') as file:
    json_input = file.read()


emf_data = extract_emf_data(json_input)
inherited_classes, non_inherited_classes, inheritance_map = process_json_and_create_matrices_with_inheritance(json_input)

empty_matrices = create_empty_matrix_for_all_classes(non_inherited_classes, inherited_classes)
pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
pd.set_option('display.width', None)

draw_matrices_with_pandas(empty_matrices, "Empty Matrices for All Classes")


emf_matches = match_emf_data_with_non_inherited(non_inherited_classes, emf_data, empty_matrices)

first_level_dum = update_matrix(empty_matrices)
pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
pd.set_option('display.width', None)

first_level_dum_non_inherited = {
    class_name: matrix_data
    for class_name, matrix_data in first_level_dum.items()
    if class_name in non_inherited_classes
}

draw_matrices_with_pandas(first_level_dum_non_inherited, "First Level DUM (Non-Inherited Classes)")

def propagate_values_based_on_emm(first_level_dum_non_inherited, empty_matrices, emm_data):

    # Create a call graph from the emm_data (mapping each caller to a list of callees)
    call_graph = {}
    for caller, callee in emm_data:
        call_graph.setdefault(caller, []).append(callee)

    # Helper function to find all the final methods called by a specific method
    def get_final_methods(method, visited):
        # If method is not in the call graph or already visited, return the method itself as a set
        if method not in call_graph or method in visited:
            return {method}  # Return a set containing the method

        visited.add(method)
        final_methods = set()

        # Recursively find all methods called by the current method
        for next_method in call_graph[method]:
            final_methods.update(get_final_methods(next_method, visited))

        return final_methods if final_methods else {method}  # Return the final methods if found, else the current method

    # Iterate through all the matrices to update their values
    for class_name, matrix_data in empty_matrices.items():
        # Skip the class if it's not in the first level of non-inherited methods
        if class_name not in first_level_dum_non_inherited:
            continue

        source_matrix = first_level_dum_non_inherited[class_name]  # Get the source matrix for the class

        # Loop through rows and columns in the matrix
        for row in matrix_data["rows"]:
            for col in matrix_data["columns"]:
                method_key = f"{class_name}.{col}"  # Create a full method name

                # Check if the method is part of the call graph
                if method_key in call_graph:
                    final_methods = get_final_methods(method_key, set())  # Get all final methods for the current method

                    for final_method in final_methods:
                        final_method_name = final_method.split("(")[0].split(".")[-1]  # Extract the method name
                        final_method_params = final_method.split("(")[1].split(")")[0] if "(" in final_method else ""  # Extract parameters

                        # Check if the final method matches an existing method in the source matrix
                        for existing_col in source_matrix["columns"]:
                            existing_col_name = existing_col.split("(")[0]  # Extract the column (method) name
                            existing_col_params = existing_col.split("(")[1].split(")")[
                                0] if "(" in existing_col else ""  # Extract parameters

                            # If the method and its parameters match, update the matrix value
                            if final_method_name == existing_col_name and final_method_params == existing_col_params:
                                row_idx, col_idx = matrix_data["rows"].index(row), matrix_data["columns"].index(col)
                                final_col_idx = source_matrix["columns"].index(existing_col)
                                final_value = source_matrix["matrix"][row_idx][final_col_idx]

                                # If the final value is non-zero, update the empty matrix
                                if final_value != 0:
                                    matrix_data["matrix"][row_idx][col_idx] = final_value

    return empty_matrices



def extract_emm_data_for_non_inherited(json_file_path, non_inherited_classes):
    with open(json_file_path, 'r', encoding='utf-8') as file:
        json_data = file.read()

    # Check if the file is not empty or just whitespace
    if not json_data.strip():
        raise ValueError("JSON file is empty or contains only whitespace.")

    try:
        data = json.loads(json_data)
    except json.JSONDecodeError as e:
        # Raise an error if the JSON format is invalid
        raise ValueError(f"Invalid JSON format: {e}")

    emm_data = []

    # Iterate through the classes in the parsed JSON data
    for class_name, class_data in data.items():
        # If the class is in the list of non-inherited classes, extract its 'Emm' data
        if class_name in non_inherited_classes:
            emm_data.extend(class_data.get("Emm", []))  # Add the "Emm" data to the result list

    return emm_data



emm_data = extract_emm_data_for_non_inherited(json_file_path, non_inherited_classes)

# Run the propagation and draw the updated matrices
updated_matrices = propagate_values_based_on_emm(first_level_dum_non_inherited, empty_matrices, emm_data)
draw_matrices_with_pandas(updated_matrices, "Updated Matrices After Propagation")

def extract_nonzero_columns(matrices):
    u_1 = []
    for class_name, matrix_data in matrices.items():
        for j, column in enumerate(matrix_data["columns"]):
            has_nonzero = any(matrix_data["matrix"][i][j] != 0 for i in range(len(matrix_data["rows"])))
            if has_nonzero:
                u_1.append(column)
    return u_1

def find_related_columns_for_non_inherited(u_1, emm_data):
    related_pairs = []
    for pair in emm_data:
        method1 = pair[0].split(".")[1]
        method2 = pair[1].split(".")[1]
        if method1 in u_1 or method2 in u_1:
            related_pairs.append([method1, method2])
    return related_pairs

def filter_related_pairs(matrices, related_pairs):
    filtered_pairs = []  # List to store filtered related pairs
    # Iterate through each related pair
    for pair in related_pairs:
        element1, element2 = pair
        # Iterate through each class and its matrix data
        for class_name, matrix_data in matrices.items():
            # If element2 exists in the columns of the class, check for non-zero values
            if element2 in matrix_data["columns"]:
                col_idx = matrix_data["columns"].index(element2)  # Get the index of element2 in the columns
                # Check if any value in the column corresponding to element2 is non-zero
                has_nonzero = any(matrix_data["matrix"][i][col_idx] != 0 for i in range(len(matrix_data["rows"])))
                if has_nonzero:  # If a non-zero value is found, add the pair to filtered_pairs
                    filtered_pairs.append(pair)
                break  # No need to continue checking for other columns in this class
    return filtered_pairs  # Return the filtered list of related pairs

u_1 = extract_nonzero_columns(first_level_dum)
related_pairs_non_inherited = find_related_columns_for_non_inherited(u_1, emm_data)
print(related_pairs_non_inherited)
filtered_pairs = filter_related_pairs(first_level_dum, related_pairs_non_inherited)

def update_final_list_based_on_filtered_pairs(emf_matches, filtered_pairs):
    # Step 1: Create result list
    result = [[entry['row'], entry['column']] for entry in emf_matches]

    # Step 2: Create a dictionary where the key is the second element of the pair and the value is a list of first elements
    list2_dict = defaultdict(list)
    for item in filtered_pairs:
        list2_dict[item[1]].append(item[0])

    # Step 3: Initialize final_list by processing result and adding related elements from list2_dict
    final_list = []
    for item in result:
        if item[1] in list2_dict:
            for value in list2_dict[item[1]]:
                final_list.append(item + [value])
        else:
            final_list.append(item)

    # Step 4: Create the updated_final_list by adding matching pairs from filtered_pairs
    updated_final_list = []
    processed_indices = set()
    for item in final_list:
        if item[-1] in [pair[1] for pair in filtered_pairs]:
            matching_pairs = [pair[0] for pair in filtered_pairs if pair[1] == item[-1]]
            for pair_value in matching_pairs:
                updated_item = item + [pair_value]
                updated_final_list.append(updated_item)
            processed_indices.add(tuple(item))
        elif tuple(item) not in processed_indices:
            updated_final_list.append(item)

    return updated_final_list
updated_final_list = update_final_list_based_on_filtered_pairs(emf_matches, filtered_pairs)

def create_dum_with_conditions(matrices, fourth_matrix, updated_final_list):
    fifth_level_dum = {}

    # Iterate through each class and its associated matrix data
    for class_name, matrix_data in matrices.items():
        rows = matrix_data["rows"]
        columns = matrix_data["columns"]
        fourth_matrix_data = fourth_matrix[class_name]["matrix"]  # Get the fourth level matrix for the class
        fifth_matrix = copy.deepcopy(fourth_matrix_data)  # Create a deep copy of the fourth matrix to modify it

        # Iterate through the updated_final_list to apply conditions for each item
        for item in updated_final_list:
            if len(item) >= 4:
                # If item has 4 elements: row_name, col1, col2, col3
                row_name, col1, col2, col3 = item
                # Check if row_name is in rows and col1, col2, col3 are in columns
                if row_name in rows and col1 in columns and col2 in columns and col3 in columns:
                    row_idx = rows.index(row_name)  # Get the index of the row
                    col1_idx = columns.index(col1)  # Get the index of col1
                    col2_idx = columns.index(col2)  # Get the index of col2
                    col3_idx = columns.index(col3)  # Get the index of col3
                    # Get the values from the fourth matrix for these columns
                    value1 = fourth_matrix_data[row_idx][col1_idx]
                    value2 = fourth_matrix_data[row_idx][col2_idx]
                    value3 = fourth_matrix_data[row_idx][col3_idx]
                    # If value1 equals value2, update the fifth matrix with a marked value
                    if value1 == value2:
                        fifth_matrix[row_idx][col2_idx] = [value2, "R"]
                    # If value2 equals value3, update the fifth matrix with a marked value
                    if value2 == value3:
                        fifth_matrix[row_idx][col3_idx] = [value3, "R"]

            elif len(item) == 3:
                # If item has 3 elements: row_name, col1, col2
                row_name, col1, col2 = item
                # Check if row_name is in rows and col1, col2 are in columns
                if row_name in rows and col1 in columns and col2 in columns:
                    row_idx = rows.index(row_name)  # Get the index of the row
                    col1_idx = columns.index(col1)  # Get the index of col1
                    col2_idx = columns.index(col2)  # Get the index of col2
                    # Get the values from the fourth matrix for these columns
                    value1 = fourth_matrix_data[row_idx][col1_idx]
                    value2 = fourth_matrix_data[row_idx][col2_idx]
                    # If value1 equals value2, update the fifth matrix with a marked value
                    if value1 == value2:
                        fifth_matrix[row_idx][col2_idx] = [value2, "R"]

            elif len(item) == 2:
                # If item has 2 elements: row_name, col_name
                row_name, col_name = item
                # Check if row_name is in rows and col_name is in columns
                if row_name in rows and col_name in columns:
                    row_idx = rows.index(row_name)  # Get the index of the row
                    col_idx = columns.index(col_name)  # Get the index of col_name
                    # Get the value from the fourth matrix
                    value = fourth_matrix_data[row_idx][col_idx]
                    # Set the value in the fifth matrix
                    fifth_matrix[row_idx][col_idx] = value

        # Save the modified matrix to the fifth_level_dum dictionary for this class
        fifth_level_dum[class_name] = {"rows": rows, "columns": columns, "matrix": fifth_matrix}

    return fifth_level_dum  # Return the populated fifth level matrix data

fifth_level_dum_with_conditions = create_dum_with_conditions(
    non_inherited_classes, updated_matrices, updated_final_list
)
draw_matrices_with_pandas(fifth_level_dum_with_conditions, " DUM with Conditions (Non-Inherited Classes)")

def create_madum_from_fifth_level(fifth_level_dum_with_conditions):
    madum = {}

    for class_name, matrix_data in fifth_level_dum_with_conditions.items():
        rows = matrix_data["rows"]
        columns = matrix_data["columns"]
        fifth_matrix_data = matrix_data["matrix"]

        madum_matrix = []
        for row in fifth_matrix_data:
            new_row = []
            for cell in row:
                # Case 1: If the cell is a list and contains "R", replace it with [0] (in a list)
                if isinstance(cell, list) and "R" in cell:
                    new_row.append([0])  # Append 0 in a list
                # Case 2: If the cell is a list and is not a list of "R", append the first character of the first element
                elif isinstance(cell, list) and isinstance(cell[0], str):
                    new_row.append(cell[0][0])  # Only append the first character of the first element
                # Case 3: If the cell is not a list (like an integer), retain the original value
                else:
                    new_row.append(cell)  # Keep the original value (like an integer)

            madum_matrix.append(new_row)

        madum[class_name] = {"rows": rows, "columns": columns, "matrix": madum_matrix}

    return madum

madum = create_madum_from_fifth_level(fifth_level_dum_with_conditions)

draw_matrices_with_pandas(madum, "Madum Matrix (Non-Inherited Classes)")


def update_inherited_classes_with_madum(madum, inherited_classes, inheritance_map):
    """
    Updates the inherited_classes with values from madum for shared rows and columns.

    Parameters:
    - madum (dict): MADUM matrix containing the base values.
    - inherited_classes (dict): Classes that inherit from other classes.
    - inheritance_map (dict): A map of classes to their parent classes.

    Returns:
    - dict: The updated inherited_classes with values populated from madum.
    """
    # Make a deep copy of inherited_classes to ensure original data is not modified
    updated_inherited_classes = copy.deepcopy(inherited_classes)

    # Iterate through each child class and its parent classes
    for child_class, parent_classes in inheritance_map.items():
        # For each parent class of the child class
        for parent_class in parent_classes:
            # If both the parent class exists in madum and the child class in inherited_classes, proceed
            if parent_class in madum and child_class in inherited_classes:
                parent_matrix = madum[parent_class]  # Get the matrix for the parent class
                child_matrix = updated_inherited_classes[child_class]  # Get the matrix for the child class

                # Extract rows, columns, and matrix values from parent and child matrices
                parent_rows, parent_columns, parent_values = (
                    parent_matrix["rows"],
                    parent_matrix["columns"],
                    parent_matrix["matrix"],
                )
                child_rows, child_columns = (
                    child_matrix["rows"],
                    child_matrix["columns"],
                )

                # Initialize the matrix for the child class if it doesn't exist or is empty
                if "matrix" not in child_matrix or not child_matrix["matrix"]:
                    child_matrix["matrix"] = [[0 for _ in range(len(child_columns))] for _ in range(len(child_rows))]

                # Copy values from the parent matrix to the child matrix if the rows and columns match
                for i, row in enumerate(child_rows):
                    if row in parent_rows:
                        parent_row_idx = parent_rows.index(row)
                        for j, col in enumerate(child_columns):
                            if col in parent_columns:
                                parent_col_idx = parent_columns.index(col)
                                # Copy the value from the parent matrix to the child matrix
                                child_matrix["matrix"][i][j] = parent_values[parent_row_idx][parent_col_idx]

    return updated_inherited_classes

updated_inherited_matrices = update_inherited_classes_with_madum(madum, inherited_classes, inheritance_map)

draw_matrices_with_pandas(updated_inherited_matrices, "Fill Quadrant II")

def update_inherited_matrices_with_emf(updated_inherited_matrices, emf_data):
    """
    Updates the updated_inherited_matrices with values from emf_data for inherited_classes only.

    Parameters:
    - updated_inherited_matrices (dict): The updated version of inherited_classes, previously populated with MADUM.
    - emf_data (list): A list of Emf data.

    Returns:
    - dict: The updated_inherited_matrices with values filled from Emf.
    """
    # Create a deep copy of updated_inherited_matrices to avoid modifying the original data
    updated_matrices = copy.deepcopy(updated_inherited_matrices)

    # Iterate through each class's matrix in the updated_matrices
    for class_name, matrix_data in updated_matrices.items():
        rows, columns = matrix_data["rows"], matrix_data["columns"]

        # Initialize the matrix if it hasn't been initialized yet
        if "matrix" not in matrix_data or not matrix_data["matrix"]:
            matrix_data["matrix"] = [[0 for _ in range(len(columns))] for _ in range(len(rows))]

        matrix = matrix_data["matrix"]

        # Iterate through each entry in the emf_data list
        for emf_entry in emf_data:
            method_full, attribute_full, value_type = emf_entry

            # Extract the class and method/attribute names from the full strings
            method_class, method_name = method_full.split(".", 1)
            attribute_class, attribute_name = attribute_full.split(".", 1)

            # Check if the class matches the inherited class and both method and attribute belong to the same class
            if class_name == method_class == attribute_class:
                # Find possible columns that match the method name
                possible_methods = [col for col in columns if col.startswith(method_name)]

                if len(possible_methods) > 1:
                    # If there are multiple methods (overrides), select the version with `reset()` at the end
                    overridden_method_name = next((col for col in possible_methods if col.endswith("'")), method_name)
                else:
                    # If only one method is found, select it
                    overridden_method_name = method_name

                # Fill the matrix only if both the row and column are found
                if overridden_method_name in columns and attribute_name in rows:
                    row_idx = rows.index(attribute_name)
                    col_idx = columns.index(overridden_method_name)
                    matrix[row_idx][col_idx] = value_type  # Assign the value (`o` or `t`) to the matrix

    return updated_matrices

final_updated_inherited_matrices = update_inherited_matrices_with_emf(updated_inherited_matrices, emf_data)

draw_matrices_with_pandas(final_updated_inherited_matrices, "Fill Quadrant IV")



# Main Function
# def main():
#     path = "C:/Users/98910/Desktop/test_ECG2"
#     udb_path = create_understand_database(path, path)
#     output_file = "ecg_output_with_categories.json"  # Output file for ECG
#     output_folder = "ecg_graphs"  # Folder for Graphviz output
#
#     db = open_udb(udb_path)
#     if db:
#         ecg = extract_ecg_with_categories(db)
#         save_ecg_to_file(ecg, output_file)
#         visualize_ecg(ecg, output_folder)
#         db.close()
#
#
# if __name__ == "__main__":
#     main()
