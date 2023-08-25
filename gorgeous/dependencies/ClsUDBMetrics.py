import os
import subprocess
os.add_dll_directory("C:\\Program Files\\SciTools\\bin\\pc-win64")

import understand
import understand as und
from dotenv import dotenv_values
import json


class ClsUDB_Metrics:
    def __init__(self):
        pass

    def create_understand_database_from_project(self, root_path):
        """
        This function creates understand database for the given project directory.
        Args:
            project_dir (str): The absolute path of project's directory.
            db_dir (str): The absolute directory path to save Understand database (.udb or .und binary file)
        Returns:
            str: Understand database path
        """
        my_path = os.getcwd() + "/Resources/projects/" + root_path
        assert os.path.isdir(my_path)
        db_name = os.path.basename(os.path.normpath(root_path)) + ".und"
        db_path = os.path.join("Resources/und_db/", db_name)
        if os.path.exists(db_path):
            return db_path
        # An example of command-line is:
        # und create -languages c++ add @myFiles.txt analyze -all myDb.udb
        # understand_5_cmd = ['und', 'create', '-languages', 'Java', 'add', project_dir, 'analyze', '-all', db_path]
        understand_6_cmd = ["und", "create", "-db", db_path, "-languages", "java"]
        understand_7_cmd = [
            "und",
            "-db",
            db_path,
            "add",
            "Resources/projects/" + root_path,
            "analyze",
            "-all",
        ]

        result = subprocess.run(
            understand_6_cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE
        )
        result_2 = subprocess.run(
            understand_7_cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE
        )

        if result.returncode != 0:
            error_ = result.stderr.decode("utf-8")
            print(f"return code: {result.returncode} msg: {error_}")
        else:
            print(f"Understand project was created successfully!")

        if result_2.returncode != 0:
            error_ = result_2.stderr.decode("utf-8")
            print(f"return code: {result_2.returncode} msg: {error_}")
        else:
            print(f"Understand analyze successfully!")

        return db_path

    def get_metrics(self, my_path):
        db = understand.open("Resources/und_db/" + my_path + ".und")
        metrics = db.metric(dotenv_values().get("LIST_METRICS_CLASS").split(" "))
        for k, v in sorted(metrics.items()):
            print(k, "=", v)
        db.close()

    def get_metrics_of_each_function(self, my_path: str):
        db = understand.open(my_path)
        for func in db.ents("function,method,procedure"):
            metric = func.metric(dotenv_values().get("LIST_METRICS_METHOD").split(" "))
            for k, v in metric.items():
                print(k, "=", v)
        db.close()

    def get_metrics_of_each_class(self, my_path: str = "", element: list = None):
        db = understand.open(my_path)
        for func in db.ents("class"):
            for i in element:
                metric = func.metric(
                    dotenv_values().get("LIST_METRICS_CLASS").split(" ")
                )
                if i == func.name():
                    print("IN IF", func.name())
                    db.close()
                    return metric, True
        return None, False

    def get_dep_of_each_class(self, csv_path: str, db_path: str):
        """
        Exports understand dependencies into a csv file.
        :param csv_path: The absolute address of csv file to generate.
        :param db_path: The absolute address of project path.
        :return: None
        """

        csv_path = csv_path + db_path + "_dep.csv"
        db_path = "Resources/und_db/" + db_path + ".und"
        command = [
            "und",
            "export",
            "-db",
            db_path,
            "-dependencies",
            "class",
            "matrix",
            csv_path,
        ]
        result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        if result.returncode != 0:
            error_ = result.stderr.decode("utf-8")
            print(f"return code: {result.returncode} msg: {error_}")
        else:
            print("Modular dependency graph (MDG.csv) was exported.")

    def update_understand_database(self, udb_path):
        """
        This function updates database due to file changes.
        If any error, such as database is locked or read only, occurred it tries again and again to update db.
        Arges:
            udb_path (str): The absolute path of understand database.
        Return:
            None
        """
        understand_5_cmd = ["und", "analyze", "-rescan", "-changed", udb_path]
        understand_6_cmd = [
            "und",
            "analyze",
            "-changed",
            udb_path,
        ]  # -rescan option is not required for understand >= 6.0

        result = subprocess.run(
            understand_6_cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE
        )

        # info_ = result.stdout.decode('utf-8')
        # error_ = result.stderr.decode('utf-8')
        # print(info_[:85])
        # print(f'return code: {result.returncode} --- error: {error_}')
        trials = 0
        while result.returncode != 0:
            try:
                db: understand.Db = understand.open(
                    "Resources/und_db/"
                    + dotenv_values().get("RESOURCES_PATH").split(" ")[0]
                    + ".und"
                )
                db.close()
            except:
                pass
            finally:

                result = subprocess.run(
                    understand_6_cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE  #
                )
                # info_ = result.stdout.decode('utf-8')
                error_ = result.stderr.decode("utf-8")
                # print(info_[:85])
                print(f"return code: {result.returncode} msg: {error_}")
                trials += 1
                if trials > 5:
                    break


class DesignMetrics:
    """
    Class to compute 11 design metrics listed by J. Bansiya et G. Davis, 2002
    """

    def __init__(self, udb_path):
        self.udb_path = udb_path

        filter1 = "Java Class ~TypeVariable ~Anonymous ~Enum, Java Interface"
        filter3 = "Java Class ~Unresolved ~Unknown ~TypeVariable ~Anonymous ~Enum ~Jar ~Library ~Standard, Java Interface"
        self.all_classes = self.get_classes_simple_names(filter1)
        self.user_defined_classes = self.get_classes_simple_names(filter3)

    def __del__(self):
        # self.db.close()
        pass

    @property
    def CAMC(self):
        """
        CAMC or CAM - Cohesion Among Methods of class, to be a project-level design metric
        :return: AVG(All Class's CAMC)
        """
        return self.get_class_average(self.CAMC_class_level)

    @property
    def DCC(self):
        """
        DCC - Direct Class Coupling, to be a project-level design metric
        :return: AVG(All class's DCC)
        """
        return self.get_class_average(self.DCC_class_level)

    def CAMC_class_level(self, class_entity: und.Ent):
        """
        CAMC - Class Level Cohesion Among Methods of class
        Measures of how related methods are in a class in terms of used parameters.
        It can also be computed by: 1 - LackOfCohesionOfMethods()
        :param class_entity: The class entity.
        :return:  A float number between 0 (1) and 1 (2).
        """
        if "Interface" in class_entity.kindname():
            return 2.0

        percentage = class_entity.metric(["PercentLackOfCohesion"]).get(
            "PercentLackOfCohesion", 0
        )

        if percentage is None:
            percentage = 0
        cohesion_ = 1.0 - (percentage / 100.0)
        # print(class_entity.longname(), cohesion_)
        return 1.0 + round(cohesion_, 5)

    def DCC_class_level(self, class_entity: und.Ent):
        """
        DCC - Class Level Direct Class Coupling
        :param class_entity: The class entity
        :return: Number of other classes a class relates to, either through a shared attribute or
        a parameter in a method.
        """
        others = list()
        if "Interface" in class_entity.kindname():
            return 0

        for ref in class_entity.refs("Define", "Variable"):
            if ref.ent().type() in self.all_classes:
                others.append(ref.ent().type())

        kind_filter = (
            "Method ~Unknown ~Jar ~Library ~Constructor ~Implicit ~Lambda ~External"
        )
        for ref in class_entity.refs("Define", kind_filter):
            for ref2 in ref.ent().refs("Java Define", "Java Parameter"):
                if ref2.ent().type() in self.all_classes:
                    others.append(ref2.ent().type())

        for ref in class_entity.refs("Define", kind_filter):
            for ref2 in ref.ent().refs("Java Use Return"):
                if ref2.ent().type() in self.all_classes:
                    others.append(ref2.ent().type())

        return len(set(others))

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
        filter2 = "Java Class ~Unknown ~TypeVariable ~Anonymous ~Enum, Java Interface"
        known_class_entities = dbx.ents(filter2)
        for class_entity in known_class_entities:
            class_metric = class_level_design_metric(class_entity)
            scores.append(class_metric)

        dbx.close()
        return round(sum(scores) / len(scores), 5)
        # return sum(scores)

    def print_project_metrics(self):
        dbx = und.open(self.udb_path)
        db_level_metrics = dbx.metric(dbx.metrics())
        for k, v in sorted(db_level_metrics.items()):
            print(k, "=", v)
        dbx.close()


class Similarity:
    def __init__(self, mode: int = 1, actors: list = None, udb_path: str = ""):
        """
        if mode == 1 => class base | if mode == 2 => method base
        7 metric for class base | two metric for methode base
        :param mode:
        :param metrics:
        """
        self.mode = mode
        self.actors = actors
        self.udb_path = udb_path

    def read_class_json(self):
        """
        read json files that save min and max of metric from refactoring class level model
        :return:
        """
        f = open("Resources/json_files/class_cluster.json").read()
        clusters = json.loads(f)
        return clusters

    def read_method_json(self):
        """
        read json files that save min and max of metric from refactoring method level model
        :return:
        """
        f = open("../gorgeous/Resources/json_files/method_cluster.json").read()
        clusters = json.loads(f)
        return clusters

    def rsim(self):
        """
        if elments in cluster exist
        :param elements:
        :return:
        """
        counter = 0
        cluster = self.read_class_json()
        length = len(cluster)
        for i in self.actors:
            for ac in i["obj"]:
                if ac.refactoring.find("ERROR") != -1:
                    for item in cluster:
                        for j in ac.source:
                            if int(dotenv_values().get("MODE_SIM")) == 1:
                                if j in item["Class"]:
                                    counter += 1
                            elif int(dotenv_values().get("MODE_SIM")) == 2:
                                if j in item["Method"]:
                                    counter += 1
        if length > 0:
            return counter / length
        else:
            return 0

    def tsim(self):
        """
        calculate number of similarity between model and metrics of element
        :param clusters:
        :param metrics:
        :return:
        """
        obj0 = ClsUDB_Metrics()
        counter = 0
        cluster = self.read_class_json()
        length = len(cluster)
        for i in self.actors:
            for ac in i["obj"]:
                if ac.refactoring.find("ERROR") != -1:
                    print("SOURCES : ", ac.source)
                    print("SOURCES : ", [ac.source[-1]])
                    print("SOURCES : ", type(ac.source))
                    m, flag = obj0.get_metrics_of_each_class(
                        my_path=self.udb_path, element=[ac.source[-1]]
                    )
                    if flag:
                        for k, v in m.items():
                            for item in cluster:
                                if v is not None:
                                    if item[k]["MAX"] >= float(v) and item[k][
                                        "MIN"
                                    ] <= float(v):
                                        counter += 1
        if length > 0:
            return counter / length
        else:
            return 0

    def sim(self):
        """
        method to calculate similarity between number of refactoring and similarity elements of it
        1/2 rsim + tsim
        :return:
        """
        if self.mode == 1:
            length = len(self.actors)
            if length > 0:
                return 0.5 * (self.tsim() + self.rsim()) / length
            else:
                return 0
        elif self.mode == 2:
            pass


class DesignQualityAttributes:
    """
    Class to compute six quality attribute proposed by J. J. Bansiya et G. Davis, 2002
    The QMOOD quality attribute are:
        1. Quality : coh / (coh + cop/2)
    """

    def __init__(self, udb_path):
        """
        Implements Project Objectives due to QMOOD design metrics
        :param udb_path: The understand database path
        """
        self.udb_path = udb_path
        self.__qmood = DesignMetrics(udb_path=udb_path)
        # Calculating once and using multiple times
        self.CAMC = self.__qmood.CAMC  # Cohesion, CAM
        self.DCC = self.__qmood.DCC  # Coupling
        # For caching results
        self._quality = None

    @property
    def quality(self):
        divider = self.CAMC + (self.DCC / 2)
        if divider == 0.0:
            divider = 0.01
        return self.CAMC / divider
