"""

The module provide high-level API for computing object-oriented source code metrics.
To be used in CodART project

@ ToDo complete

"""

__version__ = '0.1.0'
__author__ = 'Morteza'

from abc import ABC, abstractmethod


class Metric(ABC):
    def __init__(self, db=None,
                 project_name: str = None, ):
        self.db = db
        self.project_name = project_name

    @abstractmethod
    def compute_metric(self, metric_name: str = None):
        pass


class PackageMetric(Metric):
    def __init__(self, db=None,
                 project_name: str = None,
                 package_name: str = None, ):
        super(PackageMetric, self).__init__(db=db, project_name=project_name)
        self.package_name = package_name

    def compute_metric(self, metric_name: str = None):
        pass


class ClassMetric(PackageMetric):
    def __init__(self, db=None,
                 project_name: str = None,
                 package_name: str = None,
                 class_name: str = None,
                 method_name: str = None):
        super(ClassMetric, self).__init__(db=db, project_name=project_name, package_name=package_name)
        self.class_name = class_name



    def compute_metric(self, metric_name: str = None):
        if metric_name == 'MinCyclomatic':
            pass



class MethodMetric(ClassMetric):
    def __init__(self, db=None,
                 project_name: str = None,
                 package_name: str = None,
                 class_name: str = None,
                 method_name: str = None):
        super(MethodMetric, self).__init__(db=db,
                                           project_name=project_name,
                                           package_name=package_name,
                                           class_name=class_name)
        self.method_name = method_name

    def compute_metric(self, metric_name: str = None):
        pass
