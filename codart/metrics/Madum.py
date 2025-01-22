import os
import sys
from graphviz import Digraph
import json
from codart.utility.directory_utils import create_understand_database
os.add_dll_directory("C:\\Program Files\\SciTools\\bin\\pc-win64\\")
sys.path.append("C:\\Program Files\\SciTools\\bin\\pc-win64\\python")
import understand as und


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

    for member in class_entity.ents("Define", "Java Method"):
        method_identifier = f"{member.longname()}({member.parameters()})"
        methods.append((member, method_identifier))  # Include parameter details
        # print("..", member, "..", member.kind(), "..", member.ref() )
        for mem in (member.ents("Set, Use, Define, Modify", "Java Variable") +
                    member.ents("Define, Use, Set", "Java Parameter")):
            fields.append(mem)
        for mem2 in member.ents("Override", "Java Method"):
            method_identifier = f"{mem2.longname()}({mem2.parameters()})"
            methods.append((mem2, method_identifier))
    for member in class_entity.ents("Define, Use", "Java Variable"):
        fields.append(member)
    return methods, fields


# Categorize a method
def categorize_method(method, fields):
    """
    Categorize a method as constructor (c), transformer (t), reporter (r), or other (o).
    """
    if method.kind().check("Constructor"):
        return "c"  # Constructor

        # Check if the method modifies any field
    modifies_field = any(
        ref.ent() in fields and ref.kind().check("Set, Modify")
        for ref in method.refs("Use, Set, Modify", "Variable")
    )
    if modifies_field:
        return "t"  # Transformer

    # Check if the method only returns a field's value
    accesses_fields = [ref.ent() for ref in method.refs("Use", "Variable")]
    if all(field in fields for field in accesses_fields) and not modifies_field:
        return "r"  # Reporter

    return "o"  # Other


# Extract Enhanced Call Graph (ECG) with categorization
def extract_ecg_with_categories(db):
    ecg = {}

    for class_entity in db.ents("Class"):
        # print(class_entity, ":",  class_entity.kind(), ":", class_entity.refs())
        class_name = class_entity.longname()
        methods_with_identifiers, fields = extract_class_members(class_entity)

        # Build M(C) and F(C)
        M_C = [method_id for _, method_id in methods_with_identifiers]
        F_C = [field.longname() for field in fields]

        # Categorize methods
        method_categories = {
            method_id: categorize_method(method, fields)
            for method, method_id in methods_with_identifiers
        }

        # Build Emf and Emm
        Emf = set()
        Emm = set()

        for method, method_id in methods_with_identifiers:
            # Emf: Method -> Field accesses
            for ref in method.refs("Use, Set, Modify", "Variable") + method.refs("Use, Set, Modify,", "Parameter"):
                field = ref.ent()
                # if field in fields:
                Emf.add((method_id, field.longname()))

            # Emm: Method -> Method calls
            for ref in method.refs("Call, Extend, Define, Override", "Method"):
                callee = ref.ent()
                callee_identifier = f"{callee.longname()}({callee.parameters()})"
                if callee in [m for m, _ in methods_with_identifiers]:
                    Emm.add((method_id, callee_identifier))

        ecg[class_name] = {
            "M(C)": M_C,
            "F(C)": F_C,
            "Method Categories": method_categories,  # Add categories
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
            for ref_method, field in data["Emf"]:
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
                        fontsize="8"
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


# Main Function
def main():
    path = "C:/Users/98910/Desktop/test_ECG2"
    udb_path = create_understand_database(path, path)
    output_file = "ecg_output_with_categories.json"  # Output file for ECG
    output_folder = "ecg_graphs"  # Folder for Graphviz output

    db = open_udb(udb_path)
    if db:
        ecg = extract_ecg_with_categories(db)
        save_ecg_to_file(ecg, output_file)
        visualize_ecg(ecg, output_folder)
        db.close()


if __name__ == "__main__":
    main()
