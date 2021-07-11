"""
Project's objectives

## Reference
[1] J. Bansiya and C. G. Davis, “A hierarchical model for object-oriented design quality assessment,” IEEE Trans. Softw. Eng., vol. 28, no. 1, pp. 4–17, 2002.
"""

__version__ = '0.1.0'
__author__ = 'Mina Tahaei'

import os

from metrics.qmood import QMOOD


class Objectives:
    def __init__(self, udb_path):
        """
        Implements Project Objectives due to QMOOD design metrics
        :param udb_path: The understand database path
        """
        assert os.path.isfile(udb_path)
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
        score = 0.33 * self.qmood.ANA + 0.33 * self.qmood.DAM - 0.33 * self.qmood.DCC + \
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
