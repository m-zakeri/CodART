"""

"""

from refactorings.utils.utils_listener_fast import Program


def get_removemethods(program: Program, packagename: str, superclassname: str, methodkey: str, classname: str):
    extendedclass = []
    removemethods = {}

    met = program.packages[packagename].classes[classname].methods[methodkey]
    body_text_method = met.body_text
    parammethod = met.parameters
    returntypeofmethod = met.returntype
    nameofmethod = met.name
    # print(program)
    for package_name in program.packages:
        package = program.packages[package_name]
        # print(package)
        for class_name in package.classes:
            _class = package.classes[class_name]

            if _class.superclass_name == superclassname:
                extendedclass.append(_class)

    i = 0
    for d in extendedclass:
        class_ = extendedclass[i]
        i = i + 1
        for mk in class_.methods:
            m_ = class_.methods[mk]
            m = mk[:mk.find('(')]
            if (
                    m_.body_text == body_text_method and m_.returntype == returntypeofmethod and m_.parameters == parammethod and m_.name == nameofmethod and m_.is_constructor == False):
                if class_.name not in removemethods:
                    removemethods[class_.name] = [methodkey]
                else:

                    removemethods[class_.name].append(methodkey)
    # removemethods[classname]=[nameofmethod]
    removemethods[classname] = [methodkey]
    return removemethods
