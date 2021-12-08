"""
Script for detecting naming smells in the source code.

"""
import random
import re as re
from collections import Counter
from copy import deepcopy
from typing import List

import matplotlib.pyplot as plt
import nltk
import numpy as np
from gensim.models.word2vec import Word2Vec
from scipy.spatial import distance
from sklearn.decomposition import PCA
from sklearn.neighbors import LocalOutlierFactor
from sklearn.neighbors import NearestNeighbors
from spellchecker import SpellChecker

try:
    import understand as und
except ImportError as e:
    print(e)

__version__ = '0.3.0'
__author__ = 'Morteza'


class UnderstandUtility(object):
    """
    https://scitools.com/documents/manuals/python/understand.html
    https://scitools.com/documents/manuals/perl/#ada_entity_kinds
    """

    @classmethod
    def get_db_tokens(cls, db, look_up_string=".\.cc|.\.h"):
        token_types = ['Newline', 'Whitespace', 'Indent', 'Dedent', 'Comment']
        files = db.lookup(look_up_string, 'file')
        # files = db.lookup('.', 'file')
        print('files:', len(files))
        number_of_all_tokens = 0
        number_of_identifiers = 0
        number_of_error = 0
        token_type_list = list()

        for file in files:
            print('-' * 50, file)
        # input()
        for file in files:
            print('-' * 50, file)
            # if file.name().find('.pb.') != -1 or file.name() == 'logging.h':
            #     continue
            try:
                for lexeme in file.lexer():
                    print(lexeme.text(), ': ', lexeme.token())
                    # if lexeme.ent():
                    #     print('@', lexeme.ent() )
                    if lexeme.token() == 'Identifier':
                        number_of_identifiers += 1
                    if lexeme.token() not in token_types:
                        number_of_all_tokens += 1
                    token_type_list.append(lexeme.token())
            except:
                print('ERROR!')
                number_of_error += 1
            # input()
        print('All tokens:', number_of_all_tokens)
        print('All identifiers:', number_of_identifiers)
        print('identifier ratio to all tokens:', 100 * number_of_identifiers / number_of_all_tokens, '%')
        print('error', number_of_error)
        counter = Counter(token_type_list)
        print('All token types:', counter)

    # -------------------------------------------
    # Getting Types list: Class (three method), Abstract Class, Interface, Enum, Type
    @classmethod
    def get_class_names(cls, db):
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
        entities = db.ents('Java Class ~Interface ~Enum ~Unknown ~Unresolved ~Jar ~Library')
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

        entities = db.ents('Type')  ## Use this for evo-suite SF110 already measured class
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
    def get_base_metric(cls, db, class_name):
        class_entity = UnderstandUtility.get_entity_by_name(db=db, class_name=class_name)

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
    def get_package_clasess_java(cls, db=None, package_entity=None):
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
    def get_package_classes_by_accessor_method_java(cls, db=None, package_entity=None, accessor_method=''):
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
    def get_package_interfaces_java(cls, db=None, package_entity=None):
        # classes = package_entity.ents('Contain', 'class')
        # interfaces = package_entity.ents('Contain', 'interface')
        all_acs = package_entity.ents('Contain', 'Java Interface ~Unknown ~Unresolved')
        # print('number of classes', len(classes))
        # print('number of interface', len(interfaces))
        # print('Number of package interfaces:', len(all_acs))
        return all_acs

    @classmethod
    def get_package_abstract_class_java(cls, db=None, package_entity=None):
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
    def funcWithParameter(cls, db):
        # Test understandability
        ents = db.ents("function, method, procedure")
        for func in sorted(ents, key=UnderstandUtility.sort_key):
            # If the file is from the Ada Standard library, skip to the next
            if func.library() != "Standard":
                print(func.longname(), ' - ', func.name(), '==>', func.parent(), " --> ", func.parameters(), sep="",
                      end="\n")
                # func.draw('Control Flow', 'cfg.png')

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

    # -------------------------------------------
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


class Identifier(object):
    """
    Represent a programmer identifier
    """

    def __init__(self, id_name: str, unum: int = 0, kind: str = None, parent: str = None, model: Word2Vec = None):
        self.unique_number = unum
        self.id_name = id_name
        if self.id_name[0] == '~':
            self.id_name = self.id_name[1:]
        self.entity_kind = kind  # function_name, class_name, namespace_name
        self.parent = parent
        self.is_constructor = None

        self.parts = self.get_identifier_parts()

        self.vector = self.get_single_vector_for_identifier(model=model)
        self.vector_2d = None  # Vector come from PCA

        self.local_outlier_factor = None
        self.naming_debt = None
        self.naming_smells = list()
        self.recommended_names = list()
        self.change_history = list()

    def __str__(self):
        if self.entity_kind == 'function' or self.entity_kind == 'attribute':
            return 'id: {0}, class: {1}, vector: {2}, constructor: {3}'.format(self.id_name, self.parent, 'self.vector',
                                                                               self.is_constructor)
        if self.entity_kind == 'class':
            return 'id: {0}, namespace: {1}, vector: {2}'.format(self.id_name, self.parent, 'self.vector')

    def get_identifier_parts(self):
        """
        Separate identifier to valid parts
        :return:
        """
        identifier_parts = list()
        # First: split based-on CamelCase
        matches = re.finditer('.+?(?:(?<=[a-z])(?=[A-Z])|(?<=[A-Z])(?=[A-Z][a-z])|$)', self.id_name)
        camel_cases = [m.group(0) for m in matches]

        # Second: split based-on underscore character '_'
        for case in camel_cases:
            case = case.lower()
            case = case.split('_')
            identifier_parts.extend(case)

        return identifier_parts

    def get_single_vector_for_identifier(self, model: Word2Vec = None):
        vector_list = list()
        for part in self.parts:
            if part in model.wv.vocab:
                # print(model[part])
                vector_list.append(model[part])
            else:
                print('Part "{0}" in identifier "{1}" is not in the vocabulary!'.format(part, self.id_name))

        if len(vector_list) == 0:
            print('Voector for "{0}" is None.'.format(self.id_name))
            return None
        vectors_array = np.array(vector_list)
        average_vector = np.mean(vectors_array, axis=0)
        # print('avg:', average_vector)
        # sim = model.wv.similar_by_vector(average_vector)
        # print('sim:', sim)
        return average_vector


class NamingSmell(object):
    """

    """

    def __init__(self, model: Word2Vec = None, ):
        self.model = model
        self.identifiers = list()

        self.lower_whisker = None
        self.upper_whisker = None
        self.mean = None
        # self.compute_box_whisker()

    def create_intra_class_identifier_list(self, db=None, class_name: str = 'MPCController'):
        method_names = UnderstandUtility.get_method_of_class_java(db=db, class_name=class_name)
        attribute_names = UnderstandUtility.get_attribute_of_class(db=db, class_name=class_name)

        for method_name in method_names:
            identifier = Identifier(id_name=method_name, kind='function', parent=class_name, model=model)
            if method_name == class_name or method_name[1:] == class_name:
                identifier.is_constructor = True
                method_name = method_name[1:]
            # Avoid repeating names
            if method_name not in [identifier.id_name for identifier in self.identifiers]:
                identifier.unique_number = len(self.identifiers) + 1
                self.identifiers.append(identifier)

        for attr_name in attribute_names:
            identifier = Identifier(id_name=attr_name, kind='attribute', parent=class_name, model=model)
            # Avoid repeating names
            if attr_name not in [identifier.id_name for identifier in self.identifiers]:
                identifier.unique_number = len(self.identifiers) + 1
                self.identifiers.append(identifier)

        print('-' * 75)
        print('There is "{0}" method in class "{1}"'.format(len(method_names), class_name))
        print('There is "{0}" attributes in class "{1}"'.format(len(attribute_names), class_name))
        print('-' * 75)
        print('There is "{0}" identifiers in class "{1}"'.format(len(self.identifiers), class_name))
        identifiers_with_none_vector = [identifier for identifier in self.identifiers if identifier.vector is None]
        print('There is "{0}" identifiers with none vector in class "{1}"'.format(len(identifiers_with_none_vector),
                                                                                  class_name))

        print('all identifiers in detail {0}'.format(str(self.identifiers)))
        for i, identifier in enumerate(reversed(self.identifiers)):
            if len(identifier.id_name) < 4:
                self.identifiers.remove(identifier)

    def find_smelly_names(self):
        for identifier in self.identifiers:
            print('-' * 75)
            self.detect_smell(identifier)

    def detect_smell(self, identifier):
        """
        The comparative and the superlative

        :return:
        """
        # 1. Check if name is too short / non-searchable name / single or double letter
        self.non_searchable_id(identifier)

        # 2. Check if name is non-pronounceable
        self.non_pronounceable_id(identifier)

        # 3. Check if function have a verb in name
        if identifier.entity_kind == 'function':
            self.function_name_should_be_verb(identifier)
        elif identifier.entity_kind == 'class':
            self.class_name_should_be_noun(identifier)

        # 4. Check if name is not in solution or problem domain names / Conceptually irrelevant name
        self.detect_conceptually_irrelevant_name(identifier)

    def non_searchable_id(self, identifier):

        for part in identifier.parts:
            if len(part) <= 3:  # A naive approach
                print(str(id), '\tNon-searchable part found in id:', part)

    def non_pronounceable_id(self, identifier):
        spell = SpellChecker()
        misspelled_parts = spell.unknown(identifier.parts)
        if misspelled_parts is not None:
            print('{0} misspelled part found in the name'.format(len(misspelled_parts)))
            for misspelled_word in misspelled_parts:
                print(str(id), 'misspelled part in name:', misspelled_word)
                print('\tcandidates', spell.candidates(misspelled_word))

    def function_name_should_be_verb(self, identifier):
        """
         Alphabetical list of part-of-speech tags used in the Penn Treebank Project
         https://www.ling.upenn.edu/courses/Fall_2003/ling001/penn_treebank_pos.html
        :param identifier:
        :return:
        """
        spell = SpellChecker()
        misspelled_parts = spell.unknown(identifier.parts)
        identifier_parts_correct = list()
        for part in identifier.parts:
            if part not in misspelled_parts:
                identifier_parts_correct.append(part)
        pos_tags_result = nltk.pos_tag(identifier_parts_correct)
        print(pos_tags_result)

        number_of_verbs_in_function_name = 0
        for pair in pos_tags_result:
            if pair[1] == 'VB':
                print(str(id), '\tVerb is found in {}'.format(pair))
                number_of_verbs_in_function_name += 1
        if number_of_verbs_in_function_name == 0:
            print(str(id), '\t function name should be verb')
            return True
        else:
            return False

    def class_name_should_be_noun(self, identifier):
        # 3. Check if function have a verb in name
        spell = SpellChecker()
        misspelled_parts = spell.unknown(identifier.parts)
        identifier_parts_correct = list()
        for part in identifier.parts:
            if part not in misspelled_parts:
                identifier_parts_correct.append(part)
        pos_tags_result = nltk.pos_tag(identifier_parts_correct)
        print(pos_tags_result)

        number_of_names_in_class_name = 0
        for pair in pos_tags_result:
            if pair[1] in ['NN', 'NNP', 'NOUN']:
                print(str(id), '\tVerb is found in {}'.format(pair))
                number_of_names_in_class_name += 1
        if number_of_names_in_class_name == 0:
            print(str(id), '\t class name should be noun')
            return True
        else:
            return False

    def compute_conceptual_naming_debt(self):
        identifiers_with_vector = [identifier for identifier in self.identifiers if identifier.vector is not None]
        vectors = [identifier.vector for identifier in self.identifiers if identifier.vector is not None]

        # 1. Outlier detection
        # fit the model for outlier detection (default)
        clf = LocalOutlierFactor(n_neighbors=int(len(vectors) / 3.), )
        # use fit_predict to compute the predicted labels of the training samples
        # (when LOF is used for outlier detection, the estimator has no predict,
        # decision_function and score_samples methods).
        y_pred = clf.fit_predict(vectors)
        lof_scores = clf.negative_outlier_factor_
        # Normalization
        lof_scores_normalized = (lof_scores.max() - lof_scores) / (lof_scores.max() - lof_scores.min())

        for i, identifier in enumerate(identifiers_with_vector):
            identifier.local_outlier_factor = lof_scores_normalized[i]
        identifiers_with_vector_sorted = sorted(identifiers_with_vector, key=lambda k: k.local_outlier_factor,
                                                reverse=True)

        for i, identifier in enumerate(identifiers_with_vector_sorted):
            print('-' * 75)
            print(str(identifier))
            print('\tlof score: "{0}", lof score normalized: "{1}"'.format(lof_scores[i], lof_scores_normalized[i]))

        print('-' * 75)
        print('average naming debt: "{0}"'.format(np.mean(lof_scores_normalized)))

        attribute_name_with_vector = [identifier for identifier in identifiers_with_vector if
                                      identifier.entity_kind == 'attribute']
        Visualized.draw_names_plot(identifiers=identifiers_with_vector, lof_scores_normalized=lof_scores_normalized)

    def detect_conceptually_irrelevant_name(self):
        identifiers_with_vector = [identifier for identifier in self.identifiers if identifier.vector is not None]
        identifiers_with_vector_original = deepcopy(identifiers_with_vector)
        vectors = [identifier.vector for identifier in self.identifiers if identifier.vector is not None]
        vectors_original = deepcopy(vectors)

        clf = LocalOutlierFactor(n_neighbors=int(len(vectors_original) / 3.), )
        y_pred = clf.fit_predict(vectors_original)
        lof_scores = clf.negative_outlier_factor_
        # Normalization
        lof_scores_normalized_original = (lof_scores.max() - lof_scores) / (lof_scores.max() - lof_scores.min())
        print('lof_scores_normalized_original', lof_scores_normalized_original)
        print('average naming debt: "{0}"'.format(np.mean(lof_scores_normalized_original)))
        Visualized.draw_names_plot(identifiers=identifiers_with_vector_original,
                                   lof_scores_normalized=lof_scores_normalized_original)
        if len(vectors_original) < 10:
            return

        vectors_avg = np.mean(vectors)
        iteration = 0
        id_out_list = list()
        id_in_list = list()

        flag = True

        while flag and iteration < 100:
            print('-' * 75)
            print('iteration "{}" ...'.format(iteration))
            clf = LocalOutlierFactor(n_neighbors=int(len(vectors) / 3.), )
            y_pred = clf.fit_predict(vectors)
            lof_scores = clf.negative_outlier_factor_
            # Normalization
            lof_scores_normalized = (lof_scores.max() - lof_scores) / (lof_scores.max() - lof_scores.min())
            for i, identifier in enumerate(identifiers_with_vector):
                identifier.local_outlier_factor = lof_scores_normalized[i]

            identifiers_with_vector_sorted = sorted(identifiers_with_vector,
                                                    key=lambda k: k.local_outlier_factor,
                                                    reverse=True)

            print('Average naming debt is "{0}"'.format(np.mean(lof_scores_normalized)))

            id_out_list.append(deepcopy(identifiers_with_vector_sorted[0]))
            print('The identifier "{0}" should be renamed'.format(identifiers_with_vector_sorted[0]))
            # Avg version
            remained_identifiers_vectors = [identifier.vector for identifier in identifiers_with_vector_sorted[1:]]
            # remained_identifiers_vectors_avg = np.mean(remained_identifiers_vectors, axis=0)
            # print('remained_identifiers_vectors_avg', remained_identifiers_vectors_avg)
            # recommended_names = self.model.wv.similar_by_vector(remained_identifiers_vectors_avg, topn=10)
            # distance_to_neighbor = [distance.cosine(id_out_list[-1].vector, vector)
            #                         for vector in remained_identifiers_vectors]

            # for i, dist in enumerate(distance_to_neighbor):
            #     if dist == 0:
            #         distance_to_neighbor[i] = max(distance_to_neighbor)

            # nearest_neighbor_index = distance_to_neighbor.index(min(distance_to_neighbor))

            nbrs = NearestNeighbors(n_neighbors=2, algorithm='ball_tree').fit(remained_identifiers_vectors)
            distances, indices = nbrs.kneighbors([id_out_list[-1].vector], n_neighbors=5)
            print('I ', indices[0])
            random.shuffle(indices[0])
            nearest_neighbor_indice = indices[0][0]

            recommended_names = self.model.wv.similar_by_vector(remained_identifiers_vectors[nearest_neighbor_indice],
                                                                topn=len(self.identifiers) + 1)

            print('similar by vector,', recommended_names)

            # Check post conditions
            # Check if the name is verb for function or noun for attribute

            recommended_name = recommended_names[0][0]
            rank = 1
            while recommended_name in [identifier.id_name for identifier in identifiers_with_vector] \
                    or len(recommended_name) < 4 \
                    or recommended_name in ['char', 'int', 'float', 'double', 'string', 'class']:
                recommended_name = recommended_names[rank][0]
                rank += 1

            for identifier in identifiers_with_vector:
                if identifier.unique_number == id_out_list[-1].unique_number:
                    identifier.id_name = recommended_name
                    identifier.parts = identifier.get_identifier_parts()
                    identifier.vector = identifier.get_single_vector_for_identifier(model=self.model)
                    id_in_list.append(deepcopy(identifier))
                    print('##### id changed', identifier.unique_number)
                    break

            vectors = [identifier.vector for identifier in identifiers_with_vector]
            vectors_avg_new = np.mean(vectors, axis=0)
            d = distance.cosine(vectors_avg, vectors_avg_new)
            print('distance', d)
            print('improvement', )
            if d <= 0.05:
                flag = False
            vectors_avg = vectors_avg_new
            iteration += 1

        print('Number of iterations: "{0}"'.format(iteration))
        print('To be renamed ids: "{0}"'.format([identifier.id_name for identifier in id_out_list]))
        print('Recommended names ids: "{0}"'.format([identifier.id_name for identifier in id_in_list]))
        Visualized.draw_names_plot(identifiers=identifiers_with_vector,
                                   lof_scores_normalized=lof_scores_normalized)

        print('Final IDs', [identifier.id_name for identifier in identifiers_with_vector])

    def detect_conceptually_irrelevant_name2(self, identifier):
        if identifier.vector is None:
            print('None vector, conceptually_irrelevant_name: "{0}"'.format(str(identifier)))
        else:
            if np.greater_equal(identifier.vector, self.upper_whisker).all() or np.less_equal(identifier.vector,
                                                                                              self.lower_whisker).all():
                print('@@@Outlier, conceptually_irrelevant_name: "{0}"'.format(str(identifier)))
                print('@@@\tRecommended Name "{0}"'.format(self.model.wv.similar_by_vector(self.mean, topn=5)))

    def compute_box_whisker(self):
        vectors = [identifier.vector for identifier in self.identifiers if identifier.vector is not None]
        # print(vectors)
        # quit()
        vectors = np.array(vectors)
        q1 = np.percentile(vectors, 25, axis=0)
        q2 = np.percentile(vectors, 50, axis=0)
        q3 = np.percentile(vectors, 75, axis=0)
        iqr = np.subtract(q3, q1)
        self.lower_whisker = np.subtract(q1, 1.50 * iqr)
        self.upper_whisker = np.add(q3, 1.50 * iqr)
        self.mean = q2
        print('lower_whisker: {0}, upper_whisker= {1}'.format(self.lower_whisker, self.upper_whisker))


class Visualized:
    """

    """

    @classmethod
    def draw_names_plot(cls, identifiers: List = None, lof_scores_normalized=None):
        """

        :param identifiers:
        :param lof_scores_normalized:
        :return: Void
        """

        # 1. Perform PCA
        vectors = [identifier.vector for identifier in identifiers]
        pca = PCA(n_components=2)
        pca.fit(np.array(vectors))
        vectors_2d = pca.transform(np.array(vectors))
        # print(vectors_2d)

        # j = 0
        # id_outlier_scores = list()
        # for i, identifier in enumerate(self.identifiers):
        #     if identifier.vector is not None:
        #         id_outlier_scores.append((identifier.id_name, lof_scores_normalized[j]))  # Tuple (id, score)
        #         j += 1
        # id_outlier_scores = sorted(id_outlier_scores, key=lambda k: k[1], reverse=True)
        #
        # print('Outlier intensity: {}'.format(id_outlier_scores))
        # print('-' * 75)
        # for item in id_outlier_scores:
        #     if item[1] > 0.60:
        #         print('conceptually_irrelevant_name: {0}'.format(item))

        # outlier_id = id_outlier_scores[0][0]
        # new_identifier_list = list()
        # for id in self.identifiers:
        #     if id.id != outlier_id:
        #         new_identifier_list.append(id)
        #
        # print('NEW', new_identifier_list)
        # new_vectors = [id.vector for id in new_identifier_list if id.vector is not None]
        # avg = np.mean(new_vectors, axis=0)
        # print('avg', avg)

        # sims = self.model.wv.similar_by_vector(avg)
        # print('SIMS:', sims)
        # lemmatizer = WordNetLemmatizer()
        # for sim in sims:
        #     syn = wordnet.synsets(sim[0])[0]
        #     print('Sim {0} with Syn tag {1} '.format(sim, syn.pos()))
        #
        #     print('Verb lemma', lemmatizer.lemmatize(sim[0], wordnet.VERB))

        # avg2 = pca.transform(np.array([avg]))
        # interrupt = pca.transform(np.array([self.model['routing']]))
        # X = np.append(X, avg2, axis=0)
        # X = np.append(X, interrupt, axis=0)

        # 2. Draw a scatter plot
        x = [x[0] for x in vectors_2d]
        y = [x[1] for x in vectors_2d]
        id_labels = [identifier.id_name for identifier in identifiers if identifier.vector is not None]
        # id_labels.append('AVG')
        # id_labels.append('routing')

        fig, ax = plt.subplots()
        # ax.scatter(z, y)
        ax.scatter(vectors_2d[:, 0], vectors_2d[:, 1], color='k', s=3., label='Identifier')
        for i, txt in enumerate(id_labels):
            ax.annotate(txt, (x[i], y[i]))
        # plt.show()
        # plot circles with radius proportional to the outlier scores
        # radius = (lof_scores.max() - lof_scores) / (lof_scores.max() - lof_scores.min())
        ax.scatter(vectors_2d[:, 0], vectors_2d[:, 1], s=1000. * lof_scores_normalized, edgecolors='r',
                   facecolors='none', label='Outlier score')

        plt.axis('tight')
        # plt.xlim((-5, 5))
        # plt.ylim((-5, 5))
        # plt.xlabel("prediction errors: %d" % (n_errors))
        legend = plt.legend(loc='upper left')
        legend.legendHandles[0]._sizes = [10]
        legend.legendHandles[1]._sizes = [20]
        plt.show()


if __name__ == '__main__':
    # Sample Database path
    # path = '../input_source/DemoProjectForSTART/DemoProjectForSTART.udb'
    path = '../input_source/apollo5-master/understand/understand_analysis.udb'
    path = '../testability/sf110_without_test/110_firebird.udb'
    path = '../testability/sf110_without_test/107_weka.udb'
    # path = '../testability/sf110_without_test/101_netweaver.udb'
    db = und.open(path)

    # Word2Vec model
    # model = Word2Vec.load('../codeembedding/text8_model')
    # model = api.load("glove-wiki-gigaword-50")

    # id = Identifier(id='Teacher', kind='function', parent='MPCController')
    # identifiers.append(id)

    # Naming semll
    # naming_smell = NamingSmell(model=model)
    # class_name = 'ClassLoader'
    # class_name = 'MPCController'
    # naming_smell.create_intra_class_identifier_list(db=db, class_name=class_name)
    # naming_smell.compute_conceptual_naming_debt()
    # naming_smell.detect_conceptually_irrelevant_name()

    # Test for dataset version 0.3.0

    # all_attr = UnderstandUtility.get_class_attributes_java(db=db, class_name='org.firebirdsql.jdbc.FBDataSource')
    # print(all_attr)
    # dac = UnderstandUtility.get_data_abstraction_coupling(db=db,
    #                                                       class_name=r'org.firebirdsql.jdbc.FBDataSource')
    # print(dac)

    # UnderstandUtility.ATFD(db=db, class_name=r'org.firebirdsql.jdbc.AbstractDriver')
    # UnderstandUtility.NOII(db=db)
    # UnderstandUtility.number_of_method_call(db=db, class_name=r'org.firebirdsql.jdbc.AbstractDriver')

    print('-' * 75)

    # pk = UnderstandUtility.get_package_of_given_class(db=db,
    #                                              class_name=r'org.firebirdsql.jdbc.FBDataSource')
    # UnderstandUtility.get_package_of_given_class_2(db=db,
    # class_name=r'org.firebirdsql.jdbc.FBDataSource'
    # class_name=r'org.firebirdsql.jdbc.parser.StatementParser'
    # )

    # UnderstandUtility.get_package_interfaces_java(package_entity=pk)
    # UnderstandUtility.get_package_abstract_class_java(package_entity=pk)
    # UnderstandUtility.get_package_classes_by_accessor_method_java(package_entity=pk, accessor_method='Default')
    # UnderstandUtility.get_project_files_java(db=db)

    # Test for dataset version 0.5.0
    # l2 = UnderstandUtility.get_project_classes_longnames_java(db=db)
    #
    # l3 = UnderstandUtility.get_project_classes_java(db=db)
    # l4 = UnderstandUtility.get_project_interfaces_java(db=db)
    # l5 = UnderstandUtility.get_project_abstract_classes_java(db=db)
    # l6 = UnderstandUtility.get_project_enums_java(db=db)
    #
    # l7 = UnderstandUtility.get_project_types_java(db=db)
    # l8 = UnderstandUtility.get_constructor_of_class_java(db=db, class_name='weka.gui.graphvisualizer.DotParser')

    method_list = UnderstandUtility.get_method_of_class_java2(db=db, class_name='weka.gui.graphvisualizer.DotParser')
    db.close()
    # for i, method in enumerate(method_list):
    #     print(i+1, method.longname())
    #     for j, m in enumerate(method.metrics()):
    #         print('\t', j+1, method.metric([m]))

    # UnderstandUtility.get_number_of_class_in_file_java(db=db, class_name='weka.gui.graphvisualizer.DotParser')
    # UnderstandUtility.draw_cfg_for_class_java(db=db, class_name='weka.gui.graphvisualizer.DotParser')
    # UnderstandUtility.get_class_entity_by_name(db=db, class_name='com.sap.netweaver.porta.core.ApplicationStatus')
