import os

os.add_dll_directory(r'C:\\Program Files\\SciTools\\bin\\pc-win64')
import understand as und
from codart import config


class UnderstandUtility2:

    @classmethod
    def get_method_of_class_java(cls, db, class_name):
        method_list = list()
        # entities = db.ents('function, method Member ~Unresolved')
        entities = db.ents('Java Method')
        # print(class_name)
        for method_ in sorted(entities, key=UnderstandUtility2.sort_key):
            # print(method_)
            # print(method_.parent().longname())
            if method_.parent() is None:
                continue
            if str(method_.parent().longname()) == class_name:
                # print('\tname:', method_.name(), '\tkind:', method_.kind().name(), '\ttype:', method_.type())
                method_list.append(method_)
        # print('len method list', len(method_list))
        # print(method_list)
        return method_list

    @classmethod
    def sort_key(cls, ent):
        return str.lower(ent.longname())

    @classmethod
    def FANIN(cls, db=None) -> int:
        """
        Method for computing the fanin for a given class
        :param db: Understand database of target project
        :param class_entity: Target class entity for computing fanin
        :return: fain: The FanIn of the class
        """
        # Open the Understand database
        db = und.open(config.UDB_PATH)
        total_fanin = 0
        # Get all entities of kind "class" from the project
        for java_class in db.ents('class'):
            # print(java_class.longname(), str(java_class.kind()))
            if str(java_class.kind()) == 'Class' or 'Public Class' or 'Private Class' or 'Public Abstract Class':
                method_list = UnderstandUtility2.get_method_of_class_java(db=db, class_name=java_class.longname())
                fanin = 0
                for method_entity in method_list:
                    method_fanin = method_entity.metric(['CountInput'])['CountInput']
                    if method_fanin is None:
                        fanin += 0
                    else:
                        fanin += method_fanin
                total_fanin += fanin
       # Return the count of fanin
        return total_fanin

    @classmethod
    def FANOUT(cls, db) -> int:
        # Open the Understand database
        db = und.open(config.UDB_PATH)
        total_fanout = 0
        # Get all entities of kind "class" from the project
        for java_class in db.ents('class'):
            # print(java_class.longname(), str(java_class.kind()))
            if str(java_class.kind()) == 'Class' or 'Public Class' or 'Private Class' or 'Public Abstract Class':
                method_list = UnderstandUtility2.get_method_of_class_java(db=db, class_name=java_class.longname())
                fanout = 0
                for method_entity in method_list:
                    method_fanout = method_entity.metric(['CountOutput'])['CountOutput']
                    if method_fanout is None:
                        fanout += 0
                    else:
                        fanout += method_fanout
                total_fanout += fanout

        # Return the count of fanout
        return total_fanout

    # Calculating abstract classes
    def count_abstract_classes(project_path):
        # Open the Understand database
        db = und.open(project_path)
        entities = db.ents('Java Abstract Class ~Interface ~Enum ~Unknown ~Unresolved ~Jar ~Library')
        abstract_class_count = 0
        # Get all entities of kind "abstract" from the project
        for java_class in entities:
            abstract_class_count += 1
            #print(abstract_class_count)

        # Return the count of abstract classes
        return abstract_class_count  # return num_abstract_components / num_total_components

    # Calculating interfaces
    def count_interface(project_path):
        # Open the Understand database
        db = und.open(project_path)
        interface_count = 0
        # Get all entities of kind "interface" from the project
        for java_class in db.ents('interface'):
            # print(java_class.longname(), str(java_class.kind()))
            if str(java_class.kind()) == 'Public Interface' or 'Public Generic Interface':
                interface_count += 1
                # print(interface_count)

        # Return the count of interface
        return interface_count

    def count_total_classes(project_path):
        # Open the Understand database
        db = und.open(project_path)
        class_count = 0
        # Get all entities of kind "class" from the project
        for java_class in db.ents('Java Class ~Enum ~Unknown ~Unresolved ~Jar ~Library'):
            # print(java_class.longname(), str(java_class.kind()))
                class_count += 1
                #print(class_count)

        # Return the count of interface
        return class_count

    def calculate_abstractness(na, i, nc):
        a = (na + i) / nc
        return a

    def calculate_instability(project_path):    #(component, all_components):
        # Open the Understand database
        db = und.open(project_path)
        fan_in = UnderstandUtility2.FANIN(db=project_path)
        fan_out = UnderstandUtility2.FANOUT(db=project_path)
        instability = fan_out / (fan_out + fan_in)
        return instability


def main(db_path, initial_value=1.0):
    # Open the Understand database

    db = und.open(db_path)
    abstract_count = UnderstandUtility2.count_abstract_classes(db_path)
    interface_count = UnderstandUtility2.count_interface(db_path)
    class_count = UnderstandUtility2.count_total_classes(db_path)
    a = UnderstandUtility2.calculate_abstractness(abstract_count, interface_count, class_count)
    i = UnderstandUtility2.calculate_instability(db_path)
    d = abs(a + i - 1)
    # Close the Understand database
    db.close()
    return d

if __name__ == '__main__':
    project_path = config.UDB_PATH

    # Call the function to count abstract classes
    abstract_count = UnderstandUtility2.count_abstract_classes(project_path)
    interface_count = UnderstandUtility2.count_interface(project_path)
    class_count = UnderstandUtility2.count_total_classes(project_path)
    class_abstractness = UnderstandUtility2.calculate_abstractness(abstract_count, interface_count, class_count)

    # Print the result
    print("Number of abstract classes: ", abstract_count)
    print("Number of interfaces: ", interface_count)
    print("Number of classes: ", class_count)
    print("Abstractness: ", class_abstractness)
    print("Fanin: ", UnderstandUtility2.FANIN(db=project_path))
    print("Fanout: ", UnderstandUtility2.FANOUT(db=project_path))
    print("Instability: ", UnderstandUtility2.calculate_instability(project_path))
    print(f"UDB path: {config.UDB_PATH}")
    for i in range(0, 1):
        print(main(config.UDB_PATH, initial_value=1.0))

