# expression -> NEW creator


"""
## Description
This module find all OpenUnderstand call and callby references in a Java project


## References


"""

__author__ = "zahra habibolah, G4"
# __version__ = "0.1.0"

# Omitted imports and other code for brevity
from gen.javaLabeled.JavaParserLabeledListener import JavaParserLabeledListener
from gen.javaLabeled.JavaParserLabeled import JavaParserLabeled
import openunderstand.analysis_passes.class_properties as class_properties


class CreateAndCreateBy(JavaParserLabeledListener):
    def __init__(self):
        self.package_long_name = ""
        self.create = []
        # Initialize new flags for blockStatement and variableInitializer
        self.isBlockStatement1 = False
        self.isVariableInitializer1 = False
        self.isStatement15 = False  # New flag

    def findmethodreturntype(self, c):
        parents = ""
        context = ""
        current = c
        while current is not None:
            if type(current.parentCtx).__name__ == "MethodDeclarationContext":
                parents = current.parentCtx.typeTypeOrVoid().getText()
                context = current.parentCtx.getText()
                break
            current = current.parentCtx

        return parents, context

    # def findmethodaccess(self, c):
    #     parents = ""
    #     modifiers=[]
    #     current = c
    #     while current is not None:
    #         if "ClassBodyDeclaration" in type(current.parentCtx).__name__:
    #             parents=(current.parentCtx.modifier())
    #             break
    #         current = current.parentCtx
    #     for x in parents:
    #         if x.classOrInterfaceModifier():
    #             modifiers.append(x.classOrInterfaceModifier().getText())
    #     return modifiers

    def findmethodaccess(self, ctx):
        modifiers_list = [
            "Default",
            "Private",
            "Public",
            "Protected",
            "Static",
            "Generic",
            "Abstract",
            "Final",
        ]
        parent_modifiers = ""
        modifiers = []
        parent_type = ""
        current = ctx
        while current is not None:
            if "ClassBodyDeclaration2" in type(current.parentCtx).__name__:
                parent_modifiers = current.parentCtx.modifier()
                if "MethodDeclaration" in type(current.children[0]).__name__:
                    parent_type = "Method"
                elif "ConstructorDeclaration" in type(current.children[0]).__name__:
                    parent_type = "Constructor"
                # elif "FieldDeclaration" in type(current.children[0]).__name__:
                #     parent_type = "Method"
                elif "ClassDeclaration" in type(current.children[0]).__name__:
                    parent_type = "Class"
                elif "EnumDeclaration" in type(current.children[0]).__name__:
                    parent_type = "Enum"
                else:
                    parent_type = "Unresolved"
                break
            current = current.parentCtx

        for modifier in parent_modifiers:
            if modifier.classOrInterfaceModifier():
                if (
                    modifier.classOrInterfaceModifier().getText().title()
                    in modifiers_list
                ):
                    modifiers.append(modifier.classOrInterfaceModifier().getText())

        return modifiers, parent_type

    create = []

    # Add new method for statement15
    def enterStatement15(self, ctx):
        if self.isBlockStatement1:
            # Set flag if we are within blockStatement1
            self.isStatement15 = True

    # Override for blockStatement1
    def enterBlockStatement1(self, ctx):
        # Set context to blockStatement1
        self.isBlockStatement1 = True
        # Reset other flags
        self.isVariableInitializer1 = False
        self.isStatement15 = False

    # Override for variableInitializer1
    def enterVariableInitializer1(self, ctx):
        # Set context to variableInitializer1
        self.isVariableInitializer1 = True
        # Reset blockStatement1 context
        self.isBlockStatement1 = False
        # We do not reset isStatement15 because it's not related to variable initialization

    # Override exit methods to reset the flags when the context ends
    def exitBlockStatement1(self, ctx):
        self.isBlockStatement1 = False

    def exitVariableInitializer1(self, ctx):
        self.isVariableInitializer1 = False

    def exitStatement15(self, ctx):
        self.isStatement15 = False

    def enterExpression4(self, ctx: JavaParserLabeled.Expression4Context):
        # Check for specific sequences
        if self.isBlockStatement1 and self.isStatement15:
            # Process Expression4 only if followed by statement15 in a blockStatement1
            self.processExpression4(ctx)
        elif self.isVariableInitializer1:
            # Process Expression4 only if it follows a variableInitializer1
            # Assuming you are 'throwing away' variable declarators before this
            self.processExpression4(ctx)
        # Reset flags after checking for the specific sequence
        self.isBlockStatement1 = False
        self.isVariableInitializer1 = False
        self.isStatement15 = False

    def enterExpression4(self, ctx: JavaParserLabeled.Expression4Context):
        # Perform the context check before processing the expression4
        if self.isBlockStatement1 or self.isVariableInitializer1:
            modifiers, parent_type = self.findmethodaccess(ctx)
            methodreturn, methodcontext = self.findmethodreturntype(ctx)

            # First check to ensure we're working with creator1
            creator = ctx.creator()
            if creator.arrayCreatorRest() or creator.classCreatorRest():
                createdName = creator.createdName()
                all_parents = class_properties.ClassPropertiesListener.findParents(ctx)
                scope_name = all_parents[-1]
                scope_longname = self.package_long_name + "." + ".".join(all_parents)
                [line, col] = str(ctx.start).split(",")[3].split(":")

                # if creator.arrayCreatorRest() or creator.classCreatorRest():
                # If we're in the correct context for creator1, then check for createdName0
                # createdName = creator.createdName()
                # if isinstance(createdName, JavaParserLabeled.CreatedName0Context):
                # all_parents = class_properties.ClassPropertiesListener.findParents(ctx)
                # scope_name = all_parents[-1]
                # scope_longname = self.package_long_name + "." + ".".join(all_parents)
                # [line, col] = str(ctx.start).split(",")[3].split(":")

                self.create.append(
                    {
                        "scopename": scope_name,
                        "scopelongname": scope_longname,
                        "scopemodifiers": modifiers,
                        "parent_type": parent_type,
                        "scopereturntype": methodreturn,
                        "scopecontent": methodcontext,
                        "line": line.strip(),
                        "col": col.strip(),
                        "refent": createdName.getText(),
                        "scope_parent": (
                            all_parents[-2] if len(all_parents) > 1 else None
                        ),
                        "potential_refent": ".".join(all_parents[:-1])
                        + "."
                        + createdName.getText(),
                    }
                )

        # Reset the flags whether context condition was met or not
        self.isBlockStatement1 = False
        self.isVariableInitializer1 = False

    def enterPackageDeclaration(self, ctx: JavaParserLabeled.PackageDeclarationContext):
        self.package_long_name = ctx.qualifiedName().getText()


# This code does not show the parts related to THROW, i.e. statement11
# the code below is the version that shows it, but the outputs are more in Linux.

# Omitted imports and other code for brevity
# from gen.javaLabeled.JavaParserLabeledListener import JavaParserLabeledListener
# from gen.javaLabeled.JavaParserLabeled import JavaParserLabeled
# import analysis_passes.class_properties as class_properties
#
# class CreateAndCreateBy(JavaParserLabeledListener):
#     def __init__(self):
#         self.package_long_name = ""
#         self.create = []
#         # Initialize new flags for blockStatement and variableInitializer
#         self.isBlockStatement1 = False
#         self.isVariableInitializer1 = False
#         self.isStatement15 = False
#         self.isStatement11 = False
#
#     def findmethodreturntype(self, c):
#         parents = ""
#         context = ""
#         current = c
#         while current is not None:
#             if type(current.parentCtx).__name__ == "MethodDeclarationContext":
#                 parents = current.parentCtx.typeTypeOrVoid().getText()
#                 context = current.parentCtx.getText()
#                 break
#             current = current.parentCtx
#
#         return parents, context
#
#     # def findmethodaccess(self, c):
#     #     parents = ""
#     #     modifiers=[]
#     #     current = c
#     #     while current is not None:
#     #         if "ClassBodyDeclaration" in type(current.parentCtx).__name__:
#     #             parents=(current.parentCtx.modifier())
#     #             break
#     #         current = current.parentCtx
#     #     for x in parents:
#     #         if x.classOrInterfaceModifier():
#     #             modifiers.append(x.classOrInterfaceModifier().getText())
#     #     return modifiers
#
#     def findmethodaccess(self, ctx):
#         modifiers_list = [
#             "Default",
#             "Private",
#             "Public",
#             "Protected",
#             "Static",
#             "Generic",
#             "Abstract",
#             "Final",
#         ]
#         parent_modifiers = ""
#         modifiers = []
#         parent_type = ""
#         current = ctx
#         while current is not None:
#             if "ClassBodyDeclaration2" in type(current.parentCtx).__name__:
#                 parent_modifiers = current.parentCtx.modifier()
#                 if "MethodDeclaration" in type(current.children[0]).__name__:
#                     parent_type = "Method"
#                 elif "ConstructorDeclaration" in type(current.children[0]).__name__:
#                     parent_type = "Constructor"
#                 # elif "FieldDeclaration" in type(current.children[0]).__name__:
#                 #     parent_type = "Method"
#                 elif "ClassDeclaration" in type(current.children[0]).__name__:
#                     parent_type = "Class"
#                 elif "EnumDeclaration" in type(current.children[0]).__name__:
#                     parent_type = "Enum"
#                 else:
#                     parent_type = "Unresolved"
#                 break
#             current = current.parentCtx
#
#         for modifier in parent_modifiers:
#             if modifier.classOrInterfaceModifier():
#                 if (
#                     modifier.classOrInterfaceModifier().getText().title()
#                     in modifiers_list
#                 ):
#                     modifiers.append(modifier.classOrInterfaceModifier().getText())
#
#         return modifiers, parent_type
#
#     create = []
#
#     # Add new method for statement15
#     def enterStatement15(self, ctx):
#         if self.isBlockStatement1:
#             # Set flag if we are within blockStatement1
#             self.isStatement15 = True
#
#     # Override for blockStatement1
#     def enterBlockStatement1(self, ctx):
#         # Set context to blockStatement1
#         self.isBlockStatement1 = True
#         # Reset other flags
#         self.isVariableInitializer1 = False
#         self.isStatement15 = False
#
#     # Override for variableInitializer1
#     def enterVariableInitializer1(self, ctx):
#         # Set context to variableInitializer1
#         self.isVariableInitializer1 = True
#         # Reset blockStatement1 context
#         self.isBlockStatement1 = False
#         # We do not reset isStatement15 because it's not related to variable initialization
#
#     # Override exit methods to reset the flags when the context ends
#     def exitBlockStatement1(self, ctx):
#         self.isBlockStatement1 = False
#
#     def exitVariableInitializer1(self, ctx):
#         self.isVariableInitializer1 = False
#
#     def exitStatement15(self, ctx):
#         self.isStatement15 = False
#
#     def enterStatement11(self, ctx):
#         self.isStatement11 = True
#
#     def exitStatement11(self, ctx):
#         self.isStatement11 = False
#
#     def enterExpression4(self, ctx: JavaParserLabeled.Expression4Context):
#         # Check for specific sequences
#         if self.isBlockStatement1 or self.isVariableInitializer1:
#             if self.isBlockStatement1 and self.isStatement15 or self.isStatement11:
#                 # Process Expression4 only if followed by statement15 in a blockStatement1
#                 self.processExpression4(ctx)
#             elif self.isVariableInitializer1:
#                 # Process Expression4 only if it follows a variableInitializer1
#                 # Assuming you are 'throwing away' variable declarators before this
#                 self.processExpression4(ctx)
#             # Reset flags after checking for the specific sequence
#         self.isBlockStatement1 = False
#         self.isVariableInitializer1 = False
#         self.isStatement15 = False
#
#     def processExpression4(self, ctx):
#         # Perform the context check before processing the expression4
#         #if self.isBlockStatement1 or self.isVariableInitializer1:
#             modifiers, parent_type = self.findmethodaccess(ctx)
#             methodreturn, methodcontext = self.findmethodreturntype(ctx)
#
#             # First check to ensure we're working with creator1
#             creator = ctx.creator()
#             if creator.arrayCreatorRest() or creator.classCreatorRest():
#                 createdName = creator.createdName()
#                 all_parents = class_properties.ClassPropertiesListener.findParents(ctx)
#                 scope_name = all_parents[-1]
#                 scope_longname = self.package_long_name + "." + ".".join(all_parents)
#                 [line, col] = str(ctx.start).split(",")[3].split(":")
#
#             #if creator.arrayCreatorRest() or creator.classCreatorRest():
#                 # If we're in the correct context for creator1, then check for createdName0
#                 #createdName = creator.createdName()
#                 #if isinstance(createdName, JavaParserLabeled.CreatedName0Context):
#                     #all_parents = class_properties.ClassPropertiesListener.findParents(ctx)
#                     #scope_name = all_parents[-1]
#                     #scope_longname = self.package_long_name + "." + ".".join(all_parents)
#                     #[line, col] = str(ctx.start).split(",")[3].split(":")
#
#
#                 self.create.append(
#                     {
#                         "scopename": scope_name,
#                         "scopelongname": scope_longname,
#                         "scopemodifiers": modifiers,
#                         "parent_type": parent_type,
#                         "scopereturntype": methodreturn,
#                         "scopecontent": methodcontext,
#                         "line": line.strip(),
#                         "col": col.strip(),
#                         "refent": createdName.getText(),
#                         "scope_parent": all_parents[-2] if len(all_parents) > 1 else None,
#                         "potential_refent": ".".join(all_parents[:-1]) + "." + createdName.getText(),
#                     }
#                 )
#
#         # Reset the flags whether context condition was met or not
#             self.isBlockStatement1 = False
#             self.isVariableInitializer1 = False
#
#     def enterPackageDeclaration(self, ctx: JavaParserLabeled.PackageDeclarationContext):
#         self.package_long_name = ctx.qualifiedName().getText()
