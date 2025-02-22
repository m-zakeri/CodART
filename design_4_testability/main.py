from design_4_testability.class_diagram_extraction.class_diagram import ClassDiagram
from codart.refactoring_design_patterns.factory import Factory
from codart.refactoring_design_patterns.injection import Injection
from utils.utils import File
import config
import networkx as nx
import json


def project_info(java_project):
    java_project_address = config.projects_info[java_project]['path']
    base_dirs = config.projects_info[java_project]['base_dirs']
    files = File.find_all_file(java_project_address, 'java')
    index_dic = File.indexing_files_directory(files, 'class_index.json', base_dirs)
    cd = ClassDiagram(java_project_address, base_dirs, files, index_dic)
    cd.make_class_diagram()
    return base_dirs, files, index_dic, cd


if __name__ == "__main__":
    # java_projects = [
    #     '10_water-simulator',
    #     '61_noen',
    #     '88_jopenchart',
    #     'commons-codec',
    #     'xerces2j'
    # ]
    java_projects = ["JSON-java"]
    for java_project in java_projects:
        base_dirs, files, index_dic, cd = project_info(java_project)
        # cd.set_stereotypes()
        # cd.save('class_diagram.gml')
        #cd.load('class_diagram.gml')
        # cd.show(cd.class_diagram_graph)
        # g = cd.class_diagram_graph
        # print(len(list(nx.weakly_connected_components(g))))
        # for i in nx.weakly_connected_components(g):
        #     print(i)
        #g = cd.class_diagram_graph
        #print(len(list(nx.weakly_connected_components(g))))
        # f = Factory(index_dic, cd.class_diagram_graph, base_dirs)
        # report = f.refactor(0.1)
        #
        # base_dirs, files, index_dic, cd = project_info(java_project)

        injection = Injection(base_dirs, index_dic, files, cd.class_diagram_graph)
        injection.refactor()

        base_dirs, files, index_dic, cd = project_info(java_project)

        # files = File.find_all_file(java_project_address, 'java')
        # index_dic = File.indexing_files_directory(files, 'class_index.json', base_dirs)
        # cd2 = ClassDiagram(java_project_address, base_dirs, files, index_dic)
        # cd2.make_class_diagram()
        # cd2.set_stereotypes()
        # cd2.show(cd2.class_diagram_graph)
        # CDG = cd2.get_CDG()
        # cd.show(CDG)
        # g = cd2.class_diagram_graph
        # print(len(list(nx.weakly_connected_components(g))))
        # for i in nx.weakly_connected_components(g):
        #     print(i)
