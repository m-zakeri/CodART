"""
The configuration module

"""
import os

import networkx as nx
from design_4_testability.utils.utils import dir_total_size


__version__ = '0.1.2'
__author__ = 'Sadegh Jafari, Morteza Zakeri'

# BASE_DIR = 'benchmarks/SF110/projects/'
BASE_DIR = 'C:/Users/98910/CodART/design_4_testability/resources/benchmarks/'
UBD_DIR = 'C:/Users/98910/CodART/design_4_testability/resources/und_db/'
D4T_LOG_DIR = 'C:/Users/98910/CodART/design_4_testability/resources/reports/'
projects_info = dict()


# SF110 projects
SF110_projects = [f for f in os.listdir(BASE_DIR) if not os.path.isfile(os.path.join(BASE_DIR, f))]

for project_name in SF110_projects:
    projects_info[project_name] = dict()
    java_project_address = f'{BASE_DIR}{project_name}/src/main/java'
    base_dirs = list()
    base_dirs.append(f'{BASE_DIR}{project_name}/src/main/java/')
    projects_info[project_name]['size'] = dir_total_size(java_project_address)
    projects_info[project_name]['path'] = java_project_address
    projects_info[project_name]['base_dirs'] = base_dirs
    projects_info[project_name]['db_path'] = f'{UBD_DIR}{project_name}.und'
    projects_info[project_name]['log_path'] = f'{D4T_LOG_DIR}{project_name}/{project_name}_log.csv'
    if not os.path.exists(f'{D4T_LOG_DIR}{project_name}'):
        os.mkdir(f'{D4T_LOG_DIR}{project_name}')

projects_info = dict(sorted(projects_info.items(), key=lambda item: item[1]['size']))

# ======================================
# Complexity

test_class_diagram = nx.DiGraph()
relationships_name = ['implements', 'extends', 'create', 'use_consult', 'use_def']

# nodes
for i in range(16):
    test_class_diagram.add_node(i)
    test_class_diagram.nodes[i]['type'] = 'normal'

# extends path
test_class_diagram.add_edge(1, 0)
test_class_diagram[1][0]['relation_type'] = 'extends'

test_class_diagram.add_edge(2, 0)
test_class_diagram[2][0]['relation_type'] = 'extends'

test_class_diagram.add_edge(3, 0)
test_class_diagram[3][0]['relation_type'] = 'extends'

test_class_diagram.add_edge(4, 3)
test_class_diagram[4][3]['relation_type'] = 'extends'

test_class_diagram.add_edge(5, 3)
test_class_diagram[5][3]['relation_type'] = 'extends'

test_class_diagram.add_edge(6, 3)
test_class_diagram[6][3]['relation_type'] = 'extends'

test_class_diagram.add_edge(9, 8)
test_class_diagram[9][8]['relation_type'] = 'extends'

test_class_diagram.add_edge(10, 8)
test_class_diagram[10][8]['relation_type'] = 'extends'

test_class_diagram.add_edge(11, 8)
test_class_diagram[11][8]['relation_type'] = 'extends'

test_class_diagram.add_edge(12, 8)
test_class_diagram[12][8]['relation_type'] = 'extends'

test_class_diagram.add_edge(13, 8)
test_class_diagram[13][8]['relation_type'] = 'extends'

test_class_diagram.add_edge(14, 8)
test_class_diagram[14][8]['relation_type'] = 'extends'

test_class_diagram.add_edge(15, 8)
test_class_diagram[15][8]['relation_type'] = 'extends'

test_class_diagram.add_edge(9, 8)
test_class_diagram[9][8]['relation_type'] = 'extends'

# use paths
test_class_diagram.add_edge(7, 8)
test_class_diagram[7][8]['relation_type'] = 'use_def'

test_class_diagram.add_edge(8, 7)
test_class_diagram[8][7]['relation_type'] = 'use_def'

test_class_diagram.add_edge(7, 0)
test_class_diagram[7][0]['relation_type'] = 'use_def'

test_class_diagram.add_edge(0, 7)
test_class_diagram[0][7]['relation_type'] = 'use_def'

test_class_diagram.add_edge(8, 0)
test_class_diagram[8][0]['relation_type'] = 'use_def'
