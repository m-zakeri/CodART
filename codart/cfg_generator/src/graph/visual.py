import html
from collections import defaultdict

import graphviz as gv
import re
from codart.cfg_generator.src.data_structures.graph.builder_interface import IDiGraphBuilder
from codart.cfg_generator.src.antlr.rule_utils import extract_exact_text
from codart.cfg_generator.src.graph.utils import head_node, last_node

FONT_SIZE = "22"
PEN_WIDTH = "2"


def draw_CFG(graph, end_nodes, filename, token_stream=None, format="png", verbose=True, function_name=None,
             output_list=None):
    if output_list is None:
        output_list = []  # Initialize the output list if not provided

    if graph.nodes:
        gr = gv.Digraph(comment=filename, format=format, node_attr={"shape": "none"})
        gr.node("start", style="filled", fillcolor="#aaffaa", shape="oval", fontsize=FONT_SIZE)

        output_dict = {}

        for node, data in graph.nodes.data():
            if node not in output_dict:
                output_dict[node] = {
                    "basic node id": node,
                    "text": [],
                    "line": [],
                    "type": "Unknown",
                    "previous node": [],
                    "next node": [],
                    "function name": function_name,
                    "end nodes": []  # فیلد جدید برای end_nodes
                }

            if 'value' in data and isinstance(data['value'], list) and data['value']:
                last_value = data['value'][-1]
                output_dict[node]["type"] = type(last_value).__name__
            else:
                output_dict[node]["type"] = "Unknown"

            block_contents = (stringify_block(data, token_stream) if verbose else stringify_block_lineno_only(data))
            matches = re.findall(r'(\d+):\s*([^<]+)', block_contents)

            for integer_id, text in matches:
                if integer_id not in output_dict[node]["line"]:
                    output_dict[node]["line"].append(integer_id)

                if text.strip() not in output_dict[node]["text"]:
                    output_dict[node]["text"].append(html.unescape(text.strip()))

            gr.node(str(node), label=build_node_template(node, block_contents))

        gr.node("end", style="filled", fillcolor="#aaffaa", shape="oval", fontsize=FONT_SIZE)

        for f, t, data in graph.edges.data():
            if t not in output_dict[f]["next node"]:
                output_dict[f]["next node"].append(t)

            if f not in output_dict[t]["previous node"]:
                output_dict[t]["previous node"].append(f)

            gr.edge(f"{str(f)}", f"{str(t)}", fontsize=FONT_SIZE, penwidth=PEN_WIDTH)

        # ثبت end_nodes در output_dict
        if end_nodes:
            for end in end_nodes:
                node_id, label = end
                if node_id in output_dict:
                    output_dict[node_id]["end nodes"].append(label)
                gr.edge(str(node_id), "end", penwidth=PEN_WIDTH, label=label)
        else:
            last_node_id = last_node(graph)
            if last_node_id in output_dict:
                output_dict[last_node_id]["end nodes"].append("default end")
            gr.edge(str(last_node_id), "end", penwidth=PEN_WIDTH)

        # اضافه کردن اطلاعات به output_list
        output_list.extend(output_dict.values())

        gr.edge("start", str(head_node(graph)) if len(graph.nodes) > 0 else "end", penwidth=PEN_WIDTH)

        gr.render(f"{filename}-cfg.gv", view=False)



def build_node_template(node_label, contents):
    b_len = len(contents.splitlines())
    line_height = 40
    s = f"""<<FONT POINT-SIZE="{FONT_SIZE}">  
        <TABLE BORDER="0" CELLBORDER="1" CELLSPACING="0">
            <tr>
                <td width="50" height="50" fixedsize="true">{node_label + 1}</td>
                <td width="9" height="9" fixedsize="true" style="invis"></td>
                <td width="9" height="9" fixedsize="true" style="invis"></td>
            </tr>
            <tr>
                <td width="50" height="{b_len * line_height}" fixedsize="true" sides="tlb"></td>
                <td width="50" height="{b_len * line_height}" fixedsize="false" sides="bt" PORT="here">{contents}</td>
                <td width="50" height="{b_len * line_height}" fixedsize="true" sides="brt"></td>
            </tr>
        </TABLE>
    </FONT>>"""
    return strip_lines(s)


def strip_lines(x: str): return "\n".join(line.strip() for line in x.splitlines())


def node_content_to_html(node_contents):
    delimiter = '<br align="left"/>\n'
    grouped_tuples = defaultdict(list)
    for t in node_contents:
        grouped_tuples[t[0]].append(t[1])

    new_contents = []
    for key, values in grouped_tuples.items():
        if len(values) > 1:
            new_contents.append((key, ' '.join(values)))
        else:
            new_contents.append((key, values[0]))

    content_list_string = delimiter.join([html.escape(f"{l}: {content}") for l, content in new_contents])

    return content_list_string + delimiter


def stringify_block(node_args, token_stream):
    if node_args == {}:
        return ""
    else:
        cs = []
        for rule in node_args["value"]:
            if not hasattr(rule, 'symbol'):
                cs.append((rule.start.line, extract_exact_text(token_stream, rule)))
            else:
                cs.append((rule.symbol.line, rule.symbol.text))
        b = node_content_to_html(cs)
        return b

def stringify_block_lineno_only(node_args):
    data = node_args["value"]
    left, right = data[0].start.line, data[-1].stop.line
    if left == right:
        return f"{left}"

    return f"{left}..{right}"
