"""
QMOOD Design Metrics
"""

__version__ = '0.1.1'
__author__ = 'Seyyed Ali Ayati, Mina Tahaei'

import os
import logging

try:
    import understand as und
except ImportError:
    print("Cannot import understand.")

# Config logging
logging.basicConfig(filename='codart_result.log', level=logging.DEBUG)
logger = logging.getLogger(os.path.basename(__file__))

from sbse.config import CURRENT_QMOOD_METRICS, UDB_PATH


def divide_by_initial_value(func):
    def wrapper(*args, **kwargs):
        value = func(*args, **kwargs)
        initial = CURRENT_QMOOD_METRICS.get(func.__name__)
        return round(value / initial, 2)

    return wrapper


class QMOOD:
    def __init__(self, udb_path):
        # To be used with Sci-tools Understand 6.x the following two line should be commented.
        # if not os.path.isfile(udb_path):
        #     raise ValueError("Project directory is not valid.")
        self.db = und.open(udb_path)
        self.metrics = self.db.metric(self.db.metrics())
        self.user_defined_classes = self.get_classes()
        self.all_classes = self.get_classes(filter_string="Class")
        self.known_class_entities = self.db.ents(kindstring='Class ~Unknown')

    def __del__(self):
        logger.debug("Database closed after calculating metrics.")
        self.db.close()

    @property
    @divide_by_initial_value
    def DSC(self):
        """
        DSC - Design Size in Classes
        :return: Total number of classes in the design.
        """
        return self.metrics.get('CountDeclClass', 0)

    @property
    @divide_by_initial_value
    def NOH(self):
        """
        NOH - Number Of Hierarchies
        count(MaxInheritanceTree(class)) = 0
        :return: Total number of 'root' classes in the design.
        """
        count = 0
        for ent in self.known_class_entities:
            is_tree = False
            for ref in ent.refs("ExtendBy"):
                if ref:
                    is_tree = True
                    break
            mit = ent.metric(['MaxInheritanceTree'])['MaxInheritanceTree']
            if mit == 1 and is_tree:
                count += 1
        return count

    @property
    @divide_by_initial_value
    def ANA(self):
        """
        ANA - Average Number of Ancestors
        :return: Average number of classes in the inheritance tree for each class
        """
        MITs = []
        for ent in self.known_class_entities:
            mit = ent.metric(['MaxInheritanceTree'])['MaxInheritanceTree']
            MITs.append(mit - 1)
        return sum(MITs) / len(MITs)

    @property
    @divide_by_initial_value
    def MOA(self):
        """
        MOA - Measure of Aggregation
        :return: AVG(All Class's MOA).
        """
        return self.get_class_average(self.ClassLevelMOA)

    @property
    @divide_by_initial_value
    def DAM(self):
        """
        DAM - The Average of Direct Access Metric for all classes
        :return: AVG(All Class's DAM).
        """
        return self.get_class_average(self.ClassLevelDAM)

    @property
    @divide_by_initial_value
    def CAMC(self):
        """
        CAMC - Cohesion Among Methods of class
        :return: AVG(All Class's CAMC)
        """
        return self.get_class_average(self.ClassLevelCAMC)

    @property
    @divide_by_initial_value
    def CIS(self):
        """
        CIS - Class Interface Size
        :return: AVG(All class's CIS)
        """
        return self.get_class_average(self.ClassLevelCIS)

    @property
    @divide_by_initial_value
    def NOM(self):
        """
        NOM - Number of Methods
        :return: AVG(All class's NOM)
        """
        return self.get_class_average(self.ClassLevelNOM)

    @property
    @divide_by_initial_value
    def DCC(self):
        """
        DCC - Direct Class Coupling
        :return: AVG(All class's DCC)
        """
        return self.get_class_average(self.ClassLevelDCC)

    @property
    @divide_by_initial_value
    def MFA(self):
        """
        MFA - Measure of Functional Abstraction
        :return: AVG(All class's MFA)
        """
        return self.get_class_average(self.ClassLevelMFA)

    @property
    @divide_by_initial_value
    def NOP(self):
        """
        NOP - Number of Polymorphic Methods
        :return: AVG(All class's NOP)
        """
        return self.get_class_average(self.ClassLevelNOP)

    def ClassLevelMOA(self, class_longname):
        """
        MOA - Class Level Measure of Aggregation
        :param class_longname: The longname of a class. For examole: package_name.ClassName
        :return: Count of number of attributes whose type is user defined class(es).
        """
        class_entity = self.get_class_entity(class_longname)
        counter = 0
        for ref in class_entity.refs("Define", "Variable"):
            if ref.ent().type() in self.user_defined_classes:
                counter += 1
        for ref in class_entity.refs("Define", "Method"):
            for ref2 in ref.ent().refs("Define", "Variable"):
                if ref2.ent().type() in self.user_defined_classes:
                    counter += 1
        return counter

    def ClassLevelDAM(self, class_longname):
        """
        DAM - Class Level Direct Access Metric
        :param class_longname: The longname of a class. For examole: package_name.ClassName
        :return: Ratio of the number of private and protected attributes to the total number of attributes in a class.
        """
        public_variables = 0
        protected_variables = 0
        private_variables = 0

        class_entity = self.get_class_entity(class_longname)
        for ref in class_entity.refs("Define", "Variable"):
            define = ref.ent()
            kind_name = define.kindname()
            if "Public" in kind_name:
                public_variables += 1
            elif "Private" in kind_name:
                private_variables += 1
            elif "Protected" in kind_name:
                protected_variables += 1

        try:
            ratio = (private_variables + protected_variables) / (
                    private_variables + protected_variables + public_variables)
        except ZeroDivisionError:
            ratio = 0.0
        return ratio

    def ClassLevelCAMC(self, class_longname):
        """
        CAMC - Class Level Cohesion Among Methods of class
        Measures of how related methods are in a class in terms of used parameters.
        It can also be computed by: 1 - LackOfCohesionOfMethods()
        :param class_longname: The longname of a class. For examole: package_name.ClassName
        :return:  A float number between 0 and 1.
        """
        class_entity = self.get_class_entity(class_longname)
        percentage = class_entity.metric(['PercentLackOfCohesion']).get('PercentLackOfCohesion', 0)
        if percentage is None:
            percentage = 0
        return 1.0 - percentage / 100

    def ClassLevelCIS(self, class_longname):
        """
        CIS - Class Level Class Interface Size
        :param class_longname: The longname of a class. For examole: package_name.ClassName
        :return: Number of public methods in class
        """
        class_entity = self.get_class_entity(class_longname)
        value = class_entity.metric(['CountDeclMethodPublic']).get('CountDeclMethodPublic', 0)
        if value is None:
            value = 0
        return value

    def ClassLevelNOM(self, class_longname):
        """
        NOM - Class Level Number of Methods
        :param class_longname: The longname of a class. For examole: package_name.ClassName
        :return: Number of methods declared in a class.
        """
        class_entity = self.get_class_entity(class_longname)
        if class_entity:
            return class_entity.metric(['CountDeclMethod']).get('CountDeclMethod', 0)
        return 0

    def ClassLevelDCC(self, class_longname):
        """
        DCC - Class Level Direct Class Coupling
        :param class_longname: The longname of a class. For examole: package_name.ClassName
        :return: Number of other classes a class relates to, either through a shared attribute or a parameter in a method.
        """
        class_entity = self.get_class_entity(class_longname)
        others = set()
        for ref in class_entity.refs("Define", "Variable"):
            if ref.ent().type() in self.all_classes:
                others.add(ref.ent().type())

        for ref in class_entity.refs("Define", "Method"):
            for ref2 in ref.ent().refs("Define", "Parameter"):
                if ref2.ent().type() in self.all_classes:
                    others.add(ref2.ent().type())

        return len(others)

    def ClassLevelMFA(self, class_longname):
        """
        MFA - Class Level Measure of Functional Abstraction
        :param class_longname: The longname of a class. For examole: package_name.ClassName
        :return: Ratio of the number of inherited methods per the total number of methods within a class.
        """
        class_entity = self.get_class_entity(class_longname)
        metrics = class_entity.metric(['CountDeclMethod', 'CountDeclMethodAll'])
        local_methods = metrics.get('CountDeclMethod')
        all_methods = metrics.get('CountDeclMethodAll')
        if all_methods == 0:
            return 0
        return (all_methods - local_methods) / all_methods

    def ClassLevelNOP(self, class_longname):
        """
        NOP - Class Level Number of Polymorphic Methods
        Any method that can be used by a class and its descendants.
        :param class_longname: The longname of a class. For examole: package_name.ClassName
        :return: Counts of the number of methods in a class excluding private, static and final ones.
        """
        class_entity = self.get_class_entity(class_longname)
        if "Final" in class_entity.kindname():
            return 0
        instance_methods = class_entity.metric(['CountDeclInstanceMethod']).get('CountDeclInstanceMethod', 0)
        private_methods = class_entity.metric(['CountDeclMethodPrivate']).get('CountDeclMethodPrivate', 0)
        final_methods = 0
        for ref in class_entity.refs("Define", "Method"):
            if "Final" in ref.ent().kindname():
                final_methods += 1
        return instance_methods - (private_methods + final_methods)

    def test(self):
        print("Entity:", "Project")
        print(self.NOP)

    def get_class_entity(self, class_longname):
        for ent in self.known_class_entities:
            if ent.longname() == class_longname:
                return ent
        return None

    def get_class_average(self, class_level_metric):
        scores = []
        for ent in self.known_class_entities:
            class_metric = class_level_metric(ent.longname())
            scores.append(class_metric)
        return sum(scores) / len(scores)

    def print_all(self):
        for k, v in sorted(self.metrics.items()):
            print(k, "=", v)

    def get_classes(self, filter_string="Class ~Unknown ~TypeVariable ~Anonymous"):
        """
        :return: a set of all class names
        """
        classes = set()
        for ent in self.db.ents(kindstring=filter_string):
            classes.add(ent.simplename())
        return classes


if __name__ == '__main__':
    print(f"Path: {UDB_PATH}")
    metric = QMOOD(UDB_PATH)
    print("Object created.")
    print(f"DSC: ", metric.DSC)
    print(f"NOH: ", metric.NOH)
    print(f"ANA: ", metric.ANA)
    print(f"MOA: ", metric.MOA)
    print(f"DAM: ", metric.DAM)
    print(f"CAMC: ", metric.CAMC)
    print(f"CIS: ", metric.CIS)
    print(f"NOM: ", metric.NOM)
    print(f"DCC: ", metric.DCC)
    print(f"MFA: ", metric.MFA)
    print(f"NOP: ", metric.NOP)
    del metric
