from utils_listener_fast import TokensInfo, Program



def get_removemethods(program: Program,packagename :str,superclassname : str,methodname:str,classname : str):
    extendedclass=[]
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

    i=0
    for d in extendedclass:
      class_=  extendedclass[i]
      i+1
      for m in class_.methods:
         m_=class_.methods[m]
         if(m_.body_text == body_text_method and m_.returntype == returntypeofmethod and m_.parameters == parammethod and m_.name == nameofmethod):
             if class_.name not in  removemethods:
                 removemethods[class_.name] = [m]
             else:

              removemethods[class_.name].append(m)
      removemethods[classname]=[nameofmethod]
      return removemethods


