import re
from peewee import fn
from openunderstand.oudb.models import *
from dataclasses import dataclass
from functools import reduce
from openunderstand.ounderstand.parsing_process import process_file
from openunderstand.metrics.count_decl_method_all import count_decl_method_all
from openunderstand.metrics.count_decl_class_variable import declare_class_variables
from openunderstand.metrics.AvgCyclomatic import avg_cyclomatic
from openunderstand.metrics.AvgCyclomaticModified import avg_cyclomatic_modified
from openunderstand.metrics.AvgCyclomaticStrict import avg_cyclomatic_strict
from openunderstand.metrics.AvgEssential import avg_essential
from openunderstand.metrics.count_decl_class_method import declare_method_count
from openunderstand.metrics.RatioCommentToCode import get_ratio_comment_to_code
from openunderstand.metrics.PercentLackOfCohesionModified import (
    get_percent_lack_of_cohesion_modified,
)
from openunderstand.metrics.count_stmt import statement_counter
from openunderstand.metrics.count_stmt_decl import statement_counter_delc
from openunderstand.metrics.PercentLackOfCohesion import get_percent_lack_of_cohesion
from openunderstand.metrics.sum_cyclomatic_modified import get_sum_cyclomatic_modified
from openunderstand.metrics.sum_cyclomatic_strict import get_sum_cyclomatic_strict
from openunderstand.metrics.sumOfCyclomatics import get_sum_of_cyclomatics
from openunderstand.metrics.count_decl_method_private import count_decl_method_private
from openunderstand.metrics.count_decl_method_protected import (
    count_decl_method_protected,
)
from openunderstand.metrics.count_decl_method_default import count_decl_method_default
from openunderstand.metrics.count_decl_file import declare_file
from openunderstand.metrics.sum_essentials import get_sum_essentials
from openunderstand.metrics.count_decl_executable_unit import declare_executable_unit
from openunderstand.metrics.min_max_essential_knots import min_max_essential_knots
from openunderstand.metrics.namm import get_namm
from openunderstand.metrics.MaxCalculator_G12 import max_cyclomatic
from openunderstand.metrics.MaxCalculator_G12 import max_essential
from openunderstand.metrics.MaxCalculator_G12 import max_cyclomatic_modified
from openunderstand.metrics.MaxCalculator_G12 import max_cyclomatic_stricts
from openunderstand.metrics.max_nesting import MaxNesting
from openunderstand.metrics.max_inheritance import FindAllInheritances
from openunderstand.metrics.knots_inheritance_nesting import get_knot_inheritance_nested
from openunderstand.metrics.knots_inheritance_nesting import get_max_inheritance
from openunderstand.metrics.Lineofcode import get_line_of_codes
from openunderstand.metrics.count_stmt_exe import statement_counter_exe
from openunderstand.metrics.cyclomatic import cyclomatic
from openunderstand.metrics.CyclomaticStrict_G12 import cyclomatic_strict
from openunderstand.metrics.Essential_G12 import essential
from openunderstand.metrics.CyclomaticModified_G12 import cyclomatic_modified
from openunderstand.metrics.G11_knots import knot

"""
This is the python interface to Understand databases.

It provides class-orientated access to Understand databases. Most
of the class objects are only valid when returned from a function.

The following classes and methods are in this module:
Classes:
  ounderstand.Arch
  ounderstand.Db
  ounderstand.Ent
  ounderstand.Kind
  ounderstand.Lexeme
  ounderstand.Lexer
  ounderstand.LexerIter
  ounderstand.Metric
  ounderstand.Ref
  ounderstand.UnderstandError
  ounderstand.Visio
Methods:
  ounderstand.checksum(text [,len])
  ounderstand.license(path)
  ounderstand.open(dbname)
  ounderstand.version()

Examples

The following examples are meant to be complete, yet simplistic
scripts that demonstrate one or more features each. For the sake of
brevity, most try, except statements statements are ommitted.

Sorted List of All Entities
---------------------------

import ounderstand

# Open Database
oudb = ounderstand.open("test.udb")

for ent in sorted(oudb.ents(),key= lambda ent: ent.name()):
  print (ent.name(),"  [",ent.kindname(),"]",sep="",end="\n")


List of Files
-------------

import ounderstand

oudb = ounderstand.open("test.udb")

for file in oudb.ents("File"):
  # print directory name
  print (file.longname())


Lookup an Entity (Case Insensitive)
-----------------------------------

import ounderstand
import re

oudb = ounderstand.open("test.udb")

# Create a regular expression that is case insensitive
searchstr = re.compile("test*.cpp",re.I)
for file in oudb.lookup(searchstr,"File"):
  print (file)


Global Variable Usage
---------------------

import ounderstand

oudb = ounderstand.open("test.udb")

for ent in oudb.ents("Global Object ~Static"):
  print (ent,":",sep="")
  for ref in ent.refs():
    print (ref.kindname(),ref.ent(),ref.file(),"(",ref.line(),",",ref.column(),")")
  print ("\n",end="")


List of Functions with Parameters
---------------------------------

import ounderstand

def sortKeyFunc(ent):
  return str.lower(ent.longname())

oudb = ounderstand.open("test.udb")

ents = oudb.ents("function,method,procedure")
for func in sorted(ents,key = sortKeyFunc):
  print (func.longname()," (",sep="",end="")
  first = True
  for param in func.ents("Define","Parameter"):
    if not first:
      print (", ",end="")
    print (param.type(),param,end="")
    first = False
  print (")")


List of Functions with Associated Comments
------------------------------------------

import ounderstand

oudb = ounderstand.open("test.udb")

for func in oudb.ents("function ~unresolved ~unknown"):
  comments = func.comments("after")
  if comments:
    print (func.longname(),":\n  ",comments,"\n",sep="")


List of Ada Packages
--------------------

import ounderstand

oudb = ounderstand.open("test.udb")

print ("Standard Packages:")
for package in oudb.ents("Package"):
  if package.library() == "Standard":
    print ("  ",package.longname())

print ("\nUser Packages:")
for package in oudb.ents("Package"):
  if package.library() != "Standard":
    print("  ",package.longname())


All Project Metrics
-------------------

import ounderstand

oudb = ounderstand.open("test.udb")

metrics = oudb.metric(oudb.metrics())
for k,v in sorted(metrics.items()):
  print (k,"=",v)


Cyclomatic Complexity of Functions
----------------------------------

import ounderstand

oudb = ounderstand.open("test.udb")

for func in oudb.ents("function,method,procedure"):
  metric = func.metric(("Cyclomatic",))
  if metric["Cyclomatic"] is not None:
    print (func," = ",metric["Cyclomatic"],sep="")


"Called By" Graphs of Functions
-------------------------------

import ounderstand

oudb = ounderstand.open("test.udb")

for func in oudb.ents("function,method,procedure"):
  file = "callby_" + func.name() + ".png"
  print (func.longname(),"->",file)
  func.draw("Called By",file)


Info Browser View of Functions
------------------------------

import ounderstand

oudb = ounderstand.open("test.udb")

for func in oudb.ents("function,method,procedure"):
  for line in func.ib():
    print(line,end="")


Lexical Stream
--------------

import ounderstand

oudb = ounderstand.open("test.udb")

file = oudb.lookup("test.cpp")[0]
for lexeme in file.lexer():
  print (lexeme.text(),end="")
  if lexeme.ent():
    print ("@",end="")
"""

# Variables with simple values

COMMENT = "Comment"
CONTINUATION = "Continuation"
DEDENT = "Dedent"
ENDOFSTATEMENT = "EndOfStatement"
EOF = "EOF"
IDENTIFIER = "Identifier"
IDSEQ = "IdSeq"
INDENT = "Indent"
KEYWORD = "Keyword"
LABEL = "Label"
LITERAL = "Literal"
NEWLINE = "Newline"
OPERATOR = "Operator"
PREPROCESSOR = "Preprocessor"
PUNCTUATION = "Punctuation"
STRING = "String"
WHITESPACE = "Whitespace"

import os
import git
from openunderstand.oudb.models import EntityModel, ReferenceModel


def update_db(repo_path: str = "", branch: str = "origin/master"):
    for file in [
        file
        for file in git.Repo(repo_path).git.diff(branch, name_only=True).split("\n")
        if file.endswith(".java")
    ]:
        process_file(file_address=file)


def create_db(
    dbname: str = "", project_dir: str = "", project_name: str = None, db_path: str = ""
):
    path_of_db_file = os.path.join(db_path, dbname)
    db = SqliteDatabase(
        path_of_db_file,
        pragmas={
            "journal_mode": "wal",
            "cache_size": -1 * 64000,  # 64MB
            "ignore_check_constraints": 0,
            "synchronous": 0,
        },
    )
    db.bind([KindModel, EntityModel, ReferenceModel, ProjectModel])
    db.create_tables([KindModel, EntityModel, ReferenceModel, ProjectModel])

    ProjectModel.get_or_create(
        name=project_name or os.path.basename(project_dir),
        root=project_dir,
        db_path=path_of_db_file,
    )
    return open(path_of_db_file)


def open(dbname):  # real signature unknown; restored from __doc__
    """
    ounderstand.open(dbname) -> ounderstand.Db

    Open a database from the passed in filename.

    This returns a new ounderstand.Db given the dbname (string). It
    will throw an ounderstand.UnderstandError if unsuccessful. Possible causes
    for error are:
      DBAlreadyOpen        - only one database may be open at once
      DBCorrupt            - bad database file
      DBOldVersion         - database needs to be rebuilt
      DBUnknownVersion     - database needs to be rebuilt
      DBUnableOpen         - database is unreadable or does not exist
      NoApiLicense         - Understand license required
    """
    if not os.path.isfile(dbname):
        raise UnderstandError()

    db = SqliteDatabase(
        dbname,
        pragmas={
            "journal_mode": "wal",
            "cache_size": -1 * 64000,  # 64MB
            "ignore_check_constraints": 0,
            "synchronous": 0,
        },
    )

    db.bind([KindModel, EntityModel, ReferenceModel, ProjectModel])

    obj = ProjectModel.get_or_none(db_path=dbname)
    return Db(db_obj=obj)


def version():  # real signature unknown; restored from __doc__
    """
    ounderstand.version() -> int

    Return the current build number for this module
    """
    return "0.1.0"


# classes


class Db:
    """
    This class represents an ounderstand database. With the exception of
    Db.close(), all methods require an open database. A database is
    opened through the module function ounderstand.open(dbname). Available
    methods are:

      ounderstand.Db.add_annotation_file(path)
      ounderstand.Db.annotations()
      ounderstand.Db.archs(ent)
      ounderstand.Db.close()
      ounderstand.Db.comparison_db()
      ounderstand.Db.ent_from_id(id)
      ounderstand.Db.ents([kindstring])
      ounderstand.Db.language()
      ounderstand.Db.lookup(name [,kindstring])
      ounderstand.Db.lookup_arch(longname)
      ounderstand.Db.lookup_uniquename(uniquename)
      ounderstand.Db.metric(metriclist)
      ounderstand.Db.metrics()
      ounderstand.Db.metrics_treemap(file, sizemetric, colormetric [enttype [,arch]])
      ounderstand.Db.name()
      ounderstand.Db.relative_file_name()
      ounderstand.Db.root_archs()  ounderstand.Db.__str__() --name
    """

    def __init__(self, db_obj):
        self._name = db_obj.name
        self._root = db_obj.root
        self._language = db_obj.language

    def close(self):  # real signature unknown; restored from __doc__
        """
        oudb.close() -> None

        Close the database.

        This allows a new database to be opened. It will never throw an
        error and is safe to call even if the database is already closed.
        After the database is closed, accessing objects associated with
        the database (ents, refs, ...) can cause Python to crash.
        """
        return None

    def ents(self, kindstring=None):  # real signature unknown; restored from __doc__
        """
        oudb.ents([kindstring]) -> list of Ent

        Return a list entities in the database.

        If the optional parameter kindstring(string) is not passed, then all
        the entities in the database are returned. Otherwise, kindstring
        should be a language-specific entity filter string. The database
        must be open or a UnderstandError will be thrown.
        """

        all_ents = set()

        if kindstring is None:
            query = EntityModel.select()
        else:
            # TODO: Complete this later
            kindstrings = kindstring.split(" ")
            query = EntityModel.select()
            conditions = []
            for item in kindstrings:
                kinds = KindModel.select().where(KindModel._name.contains(item))
                conditions.append(EntityModel._kind.in_(kinds))
            if conditions:
                query = query.where(reduce(lambda a, b: a | b, conditions)).where(
                    reduce(lambda a, b: a & b, conditions)
                )
        for ent in query:
            my_ent = Ent(**ent.__dict__.get("__data__"))
            all_ents.add(my_ent)
        return all_ents

    def ent_from_id(self, id: int):  # real signature unknown; restored from __doc__
        """
        oudb.ent_from_id(id) -> ounderstand.Ent

        Return the ent associated with the id.

        The id is obtained using ent.id. This should only be called for
        identifiers that have been obtained while the database has remained
        open. When a database is reopened, the identifier is not guaranteed
        to remain consistent and refer to the same entity.
        """
        try:
            ent = EntityModel.get_by_id(pk=id)
            return Ent(**ent.__dict__.get("__data__"))
        except EntityModel.DoesNotExist:
            return None

    def language(self):  # real signature unknown; restored from __doc__
        """
        oudb.language() -> tuple of strings

        Return a tuple with project languages

        This method returns a tuple containing all the language names
        enabled in the project. Possible language names are: "Ada", "C++",
        "C#", "Fortran", "Java", "Jovial", "Pascal", "Plm",
        "Python", "VHDL", or "Web". C is included with "C++"
        This will throw a UnderstandError if the database has been closed.
        """
        return str(self._language)

    def lookup(
        self, name, kindstring=None
    ):  # real signature unknown; restored from __doc__
        """
        oudb.lookup(name [,kindstring]) -> list of ounderstand.Ent

        Return a list of entities that match the specified name.

        The parameter name should be a regular expression, either compiled or
        as a string. By default, regular expressions are case sensitive. For
        case insensitive search, compile the regular expression like this:
          import re
          oudb.lookup(re.compile("searchstring",re.I))
        The re.I flag is for case insensitivity. Otherwise, the lookup command
        can be run simply
          oudb.lookup("searchstring")
        The optional paramter kindstring is a language-specific entity filter
        string. So, for example,
          oudb.lookup(".Test.","File")
        would return a list of file entities containing "Test" (case sensitive)
        in their names.
        """
        ents = []
        query = EntityModel.select()
        if kindstring:
            kinds = KindModel.select().where(
                fn.Lower(KindModel._name).contains(kindstring.lower())
            )
            query = query.where(EntityModel._kind.in_(kinds))

        query = query.where(
            (EntityModel._name.contains(name)) | (EntityModel._longname.contains(name))
        )

        for ent in query:
            if re.search(f'Java\\s+{kindstring}'.lower(), str(ent._kind._name).lower()):
                ents.append(Ent(**ent.__dict__.get("__data__")))
        return ents

    def lookup_uniquename(
        self, uniquename
    ):  # real signature unknown; restored from __doc__
        """
        oudb.lookup_uniquename(uniquename) -> ent

        Return the entity identified by uniquename.

        Uniquename is the name returned by ent.uniquename and repr(ent). This
        will return None if no entity is found.
        """
        pass

    def name(self):  # real signature unknown; restored from __doc__
        """
        oudb.name() -> string

        Return the filename of the database.

        This will throw a UnderstandError if the database has been closed.
        """
        return str(self._name)

    def relative_file_name(
        self, absolute_path
    ):  # real signature unknown; restored from __doc__
        """
        oudb.relative_file_name(absolute_path) -> string

        Return the relative file name like ent.relname() but for an arbitrary path.
        """
        list_of_paths = [self._root, absolute_path]
        common_prefix = os.path.commonprefix(list_of_paths)
        return os.path.relpath(absolute_path, common_prefix)

    def __str__(self, *args, **kwargs):  # real signature unknown
        """Return str(self)."""
        return self.name()


@dataclass
class Ent:
    """
    This class represents an ounderstand entity(files, functions,
    variables, etc). Available methods are:

      ounderstand.Ent.contents()
      ounderstand.Ent.depends()
      ounderstand.Ent.dependsby()
      ounderstand.Ent.ents(refkindstring [,entkindstring])
      ounderstand.Ent.__eq__() --by id
      ounderstand.Ent.filerefs([refkindstring [,entkindstring [,unique]]])
      ounderstand.Ent.__ge__() --by id
      ounderstand.Ent.__gt__() --by id
      ounderstand.Ent.__hash__() --id
      ounderstand.Ent.ib([options])
      ounderstand.Ent.id()
      ounderstand.Ent.kind()
      ounderstand.Ent.kindname()
      ounderstand.Ent.language()
      ounderstand.Ent.__le__() --by id
      ounderstand.Ent.lexer([lookup_ents [,tabstop [,show_inactive [,expand_macros]]]])
      ounderstand.Ent.library()
      ounderstand.Ent.longname()
      ounderstand.Ent.__lt__() --by id
      ounderstand.Ent.metric(metriclist)
      ounderstand.Ent.metrics()
      ounderstand.Ent.name()
      ounderstand.Ent.__ne__() --by id
      ounderstand.Ent.parameters(shownames = True)
      ounderstand.Ent.parent()
      ounderstand.Ent.parsetime()
      ounderstand.Ent.ref([refkindstring [,entkindstring]])
      ounderstand.Ent.refs([refkindstring [,entkindstring [,unique]]])
      ounderstand.Ent.relname()
      ounderstand.Ent.__repr__() --uniquename
      ounderstand.Ent.simplename()
      ounderstand.Ent.__str__() --name
      ounderstand.Ent.type()
      ounderstand.Ent.uniquename()
      ounderstand.Ent.value()
    """

    _id: int
    _kind: int
    _parent: int
    _name: str
    _longname: str
    _value: str
    _type: str
    _contents: str

    def contents(self):  # real signature unknown; restored from __doc__
        """
        ent.contents() -> string

        Return the contents of the entity.

        Only certain entities are supported, such as files and defined
        functions. Entities with no contents will return empty string.
        """
        return str(self._contents)

    def depends(self):  # real signature unknown; restored from __doc__
        """
        ent.depends() -> dict key=ounderstand.Ent value=list of ounderstand.Ref

        Return the dependencies of the class or file

        This function returns all the dependencies as a dictionary between an
        ent and the references occurring in the ent. An empty dictionary will
        be returned if there are no dependencies for the ent. The ent should be
        a class or file.
        """
        return {}

    def dependsby(self):  # real signature unknown; restored from __doc__
        """
        ent.dependsby() -> dict key=ounderstand.Ent value=list of ounderstand.Ref

        Return the ents depended on by the class or file

        This function returns all the dependencies as a dictionary between an
        ent and the references occurring in the ent. An empty dictionary will
        be returned if there are no dependencies on the ent. The ent should be
        a class or file.
        """
        return {}

    def ents(
        self, refkindstring, entkindstring=None
    ):  # real signature unknown; restored from __doc__
        """
        ent.ents(refkindstring [,entkindstring]) -> list of ounderstand.Ent

        Return a list of entities that reference, or are referenced by, the entity.

        The parameter refkindstring (string) should be a language-specific
        reference filter string.

        The optional paramater entkindstring (string) should be a language-
        specific entity filter string that specifies what kind of referenced
        entities are to be returned. If it is not included, all referenced
        entities are returned.
        """
        ents = set()
        query = ReferenceModel.select().where(
            (ReferenceModel._ent == self._id) | (ReferenceModel._scope == self._id)
        )
        if refkindstring:
            kinds = KindModel.select().where(
                (KindModel._name.contains(refkindstring))
                & (KindModel.is_ent_kind == False)
            )
            query = query.where(ReferenceModel._kind.in_(kinds))

        for ref in query:
            if entkindstring is not None:
                if entkindstring.lower() not in ref._ent._kind._name.lower():
                    continue
            ents.add(Ent(**ref._ent.__dict__.get("__data__")))
        return list(ents)

    def filerefs(
        self, refkindstring=None, entkindstring=None, unique=None
    ):  # real signature unknown; restored from __doc__
        """
        ent.filerefs([refkindstring [,entkindstring [,unique]]]) -> list of ounderstand.Ref

        Return a list of all references that occur in a file entity.

        If this is called on a non-file entity, it will return an empty list.
        The references returned will not necessarily have the file entity for
        their .scope value.

        The optional paramter refkindstring (string) should be a language-
        specific reference filter string. If it is not given, all references
         are returned.

        The optional paramter entkindstring (string) should be a language-
        specific entity filter string that specifies what kind of referenced
        entities should be returned. If it is not given, all references to
        any kind of entity are returned.

        The optional parameter unique (bool) is false by default. If it is
        true, only the first matching reference to each unique entity is
        returned
        """
        # TODO: Implement this later!
        return []

    def freetext(self, option):  # real signature unknown; restored from __doc__
        """ent.freetext(option) -> string"""
        return ""

    def ib(self, options=None):  # real signature unknown; restored from __doc__
        """
        ent.ib([options]) -> list of strings

        Return the Info Browser information for an entity.

        The optional parameter options (string) may be used to specify some
        parameters used to create the text. The format of the options string
        is "name=value" or "{field-name}name=value". Multiple options are
        separated with a semicolon. Spaces are allowed and are significant
        between multi-word field names, whereas, case is not significant. An
        option that specifies a field name is specific to that named field of
        the Info Browser. The available field names are exactly as they appear
        in the Info Browser. When a field is nested within another field, the
        correct name is the two names combined. For example, in C++, the field
        Macros within the field Local would be specified as "Local Macros".

        A field and its subfields may be disabled by specifying levels=0, or
        by specifying the field off, without specifying any option. For example,
        either of the will disable and hide the Metrics field:
          {Metrics}levels=0;
          {Metrics}=off;
        The following option is currently available only without a field name.
          Indent    - this specifies the number of indent spaces to output for
                      each level of a line of text. The default is 2.

        Other options are the same as are displayed when right-clicking on the
        field name in the Understand tool. No defaults are given for these
        options, as the defaults are specific for each language and each field
        name
        An example of a properly formatted option string would be:
          "{Metrics}=off;{calls}levels=-1;{callbys}levels=-1;{references}sort=name"

        The Architectures field is not generated by this command and can be
        generated separately using oudb.archs(ent)
        """
        return []

    def id(self):  # real signature unknown; restored from __doc__
        """
        ent.id() -> int

        Return a unique numeric identifier for the entity.

        The identifier is not guaranteed to remain constant after the
        database has been updated. An id can be converted back into an
        ounderstand.Ent with oudb.ent_from_id(id). The id is used for
        comparisons and the hash function.
        """
        return self._id

    def kind(self):  # real signature unknown; restored from __doc__
        """
        ent.kind() -> Kind

        Return the kind object for the entity.
        """
        kind = KindModel.get_by_id(self._kind)
        return Kind(**kind.__dict__.get("__data__"))

    def kindname(self):  # real signature unknown; restored from __doc__
        """
        ent.kindname() -> string

        Return the simple name for the kind of the entity.

        This is similar to ent.kind().name(), but does not create a Kind
        object.
        """
        return self.kind().name()

    def language(self):  # real signature unknown; restored from __doc__
        """
        ent.language() -> string

        Return the language of the entity

        Possible values include "Ada", "C++","C#", "Fortran",
        "Java", "Jovial", "Pascal", "Plm", "Python",
        "VHDL" or "Web". C is included with "C++".
        """
        return "Java"

    def longname(self):  # real signature unknown; restored from __doc__
        """
        ent.longname() -> string

        Return the long name of the entity.

        If there is no long name defined, the regular name (ent.name()) is
        returned. Examples of entities with long names include files, c++
        members, and most ada entities.
        """
        return str(self._longname)

    def metric(
        self, metric_list: list = None
    ) -> dict:  # real signature unknown; restored from __doc__
        """
        ent.metric(metriclist) -> dict key=string value=metricvalue

        Return the metric value for each item in metriclist

        Metric list must be a tuple or list containing the names of metrics
        as strings. If the metric is not available, it's value will be None.
        """
        metrics = {}
        for item in metric_list:
            if item not in self.metrics():
                raise ValueError(f"metric {item} is not in metric list")
        for item in metric_list:
            if item == "CountDeclMethodAll":
                metrics.update({"CountDeclMethodAll": count_decl_method_all(self)})
            elif item == "CountDeclClassVariable":
                metrics.update(
                    {"CountDeclClassVariable": declare_class_variables(self)}
                )
            elif item == "AvgCyclomatic":
                metrics.update({"AvgCyclomatic": avg_cyclomatic(self)})
            elif item == "AvgCyclomaticModified":
                metrics.update({"AvgCyclomaticModified": avg_cyclomatic_modified(self)})
            elif item == "AvgCyclomaticStrict":
                metrics.update({"AvgCyclomaticStrict": avg_cyclomatic_strict(self)})
            elif item == "AvgEssential":
                metrics.update({"AvgEssential": avg_essential(self)})
            elif item == "CountDeclClassMethod":
                metrics.update({"CountDeclClassMethod": declare_method_count(self)})
            elif item == "AvgLine":
                raise NotImplementedError("metric AvgLine is not implemented")
            elif item == "AvgLineBlank":
                raise NotImplementedError("metric AvgLineBlank is not implemented")
            elif item == "AvgLineCode":
                raise NotImplementedError("metric AvgLineCode is not implemented")
            elif item == "AvgLineComment":
                raise NotImplementedError("metric AvgLineComment is not implemented")
            elif item == "CountClassBase":
                raise NotImplementedError("metric CountClassBase is not implemented")
            elif item == "CountClassCoupled":
                raise NotImplementedError("metric CountClassCoupled is not implemented")
            elif item == "CountClassCoupledModified":
                raise NotImplementedError(
                    "metric CountClassCoupledModified is not implemented"
                )
            elif item == "CountClassDerived":
                raise NotImplementedError("metric CountClassDerived is not implemented")
            elif item == "CountDeclClass":
                raise NotImplementedError("metric CountDeclClass is not implemented")
            elif item == "CountDeclFile":
                metrics.update({"CountDeclFile": declare_file(self)})
            elif item == "CountDeclClassMethod":
                raise NotImplementedError(
                    "metric CountDeclClassMethod is not implemented"
                )
            elif item == "CountDeclExecutableUnit":
                metrics.update(
                    {"CountDeclExecutableUnit": declare_executable_unit(self)}
                )
            elif item == "CountDeclFunction":
                raise NotImplementedError("metric CountDeclFunction is not implemented")
            elif item == "CountDeclInstanceMethod":
                raise NotImplementedError(
                    "metric CountDeclInstanceMethod is not implemented"
                )
            elif item == "CountDeclInstanceVariable":
                raise NotImplementedError(
                    "metric CountDeclInstanceVariable is not implemented"
                )
            elif item == "CountDeclInstanceVariablePrivate":
                raise NotImplementedError(
                    "metric CountDeclInstanceVariablePrivate is not implemented"
                )
            elif item == "CountDeclInstanceVariableProtected":
                raise NotImplementedError(
                    "metric CountDeclInstanceVariableProtected is not implemented"
                )
            elif item == "CountDeclInstanceVariablePublic":
                raise NotImplementedError(
                    "metric CountDeclInstanceVariablePublic is not implemented"
                )
            elif item == "CountDeclMethod":
                raise NotImplementedError("metric CountDeclMethod is not implemented")
            elif item == "CountDeclMethodAll":
                metrics.update({"CountDeclMethodAll": count_decl_method_all(self)})
            elif item == "CountDeclMethodDefault":
                metrics.update(
                    {"CountDeclMethodDefault": count_decl_method_default(self)}
                )
            elif item == "CountDeclMethodProtected":
                metrics.update(
                    {"CountDeclMethodProtected": count_decl_method_protected(self)}
                )
            elif item == "CountDeclMethodPrivate":
                metrics.update(
                    {"CountDeclMethodPrivate": count_decl_method_private(self)}
                )
            elif item == "CountDeclMethodPublic":
                raise NotImplementedError(
                    "metric CountDeclMethodPublic is not implementd"
                )
            elif item == "CountInput":
                raise NotImplementedError("metric CountInput is not implemented")
            elif item == "CountLine":
                raise NotImplementedError("metric CountLine is not implemented")
            elif item == "CountLineBlank":
                raise NotImplementedError("metric CountLineBlank is not implemented")
            elif item == "CountLineCode":
                # check for number of line method objects
                metrics.update(
                    {
                        "CountLineCode": sum(
                            get_line_of_codes(self).class_countLineCode
                        )
                        + sum(get_line_of_codes(self).method_countLineCode)
                    }
                )
            elif item == "CountLineCodeDecl":
                metrics.update(
                    {
                        "CountLineCodeDecl": sum(
                            get_line_of_codes(self).class_countLineDecl
                        )
                        + sum(get_line_of_codes(self).method_countLineDecl)
                    }
                )
            elif item == "CountLineCodeExe":
                # check for number of line method objects
                metrics.update(
                    {
                        "CountLineCodeExe": sum(
                            get_line_of_codes(self).class_countLineExec
                        )
                        + sum(get_line_of_codes(self).method_countLineExec)
                    }
                )
            elif item == "CountLineComment":
                metrics.update(
                    {
                        "CountLineComment": sum(
                            get_line_of_codes(self).class_countLineComment
                        )
                        + sum(get_line_of_codes(self).method_countLineComment)
                    }
                )
            elif item == "CountOutput":
                raise NotImplementedError("metric CountOutput is not implemented")
            elif item == "CountPath":
                raise NotImplementedError("metric CountPath is not implemented")
            elif item == "CountPathLog":
                raise NotImplementedError("metric CountPathLog is not implemented")
            elif item == "CountSemicolon":
                raise NotImplementedError("metric CountSemicolon not implemented")
            elif item == "CountStmt":
                metrics.update({"CountStmt": statement_counter(self)})
            elif item == "CountStmtDecl":
                metrics.update({"CountStmtDecl": statement_counter_delc(self)})
            elif item == "CountStmtExe":
                metrics.update({"CountStmtExe": statement_counter_exe(self)})
            elif item == "Cyclomatic":
                metrics.update({"Cyclomatic": cyclomatic(self)})
            elif item == "CyclomaticModified":
                metrics.update({"CyclomaticModified": cyclomatic_modified(self)})
            elif item == "Essential":
                metrics.update({"Essential": essential(self)})
            elif item == "CyclomaticStrict":
                metrics.update({"CyclomaticStrict": cyclomatic_strict(self)})
            elif item == "Knots":
                metrics.update({"Knots": knot(self)})
            elif item == "MaxCyclomatic":
                metrics.update({"MaxCyclomatic": max_cyclomatic(self)})
            elif item == "MaxCyclomaticModified":
                metrics.update({"MaxCyclomaticModified": max_cyclomatic_modified(self)})
            elif item == "MaxCyclomaticStrict":
                metrics.update({"MaxCyclomaticStrict": max_cyclomatic_stricts(self)})
            elif item == "MaxEssential":
                metrics.update({"MaxEssential": max_essential(self)})
            elif item == "MaxEssentialKnots":
                metrics.update(
                    {"MaxEssentialKnots": min_max_essential_knots(self, False)}
                )
            elif item == "MaxInheritanceTree":
                metrics.update({"MaxInheritanceTree": get_max_inheritance(self)})
            elif item == "MaxNesting":
                metrics.update({"MaxNesting": MaxNesting(self)})
            elif item == "MinEssentialKnots":
                metrics.update(
                    {"MinEssentialKnots": min_max_essential_knots(self, True)}
                )
            elif item == "PercentLackOfCohesion":
                metrics.update(
                    {"PercentLackOfCohesion": get_percent_lack_of_cohesion(self)}
                )
            elif item == "PercentLackOfCohesionModified":
                metrics.update(
                    {
                        "PercentLackOfCohesionModified": get_percent_lack_of_cohesion_modified(
                            self
                        )
                    }
                )
            elif item == "RatioCommentToCode":
                metrics.update({"RatioCommentToCode": get_ratio_comment_to_code(self)})
            elif item == "SumCyclomatic":
                metrics.update({"SumCyclomatic": get_sum_of_cyclomatics(self)})
            elif item == "SumCyclomaticModified":
                metrics.update(
                    {"SumCyclomaticModified": get_sum_cyclomatic_modified(self)}
                )
            elif item == "SumCyclomaticStrict":
                metrics.update({"SumCyclomaticStrict": get_sum_cyclomatic_strict(self)})
            elif item == "SumEssential":
                metrics.update({"SumEssential": get_sum_essentials(self)})
        return metrics

    def metrics(self):  # real signature unknown; restored from __doc__
        """
        ent.metrics() -> list of strings
        Return a list of metric names defined for the entity.
        """

        return [
            "CountDeclMethodAll",
            "CountDeclClassVariable",
            "AvgCyclomatic",
            "AvgCyclomaticModified",
            "AvgCyclomaticStrict",
            "AvgEssential",
            "CountDeclClassMethod",
            "AvgLine",
            "AvgLineBlank",
            "AvgLineCode",
            "AvgLineComment",
            "CountClassBase",
            "CountClassCoupled",
            "CountClassCoupledModified",
            "CountClassDerived",
            "CountDeclClass",
            "CountDeclClassMethod",
            "CountDeclExecutableUnit",
            "CountDeclFile",
            "CountDeclFunction",
            "CountDeclInstanceMethod",
            "CountDeclInstanceVariable",
            "CountDeclInstanceVariablePrivate",
            "CountDeclInstanceVariableProtected",
            "CountDeclInstanceVariablePublic",
            "CountDeclMethod",
            "CountDeclMethodAll",
            "CountDeclMethodDefault",
            "CountDeclMethodPrivate",
            "CountDeclMethodProtected",
            "CountDeclMethodPublic" "CountInput",
            "CountLine",
            "CountLineBlank",
            "CountLineCode",
            "CountLineCodeDecl",
            "CountLineCodeExe",
            "CountLineComment",
            "CountOutput",
            "CountPath",
            "CountPathLog",
            "CountSemicolon",
            "CountStmt",
            "CountStmtDecl",
            "CountStmtExe",
            "Cyclomatic",
            "CyclomaticModified",
            "CyclomaticStrict",
            "Essential",
            "Knots",
            "MaxCyclomatic",
            "MaxCyclomaticModified",
            "MaxCyclomaticStrict",
            "MaxEssential",
            "MaxEssentialKnots",
            "MaxInheritanceTree",
            "MaxNesting",
            "MinEssentialKnots",
            "PercentLackOfCohesion",
            "PercentLackOfCohesionModified",
            "RatioCommentToCode",
            "SumCyclomatic",
            "SumCyclomaticModified",
            "SumCyclomaticStrict",
            "SumEssential",
        ]

    def name(self):  # real signature unknown; restored from __doc__
        """
        ent.name() -> string

        Return the shortname for an entity.

        For Java, this may return a name with a single dot in it. Use
        ent.simplename() to obtain the simplest, shortest name possible. This
        is what str() shows.
        """
        return str(self._name)

    def parameters(
        self, shownames=True
    ):  # real signature unknown; restored from __doc__
        """
        ent.parameters(shownames=True) -> string

        Return a string containing the parameters for the entity.

        The optional parameter shownames should be True or False. If it is
        False only the types, not the names, of the parameters are returned.
        There are some language-specific cases where there are no entities in
        the database for certain kinds of parameters. For example, in c++,
        there are no database entities for parameters for functions that are
        only declared, not defined, and there are no database entities for
        parameters for functional macro definitions. This method can be used
        to get some information about these cases. If no parameters are
        available, None is returned.
        """
        ents = EntityModel.select().where(EntityModel._parent == self._id)
        pars = []
        for ent in ents:
            obj = Ent(**ent.__dict__.get("__data__"))
            if obj.kind().check("parameter"):
                pars.append(f"{obj.type()} {obj.name() if shownames else ''}".strip())
        return ",".join(pars) if pars else None

    def parent(self):  # real signature unknown; restored from __doc__
        """
        ent.parent() -> ounderstand.Ent

        Return the parent of the entity or None if none
        """
        if self._parent is None:
            return None
        entity = EntityModel.get_by_id(pk=self._parent)
        return Ent(**entity.__dict__.get("__data__"))

    def parsetime(self):  # real signature unknown; restored from __doc__
        """
        ent.parsetime() -> int

        Return the last time the file entity was parse in the database.

        If the entity is not a parse file, it will be 0. The time is in
        Unix/Postix Time
        """
        return 0

    def ref(
        self, *args, **kwargs
    ):  # real signature unknown; NOTE: unreliably restored from __doc__
        """
        ent.ref([refkindstring [,entkindstring]) -> ounderstand.Ref

        This is the same as ent.refs()[:1]
        """
        return self.refs(*args, **kwargs)[:1]

    def refs(
        self, refkindstring=None, entkindstring=None, unique=None
    ):  # real signature unknown; restored from __doc__
        """
        ent.refs([refkindstring [,entkindstring [,unique]]]) -> list of ounderstand.Ref
        Return a list of references.
        The optional paramter refkindstring (string) should be a language-
        specific reference filter string. If it is not given, all references are returned.
        The optional paramter entkindstring (string) should be a language-
        specific entity filter string that specifies what kind of referenced
        entities should be returned. If it is not given, all references to
        any kind of entity are returned.
        The optional parameter unique (bool) is false by default. If it is
        true, only the first matching reference to each unique entity is
        returned
        """
        # TODO : check nested references
        mlist = [j.strip() for j in refkindstring.split(",")]
        # print(mlist)
        refs = []
        for item in mlist:
            query = ReferenceModel.select().where(ReferenceModel._scope == self._id)
            if item:
                kinds = KindModel.select().where(
                    (KindModel.is_ent_kind == False)
                    & (KindModel._name.contains(item))
                    & (fn.Lower(KindModel._name) == (f"Java {item}").lower())
                )
                if len(mlist) > 0:
                    print(kinds.count())
                    for k in kinds:
                        print("kin : ", k._name)
                        print(k._id)
                    q = ReferenceModel.select().where(ReferenceModel._kind.in_(kinds))
                    for it in query:
                        print("it : ", it._kind)
                        if str(it._kind) != "Java Define":
                            print("X :", it._kind)
                            print("X :", "Java Define")

                query = query.where(ReferenceModel._kind.in_(kinds))
                if len(mlist) > 0:
                    print(query.count())

            if entkindstring:
                kinds = KindModel.select().where(
                    (KindModel.is_ent_kind == True)
                    & (KindModel._name.contains(entkindstring))
                )
                ents = EntityModel.select().where(EntityModel._kind.in_(kinds))
                query = query.where(ReferenceModel._ent.in_(ents))

            for ref in query:
                refs.append(Ref(**ref.__dict__.get("__data__")))
        # Remove duplicates from 'refs' and store unique references in 'references' list
        references = []
        for ref in refs:
            if ref not in references:
                references.append(ref)
        if unique:
            references = references[:1]
        return references

    def relname(self):  # real signature unknown; restored from __doc__
        """
        ent.relname() -> string

        Return the relative name of the file entity.

        This is the fullname for the file, minus any root directories that
        are common for all project files. Return None for non-file entities.
        """
        # TODO: Implement this later!
        return ""

    def simplename(self):  # real signature unknown; restored from __doc__
        """
        ent.simplename() -> string

        Return the simplename for the entity.

        This is the simplest, shortest name possible for the entity. It is
        generally the same as ent.name() except for languages like Java, for
        which this will not return a name with any dots in it.
        """
        return self.name().split(".")[-1]

    def type(self):  # real signature unknown; restored from __doc__
        """
        ent.type() -> string

        Return the type string of the entity.

        This is defined for entity kinds like variables and types, as well as
        entity kinds that have a return type like functions.
        """
        if self._type is not None:
            return str(self._type)
        return None

    def uniquename(self):  # real signature unknown; restored from __doc__
        """
        ent.uniquename() -> string

        Return the unique name of the entity.

        This name is not suitable for use by an end user. Rather, it is a
        means of identifying an entity uniquely in multiple databases, perhaps
        as the source code changes slightly over time. The unique name is
        composed of things like parameters and parent names. So, the some
        code changes will in new uniquenames for the same intrinsic entity.
        Use oudb.lookup_uniquename() to convert a unqiuename back to an object
        of ounderstand.Ent. This is what repr() shows.
        """
        return ""

    def value(self):  # real signature unknown; restored from __doc__
        """
        ent.value() -> string

        Return the value associated with the entity.

        This is for enumerators, initialized variables, and macros. Not all
        languages are supported.
        """
        if self._value is not None:
            return str(self._value)
        return None

    def __eq__(self, other):  # real signature unknown
        """Return self==value."""
        if isinstance(other, Ent):
            return self.id() == other.id()
        return NotImplemented

    def __ge__(self, *args, **kwargs):  # real signature unknown
        """Return self>=value."""
        pass

    def __gt__(self, *args, **kwargs):  # real signature unknown
        """Return self>value."""
        pass

    def __hash__(self, *args, **kwargs):  # real signature unknown
        """Return hash(self)."""
        return hash(self.id())

    def __le__(self, *args, **kwargs):  # real signature unknown
        """Return self<=value."""
        pass

    def __lt__(self, *args, **kwargs):  # real signature unknown
        """Return self<value."""
        pass

    def __ne__(self, *args, **kwargs):  # real signature unknown
        """Return self!=value."""
        pass

    def __str__(self):
        return str(self.name())

    def __repr__(self):
        return str(self.longname())


@dataclass
class Kind(object):
    """
    This class represents a kind of an entity or reference. For example,an entity kind might be a "C Header File" and a reference kind
    kind could be "Call." Kindstrings and refkindstrings filters are
    built from these. A filter string may use the tilde "~" to indicate
    the absence of a token, and comma "," to "or" filters together.
    Otherwise, filters are constructed with an "and" relationship. For
    more information on filter strings or a full list of available kinds
    and reference kinds see the Understand Perl API documentation.

    Available methods are:

      ounderstand.Kind.check(kindstring)
      ounderstand.Kind.inv()
      ounderstand.Kind.longname()
      ounderstand.Kind.name()  ounderstand.Kind.__repr__() --longname
      ounderstand.Kind.__str__() --name
    Static Methods:
      ounderstand.Kind.list_entity([entkind])
      ounderstand.Kind.list_reference([refkind])
    """

    _id: int
    _inv: int
    _name: str

    is_ent_kind: bool

    def check(self, kindstring):  # real signature unknown; restored from __doc__
        """
        kind.check(kindstring) -> bool

        Return true if the kind matches the filter string kindstring.
        """
        return kindstring.lower() in self.name().lower()

    def inv(self):  # real signature unknown; restored from __doc__
        """
        kind.inv() -> ounderstand.Kind

        The logical inverse of a reference kind. This will throw an
        UnderstandError if called with an entity kind.
        """
        if self.is_ent_kind:
            raise UnderstandError()
        inverse = KindModel.get_by_id(pk=self._inv)
        return Kind(**inverse.__data__.get("__data__"))

    @staticmethod
    def list_entity(entkind=""):  # real signature unknown; restored from __doc__
        """
        Kind.list_entity([entkind]) (static method)-> list of ounderstand.Kind

        Return the list of entity kinds that match the filter entkind.

        If no entkind is given, all entity kinds are returned. For example,
        to get the list of all c function entity kinds:
          kinds = ounderstand.Kind.list_entity("c function")
        """
        query = KindModel.select().where(
            KindModel.is_ent_kind == True, KindModel._name.contains(entkind)
        )
        kinds = []
        if query.count() == 0:
            query = KindModel.select().where(KindModel.is_ent_kind == True)
        for kind in query:
            kinds.append(Kind(**kind.__dict__.get("__data__")))
        return kinds

    @staticmethod
    def list_reference(refkind=""):  # real signature unknown; restored from __doc__
        """
        Kind.list_reference([refkind]) (static method)->list of ounderstand.Kind

        Return the list of reference kinds that match the filter refkind.

        If no refkind is given, all reference kinds are returned. For example,
        to get the list of all ada declare reference kinds:
          kinds = ounderstand.Kind.list_entity("ada declare")
        """
        query = KindModel.select().where(
            KindModel.is_ent_kind == False, KindModel._name.contains(refkind)
        )
        kinds = []
        if query.count() == 0:
            query = KindModel.select().where(KindModel.is_ent_kind == False)
        for kind in query:
            kinds.append(Kind(**kind.__dict__.get("__data__")))
        return kinds

    def longname(self):  # real signature unknown; restored from __doc__
        """
        kind.longname() -> string

        Return the long form of the kind name.

        This is usually more detailed than desired for human reading. It is
        the same as repr(kind)
        """
        return self.name()

    def name(self):  # real signature unknown; restored from __doc__
        """
        kind.name() -> string

        Return the name of the kind.

        This is the same as str(kind).
        """
        return str(self._name)

    def __repr__(self, *args, **kwargs):  # real signature unknown
        """Return repr(self)."""
        return self.name()

    def __str__(self, *args, **kwargs):  # real signature unknown
        """Return str(self)."""
        return self.name()


@dataclass
class Ref(object):
    """
    A reference object stores an reference between on entity an another.
    Available methods are:

      ounderstand.Ref.column()
      ounderstand.Ref.ent()
      ounderstand.Ref.file()
      undersatnd.Ref.kind()
      ounderstand.Ref.kindname()
      ounderstand.Ref.line()
      ounderstand.Ref.scope()
      ounderstand.Ref.__str__() --kindname ent file(line)
    """

    _id: int
    _kind: int
    _file: int
    _line: int
    _column: int
    _ent: int
    _scope: int

    def column(self):  # real signature unknown; restored from __doc__
        """
        ref.column() -> int

        Return the column in source where the reference occurred.
        """
        return self._column

    def ent(self):  # real signature unknown; restored from __doc__
        """
        ref.ent() -> ounderstand.Ent

        Return the entity being referenced.
        """
        entity = EntityModel.get_by_id(pk=self._ent)
        return Ent(**entity.__dict__.get("__data__"))

    def file(self):  # real signature unknown; restored from __doc__
        """
        ref.file() -> ounderstand.Ent

        Return the file where the reference occurred.
        """
        entity = EntityModel.get_by_id(pk=self._file)
        return Ent(**entity.__dict__.get("__data__"))

    def isforward(self):  # real signature unknown; restored from __doc__
        """
        ref.isforward() -> bool

        Return True if the reference is forward.
        """
        # TODO: Is this necessary?
        return False

    def kind(self):  # real signature unknown; restored from __doc__
        """
        ref.kind() -> ounderstand.Kind

        Return the reference kind.
        """
        refkind = KindModel.get_by_id(pk=self._kind)
        return Kind(**refkind.__dict__.get("__data__"))

    def kindname(self):  # real signature unknown; restored from __doc__
        """
        ref.kindname() -> string

        Return the short name of the reference kind

        This is similar to ref.kind().name(), but does not create anunderstand.Kind object.
        """
        return self.kind().name()

    def line(self):  # real signature unknown; restored from __doc__
        """
        ref.line() -> int

        Return the line in source where the reference occurred.
        """
        return self._line

    def macroexpansion(self):  # real signature unknown; restored from __doc__
        """
        ref.macroexpansion() -> string

        Return the macro expansion text for the refence file, line and column.
        This function may return None if no text is available.
        """
        # TODO: what is this ?
        return ""

    def scope(self):  # real signature unknown; restored from __doc__
        """
        ref.scope() -> ounderstand.Ent

        Return the entity performing the reference.
        """
        entity = EntityModel.get_by_id(pk=self._scope)
        return Ent(**entity.__dict__.get("__data__"))

    def __repr__(self, *args, **kwargs):  # real signature unknown
        """Return repr(self)."""
        return f"{self.kind()} {self.ent()} {self.file()}({self._line}, {self._column})"

    def __str__(self, *args, **kwargs):  # real signature unknown
        """Return str(self)."""
        return f"{self.kind()} {self.ent()} {self.file()}({self._line}, {self._column})"


class UnderstandError(Exception):
    # no doc
    def __init__(self, *args, **kwargs):  # real signature unknown
        pass

    __weakref__ = property(
        lambda self: object(), lambda self, v: None, lambda self: None
    )  # default
    """list of weak references to the object (if defined)"""


class Violation(object):
    """
    Available Methods are:
      ounderstand.Violation.add_fixit_hint(line,column,length[,text])
    """

    def add_fixit_hint(
        self, line, column, end_line, end_column, text=None
    ):  # real signature unknown; restored from __doc__
        """
        violation.add_fixit_hint(line,column,end_line,end_column[,text]) -> None

        Add a fix-it hint associated with this violation.

        The line, column, end_line, and end_column describe a range of text to be
        replaced in the file. The range can be empty to indicate pure insertion.
        The text is the replacement text. It can be empty for pure removal.
        """
        pass

    def __init__(self, *args, **kwargs):  # real signature unknown
        pass


# variables with complex values

__loader__ = None  # (!) real value is '<_frozen_importlib_external.ExtensionFileLoader object at 0x000001CE33FC3130>'

__spec__ = None  # (!) real value is "ModuleSpec(name='ounderstand', loader=<_frozen_importlib_external.ExtensionFileLoader object at 0x000001CE33FC3130>, origin='D:\\\\program files\\\\SciTools\\\\bin\\\\pc-win64\\\\Python\\\\ounderstand.pyd')"
