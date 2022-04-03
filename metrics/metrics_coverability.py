"""
The script provide methods computing source code metrics with Understand

## References
https://scitools.com/documents/manuals/python/understand.html
https://scitools.com/documents/manuals/perl/#ada_entity_kinds


## Changelog
### v0.3.1
- Remove dependency to nlp packages
- Eliminate extra classes

"""

__version__ = '0.3.1'
__author__ = 'Morteza Zakeri'


class UnderstandUtility:
    """

    """

    @classmethod
    def is_accesor_or_mutator(cls, method_entity=None):
        if str(method_entity.simplename()).startswith(("get", "set", "Get", "Set")):
            return True
        else:
            return False

    @classmethod
    def NMO(cls, class_name):
        um = 0
        for mth in class_name.ents('Define', 'method'):
            if mth.refs('Override'):
                um += 1
        return um

    @classmethod
    def NIM(cls, class_name):
        declared_methods = 0 if class_name.metric(['CountDeclMethod'])['CountDeclMethod'] is None else \
        class_name.metric(['CountDeclMethod'])['CountDeclMethod']
        all_methods = 0 if class_name.metric(['CountDeclMethodAll'])['CountDeclMethodAll'] is None else \
        class_name.metric(['CountDeclMethodAll'])['CountDeclMethodAll']
        return all_methods - declared_methods

    @classmethod
    def CFNAMM_Class(cls, class_name):
        list1 = list()
        for meth in class_name.refs('Call', 'Java Method'):
            if meth.ent().parent() is None:
                continue
            if meth.ent().parent().longname() != class_name.longname() \
                    and meth.ent().kindname() != "Public Constructor" \
                    and not (cls.is_accesor_or_mutator(meth.ent())):
                list1.append(meth)
        return len(set(list1))

    @classmethod
    def FANIN(cls, db=None, class_entity=None) -> int:
        """
        Method for computing the fanin for a given class
        :param db: Understand database of target project
        :param class_entity: Target class entity for computing fanin
        :return: fain: The FanIn of the class
        """
        method_list = UnderstandUtility.get_method_of_class_java(db=db, class_name=class_entity.longname())
        fanin = 0
        for method_entity in method_list:
            method_fanin = method_entity.metric(['CountInput'])['CountInput']
            if method_fanin is None:
                fanin += 0
            else:
                fanin += method_fanin
        return fanin

    @classmethod
    def FANOUT(cls, db, class_entity) -> int:
        method_list = UnderstandUtility.get_method_of_class_java(db=db, class_name=class_entity.longname())
        fanout = 0
        for method_entity in method_list:
            method_fanout = method_entity.metric(['CountOutput'])['CountOutput']
            if method_fanout is None:
                fanout += 0
            else:
                fanout += method_fanout
        return fanout

    @classmethod
    def RFC(cls, class_name):
        list1 = list()
        for meth in class_name.refs('Call', 'Java Method'):
            if meth.ent().parent() is None:
                continue
            long_name = meth.ent().parent().longname()
            if long_name != class_name.longname() and meth.ent().kindname() != 'Public Constructor':
                list1.append(meth)
        return len(set(list1))

    @classmethod
    def NOMAMM(cls, class_entity):
        """
        Number of accessor (getter) and mutator (setter) methods
        Weak implementation, need to rewrite
        :param class_entity:
        :return:
        """
        count = 0
        methods = class_entity.ents('Define', 'Java Method')
        if methods is not None:
            for method_entity in methods:
                # if str(self.return_name(method_entity)).startswith(('get', 'Get', 'GET', 'set', 'Set', 'SET')):
                #     count += 1
                if str(method_entity.simplename()).startswith(('get', 'Get', 'GET', 'set', 'Set', 'SET')):
                    count += 1  # i.e., the method is accessor or mutator
        return count

    @classmethod
    def get_class_names(cls, db):
        """
        Getting types list: Class (three method), Abstract Class, Interface, Enum, Type
        """
        class_name_list = list()
        entities = db.ents('Class ~Unresolved')
        for class_ in sorted(entities, key=UnderstandUtility.sort_key):
            print(class_.name())
            class_name_list.append(class_.longname())
        # print('PJNOCN', len(class_name_list))
        return class_name_list

    # Java specific method
    @classmethod
    def get_project_classes_longnames_java(cls, db):
        class_name_list = list()
        filter1 = "Java Class ~Unresolved ~Unknown ~TypeVariable ~Anonymous ~Annotation ~Enum ~Interface ~Abstract ~Jar ~Library"
        entities = db.ents(filter1)

        # entities = db.ents('Type')
        for class_ in sorted(entities, key=UnderstandUtility.sort_key):
            # print(class_.name())
            class_name_list.append(class_.longname())
        # print('PJNOCN', len(class_name_list))
        return class_name_list

    @classmethod
    def get_project_classes_java(cls, db):
        entities = db.ents('Java Class ~Interface ~Enum ~Unknown ~Unresolved ~Jar ~Library')
        # entities = db.ents('Type')
        # print('PJNOC', len(entities))
        return entities

    @classmethod
    def get_project_abstract_classes_java(cls, db):
        entities = db.ents('Java Abstract Class ~Interface ~Enum ~Unknown ~Unresolved ~Jar ~Library')
        # print('PJNOAC', len(entities))
        return entities

    @classmethod
    def get_project_interfaces_java(cls, db):
        entities = db.ents('Java Interface ~Enum ~Unknown ~Unresolved ~Jar ~Library')
        # print('PJNOI', len(entities))
        return entities

    @classmethod
    def get_project_enums_java(cls, db):
        entities = db.ents('Java Java Enum ~Unknown ~Unresolved ~Jar ~Library')
        # print('PJNOENU', len(entities))
        return entities

    @classmethod
    def get_project_types_java(cls, db):
        entities = db.ents('Type')
        # entities = db.ents('Java Class')
        # print('PJNOT', len(entities))
        return entities

    # -------------------------------------------
    # Getting Types individually with their name
    @classmethod
    def get_class_entity_by_name(cls, db, class_name):
        # https://docs.python.org/3/library/exceptions.html#exception-hierarchy
        # Find relevant 'class' entity
        entity_list = list()

        entities = db.ents('Type')  # Use this for evo-suite SF110 already measured class
        # entities = db.ents('Java Class ~Enum ~Unknown ~Unresolved ~Jar ~Library')
        # entities = db.ents('Java Class ~Jar ~Library, Java Interface')
        if entities is not None:
            for entity_ in entities:
                if entity_.longname() == class_name:
                    entity_list.append(entity_)
                    # print('Class entity:', entity_)
                    # print('Class entity kind:', entity_.kind())
        if len(entity_list) == 0:
            # raise UserWarning('Java class with name {0} is not found in project'.format(class_name))
            return None
        if len(entity_list) > 1:
            # print('######', len(entity_list))
            # raise ValueError('There is more than one Java class with name {0} in the project'.format(class_name))
            return entity_list[0]
        else:
            return entity_list[0]

    @classmethod
    def get_method_of_class_java(cls, db, class_name):
        method_list = list()
        # entities = db.ents('function, method Member ~Unresolved')
        entities = db.ents('Java Method')
        # print(class_name)
        for method_ in sorted(entities, key=UnderstandUtility.sort_key):
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
    def get_method_of_class_java2(cls, db, class_name=None, class_entity=None):
        """
        Both methods 'get_method_of_class_java' and 'get_method_of_class_java2' works correctly.
        :param db:
        :param class_name:
        :param class_entity:
        :return:
        """
        if class_entity is None:
            class_entity = cls.get_class_entity_by_name(db=db, class_name=class_name)
        method_list = class_entity.ents('Define', 'Java Method ~Unknown ~Unresolved ~Jar ~Library')
        # print('len method list', len(method_list))
        # print(method_list)
        return method_list

    @classmethod
    def get_constructor_of_class_java(cls, db, class_name=None, class_entity=None):
        """
        :param db:
        :param class_name:
        :param class_entity:
        :return:
        """
        if class_entity is None:
            class_entity = cls.get_class_entity_by_name(db=db, class_name=class_name)
        constructor_list = class_entity.ents('Define', 'Java Method Constructor')
        # print('len constructor list', len(constructor_list))
        # print(constructor_list)
        return constructor_list

    @classmethod
    def get_method_name_of_class(cls, db, class_name):
        method_name_list = list()
        entities = db.ents('function, method Member ~Unresolved')
        # print(class_name)
        for method_ in sorted(entities, key=UnderstandUtility.sort_key):
            if str(method_.parent()) == class_name:
                # print('\tname:', method_.name(), '\tkind:', method_.kind().name(), '\ttype:', method_.type())
                method_name_list.append(method_.name())
        return method_name_list

    @classmethod
    def get_attribute_of_class(cls, db, class_name):
        attribute_name_list = list()
        # entities = db.ents('Object member ~Unresolved')  # For my C# project works well but not for Java projects
        entities = db.ents('Variable')
        print(class_name)
        for attr_ in sorted(entities, key=UnderstandUtility.sort_key):
            if str(attr_.parent()) == class_name:
                # print('\t', attr_.name(), attr_.kind().name())
                # print('\tname:', attr_.name(), '\tkind:', attr_.kind().name(), '\ttype:', attr_.type())
                attribute_name_list.append(attr_.name())
        return attribute_name_list

    @classmethod
    def get_class_attributes_java(cls, db, class_name=None, class_entity=None) -> list:
        if class_entity is None:
            class_entity = UnderstandUtility.get_class_entity_by_name(db=db, class_name=class_name)
        class_attributes_list = list()
        for java_var in class_entity.ents('Define', 'Java Variable'):
            # print(java_var.longname())
            # print(java_var.kind())
            # print('TYPE::', java_var.type())
            # print(java_var.library())
            # print('-------------')
            class_attributes_list.append(java_var)

        return class_attributes_list

    @classmethod
    def get_data_abstraction_coupling(cls, db, class_name=None, class_entity=None) -> int:
        java_primitive_types = ['byte', 'short', 'int', 'long', 'float', 'double',
                                'boolean', 'char',
                                'String'
                                ]
        attrs = UnderstandUtility.get_class_attributes_java(db, class_name=class_name, class_entity=class_entity)
        dac = 0
        for attr in attrs:
            if attr.type() not in java_primitive_types:
                dac += 1
        return dac

    @classmethod
    def get_number_of_class_in_file_java(cls, db, class_name=None, class_entity=None):
        """
        :param db:
        :param class_name:
        :param class_entity:
        :return:
        """
        if class_entity is None:
            class_entity = cls.get_class_entity_by_name(db=db, class_name=class_name)

        number_of_class_in_class_file = class_entity.parent().ents('Define',
                                                                   'Java Class ~Unknown ~Unresolved ~Jar ~Library')
        # print('number_of_class_in_class_file:', len(number_of_class_in_class_file))
        return number_of_class_in_class_file

    @classmethod
    def get_package_of_given_class(cls, db, class_name):
        # Find package: strategy 2: Dominated strategy
        class_name_list = class_name.split('.')[:-1]
        package_name = '.'.join(class_name_list)
        # print('package_name string', package_name)
        package_list = db.lookup(package_name + '$', 'Package')
        if package_list is None:
            return None
        if len(package_list) == 0:  # if len != 1 return None!
            return None
        package = package_list[0]
        print(package.longname())
        return package

    @classmethod
    def get_package_of_given_class_2(cls, db, class_name):
        class_entity = UnderstandUtility.get_class_entity_by_name(db, class_name)
        # print(class_entity.parent())
        # print('class_name', class_entity.longname())
        # print('class_name', class_name)

        if class_entity is None:
            return None, 'default'

        package_list = class_entity.ents('Containin', 'Java Package')
        while not package_list and class_entity.parent() is not None:
            package_list = class_entity.parent().ents('Containin', 'Java Package')
            class_entity = class_entity.parent()

        # print('package_name', package_list)
        if len(package_list) < 1:
            return None, 'default'
        else:
            return package_list[0], package_list[0].longname()

    @classmethod
    def get_package_clasess_java(cls, package_entity=None):
        # This method has a bug! (dataset version 0.3.0, 0.4.0)
        # Bug is now solved.
        # classes = package_entity.ents('Contain', 'class')
        # interfaces = package_entity.ents('Contain', 'interface')
        all_types = package_entity.ents('Contain', 'Java Type ~Unknown ~Unresolved ~Jar ~Library')
        # print('number of classes', len(classes))
        # print('number of interface', len(interfaces))
        # print('number of all types', len(all_types))
        # for class_entity in classes:
        #     print(class_entity.longname())
        # print('-'*75)
        # for interface_entity in interfaces:
        #     print(interface_entity.longname())

        # for type_entity in all_types:
        #     print(type_entity.longname(),
        #           type_entity.kind(),
        #           type_entity.metric(['CountLineCode'])['CountLineCode'],
        #           type_entity.metric(['CountLineCodeDecl'])['CountLineCodeDecl'],
        #           type_entity.metric(['CountLineCodeExe'])['CountLineCodeExe'],
        #           type_entity.metric(['AvgLineCode'])['AvgLineCode'],)

        return all_types

    @classmethod
    def get_package_classes_by_accessor_method_java(cls, package_entity=None, accessor_method=''):
        # classes = package_entity.ents('Contain', 'class')
        # interfaces = package_entity.ents('Contain', 'interface')
        all_types = package_entity.ents('Contain', "Java Abstract Enum Type Default Member" + accessor_method)
        # print('number of classes', len(classes))
        # print('number of interface', len(interfaces))
        # print('Number of all interfaces', len(all_types))
        for type_entity in all_types:
            print(type_entity.longname(),
                  type_entity.kind(),
                  )
        return all_types

    @classmethod
    def get_package_interfaces_java(cls, package_entity=None):
        # classes = package_entity.ents('Contain', 'class')
        # interfaces = package_entity.ents('Contain', 'interface')
        all_acs = package_entity.ents('Contain', 'Java Interface ~Unknown ~Unresolved')
        # print('number of classes', len(classes))
        # print('number of interface', len(interfaces))
        # print('Number of package interfaces:', len(all_acs))
        return all_acs

    @classmethod
    def get_package_abstract_class_java(cls, package_entity=None):
        # classes = package_entity.ents('Contain', 'class')
        # interfaces = package_entity.ents('Contain', 'interface')
        abstract_classes = package_entity.ents('Contain', 'Java Abstract Class ~Unknown ~Unresolved')
        # print('number of classes', len(classes))
        # print('number of interface', len(interfaces))
        # print('Number of package abstract class', len(abstract_classes))
        return abstract_classes

    @classmethod
    def get_project_files_java(cls, db):
        files = db.ents('Java File ~Jar')
        print('Number of files', len(files))
        # for file_entity in files:
        #     print(file_entity.longname(),
        #           file_entity.kind(),
        # file_entity.metric(['CountLineCode'])['CountLineCode'],
        # file_entity.metric(['CountLineCodeDecl'])['CountLineCodeDecl'],
        # file_entity.metric(['CountLineCodeExe'])['CountLineCodeExe'],
        # file_entity.metric(['AvgLineCode'])['AvgLineCode'],
        # file_entity.metric(['CountStmtDecl'])['CountStmtDecl'],
        # file_entity.metric(['CountStmtDecl'])['CountStmtDecl'],
        # file_entity.metric(['SumCyclomatic'])['SumCyclomatic'],
        # )

        return files

    @classmethod
    def get_local_variables(cls, db, function_name):
        local_var_name_list = list()
        entities = db.ents(' Object Local ~Unresolved')
        print(function_name)
        for attr_ in sorted(entities, key=UnderstandUtility.sort_key):
            if str(attr_.parent()) == function_name:
                # print('\t', attr_.name(), attr_.kind().name())
                # print('\tname:', attr_.name(), '\tkind:', attr_.kind().name(), '\ttype:', attr_.type())
                local_var_name_list.append(attr_.name())
        return local_var_name_list

    @classmethod
    def draw_cfg_for_class_java(cls, db, class_name=None, class_entity=None):
        """
        :param db:
        :param class_name:
        :param class_entity:
        :return:
        """
        if class_entity is None:
            class_entity = cls.get_class_entity_by_name(db=db, class_name=class_name)

        # class_entity.draw('Declaration', 'Declaration_graph.jpg')
        class_entity.draw('Control Flow Graph', 'CFG_graph.jpg')

    @classmethod
    def ATFD(cls, db, class_entity=None, class_name=None):
        java_primitive_types = ['byte', 'short', 'int', 'long', 'float', 'double',
                                'boolean', 'char',
                                'String'
                                ]
        if class_entity is None:
            class_entity = UnderstandUtility.get_class_entity_by_name(db, class_name=class_name)

        methods = class_entity.ents('Define', 'Java Method')
        all_fd_list = set()
        for method_ in methods:
            # print(method_.simplename(), '|', method_.parent(), '|', method_.kind())

            foreign_data = method_.ents('Java Define', 'Java Variable')
            # foreign_data = method_.ents('Java Use', 'Java Variable')
            # foreign_data = class_entity.ents('Modify', 'Java Variable')
            # print('Number of ATFD:', len(set(foreign_data)))

            # all_fd_list.extend(set(foreign_data))
            for fd in foreign_data:
                # print(fd.longname(), '| ', fd.parent(), '| ', fd.kind(), '| ', fd.type())
                if fd.type() not in java_primitive_types:
                    all_fd_list.add(fd.type())
            # print('-'*75)
        # print('all FD:', len(all_fd_list))
        return len(all_fd_list)

    @classmethod
    def NOII(cls, db):
        noii = 0
        interfaces = UnderstandUtility.get_project_interfaces_java(db)
        for interface in interfaces:
            usin = interface.ents('Useby', 'Java Class ~Jar')
            if usin is not None and len(usin) > 0:
                noii += 1
            # print(interface.longname(), '| ', interface.kind(), '|', interface.parent(), '|', usin)
            # print('-'*75)
        # print('Number of implemented interface: ', noii)
        return noii

    @classmethod
    def number_of_method_call(cls, db=None, class_entity=None, class_name=None):
        if class_entity is None:
            class_entity = UnderstandUtility.get_class_entity_by_name(db=db, class_name=class_name)
        method_calls = class_entity.ents('Call', )
        # print('method_calls:', len(method_calls))
        # print(method_calls)
        return len(method_calls)

    @classmethod
    def sort_key(cls, ent):
        return str.lower(ent.longname())
