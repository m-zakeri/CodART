import abc
from typing import List

from cfg_generator.src.antlr.gen.JavaParser import RuleContext
from cfg_generator.src.data_structures.graph.builder_interface import IDiGraphBuilder


class ILanguagePattern(metaclass=abc.ABCMeta):

    @classmethod
    @abc.abstractmethod
    def concat(cls,
               left: IDiGraphBuilder,
               right: IDiGraphBuilder) -> IDiGraphBuilder:
        """concatenate two graphs sequentially"""

    @classmethod
    @abc.abstractmethod
    def merge(cls,
              left: IDiGraphBuilder,
              right: IDiGraphBuilder) -> IDiGraphBuilder:
        """merge two graphs affront nodes"""

    @classmethod
    @abc.abstractmethod
    def embed_in_if(cls,
                    condition: RuleContext,
                    then_part: IDiGraphBuilder) -> IDiGraphBuilder:
        """embed the then part graph into an if graph pattern"""

    @classmethod
    @abc.abstractmethod
    def embed_in_if_else(cls,
                         condition: RuleContext,
                         then_part: IDiGraphBuilder,
                         else_part: IDiGraphBuilder) -> IDiGraphBuilder:
        """embed the then part and else part graphs into an if-else graph pattern"""

    @classmethod
    @abc.abstractmethod
    def embed_in_switch_case(cls,
                             switcher: RuleContext,
                             labels: List[RuleContext],
                             bodies: List[IDiGraphBuilder]) -> IDiGraphBuilder:
        """embed the body graphs into a switch-case graph pattern"""

    @classmethod
    @abc.abstractmethod
    def embed_in_while(cls,
                       condition: RuleContext,
                       body: IDiGraphBuilder) -> IDiGraphBuilder:
        """embed the body graph into a while graph pattern"""

    @classmethod
    @abc.abstractmethod
    def embed_in_do_while(cls,
                          condition: RuleContext,
                          body: IDiGraphBuilder) -> IDiGraphBuilder:
        """embed the body graph into a do-while graph pattern"""

    @classmethod
    @abc.abstractmethod
    def embed_in_for(cls,
                     condition: RuleContext,
                     initializer: RuleContext,
                     successor: RuleContext,
                     body: IDiGraphBuilder) -> IDiGraphBuilder:
        """embed the body graph into a for graph pattern"""

    @classmethod
    @abc.abstractmethod
    def embed_in_try_catch(cls,
                           try_body: IDiGraphBuilder,
                           exceptions: List[RuleContext],
                           catch_bodies: List[IDiGraphBuilder]) -> IDiGraphBuilder:
        """embed the body and catch graphs into a try-catch graph pattern"""

    @classmethod
    @abc.abstractmethod
    def embed_in_function(cls,
                          body: IDiGraphBuilder,
                          catchLastNodes: List) -> IDiGraphBuilder:
        """embed the body graph into a function graph pattern"""
