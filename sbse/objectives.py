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
        # Calculating once and using multiple times
        self.DSC = self.qmood.DSC
        self.NOH = self.qmood.NOH
        self.ANA = self.qmood.ANA
        self.MOA = self.qmood.MOA
        self.DAM = self.qmood.DAM
        self.CAMC = self.qmood.CAMC
        self.CIS = self.qmood.CIS
        self.NOM = self.qmood.NOM
        self.DCC = self.qmood.DCC
        self.MFA = self.qmood.MFA
        self.NOP = self.qmood.NOP
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
        self._functionality = 0.12 * self.CAMC + 0.22 * self.NOP + 0.22 * self.CIS + \
                              0.22 * self.DSC + 0.22 * self.NOH
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
        self._effectiveness = 0.2 * self.ANA + 0.2 * self.DAM + 0.2 * self.MOA + 0.2 * \
                              self.MFA + 0.2 * self.NOP
        return self._effectiveness

    @property
    def average(self):
        metrics = [
            'reusability', 'flexibility', 'understandability',
            'functionality', 'extendability', 'effectiveness',

        ]
        all_metrics = []
        for metric in metrics:
            cache = getattr(self, f'_{metric}')
            if cache is None:
                all_metrics.append(getattr(self, metric))
            else:
                all_metrics.append(cache)
        return sum(all_metrics) / len(all_metrics)


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
