"""
Project's objectives

## Reference
[1] J. Bansiya and C. G. Davis, “A hierarchical model for object-oriented design quality assessment,” IEEE Trans. Softw. Eng., vol. 28, no. 1, pp. 4–17, 2002.
"""

__version__ = '0.1.0'
__author__ = 'Seyyed Ali Ayati, Mina Tahaei'

import os

from metrics.qmood import QMOOD


class Objectives:
    def __init__(self, udb_path):
        """
        Implements Project Objectives due to QMOOD design metrics
        :param udb_path: The understand database path
        """
        self.udb_path = udb_path
        self.qmood = QMOOD(udb_path=udb_path)

    @property
    def reusability(self):
        """
        A design with low coupling and high cohesion is easily reused by other designs.
        :return: reusability score
        """
        score = -0.25 * self.qmood.DCC + 0.25 * self.qmood.CAMC + 0.5 * self.qmood.CIS + 0.5 * self.qmood.DSC
        return score

    @property
    def flexibility(self):
        """
        The degree of allowance of changes in the design.
        :return: flexibility score
        """
        score = 0.25 * self.qmood.DAM - 0.25 * self.qmood.DCC + 0.5 * self.qmood.MOA + 0.5 * self.qmood.NOP
        return score

    @property
    def understandability(self):
        """
        The degree of understanding and the easiness of learning the design implementation details.
        :return: understandability score
        """
        score = -0.33 * self.qmood.ANA + 0.33 * self.qmood.DAM - 0.33 * self.qmood.DCC + \
                0.33 * self.qmood.CAMC - 0.33 * self.qmood.NOP - 0.33 * self.qmood.NOM - \
                0.33 * self.qmood.DSC
        return score

    @property
    def functionality(self):
        """
        Classes with given functions that are publicly stated in interfaces to be used by others.
        :return: functionality score
        """
        score = 0.12 * self.qmood.CAMC + 0.22 * self.qmood.NOP + 0.22 * self.qmood.CIS + \
                0.22 * self.qmood.DSC + 0.22 * self.qmood.NOH
        return score

    @property
    def extendability(self):
        """
        Measurement of design's allowance to incorporate new functional requirements.
        :return: extendability
        """
        score = 0.5 * self.qmood.ANA - 0.5 * self.qmood.DCC + 0.5 * self.qmood.MFA + 0.5 * self.qmood.NOP
        return score

    @property
    def effectiveness(self):
        """
        Design efficiency in fulfilling the required functionality.
        :return: effectiveness score
        """
        score = 0.2 * self.qmood.ANA + 0.2 * self.qmood.DAM + 0.2 * self.qmood.MOA + 0.2 * \
                self.qmood.MFA + 0.2 * self.qmood.NOP
        return score

    @property
    def average(self):
        objs = [
            self.reusability, self.flexibility, self.understandability,
            self.functionality, self.extendability, self.effectiveness
        ]
        return sum(objs) / len(objs)


if __name__ == '__main__':
    understand_paths = [
        "D:\\Final Project\\IdeaProjects\\JSON20201115\\JSON20201115.und",
        "D:\\Final Project\\IdeaProjects\\104_vuze\\104_vuze.und",
        "D:\\Final Project\\IdeaProjects\\105_freemind\\105_freemind.und",
        "D:\\Final Project\\IdeaProjects\\107_weka\\107_weka.und",
        "D:\\Final Project\\IdeaProjects\\ganttproject_1_11_1_original\\ganttproject_1_11_1_original.und",
        "D:\\Final Project\\IdeaProjects\\jfreechart-master\\jfreechart-master.und",
        "D:\\Final Project\\IdeaProjects\\jvlt-1.3.2\\jvlt-1.3.2.und",

    ]
    for udb_path in understand_paths:
        obj = Objectives(udb_path)
        print(udb_path)
        print(f"reusability: {obj.reusability}")
        print(f"flexibility: {obj.flexibility}")
        print(f"understandability: {obj.understandability}")
        print(f"functionality: {obj.functionality}")
        print(f"extendability: {obj.extendability}")
        print(f"effectiveness: {obj.effectiveness}")
        print(f"average: {obj.average}")
