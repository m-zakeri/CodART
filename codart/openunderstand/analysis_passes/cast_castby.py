from gen.javaLabeled.JavaParserLabeled import JavaParserLabeled
from general_scope_listener import GeneralScopeListener


class CastAndCastBy(GeneralScopeListener):
    def __init__(
        self,
        file_full_path,
        available_package_classes,
        available_class_methods,
        available_class_fields,
        class_parents,
    ):
        super(CastAndCastBy, self).__init__(
            file_full_path,
            available_package_classes,
            available_class_methods,
            available_class_fields,
            class_parents,
        )
        # The dict has a key corresponding to the
        # entity_id of the reference owner entity
        # each key maps to an array of referenced entities
        # according to their entity id
        self.cast_dict = {}
        self.cast_reached = False

    def enterMethodCall0(self, ctx: JavaParserLabeled.MethodCall0Context):
        # check if in cast state (child/grandchild of expression5)
        # if yes the result of the method is being casted
        pass

    # we have reached a cast state
    def enterExpression5(self, ctx: JavaParserLabeled.Expression5Context):
        self.cast_reached = True

    # we have exited a cast state
    def exitExpression5(self, ctx: JavaParserLabeled.Expression5Context):
        self.cast_reached = False

    # casted variable is equivalent to Primary4 in the grammar
    def enterPrimary4(self, ctx: JavaParserLabeled.Primary4Context):
        pass

    # casted literal is equivalent to Primary3 in the grammar
    def enterPrimary3(self, ctx: JavaParserLabeled.Primary3Context):
        pass

    # check if in cast state (child/grandchild of expression5)
    # if yes we are seeing the type that is the target of the cast
    def enterTypeType(self, ctx: JavaParserLabeled.TypeTypeContext):
        pass
