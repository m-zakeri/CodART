"""

"""

from refactorings.utils.utils_listener_fast import Program

def Diff(li1, li2):
    return list(set(li1) - set(li2)) + list(set(li2) - set(li1))

def get_cons(program: Program, packagename: str, superclassname: str, methodkey: str, classname: str):
    extendedclass = []
    removemethods = {}
    removemethods1 = []

    met = program.packages[packagename].classes[classname].methods[methodkey]
    body_text_method = met.body_text
    parammethod = met.parameters

    for package_name in program.packages:
        package = program.packages[package_name]
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
            if m_.body_text == body_text_method and m_.parameters == parammethod and m_.is_constructor == True :
                if class_.name not in removemethods:
                    removemethods[class_.name] = [methodkey]
                else:
                    removemethods[class_.name].append(methodkey)
            elif m_.is_constructor == True:
                listBody_text = body_text_method.replace("{", "").replace("}", "").split(";")
                listm_body = m_.body_text.replace("{", "").replace("}", "").split(";")
                s1 = set(listBody_text)
                s2 = set(listm_body)
                if s2.issubset(s1):
                    removemethods1.append(Diff(listBody_text, listm_body))
                    if class_.name not in removemethods:
                        removemethods[class_.name] = [mk]
                    else:
                        removemethods[class_.name].append(mk)

    removemethods[classname] = [methodkey]
    return removemethods, removemethods1
