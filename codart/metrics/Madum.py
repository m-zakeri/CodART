import os
import sys
from graphviz import Digraph
from codart.utility.directory_utils import create_understand_database
import understand as und
import copy
import json
import copy
import pandas as pd
from collections import defaultdict


os.add_dll_directory("C:\\Program Files\\SciTools\\bin\\pc-win64\\")
sys.path.append("C:\\Program Files\\SciTools\\bin\\pc-win64\\python")


class ECGExtractor:
    def __init__(self, udb_path):
        self.udb_path = udb_path
        self.db = self.open_udb()

    def open_udb(self):
        try:
            db = und.open(self.udb_path)
            return db
        except und.UnderstandError as e:
            print(f"Error opening Understand database: {e}")
            return None

    def extract_class_members(self, class_entity):
        methods = []
        fields = []

        for member in class_entity.ents("Define", "Java Variable"):
            fields.append(member)
        for member in class_entity.ents("Define", "Java Method"):
            method_identifier = f"{member.longname()}({member.parameters()})"
            methods.append((member, method_identifier))  # Include parameter details
            for mem in member.ents("Override", "Java Method"):
                method_identifier = f"{mem.longname()}({mem.parameters()})"
                methods.append((mem, method_identifier))
                for mem2 in mem.ents("Set, Modify", "Java Variable"):
                    fields.append(mem2)
            for mem in member.ents("Set, Modify", "Protected Java Variable"):
                fields.append(mem)
        return methods, list(set(fields))

    def extract_ecg_with_categories(self):
        ecg = {}

        for class_entity in self.db.ents("Class"):
            if class_entity.library():
                continue  # Skip classes like java.lang.RuntimeException

            file_ref = class_entity.ref("Definein")
            if not file_ref or not file_ref.file():
                continue  # Skip if there's no valid file reference

            file_path = file_ref.file().longname()
            print(f"Processing class: {class_entity.longname()} in {file_path}")
            methods_with_identifiers, fields = self.extract_class_members(class_entity)

            M_C = [method_id for _, method_id in methods_with_identifiers]
            F_C = [field.longname() for field in fields]
            Emf = set()
            Emm = set()

            for method, method_id in methods_with_identifiers:
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

                for ref in method.refs("Call, Extend, Define, Override", "Method"):
                    callee = ref.ent()
                    callee_identifier = f"{callee.longname()}({callee.parameters()})"
                    if callee in [m for m, _ in methods_with_identifiers]:
                        Emm.add((method_id, callee_identifier))

            ecg[class_entity.longname()] = {
                "M(C)": M_C,
                "F(C)": F_C,
                "Emf": list(Emf),
                "Emm": list(Emm)
            }

        return ecg

    def save_ecg_to_file(self, ecg, output_file):
        with open(output_file, "w") as f:
            json.dump(ecg, f, indent=4)
        print(f"ECG saved to {output_file}")

    def visualize_ecg(self, ecg, output_folder):
        if not os.path.exists(output_folder):
            os.makedirs(output_folder)

        for class_name, data in ecg.items():
            graph = Digraph(format="png", engine="dot")

            for method in data["M(C)"]:
                subgraph = Digraph(name=f"cluster_{method}")
                subgraph.attr(style="dashed", label=method.split(".")[-1])

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

                for ref_method, field, label in data["Emf"]:
                    if ref_method == method:
                        field_label = field.split(".")[-1]
                        field_node_id = f"{method}_{field}"
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
                        subgraph.edge(method, field_node_id, color="orange", style="solid")

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
                        subgraph.edge(method, callee, color="blue", style="solid")

                graph.subgraph(subgraph)

            output_file = os.path.join(output_folder, f"{class_name}_ecg")
            graph.render(output_file)
            print(f"Graph for class {class_name} saved to {output_file}.png")


class MatrixProcessor:
    def process_json_and_create_matrices_with_inheritance(self, json_data):
        data = json.loads(json_data)

        inheritance_map = defaultdict(list)

        for class_name, class_data in data.items():
            if "M(C)" in class_data:
                for entry in class_data["M(C)"]:
                    method_prefix = entry.split(".")[0]
                    if method_prefix != class_name:
                        inheritance_map[class_name].append(method_prefix)

        inherited_classes, non_inherited_classes = {}, {}
        class_matrices = {}

        for class_name, class_data in data.items():
            if "M(C)" in class_data:
                columns = []
                seen_methods = defaultdict(list)
                for method in class_data["M(C)"]:
                    method_parts = method.split(".")
                    method_class = method_parts[0]
                    method_name = method_parts[1]
                    if method_name in seen_methods:
                        method_name = f"{method_name}'"
                    seen_methods[method_parts[1]].append(method_class)
                    columns.append(method_name)

                rows = [entry.split(".", 1)[1].split(".")[-1] for entry in class_data.get("F(C)", []) if
                        class_name + "." in entry]
                matrix = {"columns": columns, "rows": sorted(set(rows))}
                class_matrices[class_name] = matrix

        for class_name in class_matrices:
            if class_name in inheritance_map:
                inherited_classes[class_name] = {"columns": [], "rows": []}
            else:
                non_inherited_classes[class_name] = class_matrices[class_name]

        for class_name, parents in inheritance_map.items():
            inherited_matrix = class_matrices[class_name]
            parent_columns = []
            parent_rows = []
            for parent in parents:
                if parent in class_matrices:
                    parent_columns.extend(class_matrices[parent]["columns"])
                    parent_rows.extend(class_matrices[parent]["rows"])

            parent_columns = list(dict.fromkeys(parent_columns))
            parent_rows = list(dict.fromkeys(parent_rows))

            inherited_matrix["columns"] = parent_columns + [col for col in inherited_matrix["columns"] if
                                                            col not in parent_columns]
            inherited_matrix["rows"] = parent_rows + [row for row in inherited_matrix["rows"] if row not in parent_rows]
            inherited_classes[class_name] = inherited_matrix

        return inherited_classes, non_inherited_classes, inheritance_map

    def extract_emf_data(self, json_data):
        data = json.loads(json_data)
        emf_data = [emf for class_data in data.values() for emf in class_data.get("Emf", [])]
        return emf_data

    def create_empty_matrix_for_all_classes(self, non_inherited_classes, inherited_classes):
        empty_matrices = {}
        for class_name, matrix in non_inherited_classes.items():
            rows, columns = matrix["rows"], matrix["columns"]
            empty_matrix = [[0 for _ in range(len(columns))] for _ in range(len(rows))]
            empty_matrices[class_name] = {"rows": rows, "columns": columns, "matrix": empty_matrix}

        for class_name, matrix in inherited_classes.items():
            rows, columns = matrix["rows"], matrix["columns"]
            empty_matrix = [[0 for _ in range(len(columns))] for _ in range(len(rows))]
            empty_matrices[class_name] = {"rows": rows, "columns": columns, "matrix": empty_matrix}

        return empty_matrices

    def match_emf_data_with_non_inherited(self, non_inherited_classes, emf_data, empty_matrices):
        emf_matches = []
        seen_matches = set()

        for class_name, matrix in non_inherited_classes.items():
            for row in matrix["rows"]:
                for column in matrix["columns"]:
                    for emf_entry in emf_data:
                        row_match = row == emf_entry[1].split(".")[-1]
                        column_name = column.split("(")[0]
                        column_params = column.split("(")[1].split(")")[0] if "(" in column else ""
                        emf_method_full = emf_entry[0]
                        emf_method_name = emf_method_full.split("(")[0].split(".")[-1]
                        emf_params = emf_method_full.split("(")[1].split(")")[0] if "(" in emf_method_full else ""
                        method_match = column_name == emf_method_name
                        params_match = column_params == emf_params
                        class_match = emf_method_full.split(".")[0] == class_name

                        if row_match and method_match and params_match and class_match:
                            match_key = (class_name, row, column, tuple(emf_entry))
                            if match_key not in seen_matches:
                                seen_matches.add(match_key)
                                emf_matches.append({
                                    "class": class_name,
                                    "row": row,
                                    "column": column,
                                    "emf_entry": emf_entry
                                })
                                row_idx = matrix["rows"].index(row)
                                col_idx = matrix["columns"].index(column)
                                type_value = emf_entry[2] if len(emf_entry) > 2 else "Unknown"
                                empty_matrices[class_name]["matrix"][row_idx][col_idx] = type_value

        return emf_matches

    def update_matrix(self, empty_matrices):
        for class_name, matrix_data in empty_matrices.items():
            for i, row in enumerate(matrix_data["rows"]):
                for j, column in enumerate(matrix_data["columns"]):
                    if isinstance(matrix_data["matrix"][i][j], str):
                        matrix_data["matrix"][i][j] = f"{matrix_data['matrix'][i][j]}"  # No subscript added here
        return empty_matrices

    def draw_matrices_with_pandas(self, matrices, title):
        print(f"\n{title}:\n" + "=" * 50)
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

    def propagate_values_based_on_emm(self, first_level_dum_non_inherited, empty_matrices, emm_data):
        call_graph = {}
        for caller, callee in emm_data:
            call_graph.setdefault(caller, []).append(callee)

        def get_final_methods(method, visited):
            if method not in call_graph or method in visited:
                return {method}  # Return the method itself if no further calls

            visited.add(method)
            final_methods = set()

            for next_method in call_graph[method]:
                final_methods.update(get_final_methods(next_method, visited))

            return final_methods if final_methods else {method}  # Return method itself if no further calls

        for class_name, matrix_data in empty_matrices.items():
            if class_name not in first_level_dum_non_inherited:
                continue

            source_matrix = first_level_dum_non_inherited[class_name]  # Source matrix for propagation

            for row in matrix_data["rows"]:
                for col in matrix_data["columns"]:
                    method_key = f"{class_name}.{col}"  # Method key for call graph

                    if method_key in call_graph:
                        final_methods = get_final_methods(method_key, set())  # Get final methods

                        for final_method in final_methods:
                            final_method_name = final_method.split("(")[0].split(".")[-1]  # Extract method name
                            final_method_params = final_method.split("(")[1].split(")")[
                                0] if "(" in final_method else ""  # Extract method parameters

                            for existing_col in source_matrix["columns"]:
                                existing_col_name = existing_col.split("(")[0]  # Extract column name
                                existing_col_params = existing_col.split("(")[1].split(")")[
                                    0] if "(" in existing_col else ""  # Extract column parameters

                                if final_method_name == existing_col_name and final_method_params == existing_col_params:
                                    row_idx, col_idx = matrix_data["rows"].index(row), matrix_data["columns"].index(col)
                                    final_col_idx = source_matrix["columns"].index(existing_col)
                                    final_value = source_matrix["matrix"][row_idx][final_col_idx]

                                    if final_value != 0:
                                        matrix_data["matrix"][row_idx][col_idx] = final_value

        return empty_matrices

    def extract_emm_data_for_non_inherited(self, json_file_path, non_inherited_classes):
        with open(json_file_path, 'r', encoding='utf-8') as file:
            json_data = file.read()

        if not json_data.strip():
            raise ValueError("JSON file is empty or contains only whitespace.")

        try:
            data = json.loads(json_data)
        except json.JSONDecodeError as e:
            raise ValueError(f"Invalid JSON format: {e}")

        emm_data = []

        for class_name, class_data in data.items():
            if class_name in non_inherited_classes:
                emm_data.extend(class_data.get("Emm", []))  # Add Emm data to the list

        return emm_data

    def extract_nonzero_columns(self, matrices):
        u_1 = []
        for class_name, matrix_data in matrices.items():
            for j, column in enumerate(matrix_data["columns"]):
                has_nonzero = any(matrix_data["matrix"][i][j] != 0 for i in range(len(matrix_data["rows"])))
                if has_nonzero:
                    u_1.append(column)
        return u_1

    def find_related_columns_for_non_inherited(self, u_1, emm_data):
        related_pairs = []
        for pair in emm_data:
            method1 = pair[0].split(".")[1]
            method2 = pair[1].split(".")[1]
            if method1 in u_1 or method2 in u_1:
                related_pairs.append([method1, method2])
        return related_pairs

    def filter_related_pairs(self, matrices, related_pairs):
        filtered_pairs = []
        for pair in related_pairs:
            element1, element2 = pair
            for class_name, matrix_data in matrices.items():
                if element2 in matrix_data["columns"]:
                    col_idx = matrix_data["columns"].index(element2)
                    has_nonzero = any(matrix_data["matrix"][i][col_idx] != 0 for i in range(len(matrix_data["rows"])))
                    if has_nonzero:
                        filtered_pairs.append(pair)
                    break
        return filtered_pairs

    def update_final_list_based_on_filtered_pairs(self, emf_matches, filtered_pairs):
        result = [[entry['row'], entry['column']] for entry in emf_matches]
        list2_dict = defaultdict(list)
        for item in filtered_pairs:
            list2_dict[item[1]].append(item[0])

        final_list = []
        for item in result:
            if item[1] in list2_dict:
                for value in list2_dict[item[1]]:
                    final_list.append(item + [value])
            else:
                final_list.append(item)

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

    def create_dum_with_conditions(self, matrices, fourth_matrix, updated_final_list):
        fifth_level_dum = {}
        for class_name, matrix_data in matrices.items():
            rows = matrix_data["rows"]
            columns = matrix_data["columns"]
            fourth_matrix_data = fourth_matrix[class_name]["matrix"]
            fifth_matrix = copy.deepcopy(fourth_matrix_data)

            for item in updated_final_list:
                if len(item) >= 4:
                    row_name, col1, col2, col3 = item
                    if row_name in rows and col1 in columns and col2 in columns and col3 in columns:
                        row_idx = rows.index(row_name)
                        col1_idx = columns.index(col1)
                        col2_idx = columns.index(col2)
                        col3_idx = columns.index(col3)
                        value1 = fourth_matrix_data[row_idx][col1_idx]
                        value2 = fourth_matrix_data[row_idx][col2_idx]
                        value3 = fourth_matrix_data[row_idx][col3_idx]
                        if value1 == value2:
                            fifth_matrix[row_idx][col2_idx] = [value2, "R"]
                        if value2 == value3:
                            fifth_matrix[row_idx][col3_idx] = [value3, "R"]

                elif len(item) == 3:
                    row_name, col1, col2 = item
                    if row_name in rows and col1 in columns and col2 in columns:
                        row_idx = rows.index(row_name)
                        col1_idx = columns.index(col1)
                        col2_idx = columns.index(col2)
                        value1 = fourth_matrix_data[row_idx][col1_idx]
                        value2 = fourth_matrix_data[row_idx][col2_idx]
                        if value1 == value2:
                            fifth_matrix[row_idx][col2_idx] = [value2, "R"]

                elif len(item) == 2:
                    row_name, col_name = item
                    if row_name in rows and col_name in columns:
                        row_idx = rows.index(row_name)
                        col_idx = columns.index(col_name)
                        value = fourth_matrix_data[row_idx][col_idx]
                        fifth_matrix[row_idx][col_idx] = value

            fifth_level_dum[class_name] = {"rows": rows, "columns": columns, "matrix": fifth_matrix}

        return fifth_level_dum

    def create_madum_from_fifth_level(self, fifth_level_dum_with_conditions):
        madum = {}
        for class_name, matrix_data in fifth_level_dum_with_conditions.items():
            rows = matrix_data["rows"]
            columns = matrix_data["columns"]
            fifth_matrix_data = matrix_data["matrix"]

            madum_matrix = []
            for row in fifth_matrix_data:
                new_row = []
                for cell in row:
                    if isinstance(cell, list) and "R" in cell:
                        new_row.append([0])
                    elif isinstance(cell, list) and isinstance(cell[0], str):
                        new_row.append(cell[0][0])
                    else:
                        new_row.append(cell)

                madum_matrix.append(new_row)

            madum[class_name] = {"rows": rows, "columns": columns, "matrix": madum_matrix}

        return madum

    def update_inherited_classes_with_madum(self, madum, inherited_classes, inheritance_map):
        updated_inherited_classes = copy.deepcopy(inherited_classes)
        for child_class, parent_classes in inheritance_map.items():
            for parent_class in parent_classes:
                if parent_class in madum and child_class in inherited_classes:
                    parent_matrix = madum[parent_class]
                    child_matrix = updated_inherited_classes[child_class]

                    parent_rows, parent_columns, parent_values = (
                        parent_matrix["rows"],
                        parent_matrix["columns"],
                        parent_matrix["matrix"],
                    )
                    child_rows, child_columns = (
                        child_matrix["rows"],
                        child_matrix["columns"],
                    )

                    if "matrix" not in child_matrix or not child_matrix["matrix"]:
                        child_matrix["matrix"] = [[0 for _ in range(len(child_columns))] for _ in
                                                  range(len(child_rows))]

                    for i, row in enumerate(child_rows):
                        if row in parent_rows:
                            parent_row_idx = parent_rows.index(row)
                            for j, col in enumerate(child_columns):
                                if col in parent_columns:
                                    parent_col_idx = parent_columns.index(col)
                                    child_matrix["matrix"][i][j] = parent_values[parent_row_idx][parent_col_idx]

        return updated_inherited_classes

    def update_inherited_matrices_with_emf(self, updated_inherited_matrices, emf_data):
        updated_matrices = copy.deepcopy(updated_inherited_matrices)
        for class_name, matrix_data in updated_matrices.items():
            rows, columns = matrix_data["rows"], matrix_data["columns"]
            if "matrix" not in matrix_data or not matrix_data["matrix"]:
                matrix_data["matrix"] = [[0 for _ in range(len(columns))] for _ in range(len(rows))]
            matrix = matrix_data["matrix"]
            for emf_entry in emf_data:
                method_full, attribute_full, value_type = emf_entry
                method_class, method_name = method_full.split(".", 1)
                attribute_class, attribute_name = attribute_full.split(".", 1)
                if class_name == method_class == attribute_class:
                    possible_methods = [col for col in columns if col.startswith(method_name)]
                    if len(possible_methods) > 1:
                        overridden_method_name = next((col for col in possible_methods if col.endswith("'")),
                                                      method_name)
                    else:
                        overridden_method_name = method_name
                    if overridden_method_name in columns and attribute_name in rows:
                        row_idx = rows.index(attribute_name)
                        col_idx = columns.index(overridden_method_name)
                        matrix[row_idx][col_idx] = value_type
        return updated_matrices

def main():
    # Part 1: ECG Extraction
    path = "C:/Users/98910/Desktop/test_ECG2"
    udb_path = os.path.join(path, "test.udb")
    output_file = "ecg_output_with_categories.json"
    output_folder = "ecg_graphs"

    ecg_extractor = ECGExtractor(udb_path)
    db = ecg_extractor.open_udb()
    if db:
        ecg = ecg_extractor.extract_ecg_with_categories()
        ecg_extractor.save_ecg_to_file(ecg, output_file)
        ecg_extractor.visualize_ecg(ecg, output_folder)
        db.close()

    # Part 2: Matrix Processing
    with open(output_file, 'r') as file:
        json_input = file.read()

    processor = MatrixProcessor()
    emf_data = processor.extract_emf_data(json_input)
    inherited_classes, non_inherited_classes, inheritance_map = processor.process_json_and_create_matrices_with_inheritance(json_input)
    empty_matrices = processor.create_empty_matrix_for_all_classes(non_inherited_classes, inherited_classes)
    pd.set_option('display.max_rows', None)
    pd.set_option('display.max_columns', None)
    pd.set_option('display.width', None)

    processor.draw_matrices_with_pandas(empty_matrices, "Empty Matrices for All Classes")

    emf_matches = processor.match_emf_data_with_non_inherited(non_inherited_classes, emf_data, empty_matrices)
    first_level_dum = processor.update_matrix(empty_matrices)
    first_level_dum_non_inherited = {
        class_name: matrix_data
        for class_name, matrix_data in first_level_dum.items()
        if class_name in non_inherited_classes
    }

    processor.draw_matrices_with_pandas(first_level_dum_non_inherited, "First Level DUM (Non-Inherited Classes)")

    emm_data = processor.extract_emm_data_for_non_inherited(output_file, non_inherited_classes)
    updated_matrices = processor.propagate_values_based_on_emm(first_level_dum_non_inherited, empty_matrices, emm_data)
    processor.draw_matrices_with_pandas(updated_matrices, "Updated Matrices After Propagation")

    u_1 = processor.extract_nonzero_columns(first_level_dum)
    related_pairs_non_inherited = processor.find_related_columns_for_non_inherited(u_1, emm_data)
    filtered_pairs = processor.filter_related_pairs(first_level_dum, related_pairs_non_inherited)
    updated_final_list = processor.update_final_list_based_on_filtered_pairs(emf_matches, filtered_pairs)

    fifth_level_dum_with_conditions = processor.create_dum_with_conditions(non_inherited_classes, updated_matrices, updated_final_list)
    processor.draw_matrices_with_pandas(fifth_level_dum_with_conditions, "DUM with Conditions (Non-Inherited Classes)")

    madum = processor.create_madum_from_fifth_level(fifth_level_dum_with_conditions)
    processor.draw_matrices_with_pandas(madum, "Madum Matrix (Non-Inherited Classes)")

    updated_inherited_matrices = processor.update_inherited_classes_with_madum(madum, inherited_classes, inheritance_map)
    processor.draw_matrices_with_pandas(updated_inherited_matrices, "Fill Quadrant II")

    final_updated_inherited_matrices = processor.update_inherited_matrices_with_emf(updated_inherited_matrices, emf_data)
    processor.draw_matrices_with_pandas(final_updated_inherited_matrices, "Fill Quadrant IV")

if __name__ == "__main__":
    main()