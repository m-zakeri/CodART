import os
import understand


class Metric:
    def __init__(self, udb_path):
        if not os.path.isfile(udb_path):
            raise ValueError("Project directory is not valid.")
        self.db = understand.open(udb_path)
        self.metrics = self.db.metric(self.db.metrics())

    @property
    def DSC(self):
        """
        DSC - Design Size in Classes
        :return: Total number of classes in the design.
        """
        return self.metrics.get('CountDeclClass', 0)

    @property
    def NOH(self):
        """
        NOH - Number Of Hierarchies
        count(MaxInheritanceTree(class)) = 0
        :return: Total number of 'root' classes in the design.
        """
        count = 0
        for ent in sorted(self.db.ents(kindstring='class'), key=lambda ent: ent.name()):
            if ent.kindname() == "Unknown Class":
                continue
            mit = ent.metric(['MaxInheritanceTree'])['MaxInheritanceTree']
            if mit == 1:
                count += 1
        return count

    @property
    def ANA(self):
        """
        ANA - Average Number of Ancestors
        :return: Average number of classes in the inheritance tree for each class
        """
        MITs = []
        for ent in sorted(self.db.ents(kindstring='class'), key=lambda ent: ent.name()):
            if ent.kindname() == "Unknown Class":
                continue
            mit = ent.metric(['MaxInheritanceTree'])['MaxInheritanceTree']
            MITs.append(mit)
        return sum(MITs) / len(MITs)

    @property
    def MOA(self):
        """
        MOA - Measure of Aggregation
        :return: Count of number of attributes whose type is user defined class(es).
        """
        counter = 0
        user_defined_classes = []
        for ent in sorted(self.db.ents(kindstring="class"), key=lambda ent: ent.name()):
            if ent.kindname() == "Unknown Class":
                continue
            user_defined_classes.append(ent.simplename())
        for ent in sorted(self.db.ents(kindstring="variable"), key=lambda ent: ent.name()):
            if ent.type() in user_defined_classes:
                counter += 1
        return counter

    def DAM(self, class_longname):
        """
        DAM - Direct Access Metric
        :param class_longname: The longname of a class. For examole: package_name.ClassName
        :return: Ratio of the number of private and protected attributes to the total number of attributes in a class.
        """
        public_variables = 0
        protected_variables = 0
        private_variables = 0

        class_entity = self.get_class_entity(class_longname)
        for ref in class_entity.refs(refkindstring="define"):
            define = ref.ent()
            kind_name = define.kindname()
            if kind_name == "Public Variable":
                public_variables += 1
            elif kind_name == "Private Variable":
                private_variables += 1
            elif kind_name == "Protected Variable":
                protected_variables += 1

        try:
            ratio = (private_variables + protected_variables) / (
                        private_variables + protected_variables + public_variables)
        except ZeroDivisionError:
            ratio = 0.0
        return ratio

    def CMAC(self, class_longname):
        """
        CMAC - Cohesion Among Methods of class
        Measures of how related methods are in a class in terms of used parameters.
        It can also be computed by: 1 - LackOfCohesionOfMethods()
        :param class_longname: The longname of a class. For examole: package_name.ClassName
        :return:  A float number between 0 and 1.
        """
        class_entity = self.get_class_entity(class_longname)
        percentage = class_entity.metric(['PercentLackOfCohesion']).get('PercentLackOfCohesion', 0)
        return 1.0 - percentage / 100

    def CIS(self, class_longname):
        """
        CIS - Class Interface Size
        :param class_longname: The longname of a class. For examole: package_name.ClassName
        :return: Number of public methods in class
        """
        class_entity = self.get_class_entity(class_longname)
        if class_entity:
            return class_entity.metric(['CountDeclMethodPublic']).get('CountDeclMethodPublic', 0)
        return 0

    def NOM(self, class_longname):
        """
        NOM - Number of Methods
        :param class_longname: The longname of a class. For examole: package_name.ClassName
        :return: Number of methods declared in a class.
        """
        class_entity = self.get_class_entity(class_longname)
        if class_entity:
            return class_entity.metric(['CountDeclMethod']).get('CountDeclMethod', 0)
        return 0

    def DCC(self, class_longname):
        """
        DCC - Direct Class Coupling
        :param class_longname:
        :return: Number of other classes a class relates to, either through a shared attribute or a parameter in a method.
        """
        counter = 0
        class_entity = self.get_class_entity(class_longname)
        for ref in class_entity.refs():
            if ref.kindname() == "Couple":
                if ref.isforward():
                    if "class" in ref.ent().kindname().lower():
                        counter += 1
        return counter

    def test(self):
        for ent in sorted(self.db.ents(kindstring='class'), key=lambda ent: ent.name()):
            if ent.kindname() == "Unknown Class":
                continue
            print("Entity:", ent)
            print(self.DCC(ent.longname()))

    def get_class_entity(self, class_longname):
        for ent in sorted(self.db.ents(kindstring='class'), key=lambda ent: ent.name()):
            if ent.kindname() == "Unknown Class":
                continue
            if ent.longname() == class_longname:
                return ent
        return None

    def print_all(self):
        for k, v in sorted(self.metrics.items()):
            print(k, "=", v)


if __name__ == '__main__':
    db_path = "/home/ali/Desktop/code/TestProject/TestProject.udb"
    metric = Metric(db_path)
    # metric.print_all()
    print(metric.MOA)
    # metric.test()
