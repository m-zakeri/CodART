# expression -> NEW creator


"""
## Description
This module find all OpenUnderstand create and createby references in a Java project


## References


"""

__author__ = (
    "Parmida Majmasanaye , Zahra Momeninezhad , Bayan Divaani-Azar , Bavan Divaani-Azar"
)
__version__ = "0.1.0"

from gen.javaLabeled.JavaParserLabeledListener import JavaParserLabeledListener
from gen.javaLabeled.JavaParserLabeled import JavaParserLabeled
import openunderstand.analysis_passes.g6_class_properties as class_properties


class ExtendListener(JavaParserLabeledListener):
    def __init__(self):
        self.class_name = None
        self.refers = {}

    def get_refers(self):
        return self.refers

    def get_class_name(self):
        return self.class_name

    def enterClassDeclaration(self, ctx: JavaParserLabeled.ClassDeclarationContext):
        self.class_name = ctx.IDENTIFIER().getText()
        if ctx.getChild(2).getText() == "extends":
            childs = ctx.getChild(3).getChildren()
            for c in childs:
                if not self.refers.__contains__(self.class_name):
                    self.refers[self.class_name] = []
                self.refers[self.class_name].append(c.getText())
