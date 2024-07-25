from typing import Any


class SimilarityClassLevelModel:
    def __init__(
        self,
        refactoring_type: list = None,
        source: list = None,
        target: list = None,
    ):

        self._refactoring = refactoring_type
        self._source = source
        self._target = target
        self._EC = 0
        self._MM = 0
        self._PU = 0
        self._PD = 0

    @property
    def ec(self):
        return self._EC

    @property
    def mm(self):
        return self._MM

    @property
    def pu(self):
        return self._PU

    @property
    def pd(self):
        return self._PD

    @property
    def source(self):
        return self._source

    @property
    def target(self):
        return self._target

    @property
    def refactoring(self):
        return self._refactoring

    @mm.setter
    def mm(self, a):
        self._MM = a

    @ec.setter
    def ec(self, a):
        self._EC = a

    @pu.setter
    def pu(self, a):
        self._PU = a

    @pd.setter
    def pd(self, a):
        self._PD = a

    @source.setter
    def source(self, a):
        self._source = a

    @target.setter
    def target(self, a):
        self._target = a

    @refactoring.setter
    def refactoring(self, a):
        self._refactoring = a


class SimilarityMethodLevelModel:
    def __init__(
        self,
        refactoring_type: list = None,
        source: list = None,
        target: list = None,
    ):

        self._refactoring = refactoring_type
        self._source = source
        self._target = target
        self._EM = 0
        self._MM = 0
        self._PU = 0
        self._PD = 0
        self._IM = 0

    @property
    def em(self):
        return self._EM

    @property
    def im(self):
        return self._IM

    @property
    def mm(self):
        return self._MM

    @property
    def pu(self):
        return self._PU

    @property
    def pd(self):
        return self._PD

    @property
    def source(self):
        return self._source

    @property
    def target(self):
        return self._target

    @property
    def refactoring(self):
        return self._refactoring

    @mm.setter
    def mm(self, a):
        self._MM = a

    @em.setter
    def em(self, a):
        self._EM = a

    @im.setter
    def im(self, a):
        self._IM = a

    @pu.setter
    def pu(self, a):
        self._PU = a

    @pd.setter
    def pd(self, a):
        self._PD = a

    @source.setter
    def source(self, a):
        self._source = a

    @target.setter
    def target(self, a):
        self._target = a

    @refactoring.setter
    def refactoring(self, a):
        self._refactoring = a
