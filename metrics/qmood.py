"""
The module compute and normalize QMOOD design metrics and QMOOD quality attributes
to be used as six objectives in search-based refactoring

## Reference
[1] J. Bansiya and C. G. Davis, “A hierarchical model for object-oriented design quality assessment,”
IEEE Trans. Softw. Eng., vol. 28, no. 1, pp. 4–17, 2002.

"""

__version__ = '0.3.0'
__author__ = 'Morteza Zakeri'


import understand as und

from sbse import config


def divide_by_initial_value(func):
    def wrapper(*args, **kwargs):
        value = func(*args, **kwargs)
        initial = config.CURRENT_METRICS.get(func.__name__)
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
        self.udb_path = udb_path

        filter1 = "Java Class ~TypeVariable ~Anonymous ~Enum, Java Interface"
        filter3 = "Java Class ~Unresolved ~Unknown ~TypeVariable ~Anonymous ~Enum  ~Jar ~Library ~Standard, Java Interface"
        self.all_classes = self.get_classes_simple_names(filter1)
        self.user_defined_classes = self.get_classes_simple_names(filter3)

    def __del__(self):
        # self.db.close()
        pass

    @property
    @divide_by_initial_value
    def DSC(self):
        """
        DSC - Design size in classes, project-level design metric
        :return: Total number of classes in the design.
        """
        return len(self.user_defined_classes)

    @property
    @divide_by_initial_value
    def NOH(self):
        """
        NOH - Number Of Hierarchies, project-level design metric
        count(MaxInheritanceTree(class)) = 0
        :return: Total number of 'root' classes in the design.
        """
        count = 0
        dbx: und.Db = und.open(self.udb_path)
        filter2 = "Java Class ~Unresolved ~Unknown ~TypeVariable ~Anonymous ~Enum, Java Interface"
        known_class_entities = dbx.ents(filter2)
        for ent in known_class_entities:
            is_tree = False
            for ref in ent.refs("Extendby"):
                if ref:
                    is_tree = True
                    break
            mit = ent.metric(['MaxInheritanceTree'])['MaxInheritanceTree']
            if mit == 1 and is_tree:
                count += 1

        dbx.close()
        return count

    @property
    @divide_by_initial_value
    def ANA(self):
        """
        ANA - Average Number of Ancestors, project-level design metric
        :return: Average number of classes in the inheritance tree for each class
        """
        MITs = []
        dbx: und.Db = und.open(self.udb_path)
        filter2 = "Java Class ~Unresolved ~Unknown ~TypeVariable ~Anonymous ~Enum, Java Interface"
        known_class_entities = dbx.ents(filter2)

        for ent in known_class_entities:
            mit = ent.metric(['MaxInheritanceTree'])['MaxInheritanceTree']
            MITs.append(mit - 1)

        dbx.close()
        return sum(MITs) / len(MITs)

    @property
    @divide_by_initial_value
    def MOA(self):
        """
        MOA - Measure of Aggregation, to be a project-level design metric
        :return: AVG(All Class's MOA).
        """
        return self.get_class_average(self.MOA_class_level)

    @property
    @divide_by_initial_value
    def DAM(self):
        """
        DAM - The Average of Direct Access Metric of class, to be a project-level design metric
        :return: AVG(All Class's DAM).
        """
        return self.get_class_average(self.DAM_class_level)

    @property
    @divide_by_initial_value
    def CAMC(self):
        """
        CAMC or CAM - Cohesion Among Methods of class, to be a project-level design metric
        :return: AVG(All Class's CAMC)
        """
        return self.get_class_average(self.CAMC_class_level)

    @property
    @divide_by_initial_value
    def CIS(self):
        """
        CIS - Class Interface Size, to be a project-level design metric
        :return: AVG(All class's CIS)
        """
        return self.get_class_average(self.CIS_class_level)

    @property
    @divide_by_initial_value
    def NOM(self):
        """
        NOM - Number of Methods, to be a project-level design metric
        :return: AVG(All class's NOM)
        """
        return self.get_class_average(self.NOM_class_level)

    @property
    @divide_by_initial_value
    def DCC(self):
        """
        DCC - Direct Class Coupling, to be a project-level design metric
        :return: AVG(All class's DCC)
        """
        return self.get_class_average(self.DCC_class_level)

    @property
    @divide_by_initial_value
    def MFA(self):
        """
        MFA - Measure of Functional Abstraction, to be a project-level design metric
        :return: AVG(All class's MFA)
        """
        return self.get_class_average(self.MFA_class_level)

    @property
    @divide_by_initial_value
    def NOP(self):
        """
        NOP - Number of Polymorphic Methods, to be a project-level design metric
        :return: AVG(All class's NOP)
        """
        return self.get_class_average(self.NOP_class_level)

    def MOA_class_level(self, class_entity: und.Ent):
        """
        MOA - Class Level Measure of Aggregation
        :param class_entity: The class entity.
        :return: Count of number of attributes whose type is user defined class(es).
        """
        counter = 0
        for ref in class_entity.refs("Define", "Variable"):
            if ref.ent().type() in self.user_defined_classes:
                counter += 1
        for ref in class_entity.refs("Define", "Method"):
            for ref2 in ref.ent().refs("Define", "Variable"):
                if ref2.ent().type() in self.user_defined_classes:
                    counter += 1
        return counter

    def DAM_class_level(self, class_entity: und.Ent):
        """
        DAM - Class Level Direct Access Metric
        :param class_entity: The class entity.
        :return: Ratio of the number of private and protected attributes to the total number of attributes in a class.
        """
        public_variables = 0
        protected_variables = 0
        private_variables = 0
        default_variables = 0

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

    def CAMC_class_level(self, class_entity: und.Ent):
        """
        CAMC - Class Level Cohesion Among Methods of class
        Measures of how related methods are in a class in terms of used parameters.
        It can also be computed by: 1 - LackOfCohesionOfMethods()
        :param class_entity: The class entity.
        :return:  A float number between 0 and 1.
        """
        if "Interface" in class_entity.kindname():
            return 1

        percentage = class_entity.metric(['PercentLackOfCohesion']).get('PercentLackOfCohesion', 0)

        if percentage is None:
            percentage = 0
        cohesion_ = 1. - (percentage / 100.)
        # print(class_entity.longname(), cohesion_)
        return round(cohesion_, 5)

    def CIS_class_level(self, class_entity: und.Ent):
        """
        CIS - Class Level Class Interface Size
        :param class_entity: The class entity
        :return: Number of public methods in class
        """
        value = class_entity.metric(['CountDeclMethodPublic']).get('CountDeclMethodPublic', 0)
        if value is None:
            value = 0
        # print(class_entity.longname(), value)
        return value

    def NOM_class_level(self, class_entity: und.Ent):
        """
        NOM - Class Level Number of Methods (WMC)
        :param class_entity: The class entity
        :return: Number of methods declared in a class.
        """
        if class_entity is not None:
            # print(class_entity.metric(['CountDeclMethod']).get('CountDeclMethod', 0))
            # kind_filter = 'Java Method ~Unknown ~Unresolved ~Jar ~Library ~Constructor ~Implicit ~Lambda ~External'
            # method_list = class_entity.ents('Define', kind_filter)
            # counter = 0
            # for method_ in method_list:
            #     if method_.metric(['Cyclomatic']).get('Cyclomatic', 0) > 1:
            #         counter += 1
            # return counter
            if "Interface" in class_entity.kindname():
                return 0
            return class_entity.metric(['SumCyclomatic']).get('SumCyclomatic', 0)
        return 0

    def DCC_class_level(self, class_entity: und.Ent):
        """
        DCC - Class Level Direct Class Coupling
        :param class_entity: The class entity
        :return: Number of other classes a class relates to, either through a shared attribute or
        a parameter in a method.
        """
        others = set()
        if "Interface" in class_entity.kindname():
            return 0
        for ref in class_entity.refs("Define", "Variable"):
            if ref.ent().type() in self.all_classes:
                others.add(ref.ent().type())

        kind_filter = "Method ~Unknown ~Unresolved ~Jar ~Library ~Constructor ~Implicit ~Lambda ~External"
        for ref in class_entity.refs("Define", kind_filter):
            for ref2 in ref.ent().refs("Define", "Parameter"):
                if ref2.ent().type() in self.all_classes:
                    others.add(ref2.ent().type())

        return len(others)

    def MFA_class_level(self, class_entity: und.Ent):
        """
        MFA - Class Level Measure of Functional Abstraction
        :param class_entity: The class entity
        :return: Ratio of the number of inherited methods per the total number of methods within a class.
        """
        metrics = class_entity.metric(['CountDeclMethod', 'CountDeclMethodAll'])
        local_methods = metrics.get('CountDeclMethod')
        all_methods = metrics.get('CountDeclMethodAll')
        # print(class_entity.longname(), metrics)

        mfa = 0
        if "Interface" in class_entity.kindname():
            mfa = 1
        else:
            implemented_interfaces = class_entity.ents('Java Implement Couple', '~Unknown')
            if len(implemented_interfaces) == 0:
                if all_methods == 0:
                    mfa = 0
                else:
                     mfa = round((all_methods - local_methods) / all_methods, 5)
            else:
                implemented_methods = 0
                for interface_entity in implemented_interfaces:
                    implemented_methods += interface_entity.metric(['CountDeclMethodAll']).get('CountDeclMethodAll', 0)
                mfa = round((all_methods - implemented_methods) / all_methods, 5)
        # print(class_entity.longname(), mfa)
        return mfa if mfa >= 0 else 1

    def NOP_class_level(self, class_entity: und.Ent):
        """
        NOP - Class Level Number of Polymorphic Methods
        Any method that can be used by a class and its descendants.
       :param class_entity: The class entity
        :return: Counts of the number of methods in a class excluding private, static and final ones.
        """
        if "Final" in class_entity.kindname():
            return 0
        all_methods = class_entity.metric(['CountDeclMethodAll']).get('CountDeclMethodAll', 0)
        # private_methods = class_entity.metric(['CountDeclMethodPrivate']).get('CountDeclMethodPrivate', 0)
        # static_methods = class_entity.metric(['CountDeclClassMethod']).get('CountDeclClassMethod', 0)
        # final_methods = 0
        private_or_static_or_final = 0
        kind_filter = 'Java Method ~Unknown ~Unresolved ~Jar ~Library ~Constructor ~Implicit ~Lambda ~External'
        for ref in class_entity.refs('Define', kind_filter):
            if "Final" in ref.ent().kindname() or "Private" in ref.ent().kindname() or "Static" in ref.ent().kindname():
                private_or_static_or_final += 1
        poly_ = all_methods - private_or_static_or_final
        # print(class_entity.longname(), poly_)
        return poly_ if poly_ >= 0 else 0

    def get_classes_simple_names(self, filter_string: str = None) -> set:
        """
        :return: a set of all classes (short name) names matched with a given filter on db entities
        """
        classes = set()
        dbx: und.Db = und.open(self.udb_path)
        for ent in dbx.ents(filter_string):
            classes.add(ent.simplename())
        dbx.close()
        return classes

    def get_class_average(self, class_level_design_metric):
        scores = []
        dbx: und.Db = und.open(self.udb_path)
        filter2 = "Java Class ~Unresolved ~Unknown ~TypeVariable ~Anonymous ~Enum, Java Interface"
        known_class_entities = dbx.ents(filter2)
        for class_entity in known_class_entities:
            class_metric = class_level_design_metric(class_entity)
            scores.append(class_metric)

        dbx.close()
        return round(sum(scores) / len(scores), 5)

    def print_project_metrics(self):
        dbx = und.open(self.udb_path)
        db_level_metrics = dbx.metric(dbx.metrics())
        for k, v in sorted(db_level_metrics.items()):
            print(k, "=", v)
        dbx.close()


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
        self.DSC = self.__qmood.DSC  # Design Size
        self.NOH = self.__qmood.NOH  # Hierarchies
        self.ANA = self.__qmood.ANA  # Abstraction
        self.MOA = self.__qmood.MOA  # Composition, Aggregation
        self.DAM = self.__qmood.DAM  # Encapsulation
        self.CAMC = self.__qmood.CAMC  # Cohesion, CAM
        self.CIS = self.__qmood.CIS  # Messaging
        self.NOM = self.__qmood.NOM  # Complexity
        self.DCC = self.__qmood.DCC  # Coupling
        self.MFA = self.__qmood.MFA  # Inheritance
        self.NOP = self.__qmood.NOP  # Polymorphism

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
        return round(self._reusability, 5)

    @property
    def flexibility(self):
        """
        The degree of allowance of changes in the design.
        :return: flexibility score
        """
        self._flexibility = 0.25 * self.DAM - 0.25 * self.DCC + 0.5 * self.MOA + 0.5 * self.NOP
        return round(self._flexibility, 5)

    @property
    def understandability(self):
        """
        The degree of understanding and the easiness of learning the design implementation details.
        :return: understandability score
        """
        self._understandability = - 0.33 * self.ANA + 0.33 * self.DAM - 0.33 * self.DCC + 0.34 * self.CAMC \
                                  - 0.33 * self.NOP - 0.33 * self.NOM - 0.33 * self.DSC
        return round(self._understandability, 5)

    @property
    def functionality(self):
        """
        Classes with given functions that are publicly stated in interfaces to be used by others.
        :return: functionality score
        """
        self._functionality = 0.12 * self.CAMC + 0.22 * self.NOP + 0.22 * self.CIS + 0.22 * self.DSC + 0.22 * self.NOH
        return round(self._functionality, 5)

    @property
    def extendability(self):
        """
        Measurement of design's allowance to incorporate new functional requirements.
        :return: extendability
        """
        self._extendability = 0.50 * self.ANA - 0.50 * self.DCC + 0.50 * self.MFA + 0.50 * self.NOP
        return round(self._extendability, 5)

    @property
    def effectiveness(self):
        """
        Design efficiency in fulfilling the required functionality.
        :return: effectiveness score
        """
        self._effectiveness = 0.20 * self.ANA + 0.20 * self.DAM + 0.20 * self.MOA + 0.20 * self.MFA + 0.20 * self.NOP
        return round(self._effectiveness, 5)

    @property
    def average_sum(self):
        attrs = ['reusability', 'flexibility', 'understandability', 'functionality', 'extendability', 'effectiveness', ]
        all_metrics = []
        for metric in attrs:
            cache = getattr(self, f'_{metric}')
            if cache is None:
                all_metrics.append(getattr(self, metric))
            else:
                all_metrics.append(cache)
        return round(sum(all_metrics) / len(all_metrics), 5), round(sum(all_metrics), 5)


if __name__ == '__main__':
    from codart.utility.directory_utils import update_understand_database
    update_understand_database(config.UDB_PATH)
    print(f"UDB path: {config.UDB_PATH}")

    design_quality_attribute = DesignQualityAttributes(config.UDB_PATH)
    metrics_dict = {
        "DSC": design_quality_attribute.DSC,
        "NOH": design_quality_attribute.NOH,
        "ANA": design_quality_attribute.ANA,
        "MOA": design_quality_attribute.MOA,
        "DAM": design_quality_attribute.DAM,
        "CAMC": design_quality_attribute.CAMC,
        "CIS": design_quality_attribute.CIS,
        "NOM": design_quality_attribute.NOM,
        "DCC": design_quality_attribute.DCC,
        "MFA": design_quality_attribute.MFA,
        "NOP": design_quality_attribute.NOP
    }
    avg_, sum_ = design_quality_attribute.average_sum
    quality_attributes_dict = {
        "reusability": design_quality_attribute.reusability,
        "understandability": design_quality_attribute.understandability,
        "flexibility": design_quality_attribute.flexibility,
        "functionality": design_quality_attribute.functionality,
        "effectiveness": design_quality_attribute.effectiveness,
        "extendability": design_quality_attribute.extendability,
        #
        "average": avg_,
        "sum": sum_
    }
    print('QMOOD design metrics (normalized):')
    print(metrics_dict)
    print('QMOOD quality attributes:')
    print(quality_attributes_dict)
