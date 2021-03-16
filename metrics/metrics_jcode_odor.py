"""

Implementation of JCodeOdor metrics.

"""




import sys


try:
    sys.path.insert(0, "D:/program files/scitools/bin/pc-win64/python")
    import understand as und
except ModuleNotFoundError:
    # Error handling
    pass

from naming import UnderstandUtility


class cls_main:
    def main(self):
        db = und.open('CodeSmell.udb')
        obj_get_metrics = JCodeOdorMetric()
        # print(obj_get_metrics.NOM())
        # for a in db.ents('Java Variable Local'):
        # print(a)
        # print(obj_get_metrics.NOPK(db))
        for classname in db.ents("class"):
            #  if(classname.name()=='Program.FANOUT'):
            print('classname = ' + classname.name())
            for a in classname.ents('Define', 'method'):
                print('method name =' + a.name())
                #  for b in a.refs('call'):
                #   print(b.ent().name())
                print(obj_get_metrics.NOAV(a))

    # list = [1, 2, 3, 1, 1, 2]
    # s = set(list)


# print(s)
# metrics = db.metric(db.metrics())
# for k, v in sorted(metrics.items()):
#    print(k, "=", v)


# print(obj_get_metrics.NOMNOPK(db))
# for cls in db.ents('Class'):
#    print('class name = ' + cls.name())
#    for mth in cls.ents('Defined','method'):
#     print(obj_get_metrics.NOAV(mth))


__version__ = '0.3.0'
__author__ = 'Morteza'



class JCodeOdorMetric:

    # ?
    def return_name(self, method_entity=None):
        try:
            # method_name = funcname.longname()
            method_simple_name = method_entity.simplename()
            # print(method_simple_name)
            # return method_name[len(funcname.parent().longname()) + 1: len(funcname.longname())]
            return method_simple_name
        except:
            raise ValueError('Method {0} dose not have parent'.format(method_entity))

    def is_accesor_or_mutator(self, method_entity=None):
        if str(self.return_name(method_entity)).startswith(("get", "set", "Get", "Set")):
            return True
        else:
            return False

    # Must be completed
    def is_abstract_annotation_interface(self, funcname):
        if (str(funcname).startswith(("get", "set", "Set", "Get"))):
            return True
        else:
            return False

    def MAXNESTING(self, funcname):
        if (self.is_abstract_annotation_interface(funcname)):
            return 0
        else:
            return funcname.metric(["MaxNesting"])["MaxNesting"]

    def CYCLO(self, funcname):
        if (self.is_abstract_annotation_interface(funcname)):
            return 0
        else:
            return funcname.metric(["Cyclomatic"])["Cyclomatic"]

    def NOPA(self, classname):
        return classname.metric(["CountDeclInstanceVariable"])["CountDeclInstanceVariable"]

    # Consider variables in for loop as seperate variable
    def NOLV(self, db, funcname):
        count = 0
        varlist = funcname.ents("funcname", "Variable , Parameter")
        for attr in varlist:
            if str(attr.parent().name()) == str(funcname.name()):
                count += 1
        return count

    # Exception: abstract methods and interface not considered
    def NOAM(self, class_name):
        """
        Only number of accessor (getter) method
        :param class_name:
        :return:
        """
        count = 0
        for mth in class_name.ents('Define', 'method'):
            if str(self.return_name(mth)).startswith(('get', 'Get')):
                count += 1
        return count

    # By: Morteza
    def NOMAMM(self, class_entity):
        """
        Number of accessor (getter) and mutator (setter) methods
        Weak implementation, need to rewrite
        :param class_entity:
        :return:
        """
        count = 0
        methods = class_entity.ents('Define', 'Java Method')
        if methods is not None:
            for method_entity in methods:
                # if str(self.return_name(method_entity)).startswith(('get', 'Get', 'GET', 'set', 'Set', 'SET')):
                #     count += 1
                if str(method_entity.simplename()).startswith(('get', 'Get', 'GET', 'set', 'Set', 'SET')):
                    count += 1  # i.e., the method is accessor or mutator
        return count

    # def NOMNAMM(self,class_name):
    #   mth_=class_name.metric(["CountDeclMethodPublic"])
    #   total=mth_["CountDeclMethodPublic"]
    #   return  (total - self.NOAM(class_name))

    def NOMNAMM(self, class_name):
        # mth_=class_name.metric(["CountDeclClassMethod"])["CountDeclClassMethod"]     0 midad
        count = 0
        mth_ = class_name.ents('Define', 'method')
        for m in mth_:
            # check constructor not in classname
            if str(m.kind()) == "Public Constructor" and str(m.name()) != str(class_name.name()):
                count += 1
        return (len(mth_) - count) - self.NOMAMM(class_entity=class_name)

    def LOCNAMM(self, class_name):
        print(class_name.longname())
        LOC = class_name.metric(["CountLine"])["CountLine"]
        LOCAMM = 0
        for mth in class_name.ents('class_name', 'method'):
            if (str(mth).startswith(("get", "set", "Set", "Get"))):
                LOCAMM += mth.metric(["CountLine"])["CountLine"]
        return LOC - LOCAMM

    def LOC(self, funcname):
        return funcname.metric(["CountLine"])["CountLine"]

    def WOC(self, class_name):
        count_functionl = 0
        metlist = class_name.ents("class_name", "Public Method")
        for m in metlist:
            if not (self.is_abstract_annotation_interface(m)):
                count_functionl += 1
        CountDeclInstanceVariable = int(
            0 if class_name.metric(["CountDeclInstanceVariable"])["CountDeclInstanceVariable"] is None else
            class_name.metric(["CountDeclInstanceVariable"])["CountDeclInstanceVariable"])
        CountDeclMethodPublic = int(
            0 if class_name.metric(["CountDeclMethodPublic"])["CountDeclMethodPublic"] is None else
            class_name.metric(["CountDeclMethodPublic"])["CountDeclMethodPublic"])
        total = CountDeclMethodPublic + CountDeclInstanceVariable

        if total == 0:
            return 0
        else:
            return (count_functionl / total)

    def WMCNAMM(self, class_name):
        sum = 0
        for mth in class_name.ents('class_name', 'method'):
            if not (self.is_accesor_or_mutator(mth)):
                sum += int(
                    0 if mth.metric(["Cyclomatic"])["Cyclomatic"] is None else mth.metric(["Cyclomatic"])["Cyclomatic"])
        return sum

    def TCC(self, class_name):
        NDC = 0
        methodlist = class_name.ents('class_name', 'Public Method')

        method_list_visible = list()
        for mvvisible in methodlist:
            if self.is_visible(mvvisible):
                method_list_visible.append(mvvisible)

        for row in range(0, len(method_list_visible)):
            for col in range(0, len(method_list_visible)):
                if (row > col):
                    if (self.connectivity(method_list_visible[row], method_list_visible[col])):
                        NDC += 1

        N = len(method_list_visible)
        NP = N * (N - 1) / 2

        if (NP != 0):
            return NDC / NP
        else:
            return 0

    def connectivity(self, row, col):
        if (self.connectivity_directly(row, col) or self.connectivity_indirectly(row, col)):
            return True
        else:
            return False

    def connectivity_indirectly(self, row, col):
        # print(" connectivity_indirectly :::::::::::::::::::::::::::::::::::::::::::::::::::::::::::: ")
        listrow = set()
        listcol = set()
        for callrow in row.refs("call"):
            if (str(callrow.ent().name()).startswith(("get", "Get"))):
                listrow.add(callrow.ent().longname())

        for callcol in col.refs("call"):
            if (str(callcol.ent().name()).startswith(("get", "Get"))):
                listcol.add(callcol.ent().longname())

        intersect = [value for value in listrow if value in listcol]
        if (len(intersect) > 0):
            return True
        else:
            return False

    def connectivity_directly(self, row, col):
        listrow = set()
        listcol = set()
        for callrow in row.refs("use"):
            listrow.add(callrow.ent().longname())

        for callcol in col.refs("use"):
            listcol.add(callcol.ent().longname())

        intersect = [value for value in listrow if value in listcol]
        if (len(intersect) > 0):
            return True
        else:
            return False

    def is_visible(self, funcname):
        flag = False
        par = funcname.ents("funcname", "Parameter")
        for p in par:
            if (str(p.type()) == "EventArgs"):
                flag = True
                break
        if not (str(funcname.kind()) == "Public Constructor") or not (flag) or not (
                str(funcname.kind()) == "Private Method"):
            return True
        else:
            return False

    def get_Namespace(self, entity):
        while (str(entity.parent().kind()) != "Unresolved Namespace" or str(entity.parent().kind()) != "Namespace"):
            entity = entity.parent()
            if (str(entity.parent().kind()) == "Unresolved Namespace" or str(entity.parent().kind()) == "Namespace"):
                break
        return entity.parent()

    def CINT(self, db, method_name):
        count = 0
        call_set = self.give_Methods_that_the_measured_method_calls(method_name)
        print("call_set :", call_set)
        for mth in call_set:
            if ((str(mth.parent().longname()) != str(method_name.parent().longname())) and (
                    str(self.get_Namespace(mth)) == str(self.get_Namespace(method_name)))):
                count += 1
        return count

    def give_Methods_that_the_measured_method_calls(self, funcname):
        call_methods_list = set()
        for fi in funcname.refs("call"):
            if (fi.ent().parent().parent() == funcname.parent().parent()):
                call_methods_list.add(fi.ent())
        return call_methods_list

    def CDISP(self, db, method_name):
        cint = self.CINT(db, method_name)
        if cint == 0:
            return 0
        else:
            return (method_name.metric(["CountOutPut"]) / cint)

    def NOPK(self, db):
        count = 0
        for package in db.ents("Package"):
            count += 1
        return count

    def NOCS(self, input):
        count = 0
        classes = input.ents('Define', 'class')
        if (len(classes) > 0):
            count += len(classes)
            for cls in classes:
                count += self.NOCS(cls)
        else:
            count += 0
        return count

    def NOCS_Package(self, input):
        return input.metric(["CountDeclClass"])["CountDeclClass"]

    def NOCS_Project(self, input):
        return input.metric(["CountDeclClass"])["CountDeclClass"]

    def NOM(self, class_name):
        um = 0
        for mth in class_name.ents('Define', 'method'):
            if (not mth.refs('Override')):
                um += 1
        return um

    def NOA(self, class_name):
        count = 0
        entities = class_name.ents('Define', 'Variable')
        return len(entities)

    # return class_name.metric(["CountDeclClassVariable"])["CountDeclClassVariable"] + class_name.metric(["CountDeclInstanceVariable"])["CountDeclInstanceVariable"]

    def WMC(self, class_name):
        return class_name.metric(["SumCyclomaticStrict"])["SumCyclomaticStrict"]

    def AMW(self, class_name):
        return class_name.metric(["AvgCyclomaticStrict"])["AvgCyclomaticStrict"]

    def AMWNAMM(self, class_name):
        cint = self.NOMNAMM(class_name)
        if cint == 0:
            return 0
        else:
            return (self.WMCNAMM(class_name) / cint)

    def NOP(self, method_name):
        count = 0
        for Parameter in method_name.ents('Parameters'):
            if str(Parameter.kindname()) == 'Parameter':
                count += 1
        # return len(method_name.ents('Parameters'))
        return count

    def DIT(self, class_name):
        return class_name.metric(['MaxInheritanceTree'])['MaxInheritanceTree']

    def NOC(self, class_name):
        return class_name.metric(['CountClassDerived'])['CountClassDerived']

    def NIM(self, class_name):
        CountDeclMethod = int(0 if class_name.metric(['CountDeclMethod'])['CountDeclMethod'] is None else
                              class_name.metric(['CountDeclMethod'])['CountDeclMethod'])
        CountDeclMethodAll = int(0 if class_name.metric(['CountDeclMethodAll'])['CountDeclMethodAll'] is None else
                                 class_name.metric(['CountDeclMethodAll'])['CountDeclMethodAll'])
        return CountDeclMethodAll - CountDeclMethod

    def LCOM5(self, class_name):
        result = 0
        NOACC = 0
        NOM = self.NOM(class_name)
        NOA = self.NOA(class_name)
        entities = class_name.ents('Define', 'Variable')
        for enty in entities:
            for ref in enty.refs('Useby'):
                if ((ref.ent().kind() != "Constructor")):
                    NOACC += 1

        if (NOM > 1 and NOA > 0):
            result = (NOM - (NOACC / NOA)) / (NOM - 1)
        else:
            result = 0
        return result

    def FANIN(self, db=None, class_entity=None) -> int:
        """
        Method for computing the fanin for a given class
        :param db: Understand database of target project
        :param class_entity: Target class entity for computing fanin
        :return: fain: The fanin of the class
        """
        method_list = UnderstandUtility.get_method_of_class_java(db=db, class_name=class_entity.longname())
        fanin = 0
        for method_entity in method_list:
            method_fanin = method_entity.metric(['CountInput'])['CountInput']
            if method_fanin is None:
                fanin += 0
            else:
                fanin += method_fanin
        return fanin

    def FANOUT(self, db, class_entity) -> int:
        method_list = UnderstandUtility.get_method_of_class_java(db=db, class_name=class_entity.longname())
        fanout = 0
        for method_entity in method_list:
            method_fanout = method_entity.metric(['CountOutput'])['CountOutput']
            if method_fanout is None:
                fanout += 0
            else:
                fanout += method_fanout
        return fanout

    def CBO(self, class_name):
        return class_name.metric(['CountClassCoupled'])['CountClassCoupled']

    def NOI(self, db):
        return len(db.ents('interface'))

    def NMO(self, class_name):
        um = 0
        for mth in class_name.ents('Define', 'method'):
            if mth.refs('Override'):
                um += 1
        return um

    def NOII(self, class_name):
        count = 0
        for b in class_name.ents('Implement'):
            if (b.kindname() == "Interface"):
                count += 1
        return count

    def CLNAMM(self, method_name):
        count = 0
        if not (self.is_abstract_annotation_interface(method_name)):
            for meth in method_name.refs('Call'):
                if (str(meth.ent().parent().longname()) == str(method_name.parent().longname()) and not (
                        self.is_accesor_or_mutator(meth.ent()))):
                    count += 1
        return count

    def FDP(self, method_name):
        list1 = list()
        if not (self.is_abstract_annotation_interface(method_name)):
            for meth in method_name.refs('Use', 'Variable'):
                if (meth.ent().parent().longname() != method_name.parent().longname()):
                    list1.append(meth.ent().parent().parent())
        return len(set(list1))

    def RFC(self, class_name):
        count = 0
        list1 = list()
        for meth in class_name.refs('Call', 'Java Method'):
            if meth.ent().parent() is None:
                continue
            if meth.ent().parent().longname() != class_name.longname() and \
                    meth.ent().kindname() != 'Public Constructor':
                list1.append(meth)

        return len(set(list1))

    def LAA(self, method_name):
        result = 0
        listtotal = list()
        listsameclass = list()
        if not (self.is_abstract_annotation_interface(method_name)):
            for meth in method_name.refs('Use', 'Variable'):
                listtotal.append(meth)
                if (meth.ent().parent().longname() == method_name.parent().longname()):
                    listsameclass.append(meth)
            for meth in method_name.refs('call', 'method'):
                if meth.ent().kindname() != "Public Constructor":
                    if (self.is_accesor_or_mutator(meth.ent())):
                        listtotal.append(meth)
                    if (self.is_accesor_or_mutator(
                            meth.ent()) and meth.ent().parent().longname() == method_name.parent().longname()):
                        listsameclass.append(meth)
        if (len(set(listtotal)) != 0):
            result = len(set(listsameclass)) / len(set(listtotal))
        return result

    def CFNAMM_method(self, method_name):
        count = 0
        list1 = list()
        for meth in method_name.refs('call', 'method'):
            if (
                    meth.ent().parent().longname() != class_name.parent().longname() and meth.ent().kindname() != "Public Constructor" and not (
                    self.is_accesor_or_mutator(meth.ent()))):
                list1.append(meth)
        return len(set(list1))

    def CFNAMM_Class(self, class_name):
        list1 = list()
        for meth in class_name.refs('Call', 'Java Method'):
            if meth.ent().parent() is None:
                continue
            if meth.ent().parent().longname() != class_name.longname() \
                    and meth.ent().kindname() != "Public Constructor" \
                    and not (self.is_accesor_or_mutator(meth.ent())):
                list1.append(meth)
        return len(set(list1))

    def NOAV(self, method_name):
        count = 0
        if not (self.is_abstract_annotation_interface(method_name)):
            for mth in method_name.refs('Use', 'Variable'):
                count += 1
            for meth in method_name.refs('call', 'method'):
                if meth.ent().kindname() != "Public Constructor":
                    if (self.is_accesor_or_mutator(meth.ent())):
                        for mth in meth.ent().refs('Use', 'Variable'):
                            count += 1
        return count

    def give_Access_Field(self, funcname):
        # create a list and return it:Includes all the variables(fields) that a method uses
        access_field_list = set()
        for fi in funcname.refs("use"):
            access_field_list.add(fi.ent())
        return access_field_list

    def give_Methods_that_the_measured_method_calls(self, funcname):
        # create a list and return it:Includes all Methods entity(also cunstructor method ) that the measured method calls
        call_methods_list = set()
        for fi in funcname.refs("call"):
            # if namespace == method namespace
            if (fi.ent().parent().parent() == funcname.parent().parent()):
                # print(fi,"->",fi.ent().parent().parent())
                # print("_")
                call_methods_list.add(fi.ent())
        return call_methods_list

    def result(self, db):
        self.get_metrics(db)
        return [self.class_metrics, self.method_metrics]
        # return a list consist of classes and methods and thier metrics value



    def ATFD(self, class_entity):
        foreign_data = class_entity.ents('Useby', 'Java Variable')
        for fd in foreign_data:
            print(fd.longname(), '| ', fd.parent(), '| ', fd.kind())

# obj = cls_main()
# obj.main()
