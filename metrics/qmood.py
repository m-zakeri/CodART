"""
The module compute and normalize QMOOD design metrics and QMOOD quality attributes
to be used as six objectives in search-based refactoring

## Reference
[1] J. Bansiya and C. G. Davis, “A hierarchical model for object-oriented design quality assessment,”
IEEE Trans. Softw. Eng., vol. 28, no. 1, pp. 4–17, 2002.

"""

__version__ = '0.2.0'
__author__ = 'Morteza Zakeri'

import os
from pprint import pprint

try:
    import understand as und
except ImportError:
    print("Cannot import understand.")

from sbse.config import CURRENT_METRICS, UDB_PATH, logger


def divide_by_initial_value(func):
    def wrapper(*args, **kwargs):
        value = func(*args, **kwargs)
        initial = CURRENT_METRICS.get(func.__name__)
        if initial == 0:
            initial = 1.
        value = round(value / initial, 5)
        return value

    return wrapper


class DesignMetrics:
    """
    Class to compute 11 design metrics listed by J. Bansiya et G. Davis, 2002

    """

    def __init__(self, udb_path):
        # To be used with Sci-tools Understand 6.x the following two line should be commented.
        # if not os.path.isfile(udb_path):
        #     raise ValueError("Project directory is not valid.")
        self.db = und.open(udb_path)
        self.metrics = self.db.metric(self.db.metrics())

        filter1 = "Java Class ~TypeVariable ~Anonymous ~Enum ~Interface ~Jar ~Library ~Standard"
        filter2 = "Java Class ~Unresolved ~Unknown ~TypeVariable ~Anonymous ~Annotation ~Enum ~Interface ~Jar ~Library ~Standard"
        filter3 = "Java Class ~Unresolved ~Unknown ~TypeVariable ~Anonymous ~Enum ~Interface ~Jar ~Library ~Standard"
        self.all_classes = self.get_classes(filter1)
        self.known_class_entities = self.db.ents(filter2)
        self.user_defined_classes = self.get_classes(filter3)

    def __del__(self):
        # self.db.close()
        pass

    @property
    @divide_by_initial_value
    def DSC(self):
        """
        DSC - Design size in classes
        :return: Total number of classes in the design.
        """
        return len(self.user_defined_classes)

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
            for ref in ent.refs("Extendby"):
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
        CAMC or CAM - Cohesion Among Methods of class
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
        default_variables = 0

        class_entity = self.get_class_entity(class_longname)
        for ref in class_entity.refs("Define", "Variable ~Local ~Unknown"):
            defined_entity = ref.ent()
            kind_name = str(defined_entity.kindname())

            if kind_name.find('Public') != -1:
                public_variables += 1
            elif kind_name.find('Private') != -1:
                private_variables += 1
            elif kind_name.find('Protected') != -1:
                protected_variables += 1
            elif kind_name.find('Default') != -1:
                default_variables += 1
        try:
            enum_ = private_variables + protected_variables
            denum_ = private_variables + protected_variables + default_variables + public_variables
            ratio = enum_ / denum_
        except ZeroDivisionError:
            # logger.error('ZeroDivisionError in computing QMOOD DAM metric.')
            ratio = 1.0
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
            # print(class_entity.metric(['CountDeclMethod']).get('CountDeclMethod', 0))
            method_list = class_entity.ents('Define', 'Java Method ~Unknown ~Unresolved ~Jar ~Library ~Constructor ~Implicit ~Lambda ~External')
            counter = 0
            for method_ in method_list:
                if method_.metric(['Cyclomatic']).get('Cyclomatic', 0) > 1:
                    counter += 1
            return counter

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

        for ref in class_entity.refs("Define", "Method ~Unknown ~Unresolved ~Jar ~Library ~Constructor ~Implicit ~Lambda ~External"):
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
        static_methods = class_entity.metric(['CountDeclClassMethod']).get('CountDeclClassMethod', 0)
        final_methods = 0
        for ref in class_entity.refs('Define', 'Java Method ~Unknown ~Unresolved ~Jar ~Library ~Constructor ~Implicit ~Lambda ~External'):
            if "Final" in ref.ent().kindname():
                final_methods += 1
        return instance_methods - (private_methods + final_methods + static_methods)

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

    def get_classes(self, filter_string=None):
        """
        :return: a set of all class names
        """
        classes = set()
        for ent in self.db.ents(filter_string):
            classes.add(ent.simplename())
        return classes


class DesignQualityAttributes:
    """
    Class to compute six quality attribute proposed by J. J. Bansiya et G. Davis, 2002
    The QMOOD quality attribute are:
        1. Reusability
        2. Flexibility
        3. Understandability
        4. Functionality
        5. Extendability
        6. Effectiveness
    """

    def __init__(self, udb_path):
        """
        Implements Project Objectives due to QMOOD design metrics
        :param udb_path: The understand database path
        """
        self.udb_path = udb_path
        self.__qmood = DesignMetrics(udb_path=udb_path)
        # Calculating once and using multiple times
        self.DSC = self.__qmood.DSC
        self.NOH = self.__qmood.NOH
        self.ANA = self.__qmood.ANA
        self.MOA = self.__qmood.MOA
        self.DAM = self.__qmood.DAM
        self.CAMC = self.__qmood.CAMC
        self.CIS = self.__qmood.CIS
        self.NOM = self.__qmood.NOM
        self.DCC = self.__qmood.DCC
        self.MFA = self.__qmood.MFA
        self.NOP = self.__qmood.NOP

        # For caching results
        self._reusability = None
        self._flexibility = None
        self._understandability = None
        self._functionality = None
        self._extendability = None
        self._effectiveness = None

    @property
    def reusability(self):
        """
        A design with low coupling and high cohesion is easily reused by other designs.
        :return: reusability score
        """
        self._reusability = -0.25 * self.DCC + 0.25 * self.CAMC + 0.5 * self.CIS + 0.5 * self.DSC
        return self._reusability

    @property
    def flexibility(self):
        """
        The degree of allowance of changes in the design.
        :return: flexibility score
        """
        self._flexibility = 0.25 * self.DAM - 0.25 * self.DCC + 0.5 * self.MOA + 0.5 * self.NOP
        return self._flexibility

    @property
    def understandability(self):
        """
        The degree of understanding and the easiness of learning the design implementation details.
        :return: understandability score
        """
        self._understandability = -0.33 * self.ANA + 0.33 * self.DAM - 0.33 * self.DCC + \
                                  0.33 * self.CAMC - 0.33 * self.NOP - 0.33 * self.NOM - \
                                  0.33 * self.DSC
        return self._understandability

    @property
    def functionality(self):
        """
        Classes with given functions that are publicly stated in interfaces to be used by others.
        :return: functionality score
        """
        self._functionality = 0.12 * self.CAMC + 0.22 * self.NOP + 0.22 * self.CIS + 0.22 * self.DSC + 0.22 * self.NOH
        return self._functionality

    @property
    def extendability(self):
        """
        Measurement of design's allowance to incorporate new functional requirements.
        :return: extendability
        """
        self._extendability = 0.5 * self.ANA - 0.5 * self.DCC + 0.5 * self.MFA + 0.5 * self.NOP
        return self._extendability

    @property
    def effectiveness(self):
        """
        Design efficiency in fulfilling the required functionality.
        :return: effectiveness score
        """
        self._effectiveness = 0.2 * self.ANA + 0.2 * self.DAM + 0.2 * self.MOA + 0.2 *  self.MFA + 0.2 * self.NOP
        return self._effectiveness

    @property
    def average(self):
        metrics = ['reusability', 'flexibility', 'understandability', 'functionality', 'extendability', 'effectiveness',]
        all_metrics = []
        for metric in metrics:
            cache = getattr(self, f'_{metric}')
            if cache is None:
                all_metrics.append(getattr(self, metric))
            else:
                all_metrics.append(cache)
        return sum(all_metrics) / len(all_metrics)


if __name__ == '__main__':
    print(f"UDB path: {UDB_PATH}")
    design_metric = DesignMetrics(UDB_PATH)
    design_quality_attribute = DesignQualityAttributes(UDB_PATH)
    metrics_dict = {
        "DSC": design_metric.DSC,
        "NOH": design_metric.NOH,
        "ANA": design_metric.ANA,
        "MOA": design_metric.MOA,
        "DAM": design_metric.DAM,
        "CAMC": design_metric.CAMC,
        "CIS": design_metric.CIS,
        "NOM": design_metric.NOM,
        "DCC": design_metric.DCC,
        "MFA": design_metric.MFA,
        "NOP": design_metric.NOP
    }
    quality_attributes_dict = {
        "reusability": design_quality_attribute.reusability,
        "flexibility": design_quality_attribute.flexibility,
        "understandability": design_quality_attribute.understandability,
        "functionality": design_quality_attribute.functionality,
        "extendability": design_quality_attribute.extendability,
        "effectiveness": design_quality_attribute.effectiveness,
        #
        "average": design_quality_attribute.average
    }
    print('QMOOD design metrics (normalized):')
    pprint(metrics_dict)
    print('QMOOD quality attributes:')
    pprint(quality_attributes_dict)
