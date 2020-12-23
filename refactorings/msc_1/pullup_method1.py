from utils_listener import TokensInfo

from utils import get_program


def pullup_method(mylist : list,packagename :str,superclassname : str,methodname:str,classname : str):
    program = get_program(mylist)
    extendedclass=[]
    methodsofclass=[]
    pullupmethods={}
    removemethods={}

    met = program.packages[packagename].classes[classname].methods[methodname]
    body_text_method =met.body_text
    parammethod = met.parameters
    returntypeofmethod = met.returntype
    nameofmethod = met.name
     #print(program)
    for package_name in program.packages:
        package = program.packages[package_name]
        #print(package)
        for class_name in package.classes:
            _class = package.classes[class_name]

            if _class.superclass_name == superclassname:
             extendedclass.append(_class)
             removemethods[class_name]=[]

    i=0
    for d in extendedclass:
      class_=  extendedclass[i]
      i+1
      for m in class_.methods:
         m_=class_.methods[m]
         if(m_.body_text == body_text_method and m_.returntype == returntypeofmethod and m_.parameters == parammethod and m_.name == nameofmethod):
          removemethods[class_.name].append(m)
      removemethods[classname].append(nameofmethod)
      return removemethods


