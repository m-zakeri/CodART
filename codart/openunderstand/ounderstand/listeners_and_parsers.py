from openunderstand.analysis_passes.Throws_ThrowsBy import Throws_TrowsBy
from openunderstand.analysis_passes.DotRef_DorRefBy import DotRef_DotRefBy
from openunderstand.analysis_passes.callNonDynamic_callNonDynamicby import (
    CallNonDynamicAndCallNonDynamicBy,
)

from openunderstand.analysis_passes.call_callby import CallAndCallBy
from openunderstand.analysis_passes.cast_cast_by import CastAndCastBy, implementListener
from openunderstand.analysis_passes.contain_contain_by import ContainAndContainBy
from openunderstand.analysis_passes.extends_implicit_couple_coupleby import (
    PackageImportListener,
    DSCmetric,
)
from openunderstand.analysis_passes.import_importby_g10_2 import ImportListener, ImportedEntityListener
from openunderstand.analysis_passes.import_demand_g9 import ImportListenerDemand

from openunderstand.analysis_passes.define_definein import DefineListener

# from analysis_passes.define_and_definin_g6 import DefineListener
from openunderstand.analysis_passes.modify_modifyby import ModifyListener
from openunderstand.analysis_passes.entity_manager_g11 import (
    EntityGenerator,
    FileEntityManager,
    get_created_entity,
)

from openunderstand.analysis_passes.use_useby import UseAndUseByListener
from openunderstand.analysis_passes.type_typedby import TypedAndTypedByListener
from openunderstand.analysis_passes.set_setby import SetAndSetByListener
from openunderstand.analysis_passes.setinit_setinitby import SetInitAndSetByInitListener
from openunderstand.analysis_passes.setpartial_setpartialby import SetPartialAndSetByPartialListener
from openunderstand.ounderstand.override_overrideby__G12 import overridelistener
from openunderstand.analysis_passes.couple_coupleby__G12 import CoupleAndCoupleBy
from openunderstand.analysis_passes.create_createby_g9 import CreateAndCreateBy
from openunderstand.analysis_passes.declare_declarein import DeclareAndDeclareinListener
from openunderstand.analysis_passes.extend_listener_g6 import ExtendListener
from openunderstand.analysis_passes.extendcouple_extendcoupleby import ExtendCoupleAndExtendCoupleBy
from openunderstand.analysis_passes.variable_listener_g11 import VariableListener
from openunderstand.analysis_passes.open_openby import OpenListener
from openunderstand.analysis_passes.usemodule_usemoduleby_g11 import UseModuleUseModuleByListener
from openunderstand.utils.utilities import setup_logger, timer_decorator
import os
from pathlib import Path
import traceback


class ListenersAndParsers:
    def __init__(self):
        self.logger = setup_logger()

    @timer_decorator()
    def parser(self, file_address, p):
        try:
            parse_tree = p.Parse(file_address)
            file_ent = p.getFileEntity(
                path=file_address, name=os.path.basename(file_address)
            )
            tree = parse_tree
            self.logger.info("file parse success")
            return tree, parse_tree, file_ent
        except Exception as e:
            self.logger.error(
                "An Error occurred in file file parse:" + file_address + "\n" + str(e)
            )
            return None, None, None

    @timer_decorator()
    def entity_gen(self, file_address, parse_tree):
        return EntityGenerator(file_address, parse_tree)

    @timer_decorator()
    def variable_listener(self, tree, file_ent, file_address, p):
        try:
            listener = VariableListener()
            p.Walk(listener, tree)
            for item in listener.var:
                self.entity_gen(
                    file_address=file_address, parse_tree=tree
                ).get_or_create_variable_entity(res_dict=item)
            for item in listener.var_const:
                self.entity_gen(
                    file_address=file_address, parse_tree=tree
                ).get_or_create_variable_entity(res_dict=item)
            self.logger.info("variable refs success ")
        except Exception as e:
            self.logger.error(
                "An Error occurred in file variable refs :"
                + file_address
                + "\n"
                + str(e)
                + "\n"
                + traceback.format_exc()
            )

    @timer_decorator()
    def extend_coupled_listener(self, tree, file_ent, file_address, p):
        try:
            listener = ExtendCoupleAndExtendCoupleBy()
            p.Walk(listener, tree)
            p.addExtendCoupleOrExtendCoupleByRefs(
                listener.implement, file_ent, file_address
            )
            self.logger.info("extends coupled refs success ")
        except Exception as e:
            self.logger.error(
                "An Error occurred in file extends coupled refs :"
                + file_address
                + "\n"
                + str(e)
            )

    @timer_decorator()
    def extend_listener(self, tree, file_ent, file_address, p):
        try:
            listener = ExtendListener()
            p.Walk(listener, tree)
            p.addTypeRefs(listener.get_refers, file_ent)
            self.logger.info("extends refs success ")
        except Exception as e:
            self.logger.error(
                "An Error occurred in file extends refs :"
                + file_address
                + "\n"
                + str(e)
            )

    @timer_decorator()
    def type_listener(self, tree, file_ent, file_address, p):
        try:
            listener = TypedAndTypedByListener()
            p.Walk(listener, tree)
            p.addTypeRefs(listener.get_type, file_ent)
            self.logger.info("type refs success ")
        except Exception as e:
            self.logger.error(
                "An Error occurred in file type refs :" + file_address + "\n" + str(e)
            )

    @timer_decorator()
    def create_listener(self, tree, file_ent, file_address, p):
        try:
            listener = CreateAndCreateBy()
            p.Walk(listener, tree)
            p.addCreateRefs(listener.create, file_ent, file_address)
            self.logger.info("create refs success ")
        except Exception as e:
            self.logger.error(
                "An Error occurred in file create refs :" + file_address + "\n" + str(e)
            )

    @timer_decorator()
    def define_listener(self, tree, file_ent, file_address, p):
        try:
            listener = DefineListener(file_address)
            p.Walk(listener, tree)
            p.addDefineRefs(listener.defines, file_ent)
            self.logger.info("define success ")
        except Exception as e:
            self.logger.error(
                "An Error occurred for reference implement in file define:"
                + file_address
                + "\n"
                + str(e)
                + "\n"
                + traceback.format_exc()
            )

    # @timer_decorator()
    # def define_listener(self, tree, file_ent, file_address, p):
    #     try:
    #         listener = DefineListener()
    #         p.Walk(listener, tree)
    #         package_name = listener.package["package_name"]
    #         p.add_entity_package(listener.package, file_address)
    #         p.add_defined_entities(
    #             listener.classes, "class", package_name, file_address
    #         )
    #         p.add_defined_entities(
    #             listener.interfaces, "interface", package_name, file_address
    #         )
    #         p.add_defined_entities(
    #             listener.fields, "variable", package_name, file_address
    #         )
    #         p.add_defined_entities(
    #             listener.methods, "method", package_name, file_address
    #         )
    #         p.add_defined_entities(
    #             listener.local_variables,
    #             "local variable",
    #             package_name,
    #             file_address,
    #         )
    #         p.add_defined_entities(
    #             listener.formal_parameters, "parameter", package_name, file_address
    #         )
    #         self.logger.info("define success ")
    #     except Exception as e:
    #         self.logger.error(
    #             "An Error occurred for reference implement in file define:"
    #             + file_address
    #             + "\n"
    #             + str(e)
    #         )

    @timer_decorator()
    def declare_listener(self, tree, file_ent, file_address, p):
        try:
            # declare
            listener = DeclareAndDeclareinListener()
            p.Walk(listener, tree)
            p.addDeclareRefs(listener.declare, file_ent)
            self.logger.info("declare success ")
        except Exception as e:
            self.logger.error(
                "An Error occurred for reference declare in file:"
                + file_address
                + "\n"
                + str(e)
            )

    @timer_decorator()
    def modify_listener(self, parse_tree, entity_generator, file_address, p):
        try:
            listener = ModifyListener(entity_generator)
            p.Walk(listener, parse_tree)
            p.add_modify_and_modifyby_reference(listener.modify)
            self.logger.info("modify success ")
        except Exception as e:
            self.logger.error(
                "An Error occurred for reference modify in file:"
                + file_address
                + "\n"
                + str(e)
                + "\n"
                + traceback.format_exc()
            )

    @timer_decorator()
    def override_listener(self, tree, file_ent, file_address, p):
        try:
            listener = overridelistener()
            p.Walk(listener, tree)
            classesx = listener.get_classes
            extendedlist = listener.get_extendeds
            p.addoverridereference(classesx, extendedlist, file_ent)
            self.logger.info("overrides success ")
        except Exception as e:
            self.logger.error(
                "An Error occurred in override reference in file :"
                + file_address
                + "\n"
                + str(e)
            )

    @timer_decorator()
    def couple_listener(self, tree, file_ent, file_address, p):
        try:
            couple = []
            classescoupleby = {}
            listener = CoupleAndCoupleBy()
            listener.set_file(filex=file_address)
            listener.set_classesx(classesx=classescoupleby)
            listener.set_couples(couples=couple)
            p.Walk(listener, tree)
            classescoupleby = listener.get_classes
            couple = listener.get_couples
            p.addcouplereference(
                classescoupleby , couple, file_ent
            )
            self.logger.info("couple success ")
        except Exception as e:
            self.logger.error(
                "An Error occurred in couple reference in file :"
                + file_address
                + "\n"
                + str(e)
                + "\n"
                + traceback.format_exc()
            )

    @timer_decorator()
    def throws_listener(self, tree, file_ent, file_address, p):
        try:
            # Throws
            listener = Throws_TrowsBy()
            p.Walk(listener, tree)
            p.addThrows_TrowsByRefs(
                listener.implement, file_ent, file_address, 236, 237, True
            )
            self.logger.info("Throws success ")
        except Exception as e:
            self.logger.error(
                "An Error occurred in throws in file :"
                + file_address
                + "\n"
                + str(e)
                + "\n"
                + traceback.format_exc()
            )

    @timer_decorator()
    def dotref_listener(self, tree, file_ent, file_address, p):
        try:
            listener = DotRef_DotRefBy()
            p.Walk(listener, tree)
            p.addThrows_TrowsByRefs(
                listener.implement, file_ent, file_address, 198, 199, False
            )
            self.logger.info("DotRef success ")
        except Exception as e:
            self.logger.error(
                "An Error occurred in dotref in file :" + file_address + "\n" + str(e)
            )

    @timer_decorator()
    def setby_listener(self, tree, file_ent, file_address, p, stream: str = ""):
        try:
            # set ref
            listener = SetAndSetByListener(file_address)
            p.Walk(listener, tree)
            p.addSetRefs(listener.setBy, file_ent, stream)
            self.logger.info("set Ref success")
        except Exception as e:
            self.logger.error(
                "An Error occurred in set ref in file :" + file_address + "\n" + str(e)
            )

    def setinitby_listener(self, tree, file_ent, file_address, p, stream: str = ""):
        try:
            # setinit ref
            listener = SetInitAndSetByInitListener(file_address)
            p.Walk(listener, tree)
            p.addSetInitRefs(listener.set_init_by, file_ent, stream)
            self.logger.info("setInit Ref success ")
        except Exception as e:
            self.logger.error(
                "An Error occurred in setInit ref in file :"
                + file_address
                + "\n"
                + str(e)
            )

    def setbypartialby_listener(
        self, tree, file_ent, file_address, p, stream: str = ""
    ):
        try:
            # setinit ref
            listener = SetPartialAndSetByPartialListener(file_address)
            p.Walk(listener, tree)
            p.addSetPartialRefs(listener.set_by_partial, file_ent, stream)
            self.logger.info("set Partial Ref success ")
        except Exception as e:
            self.logger.error(
                "An Error occurred in setInit ref in file :"
                + file_address
                + "\n"
                + str(e)
            )

    @timer_decorator()
    def useby_listener(self, tree, file_ent, file_address, p, stream: str = ""):
        try:
            # use ref
            listener = UseAndUseByListener()
            p.Walk(listener, tree)
            p.addUseRefs(listener.useBy, file_ent, stream)
            self.logger.info("use ref success ")
        except Exception as e:
            self.logger.error(
                "An Error occurred in use ref in file :" + file_address + "\n" + str(e)
            )

    @timer_decorator()
    def callby_listener(self, tree, file_ent, file_address, p):
        try:
            listener = CallAndCallBy(
                file_full_path=file_address,
                class_parents={},
                available_class_fields=None,
                available_class_methods=None,
                available_package_classes=None,
            )
            p.Walk(listener, tree)
            p.addCallOrCallByRefs(listener.implement, file_ent, file_address)
            self.logger.info("call ref success ")
        except Exception as e:
            self.logger.error(
                "An Error occurred in call ref in file :" + file_address + "\n" + str(e)
            )

    @timer_decorator()
    def callbyNonDynamic_listener(self, tree, file_ent, file_address, p):
        try:
            listener = CallNonDynamicAndCallNonDynamicBy()
            p.Walk(listener, tree)
            p.addCallNonDynamicOrCallNonDynamicByRefs(
                listener.implement, file_ent, file_address
            )
            self.logger.info("call non dynamic ref success ")
        except Exception as e:
            self.logger.error(
                "An Error occurred in call non dynamic ref in file :"
                + file_address
                + "\n"
                + str(e)
                + "\n"
                + traceback.format_exc()
            )

    @timer_decorator()
    def cast_by_listener(self, tree, file_ent, file_address, p):
        try:
            imp = implementListener()
            p.Walk(imp, tree)
            listener = CastAndCastBy(imp.classes)
            p.Walk(listener, tree)
            p.add_cast_by(listener.cast, file_ent, file_address)
            self.logger.info("cast success ")
        except Exception as e:
            self.logger.error(
                "An Error occurred in cast in file :"
                + file_address
                + "\n"
                + str(e)
                + traceback.format_exc()
            )

    @timer_decorator()
    def contain_in_listener(self, tree, file_ent, file_address, p):
        try:
            listener = ContainAndContainBy()
            p.Walk(listener, tree)
            p.add_contain_in(listener.contain, file_ent, file_address)
            self.logger.info("contain success ")
        except Exception as e:
            self.logger.error(
                "An Error occurred in contain in file :"
                + file_address
                + "\n"
                + str(e)
                + "\n"
                + traceback.format_exc()
            )

    @timer_decorator()
    def extend_implict_listener(self, tree, file_ent, file_address, p):
        try:
            package_import_listener = PackageImportListener()
            p.Walk(package_import_listener, tree)
            my_listener = DSCmetric(package_import_listener.package_name)
            p.Walk(my_listener, tree)
            # c = ClassTypeData()
            # c.set_file_path(file_address)
            for item in my_listener.dbHandler.classTypes:
                imported_entity, importing_entity = p.add_imported_entity_factory(item)
                p.add_references(imported_entity, importing_entity, item)
            self.logger.info("extend implict success ")
        except Exception as e:
            self.logger.error(
                "An Error occurred in extend implict in file :"
                + file_address
                + "\n"
                + str(e)
            )

    @timer_decorator()
    def import_demand_listener(self, tree, file_ent, file_address, p):
        try:
            listener = ImportListenerDemand(file_address)
            p.Walk(listener, tree)
            p.add_import_demand(listener.repository, file_address)
            self.logger.info("import demand success ")
        except Exception as e:
            self.logger.error(
                "An Error occurred in import demand in file :"
                + file_address
                + "\n"
                + str(e)
            )

    @timer_decorator()
    def import_listener(self, tree, file_ent, file_address, p):
        try:
            listener = ImportListener(file_address)
            p.Walk(listener, tree)
            listener_import = ImportedEntityListener(name=Path(file_address).stem)
            for i in listener.repository:
                imported_entity = p.add_imported_entity(
                    i, file_address, listener_import
                )
                p.add_references_import(file_ent, imported_entity, i)
            self.logger.info("import success ")
        except Exception as e:
            self.logger.error(
                "An Error occurred in import in file :" + file_address + "\n" + str(e)
            )

    @timer_decorator()
    def use_module_listener(self, tree, file_ent, file_address, p):
        try:
            listener = UseModuleUseModuleByListener()
            p.Walk(listener, tree)
            p.add_use_module_reference(
                use_module=listener.useModules,
                unknown_module=listener.useUnknownModules,
                unresolved_module=listener.useUnresolvedModules,
                file_address=file_address,
            )
            self.logger.info("use module by success ")
        except Exception as e:
            self.logger.error(
                "An Error occurred in use module by in file :"
                + file_address
                + "\n"
                + str(e)
                + "\n"
                + traceback.format_exc()
            )

    @timer_decorator()
    def open_by_listener(self, tree, file_ent, file_address, p):
        try:
            listener = OpenListener(file_address)
            p.Walk(listener, tree)
            for i in listener.repository:
                imported_entity = p.add_opened_entity(i)
                p.add_references_opend(file_ent, imported_entity, i)
            self.logger.info("open by success ")
        except Exception as e:
            self.logger.error(
                "An Error occurred in open by in file :" + file_address + "\n" + str(e)
            )
