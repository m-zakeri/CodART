from typing import Any


class ProcedureModel:
    def __init__(
        self,
        refactoring_type: str = "",
        source: list = None,
        target: str = "",
        name: str = "",
        type: str = "",
    ):
        self._name = name
        self._refactoring = refactoring_type
        self._source = source
        self._target = target
        self._type = type

    @property
    def source(self):
        return self._source

    @property
    def target(self):
        return self._target

    @property
    def type(self):
        return self._type

    @property
    def refactoring(self):
        return self._refactoring

    @property
    def name(self):
        return self._name

    @source.setter
    def source(self, a):
        self._source = a

    @target.setter
    def target(self, a):
        self._target = a

    @type.setter
    def type(self, a):
        self._type = a

    @refactoring.setter
    def refactoring(self, a):
        self._refactoring = a

    @refactoring.setter
    def refactoring(self, a):
        self._refactoring = a
