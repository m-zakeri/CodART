import os
import sys
import json
import copy
import math
import numpy as np
import pandas as pd
from graphviz import Digraph
from codart.utility.directory_utils import create_understand_database
import understand as und
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
                method_identifier = f"{mem.longname()}({mem.parameters()})'"
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

            m_c = [method_id for _, method_id in methods_with_identifiers]
            f_c = [field.longname() for field in fields]
            emf = set()
            emm = set()

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
                            emf.add((method_id, field.longname(), relation))

                for ref in method.refs("Call, Extend, Define", "Method"):
                    callee = ref.ent()
                    callee_identifier = f"{callee.longname()}({callee.parameters()})"
                    if callee in [m for m, _ in methods_with_identifiers]:
                        emm.add((method_id, callee_identifier))

            ecg[class_entity.longname()] = {
                "M(C)": m_c,
                "F(C)": f_c,
                "Emf": list(emf),
                "Emm": list(emm)
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

    def extract_class_and_method(self, method_signature: str):
        """
        Safely extract class name and method name from a method signature.
        Handles parameters with dots or generics inside.
        """
        method_header = method_signature.split("(", 1)[0]  # e.g., SampleStatistic.setErrorHandler
        last_dot_index = method_header.rfind(".")
        if last_dot_index == -1:
            return "", method_signature  # fallback
        method_class = method_header[:last_dot_index]
        method_name = method_signature[last_dot_index + 1:]
        return method_class, method_name

    def process_json_and_create_matrices(self, json_data):
        data = json.loads(json_data)
        base_class_matrix = {}
        derived_class_matrix = {}
        class_matrices = {}
        inheritance_map = defaultdict(list)
        for class_name, class_data in data.items():
            if "M(C)" in class_data:
                columns = []
                for method in class_data["M(C)"]:
                    method_class, method_name = self.extract_class_and_method(method)
                    columns.append(method_name)
                    if method_class != class_name:
                        # print("***", method_class, class_name)
                        inheritance_map[class_name].append(method_class)
                rows = [entry.split(".", 1)[1].split(".")[-1] for entry in class_data.get("F(C)", []) if
                        class_name + "." in entry]
                matrix = {"columns": columns, "rows": sorted(set(rows))}
                class_matrices[class_name] = matrix

        for class_name in class_matrices:
            if class_name in inheritance_map:
                for parent_class, parents in inheritance_map.items():  # Fixed loop variable
                    parent_columns = []
                    parent_rows = []
                    derived_matrix = class_matrices[class_name]  # Create a proper reference

                    for parent in parents:
                        if parent in class_matrices:
                            parent_columns.extend(class_matrices[parent]["columns"])
                            parent_rows.extend(class_matrices[parent]["rows"])

                    parent_columns = list(dict.fromkeys(parent_columns))
                    parent_rows = list(dict.fromkeys(parent_rows))
                    derived_matrix["columns"] = parent_columns + [col for col in derived_matrix["columns"] if
                                                                  col not in parent_columns]
                    derived_matrix["rows"] = parent_rows + [row for row in derived_matrix["rows"] if
                                                            row not in parent_rows]

                    derived_class_matrix[class_name] = derived_matrix
            else:
                base_class_matrix[class_name] = class_matrices[class_name]

        return base_class_matrix, derived_class_matrix, inheritance_map

    def extract_emf_data(self, json_data):
        data = json.loads(json_data)
        emf_data = [emf for class_data in data.values() for emf in class_data.get("Emf", [])]
        return emf_data

    def create_empty_matrix_for_all_classes(self, base_class_matrix, derived_class_matrix):
        empty_matrices = {}
        for class_name, matrix in {**base_class_matrix, **derived_class_matrix}.items():
            rows, columns = matrix["rows"], matrix["columns"]
            empty_matrices[class_name] = {
                "rows": rows,
                "columns": columns,
                "matrix": [[0] * len(columns) for _ in range(len(rows))],
            }
        return empty_matrices

    def match_emf_data_for_base_classes(self, base_classes, emf_data, empty_matrices):
        emf_matches = []
        seen_matches = set()

        for class_name, matrix in base_classes.items():
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
                        method_class, method_name = self.extract_class_and_method(emf_method_full)
                        class_match = method_class == class_name

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
                                current_value = empty_matrices[class_name]["matrix"][row_idx][col_idx]
                                if current_value:
                                    existing_values = current_value.split(", ")
                                    if type_value not in existing_values:  # Only add if it's unique
                                        existing_values.append(type_value)
                                    empty_matrices[class_name]["matrix"][row_idx][col_idx] = ", ".join(existing_values)
                                else:
                                    empty_matrices[class_name]["matrix"][row_idx][col_idx] = type_value

        return emf_matches

    def update_matrix(self, empty_matrices):
        for class_name, matrix_data in empty_matrices.items():
            for i, row in enumerate(matrix_data["rows"]):
                for j, column in enumerate(matrix_data["columns"]):
                    if isinstance(matrix_data["matrix"][i][j], str):
                        matrix_data["matrix"][i][j] = f"{matrix_data['matrix'][i][j]}"
        return empty_matrices

    def draw_matrices_with_pandas(self, matrices, title, save_dir="matrices_csv"):
        print(f"\n{title}:\n" + "=" * 50)
        for class_name, matrix_data in matrices.items():
            columns_with_params = matrix_data["columns"]

            df = pd.DataFrame(matrix_data["matrix"], index=matrix_data["rows"], columns=columns_with_params)
            # Replace 0 values with NaN
            df.replace(0, np.nan, inplace=True)
            print(f"\nMatrix for class: {class_name}")
            print(df)
            print("-" * 50)

            # Save as CSV
            safe_name = class_name.replace(".", "_")  # avoid issues in filenames
            csv_path = os.path.join(save_dir, f"{safe_name}.csv")
            df.to_csv(csv_path, index=True)  # Keep row labels
            print(f"Saved CSV: {csv_path}")

    def extract_emm_data(self, json_file_path, base_classes):
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
            if class_name in base_classes:
                emm_data.extend(class_data.get("Emm", []))  # Add Emm data to the list

        return emm_data

    def propagate_through_call_graph(self,
                                     matrix_data_dict,
                                     emm_data,
                                     source_matrix_dict=None,
                                     is_derived=False,
                                     emf_data=None):
        """
        General method to propagate values through method call graph.

        Parameters:
        - matrix_data_dict: The matrices to update (empty_matrices or derived_class_matrix).
        - emm_data: EMM data as list of (caller, callee) tuples.
        - source_matrix_dict: Optional. Needed if propagating from first_level_dum_for_base_classes.
        - is_derived: If True, special logic for derived classes.
        - emf_data: Optional. Needed for derived class to pre-fill matrices.
        """
        from collections import defaultdict, deque

        call_graph = defaultdict(list)
        for caller, callee in emm_data:
            call_graph[caller].append(callee)

        def get_final_methods(method, visited):
            if method not in call_graph or method in visited:
                return {method}
            visited.add(method)
            final_methods = set()
            for next_method in call_graph[method]:
                final_methods.update(get_final_methods(next_method, visited))
            return final_methods if final_methods else {method}

        def bfs(start_method):
            queue = deque([start_method])
            visited = set()
            while queue:
                method = queue.popleft()
                for callee in call_graph.get(method, []):
                    if callee not in visited:
                        visited.add(callee)
                        queue.append(callee)
            return visited

        # Step 1: For derived classes, prefill direct accesses (using emf_data)
        if is_derived and emf_data:
            for class_name, matrix_data in matrix_data_dict.items():
                rows, columns = matrix_data["rows"], matrix_data["columns"]

                if "matrix" not in matrix_data or not matrix_data["matrix"]:
                    matrix_data["matrix"] = [[0 for _ in range(len(columns))] for _ in range(len(rows))]
                matrix = matrix_data["matrix"]

                for emf_entry in emf_data:
                    method_full, attribute_full, value_type = emf_entry
                    method_class, method_name = self.extract_class_and_method(method_full)
                    attribute_class, attribute_name = attribute_full.rsplit(".", 1)

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

        # Step 2: Build reachable methods
        reachable = defaultdict(set)
        if is_derived:
            for method in call_graph:
                reachable[method] = bfs(method)

        # Step 3: Propagate
        for class_name, matrix_data in matrix_data_dict.items():
            rows = matrix_data["rows"]
            columns = matrix_data["columns"]
            matrix = matrix_data["matrix"]

            derived_fields = set(rows) if is_derived else None  # Only fields in derived class

            if not is_derived:
                # Base class logic: propagate from source_matrix
                if class_name not in source_matrix_dict:
                    continue

                source_matrix = source_matrix_dict[class_name]

                for row in rows:
                    for col in columns:
                        method_key = f"{class_name}.{col}"

                        if method_key in call_graph:
                            final_methods = get_final_methods(method_key, set())
                            for final_method in final_methods:
                                final_method_name = final_method.split("(")[0].split(".")[-1]
                                final_method_params = final_method.split("(")[1].split(")")[
                                    0] if "(" in final_method else ""

                                for existing_col in source_matrix["columns"]:
                                    existing_col_name = existing_col.split("(")[0]
                                    existing_col_params = existing_col.split("(")[1].split(")")[
                                        0] if "(" in existing_col else ""

                                    if (final_method_name == existing_col_name and final_method_params ==
                                            existing_col_params):
                                        row_idx = rows.index(row)
                                        col_idx = columns.index(col)
                                        final_col_idx = source_matrix["columns"].index(existing_col)
                                        final_value = source_matrix["matrix"][row_idx][final_col_idx]

                                        if final_value != 0:
                                            matrix[row_idx][col_idx] = final_value
            else:
                # Derived class logic: propagate field accesses through reachable methods
                for caller_full in reachable:
                    caller_class, caller_method = self.extract_class_and_method(caller_full)
                    if caller_class != class_name:
                        continue

                    possible_caller_methods = [col for col in columns if col.startswith(caller_method)]
                    if len(possible_caller_methods) > 1:
                        caller_method_in_matrix = next((col for col in possible_caller_methods if col.endswith("'")),
                                                       caller_method)
                    else:
                        caller_method_in_matrix = caller_method

                    if caller_method_in_matrix not in columns:
                        continue

                    caller_idx = columns.index(caller_method_in_matrix)

                    for callee_full in reachable[caller_full]:
                        callee_class, callee_method = self.extract_class_and_method(callee_full)
                        if callee_class != caller_class:
                            continue

                        possible_callee_methods = [col for col in columns if col.startswith(callee_method)]
                        if len(possible_callee_methods) > 1:
                            callee_method_in_matrix = next(
                                (col for col in possible_callee_methods if not col.endswith("'")), callee_method)
                        else:
                            callee_method_in_matrix = callee_method

                        if callee_method_in_matrix not in columns:
                            continue

                        callee_idx = columns.index(callee_method_in_matrix)

                        for row_idx, field_name in enumerate(rows):
                            if field_name not in derived_fields:
                                continue

                            callee_value = matrix[row_idx][callee_idx]
                            caller_value = matrix[row_idx][caller_idx]

                            if callee_value and callee_value != 'NaN':
                                if caller_value and caller_value != 'NaN':
                                    merged_set = set([caller_value, callee_value])
                                    merged = ', '.join(sorted(merged_set))
                                    matrix[row_idx][caller_idx] = merged
                                else:
                                    matrix[row_idx][caller_idx] = callee_value
        return matrix_data_dict

    def is_nan_cell(self, cell):
        return (
                cell in ['NaN', ['NaN'], None, 0]
                or (isinstance(cell, float) and math.isnan(cell))
        )

    def has_meaningful_value(self, cell):
        # Anything that is not NaN/None/['NaN']/empty string/0 is meaningful
        if isinstance(cell, list):
            return any(self.has_meaningful_value(c) for c in cell)
        return (
                cell not in [0, 'NaN', ['NaN'], None, '']
                and not (isinstance(cell, float) and math.isnan(cell))
        )

    def mark_new_entries(self, matrix1, matrix2):
        for class_name, matrix_data in matrix1.items():
            rows = matrix_data["rows"]
            columns = matrix_data["columns"]
            base_matrix = matrix_data["matrix"]
            derived_matrix = matrix2[class_name]["matrix"]

            for i in range(len(rows)):
                for j in range(len(columns)):
                    base_cell = base_matrix[i][j]
                    derived_cell = derived_matrix[i][j]

                    if self.is_nan_cell(base_cell) and self.has_meaningful_value(derived_cell):
                        # Add 'R' to mark the new entry
                        if isinstance(derived_cell, list):
                            if 'R' not in derived_cell:
                                derived_matrix[i][j] = derived_cell + ['R']
                        elif isinstance(derived_cell, str):
                            if 'R' not in derived_cell:
                                derived_matrix[i][j] = f"{derived_cell}, R"
                        else:
                            derived_matrix[i][j] = ['R']

        return matrix2

    def compute_summary_row(self, matrix):
        """
        Compute the final summary row by collecting all unique values in each column.
        """
        summary_row = []
        num_rows = len(matrix)

        for col_idx in range(len(matrix[0])):  # Iterate over columns
            column_values = set()  # Using a set here directly to ensure uniqueness

            for row_idx in range(num_rows):
                cell = matrix[row_idx][col_idx]

                if isinstance(cell, str) and ', ' in cell:
                    values = cell.split(', ')  # Split by comma and space
                    for value in values:
                        column_values.add(value.upper())

                # Flatten lists (if a cell contains a list, extract its elements)
                elif isinstance(cell, list):
                    flat_values = map(str.upper, cell)  # Convert list items to uppercase
                else:
                    flat_values = [str(cell).upper()]  # Convert single value to uppercase

                # Add non-zero, non-NaN values to the set
                    for value in flat_values:
                        if value != "0" and value != "NAN":
                            column_values.add(value)  # Add directly to the set (ensures uniqueness)

            # Convert set to sorted list and join into a string
            unique_values = sorted(column_values)
            # Convert to final cell value
            summary_row.append(", ".join(unique_values) if unique_values else "NaN")  # Replace empty cells with NaN

        return summary_row

    def create_madum(self, union_of_dums):
        madum = {}
        for class_name, matrix_data in union_of_dums.items():
            rows = matrix_data["rows"]
            columns = matrix_data["columns"]
            fifth_matrix_data = matrix_data["matrix"]

            madum_matrix = []
            for row in fifth_matrix_data:
                new_row = []
                for col_idx, cell in enumerate(row):
                    # If column name matches the class name, set 'C'
                    if columns[col_idx].rstrip("()") == class_name:
                        new_row.append("c")
                    elif isinstance(cell, list) and "R" in cell:
                        new_row.append(['NaN'])
                    elif isinstance(cell, list) and isinstance(cell[0], str):
                        new_row.append(cell[0][0])
                    else:
                        new_row.append(cell)
                madum_matrix.append(new_row)

            # Compute the summary row dynamically
            summary_row = self.compute_summary_row(madum_matrix)
            madum_matrix.append(summary_row)

            madum[class_name] = {"rows": rows + ["Total"], "columns": columns, "matrix": madum_matrix}

        return madum

    def fill_quadrant_ii_of_derived_classes(self, madum, derived_class_matrix, inheritance_map):
        """
        Fills Quadrant II of the derived class matrix by incorporating the DUM of the base class.
        This ensures that derived class methods that override base class methods inherit their field accesses.
        """

        for child_class, parent_classes in inheritance_map.items():
            for parent_class in parent_classes:
                if parent_class not in madum:
                    # print(f"Warning: parent class '{parent_class}' not found in madum. Skipping.")
                    continue  # Skip if parent has no matrix
                if child_class in derived_class_matrix:
                    parent_matrix = madum[parent_class]
                    child_matrix = derived_class_matrix[child_class]

                    parent_rows, parent_columns, parent_values = (
                        parent_matrix["rows"],
                        parent_matrix["columns"],
                        parent_matrix["matrix"],
                    )
                    child_rows, child_columns = (
                        child_matrix["rows"],
                        child_matrix["columns"],
                    )
                    # Ensure child_matrix["matrix"] is initialized
                    if "matrix" not in child_matrix or not child_matrix["matrix"]:
                        child_matrix["matrix"] = [[0 for _ in range(len(child_columns))]
                                                  for _ in range(len(child_rows))]

                    # Copy values from parent_matrix to child_matrix
                    for i, row in enumerate(child_rows):
                        if row in parent_rows:
                            parent_row_idx = parent_rows.index(row)  # Find corresponding row in parent
                            for j, col in enumerate(child_columns):
                                if col in parent_columns:
                                    parent_col_idx = parent_columns.index(col)  # Find corresponding col in parent
                                    child_matrix["matrix"][i][j] = parent_values[parent_row_idx][parent_col_idx]

        return derived_class_matrix

    def fill_quadrant_iv_of_derived_classes(self, emf_data, derived_class_matrix, output_file):
        """
        Fills Quadrant IV of the derived class matrix using EMF data.
        Ensures that derived class methods accessing their own attributes are correctly marked.
        Quadrant II remains unchanged during this process.
        """

        for class_name, matrix_data in derived_class_matrix.items():
            rows, columns = matrix_data["rows"], matrix_data["columns"]
            if "matrix" not in matrix_data or not matrix_data["matrix"]:
                matrix_data["matrix"] = [[0 for _ in range(len(columns))] for _ in range(len(rows))]
            matrix = matrix_data["matrix"]

            for emf_entry in emf_data:
                method_full, attribute_full, value_type = emf_entry
                # method_class, method_name = method_full.split(".", 1)
                method_class, method_name = self.extract_class_and_method(method_full)
                attribute_class, attribute_name = attribute_full.rsplit(".", 1)
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
        # Step 2: Detect overridden methods (methods with `'` in their name)
        overridden_methods = {}
        for class_name, matrix_data in derived_class_matrix.items():
            columns = matrix_data["columns"]
            for col in columns:
                if col.endswith("'"):  # Identify overridden methods
                    base_method_name = col[:-1]  # Remove the `'` to get the base method name
                    if class_name not in overridden_methods:
                        overridden_methods[class_name] = []
                    overridden_methods[class_name].append(base_method_name)

        # step 3
        input_matrices = copy.deepcopy(derived_class_matrix)
        emm_data = self.extract_emm_data(output_file, derived_class_matrix)
        second_derived_class_matrix = self.propagate_through_call_graph(
            matrix_data_dict=derived_class_matrix,
            emm_data=emm_data,
            is_derived=True,
            emf_data=emf_data
        )
        # step 4
        union_of_dums = self.mark_new_entries(input_matrices, second_derived_class_matrix)
        return union_of_dums

    def fill_quadrant_iii_of_derived_classes(self, output_file, derived_class_matrix, inheritance_map,
                                             base_class_matrix, madum):
        """
        Fills Quadrant III of the derived class matrix using EMF data.
        Quadrant III represents the usage relationship between data members of the derived class
        and the methods inherited from the base class.
        """
        changed = False  # Track if any matrix is updated
        # Step 1: Extract field-method relations from Quadrant IV
        method_field_relations = {}  # {derived_class: {overridden_method: [fields]}}
        overridden_methods = {}

        for class_name, matrix_data in derived_class_matrix.items():
            rows, columns, matrix = matrix_data["rows"], matrix_data["columns"], matrix_data["matrix"]

            method_field_relations[class_name] = {}
            overridden_methods[class_name] = []

            for col_idx, col in enumerate(columns):
                if col.endswith("'"):  # Overridden method indicator
                    base_method_name = col[:-1]  # Remove `'` to get the base method name
                    overridden_methods[class_name].append(base_method_name)
                    accessed_fields = {}  # Reset for each method

                    # Check Quadrant IV for fields related to this overridden method
                    for row_idx, row in enumerate(rows):
                        relation_type = matrix[row_idx][col_idx]  # The value itself is the relation type
                        if relation_type != 0:  # If there is a field-method relation
                            accessed_fields[row] = relation_type  # Store relation type

                    if accessed_fields:  # Only store if there are actual field accesses
                        method_field_relations[class_name][base_method_name] = accessed_fields

        # Step 2: Identify base class methods calling overridden methods
        for child_class, parent_classes in inheritance_map.items():
            for parent_class in parent_classes:
                if parent_class not in madum:
                    print(f"Warning: parent class '{parent_class}' not found in madum. Skipping.")
                    continue  # Skip if parent has no matrix
                emm_data = self.extract_emm_data(output_file, base_class_matrix)
                for caller, called in emm_data:
                    for class_name, methods in overridden_methods.items():
                        if class_name == child_class:  # Only consider the current child class
                            called_name = called.split(".")[1]
                            caller_name = caller.split(".")[1]
                            if called_name in methods:
                                # print(f"Overriden method {called_name} called by {caller_name} in base class")
                                # Step 3: Update Quadrant III (Base class method → Derived class fields)
                                # Ensure you are accessing the relevant fields from method_field_relations
                                if called_name in method_field_relations[class_name]:
                                    accessed_fields = method_field_relations[class_name][called_name]
                                    for class_name, matrix_data in derived_class_matrix.items():
                                        rows, columns, matrix = (matrix_data["rows"], matrix_data["columns"],
                                                                 matrix_data["matrix"])
                                        if caller_name in columns:
                                            caller_col_idx = columns.index(caller_name)

                                            # Update Quadrant III with the relations
                                            for field, relation_type in accessed_fields.items():
                                                if field in rows:
                                                    row_idx = rows.index(field)
                                                # Copy relation
                                                    matrix[row_idx][caller_col_idx] = relation_type
                                                    changed = True  # Mark as changed
        return derived_class_matrix, changed

    def fill_quadrant_i_of_derived_classes(self, output_file, emf_data, derived_class_matrix, inheritance_map, madum):
        """
        Quadrant I: Relates member functions of the derived class to inherited data members
        of the base class. Marks usage if:
          - A derived method manipulates a base class field directly.
          - A derived method calls an inherited base class method, inheriting its field usage.
        """
        changed = False

        # Extract EMM data only once (not in inner loop)
        emm_data = self.extract_emm_data(output_file, derived_class_matrix)

        # Iterate through each derived class matrix
        for class_name, matrix_data in derived_class_matrix.items():
            rows, columns = matrix_data["rows"], matrix_data["columns"]

            # Initialize matrix if missing
            if "matrix" not in matrix_data or not matrix_data["matrix"]:
                matrix_data["matrix"] = [[0 for _ in range(len(columns))] for _ in range(len(rows))]
            matrix = matrix_data["matrix"]

            # Process each inheritance mapping (child → parents)
            for child_class, parent_classes in inheritance_map.items():
                # Filter only those parents that exist in madum
                valid_parents = [p for p in parent_classes if p in madum]
                if not valid_parents:
                    continue  # Skip if no valid parents

                # Process each emf_entry for the current child class
                for emf_entry in emf_data:
                    method_full, field_full, value_type = emf_entry
                    method_class, method_name = method_full.split(".", 1)
                    field_class, field_name = field_full.split(".", 1)

                    # Only handle if this entry belongs to the current child class
                    if child_class != method_class:
                        continue

                    for parent_class in valid_parents:
                        # Direct field access from derived method to base field
                        if parent_class == field_class:
                            if method_name in columns and field_name in rows:
                                row_idx = rows.index(field_name)
                                col_idx = columns.index(method_name)
                                matrix[row_idx][col_idx] = value_type
                                changed = True

                        # Propagate field usage via base methods called by derived methods
                        for caller, called in emm_data:
                            caller_class, caller_name = caller.split(".", 1)
                            called_class, called_name = called.split(".", 1)
                            if caller_class == child_class and called_class == parent_class:
                                if caller_name in columns and field_class == method_class:
                                    if field_name in rows:
                                        row_idx = rows.index(field_name)
                                        col_idx = columns.index(caller_name)
                                        matrix[row_idx][col_idx] = value_type
                                        changed = True

        return derived_class_matrix, changed

    def compute_test_cases_from_madum(self, madum_matrix):
        """
        Compute the number of test cases required for each class from a MaDUM matrix.

        :param madum_matrix: Dict of MaDUM matrices for each class.
        :return: Dict with number of test cases per class.
        """
        if not madum_matrix:
            return {}

        test_cases_per_class = {}

        for class_name, matrix_data in madum_matrix.items():
            rows, columns = matrix_data["rows"], matrix_data["columns"]
            matrix = matrix_data["matrix"]
            if 'Total' not in rows:
                test_cases_per_class[class_name] = 0
                continue

            row_idx = rows.index('Total')

            # Initialize counters for this class
            c = r = o = t = 0
            for col_idx, col in enumerate(columns):
                value = matrix[row_idx][col_idx]
                value_parts = [v.strip() for v in value.split(',')]
                c += value_parts.count('C')
                r += value_parts.count('R')
                o += value_parts.count('O')
                t += value_parts.count('T')

            total = c + r + o + (c * math.factorial(t))
            test_cases_per_class[class_name] = total

        return test_cases_per_class


def main():
    # Part 1: ECG Extraction
    path = "C:/Users/98910/Desktop/mad"
    udb_path = create_understand_database(path, path)
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
    base_class_matrix, derived_class_matrix, inheritance_map = processor.process_json_and_create_matrices(json_input)
    # print("Base Class Matrix Keys:", list(base_class_matrix.keys()))
    # print("Derived Class Matrix Keys:", list(derived_class_matrix.keys()))
    # print("Inheritance Map:", inheritance_map)

    empty_matrices = processor.create_empty_matrix_for_all_classes(base_class_matrix, derived_class_matrix)
    pd.set_option('display.max_rows', None)
    pd.set_option('display.max_columns', None)
    pd.set_option('display.width', None)

    processor.draw_matrices_with_pandas(empty_matrices, "Empty Matrices for All Classes")

    # Step: Filter out classes with no rows
    classes_with_no_rows = []
    for class_name, matrix_data in empty_matrices.items():
        if len(matrix_data["rows"]) == 0:
            print(f"Skipping class '{class_name}' because it has no rows.")
            classes_with_no_rows.append(class_name)

    # Set number_of_test_case to zero for skipped classes (optional — store somewhere)
    skipped_test_cases = {class_name: 0 for class_name in classes_with_no_rows}

    # Remove them from all relevant structures
    for class_name in classes_with_no_rows:
        empty_matrices.pop(class_name, None)
        base_class_matrix.pop(class_name, None)
        derived_class_matrix.pop(class_name, None)

    emf_matches = processor.match_emf_data_for_base_classes(base_class_matrix, emf_data, empty_matrices)

    first_level_dum = processor.update_matrix(empty_matrices)
    first_level_dum_for_base_class = {
        class_name: matrix_data
        for class_name, matrix_data in first_level_dum.items()
        if class_name in base_class_matrix
    }

    processor.draw_matrices_with_pandas(first_level_dum_for_base_class, "First Level DUM For Base Classes")
    input_matrices = copy.deepcopy(first_level_dum_for_base_class)
    emm_data = processor.extract_emm_data(output_file, base_class_matrix)

    updated_matrices = processor.propagate_through_call_graph(
        matrix_data_dict=first_level_dum_for_base_class,
        emm_data=emm_data,
        source_matrix_dict=empty_matrices,
        is_derived=False,)
    processor.draw_matrices_with_pandas(updated_matrices, "Second Level DUM For Base Classes")
    union_of_dums = processor.mark_new_entries(input_matrices, updated_matrices)
    processor.draw_matrices_with_pandas(union_of_dums, "Union of DUMs For Base Classes")

    madum = processor.create_madum(union_of_dums)
    processor.draw_matrices_with_pandas(madum, "MaDum Matrix For Base Classes")

    number_of_test_cases_per_class = processor.compute_test_cases_from_madum(madum)

    for class_name, count in number_of_test_cases_per_class.items():
        print(f"{class_name}: {count} test cases")

    total_test_cases = sum(number_of_test_cases_per_class.values())
    print("Total Number of Test Cases for testing a base classes:", total_test_cases)
    quadrant_ii = processor.fill_quadrant_ii_of_derived_classes(madum, derived_class_matrix, inheritance_map)
    valid_matrices = {
        class_name: data
        for class_name, data in quadrant_ii.items()
        if isinstance(data, dict) and "matrix" in data and data["matrix"]
    }
    if valid_matrices:
        processor.draw_matrices_with_pandas(valid_matrices, "Fill Quadrant II of Derived Classes")
    else:
        print("No quadrant II matrices to draw — possibly no parent MaDUM data available.")

    quadrant_iv = processor.fill_quadrant_iv_of_derived_classes(
        emf_data,
        derived_class_matrix,
        output_file,
        )
    processor.draw_matrices_with_pandas(quadrant_iv, "Fill Quadrant IV of Derived Classes")
    quadrant_iii, changed = processor.fill_quadrant_iii_of_derived_classes(output_file, derived_class_matrix,
                                                                           inheritance_map, base_class_matrix, madum)
    if changed:
        processor.draw_matrices_with_pandas(quadrant_iii, "Fill Quadrant III of Derived Classes")

    quadrant_i, changed = processor.fill_quadrant_i_of_derived_classes(
        output_file,
        emf_data,
        derived_class_matrix,
        inheritance_map, madum)
    if changed:
        processor.draw_matrices_with_pandas(quadrant_i, "Fill Quadrant I of Derived Classes")
    madum_derived = processor.create_madum(quadrant_i)
    processor.draw_matrices_with_pandas(madum_derived, "MaDum Matrix For Derived Classes")
    number_of_test_cases_per_derived_class = processor.compute_test_cases_from_madum(madum_derived)
    for class_name, count in number_of_test_cases_per_derived_class.items():
        print(f"{class_name}: {count} test cases")
    total_test_cases_derived = sum(number_of_test_cases_per_derived_class.values())
    print("Total Number of Test Cases for testing a derived classes:", total_test_cases_derived)
    total_test_case_per_project = total_test_cases + total_test_cases_derived
    print("Total test cases required for testing project:", total_test_case_per_project)


if __name__ == "__main__":
    main()
