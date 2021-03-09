"""

This script contains 281 (as version 0.3.0) names of different (object-oriented) source code metric
for Java programming language

To be used in CodART project

"""
__version__ = '0.4.0'
__author__ = 'Morteza'

metric_map = {
    # key: metric name, value: metric name in paper
    'Class': 'Class',

    'PK_CountLineCode': 'PKLOC',
    'PK_CountLineCodeDecl': 'PKLOCD',
    'PK_CountLineCodeExe': 'PKLOCE',
    'PK_AvgLineCode': 'PKLOC_AVG',
    'PK_AvgLineCodeDecl': 'PKLOCD_AVG',
    'PK_AvgLineCodeExe': 'PKLOCE_AVG',
    'PK_MaxLineCode': 'PKLOC_MAX',
    'PK_MaxLineCodeDecl': 'PKLOCD_MAX',
    'PK_MaxLineCodeExe': 'PKLOCE_MAX',
    'PK_MinLineCode': 'PKLOC_MIN',
    'PK_MinLineCodeDecl': 'PKLOCD_MIN',
    'PK_MinLineCodeExe': 'PKLOCE_MIN',
    'PK_SDLineCode': 'PKLOC',
    'PK_SDLineCodeDecl': 'PKLOCD_SD',
    'PK_SDLineCodeExe': 'PKLOCE_SD',

    'PK_CountStmt': 'PKNOST',
    'PK_CountStmtDecl': 'PKNOSTD',
    'PK_CountStmtExe': 'PKNOSTE',
    'PK_AvgStmt': 'PKNOST_AVG',
    'PK_AvgStmtDecl': 'PKNOSTD_AVG',
    'PK_AvgStmtExe': 'PKNOSTE_AVG',
    'PK_MaxStmt': 'PKNOST_MAX',
    'PK_MaxStmtDecl': 'PKNOSTD_MAX',
    'PK_MaxStmtExe': 'PKNOSTE_MAX',
    'PK_MinStmt': 'PKNOST_MIN',
    'PK_MinStmtDecl': 'PKNOSTD_MIN',
    'PK_MinStmtExe': 'PKNOSTE_MIN',
    'PK_SDStmt': 'PKNOST_SD',
    'PK_SDStmtDecl': 'PKNOSTD_SD',
    'PK_SDStmtExe': 'PKNOSTE_SD',

    'PK_CountDeclClassMethod': 'PKNOSM',
    'PK_CountDeclClassVariable': 'PKNOSA',
    'PK_CountDeclInstanceMethod': 'PKNOIM',
    'PK_CountDeclInstanceVariable': 'PKNOIA',
    'PK_PKNOMNAMM': 'PKNOMNAMM',
    'PK_CountDeclClass': 'PKNOCS',
    'PK_CountDeclFile': 'PKNOFL',

    'PK_SumCyclomatic': 'PKCC',
    'PK_SumCyclomaticModified': 'PKCCM',
    'PK_SumCyclomaticStrict': 'PKCCS',
    'PK_SumEssential': 'PKCCE',
    'PK_MaxCyclomatic': 'PKCC_MAX',
    'PK_MaxCyclomaticModified': 'PKCCM_MAX',
    'PK_MaxCyclomaticStrict': 'PKCCS_MAX',
    'PK_MaxEssential': 'PKCCE_MAX',
    'PK_AvgCyclomatic': 'PKCC_AVG',
    'PK_AvgCyclomaticModified': 'PKCCM_AVG',
    'PK_AvgCyclomaticStrict': 'PKCCS_AVG',
    'PK_AvgEssential': 'PKCCE_AVG',
    'PK_MinCyclomatic': 'PKCC_MIN',
    'PK_MinCyclomaticModified': 'PKCCM_MIN',
    'PK_MinCyclomaticStrict': 'PKCCS_MIN',
    'PK_MinEssential': 'PKCCE_MIN',
    'PK_SDCyclomatic': 'PKCC_SD',
    'PK_SDCyclomaticModified': 'PKCCM_SD',
    'PK_SDCyclomaticStrict': 'PKCCS_SD',
    'PK_SDEssential': 'PKCCE_SD',

    'PK_MaxNesting': 'PKNESTING_MAX',
    'PK_MinNesting': 'PKNESTING_MIN',
    'PK_AvgNesting': 'PKNESTING_AVG',
    'PK_SDNesting': 'PKNESTING_SD',

    'PK_CountDeclMethodDefault': 'PKNODM',
    'PK_CountDeclMethodPrivate': 'PKNOPM',
    'PK_CountDeclMethodProtected': 'PKNOPRM',
    'PK_CountDeclMethodPublic': 'PKNOPLM',
    'PK_PKNOAMM': 'PKNOAMM',

    'PK_PKNOI': 'PKNOI',
    'PK_PKNOAC': 'PKNOAC',

    'CSLEX_NumberOfTokens': 'NOTK',
    'CSLEX_NumberOfUniqueTokens': 'NOTKU',
    'CSLEX_NumberOfIdentifies': 'NOID',
    'CSLEX_NumberOfUniqueIdentifiers': 'NOIDU',
    'CSLEX_NumberOfKeywords': 'NOKW',
    'CSLEX_NumberOfUniqueKeywords': 'NOKWU',
    'CSLEX_NumberOfAssignments': 'NOASS',
    'CSLEX_NumberOfOperatorsWithoutAssignments': 'NOOP',
    'CSLEX_NumberOfUniqueOperators': 'NOOPU',
    'CSLEX_NumberOfSemicolons': 'NOSC',
    'CSLEX_NumberOfDots': 'NODOT',
    'CSLEX_NumberOfReturnAndPrintStatements': 'NOREPR',
    'CSLEX_NumberOfConditionalJumpStatements': 'NOCJST',
    'CSLEX_NumberOfUnConditionalJumpStatements': 'NOCUJST',
    'CSLEX_NumberOfExceptionStatements': 'NOEXST',
    'CSLEX_NumberOfNewStatements': 'NONEW',
    'CSLEX_NumberOfSuperStatements': 'NOSUPER',

    'CSORD_CountLineCode': 'CSLOC',
    'CSORD_CountLineCodeDecl': 'CSLOCD',
    'CSORD_CountLineCodeExe': 'CSLOCE',
    'CSORD_AvgLineCode': 'CSLOC_AVG',
    'CSORD_AvgLineCodeDecl': 'CSLOCD_AVG',
    'CSORD_AvgLineCodeExe': 'CSLOCE_AVG',
    'CSORD_MaxLineCode': 'CSLOC_MAX',
    'CSORD_MaxLineCodeDecl': 'CSLOCD_MAX',
    'CSORD_MaxLineCodeExe': 'CSLOCE_MAX',
    'CSORD_MinLineCode': 'CSLOC_MIN',
    'CSORD_MinLineCodeDecl': 'CSLOCD_MIN',
    'CSORD_MinLineCodeExe': 'CSLOCE_MIN',
    'CSORD_SDLineCode': 'CSLOC_SD',
    'CSORD_SDLineCodeDecl': 'CSLOCD_SD',
    'CSORD_SDLineCodeExe': 'CSLOCE_SD',
    'CSORD_LogLineCode': 'CSLOC_LOG',
    'CSORD_LogLineCodeDecl': 'CSLOCD_LOG',
    'CSORD_LogLineCodeExe': 'CSLOCE_LOG',
    'CSORD_CountLineCodeNAMM': 'CSLOCNAMM',
    'CSORD_CountLineCodeDeclNAMM': 'CSLOCDNAMM',
    'CSORD_CountLineCodeExeNAMM': 'CSLOCENAMM',
    'CSORD_AvgLineCodeNAMM': 'CSLOCNAMM_AVG',
    'CSORD_AvgLineCodeDeclNAMM': 'CSLOCDNAMM_AVG',
    'CSORD_AvgLineCodeExeNAMM': 'CSLOCENAMM_AVG',
    'CSORD_MaxLineCodeNAMM': 'CSLOCNAMM_MAX',
    'CSORD_MaxLineCodeDeclNAMM': 'CSLOCDNAMM_MAX',
    'CSORD_MaxLineCodeExeNAMM': 'CSLOCENAMM_MAX',
    'CSORD_MinLineCodeNAMM': 'CSLOCNAMM_MIN',
    'CSORD_MinLineCodeDeclNAMM': 'CSLOCDNAMM_MIN',
    'CSORD_MinLineCodeExeNAMM': 'CSLOCENAMM_MIN',
    'CSORD_SDLineCodeNAMM': 'CSLOCNAMM_SD',
    'CSORD_SDLineCodeDeclNAMM': 'CSLOCDNAMM_SD',
    'CSORD_SDLineCodeExeNAMM': 'CSLOCENAMM_SD',

    'CSORD_LogStmt': 'CSNOST_LOG',
    'CSORD_LogStmtDecl': 'CSNOSTD_LOG',
    'CSORD_LogStmtExe': 'CSNOSTE_LOG',
    'CSORD_CountStmt': 'CSNOST',
    'CSORD_CountStmtDecl': 'CSNOSTD',
    'CSORD_CountStmtExe': 'CSNOSTE',
    'CSORD_AvgStmt': 'CSNOST_AVG',
    'CSORD_AvgStmtDecl': 'CSNOST_AVG',
    'CSORD_AvgStmtExe': 'CSNOSTE_AVG',
    'CSORD_MaxStmt': 'CSNOST_MAX',
    'CSORD_MaxStmtDecl': 'CSNOSTD_MAX',
    'CSORD_MaxStmtExe': 'CSNOSTE_MAX',
    'CSORD_MinStmt': 'CSNOST_MIN',
    'CSORD_MinStmtDecl': 'CSNOSTD_MIN',
    'CSORD_MinStmtExe': 'CSNOSTE_MIN',
    'CSORD_SDStmt': 'CSNOST_SD',
    'CSORD_SDStmtDecl': 'CSNOSTD_SD',
    'CSORD_SDStmtExe': 'CSNOSTE_SD',
    'CSORD_CountStmtNAMM': 'CSNOSTNAMM',
    'CSORD_CountStmtDeclNAMM': 'CSNOSTDNAMM',
    'CSORD_CountStmtExeNAMM': 'CSNOSTENAMM',
    'CSORD_AvgStmtNAMM': 'CSNOSTNAMM_AVG',
    'CSORD_AvgStmtDeclNAMM': 'CSNOSTDNAMM_AVG',
    'CSORD_AvgStmtExeNAMM': 'CSNOSTENAMM_AVG',
    'CSORD_MaxStmtNAMM': 'CSNOSTNAMM_MAX',
    'CSORD_MaxStmtDeclNAMM': 'CSNOSTDNAMM_MAX',
    'CSORD_MaxStmtExeNAMM': 'CSNOSTENAMM_MAX',
    'CSORD_MinStmtNAMM': 'CSNOSTNAMM_MIN',
    'CSORD_MinStmtDeclNAMM': 'CSNOSTDNAMM_MIN',
    'CSORD_MinStmtExeNAMM': 'CSNOSTENAMM_MIN',
    'CSORD_SDStmtNAMM': 'CSNOSTNAMM_SD',
    'CSORD_SDStmtDeclNAMM': 'CSNOSTDNAMM_SD',
    'CSORD_SDStmtExeNAMM': 'CSNOSTENAMM_SD',

    'CSORD_CountDeclClassMethod': 'CSNOSM',
    'CSORD_CountDeclClassVariable': 'CSNOSA',
    'CSORD_CountDeclInstanceMethod': 'CSNOIM',
    'CSORD_CountDeclInstanceVariable': 'CSNOIA',

    'CSORD_CSNOMNAMM': 'CSNOMNAMM',
    'CSORD_SumCSNOP': 'CSNOP',
    'CSORD_MaxCSNOP': 'CSNOP_MAX',
    'CSORD_MinCSNOP': 'CSNOP_MIN',
    'CSORD_AvgCSNOP': 'CSNOP_AVG',
    'CSORD_SDCSNOP': 'CSNOP_SD',
    'CSORD_SumCSNOPNAMM': 'CSNOPNAMM',
    'CSORD_MaxCSNOPNAMM': 'CSNOPNAMM_MAX',
    'CSORD_MinCSNOPNAMM': 'CSNOPNAMM_MIN',
    'CSORD_AvgCSNOPNAMM': 'CSNOPNAMM_AVG',
    'CSORD_SDCSNOPNAMM': 'CSNOPNAMM_SD',

    'CSORD_SumCyclomatic': 'CSCC',
    'CSORD_SumCyclomaticModified': 'CSCCM',
    'CSORD_SumCyclomaticStrict': 'CSCCS',
    'CSORD_SumEssential': 'CSCCE',
    'CSORD_MaxCyclomatic': 'CSCC_MAX',
    'CSORD_MaxCyclomaticModified': 'CSCCM_MAX',
    'CSORD_MaxCyclomaticStrict': 'CSCCS_MAX',
    'CSORD_MaxEssential': 'CSCCE_MAX',
    'CSORD_AvgCyclomatic': 'CSCC_AVG',
    'CSORD_AvgCyclomaticModified': 'CSCCM_AVG',
    'CSORD_AvgCyclomaticStrict': 'CSCCS_AVG',
    'CSORD_AvgEssential': 'CSCCE_AVG',
    'CSORD_MinCyclomatic': 'CSCC_MIN',
    'CSORD_MinCyclomaticModified': 'CSCCM_MIN',
    'CSORD_MinCyclomaticStrict': 'CSCCS_MIN',
    'CSORD_MinEssential': 'CSCCE_MIN',
    'CSORD_SDCyclomatic': 'CSCC_SD',
    'CSORD_SDCyclomaticModified': 'CSCCM_SD',
    'CSORD_SDCyclomaticStrict': 'CSCCS_SD',
    'CSORD_SDEssential': 'CSCCE_SD',
    'CSORD_LogCyclomatic': 'CSCC_LOG',  # Do not have mentioned in paper1
    'CSORD_LogCyclomaticStrict': 'CSCCS_LOG',  # Do not have mentioned in paper1 but have mentioned in paper3
    'CSORD_LogCyclomaticModified': 'CSCCM_LOG',  # Do not have mentioned in paper1
    'CSORD_LogEssential': 'CSCCE_LOG',  # Do not have mentioned in paper1

    'CSORD_SumCyclomaticNAMM': 'CSCCNAMM',
    'CSORD_SumCyclomaticModifiedNAMM': 'CSCCMNAMM',
    'CSORD_SumCyclomaticStrictNAMM': 'CSCCSNAMM',
    'CSORD_SumEssentialNAMM': 'CSCCENAMM',
    'CSORD_MaxCyclomaticNAMM': 'CSCCNAMM_MAX',
    'CSORD_MaxCyclomaticModifiedNAMM': 'CSCCMNAMM_MAX',
    'CSORD_MaxCyclomaticStrictNAMM': 'CSCCSNAMM_MAX',
    'CSORD_MaxEssentialNAMM': 'CSCCENAMM_MAX',
    'CSORD_AvgCyclomaticNAMM': 'CSCCNAMM_AVG',
    'CSORD_AvgCyclomaticModifiedNAMM': 'CSCCMNAMM_AVG',
    'CSORD_AvgCyclomaticStrictNAMM': 'CSCCSNAMM_AVG',
    'CSORD_AvgEssentialNAMM': 'CSCCENAMM_AVG',
    'CSORD_MinCyclomaticNAMM': 'CSCCNAMM_MIN',
    'CSORD_MinCyclomaticModifiedNAMM': 'CSCCMNAMM_MIN',
    'CSORD_MinCyclomaticStrictNAMM': 'CSCCSNAMM_MIN',
    'CSORD_MinEssentialNAMM': 'CSCCENAMM_MIN',
    'CSORD_SDCyclomaticNAMM': 'CSCCNAMM_SD',
    'CSORD_SDCyclomaticModifiedNAMM': 'CSCCMNAMM_SD',
    'CSORD_SDCyclomaticStrictNAMM': 'CSCCSNAMM_SD',
    'CSORD_SDEssentialNAMM': 'CSCCENAMM_SD',

    'CSORD_MaxNesting': 'CSNESTING_MAX',
    'CSORD_MinNesting': 'CSNESTING_MIN',
    'CSORD_AvgNesting': 'CSNESTING_AVG',
    'CSORD_SDNesting': 'CSNESTING_SD',

    'CSORD_PercentLackOfCohesion': 'LOCM',
    'CSORD_CountClassCoupled': 'CBO',
    'CSORD_RFC': 'RFC',
    'CSORD_FANIN': 'FANIN',
    'CSORD_FANOUT': 'FANOUT',
    'CSORD_ATFD': 'ATFD',
    'CSORD_CFNAMM': 'CFNAMM',
    'CSORD_DAC': 'DAC',

    'CSORD_NumberOfMethodCalls': 'NOMCALL',
    'CSORD_CountDeclMethodDefault': 'CSNODM',
    'CSORD_CountDeclMethodPrivate': 'CSNOPM',
    'CSORD_CountDeclMethodProtected': 'CSNOPRM',
    'CSORD_CountDeclMethodPublic': 'CSNOPLM',
    'CSORD_CSNOAMM': 'CSNOAMM',

    'CSORD_MaxInheritanceTree': 'DIT',
    'CSORD_CountClassDerived': 'NOC',
    'CSORD_CountClassBase': 'NOP',
    'CSORD_NIM': 'NIM',
    'CSORD_NMO': 'NMO',
    'CSORD_NOII': 'NOII',

    'CSORD_SumCountPath': 'CSPATH',
    'CSORD_MinCountPath': 'CSPATH_MIN',
    'CSORD_MaxCountPath': 'CSPATH_MAX',
    'CSORD_AvgCountPath': 'CSPATH_AVG',
    'CSORD_SDCountPath': 'CSPATH_SD',
    'CSORD_SumCountPathLog': 'CSPATH_LOG',
    'CSORD_MinCountPathLog': 'CSPATH_LOG_MIN',
    'CSORD_MaxCountPathLog': 'CSPATH_LOG_MAX',
    'CSORD_AvgCountPathLog': 'CSPATH_LOG_AVG',
    'CSORD_SDCountPathLog': 'CSPATH_LOG_SD',

    'CSORD_SumKnots': 'CSKNOTS',
    'CSORD_MinKnots': 'CSKNOTS_MIN',
    'CSORD_MaxKnots': 'CSKNOTS_MAX',
    'CSORD_AvgKnots': 'CSKNOTS_AVG',
    'CSORD_SDKnots': 'CSKNOTS_SD',

    'CSORD_NumberOfClassConstructors': 'CSNOCON',
    'CSORD_NumberOfDepends': 'DEPENDS',
    'CSORD_NumberOfDependsBy': 'DEPENDSBy',
    'CSORD_NumberOfMethods': 'CSNOM',

    'Label_LineCoverage': 'LINECOVERAGE',
    'Label_BranchCoverage': 'BRANCHCOVERAGE',
    'Tests': 'TESTS',
    'Label_Combine1': 'COMBINE',
    'Coverageability1': 'TETSTABILITY',
}

# -----------------------------------------------
# Primary metrics list
# Class-level metrics
class_ordinary_metrics_names_primary = [
    # 1. Class size/count metrics
    # 1.1. CSLOC (30)
    # 1.1.1-15. CSLOC_All
    'CountLineCode',

    # 1.2. CSNOST (3-->30)
    # 1.2.1-15. CSNOST_All
    'CountStmt',

    # 1.3. Number of method metrics
    'CountDeclClassMethod',  # CSNOSM
    'CountDeclClassVariable',  # CSNOSA
    'CountDeclInstanceMethod',  # CSNOIM
    'CountDeclInstanceVariable',  # CSNOIA

    # 1.4. CSNOP (10)
    # 1.4.1-5. CSNOP_All
    'SumCSNOP',

    # ------------------------------------------------
    # 2. Class complexity metrics
    # 2.1. CSCC(40)
    # 2.1.1-20. CSCC_All
    'SumCyclomatic',

    # 2.2. Nesting
    'MaxNesting',

    # ------------------------------------------------
    # 3. Class cohesion metrics
    'PercentLackOfCohesion',  # LOCM

    # 4. Class coupling metrics
    'CountClassCoupled',  # CBO
    'RFC',  # RFC: Response for a class or # 'NumberOfFunctionCalls',
    'FANIN',  # Fan-in
    'FANOUT',  # Fan-out
    'ATFD',  # Access to foreign data
    'CFNAMM',  # Called foreign not accessor or mutator methods
    'DAC',  # Data Abstraction Coupling or MOA in QMOOD
    'NumberOfMethodCalls',

    # 5. Class visibility metrics
    'CountDeclMethodDefault',  # CSNODM
    'CountDeclMethodPrivate',  # CSNOPM
    'CountDeclMethodProtected',  # CSNOPRM
    'CountDeclMethodPublic',  # CSNOPLM
    'CSNOAMM',
    # NOAMM: Class number of accessor and mutator methods  # Replace with old NOAM which computed only getter methods

    # 6. Inheritance metrics
    'MaxInheritanceTree',  # DIT
    'CountClassDerived',  # NOC
    'CountClassBase',  # NOP for JAVA is 0 or 1
    'NIM',  # NIM: Number of inherited methods
    'NMO',  # NMO: Number of methods overridden
    'NOII',  # NOII: Number of implemented interfaces

    # 'CountDeclMethodAll', 'CountDeclMethod',  # Eliminated metric. Replace with 'NMO' + 'NIM' + '...' (version 0.3.0)

    # New added metric (version 0.3.0, dataset 0.5.0):
    'SumCountPath',
    'SumKnots',
    'NumberOfDepends',
    'NumberOfDependsBy',
]

# Package-level metrics
package_metrics_names_primary = [
    # 1. Package size/count metrics
    # 2.1 PKLOC (15)
    'CountLineCode',

    # 2.2 PKNOS (15)
    'CountStmt',

    # 2.3. Other Size/Count method (understand built-in metrics)
    'CountDeclClassMethod',  # PKNOSM
    'CountDeclClassVariable',  # PKNOSA
    'CountDeclInstanceMethod',  # PKNOIM
    'CountDeclInstanceVariable',  # PKNOIA
    'CountDeclClass',
    'CountDeclFile',

    # ------------------------------------------------
    # 2. Package complexity metrics
    # 2.1 PKCC (20)
    'SumCyclomatic',
    # 2.2 PKNESTING (4)
    'MaxNesting',

    # ------------------------------------------------
    # 3. Package visibility metrics
    'CountDeclMethodDefault',
    'CountDeclMethodPrivate',
    'CountDeclMethodProtected',
    'CountDeclMethodPublic',
    'PKNOAMM',  # Package number of accessor and mutator methods

    # ------------------------------------------------
    # 4. Package inheritance metrics
    'PKNOI',  # PKNOI: Package number of interfaces
    'PKNOAC',  # PKNOAC: Package number of abstract classes

    # 'CountSemicolon', Eliminated in new version of dataset (version 0.3.0)
]

# Project-level metrics
project_metrics_names_primary = [
    # 1 Size/Count metrics
    # 1.1 Systematic count/size metrics
    'CountLineCode',

    'CountStmt',

    # 1.2 Other Count/Size metrics
    'NumberOfPackages',  # PJNOPK
    'CountDeclFile',  # PJNOFL
    'CountDeclClass',  # PJNOCS
    'CountDeclMethod',  # PJNOM
    'PJNOMNAMM',  # PJNOMNAMM

    # 2. Project Complexity
    # 2.1 PJCC (20)
    'SumCyclomatic',

    # 2.2 PJNESTING(4)
    'MaxNesting',
    'Knots',

    # 3 Inheritance metrics
    'PJNOI',  # Project number of interface
    'PJNAC',  # Project number of abstract classes

    # 'CountSemicolon', Eliminated in new version of dataset (version 0.3.0)

]

# -----------------------------------------------
# Extended metrics list (including primary metrics plus systematically generated metrics)
# Class-level metrics (understand + j_code_odor + systematically created - version 0.3.0)
class_ordinary_metrics_names = [
    # 1. Class size/count metrics
    # 1.1. CSLOC (30)
    # 1.1.1-15. CSLOC_All
    'CountLineCode', 'CountLineCodeDecl', 'CountLineCodeExe',
    'AvgLineCode', 'AvgLineCodeDecl', 'AvgLineCodeExe',
    'MaxLineCode', 'MaxLineCodeDecl', 'MaxLineCodeExe',
    'MinLineCode', 'MinLineCodeDecl', 'MinLineCodeExe',
    'SDLineCode', 'SDLineCodeDecl', 'SDLineCodeExe',
    'LogLineCode', 'LogLineCodeDecl', 'LogLineCodeExe',

    # 1.1.15-30. CSLOC_NAMM
    'CountLineCodeNAMM', 'CountLineCodeDeclNAMM', 'CountLineCodeExeNAMM',
    'AvgLineCodeNAMM', 'AvgLineCodeDeclNAMM', 'AvgLineCodeExeNAMM',
    'MaxLineCodeNAMM', 'MaxLineCodeDeclNAMM', 'MaxLineCodeExeNAMM',
    'MinLineCodeNAMM', 'MinLineCodeDeclNAMM', 'MinLineCodeExeNAMM',
    'SDLineCodeNAMM', 'SDLineCodeDeclNAMM', 'SDLineCodeExeNAMM',
    'LogStmt', 'LogStmtDecl', 'LogStmtExe',

    # 1.2. CSNOST (3-->30)
    # 1.2.1-15. CSNOST_All
    'CountStmt', 'CountStmtDecl', 'CountStmtExe',
    'AvgStmt', 'AvgStmtDecl', 'AvgStmtExe',
    'MaxStmt', 'MaxStmtDecl', 'MaxStmtExe',
    'MinStmt', 'MinStmtDecl', 'MinStmtExe',
    'SDStmt', 'SDStmtDecl', 'SDStmtExe',

    # 1.2.16-30. CSNOST_NAMM
    'CountStmtNAMM', 'CountStmtDeclNAMM', 'CountStmtExeNAMM',
    'AvgStmtNAMM', 'AvgStmtDeclNAMM', 'AvgStmtExeNAMM',
    'MaxStmtNAMM', 'MaxStmtDeclNAMM', 'MaxStmtExeNAMM',
    'MinStmtNAMM', 'MinStmtDeclNAMM', 'MinStmtExeNAMM',
    'SDStmtNAMM', 'SDStmtDeclNAMM', 'SDStmtExeNAMM',

    # 1.3. Number of method metrics
    'CountDeclClassMethod',  # CSNOSM
    'CountDeclClassVariable',  # CSNOSA
    'CountDeclInstanceMethod',  # CSNOIM
    'CountDeclInstanceVariable',  # CSNOIA
    'CSNOMNAMM',  # CSNOMNAMM

    # 1.4. CSNOP (10)
    # 1.4.1-5. CSNOP_All
    'SumCSNOP', 'MaxCSNOP', 'MinCSNOP', 'AvgCSNOP', 'SDCSNOP',
    # 1.4.6-10. CSNOP_NAMM
    'SumCSNOPNAMM', 'MaxCSNOPNAMM', 'MinCSNOPNAMM', 'AvgCSNOPNAMM', 'SDCSNOPNAMM',

    # ------------------------------------------------
    # 2. Class complexity metrics
    # 2.1. CSCC(40)
    # 2.1.1-20. CSCC_All
    'SumCyclomatic', 'SumCyclomaticModified', 'SumCyclomaticStrict', 'SumEssential',
    'MaxCyclomatic', 'MaxCyclomaticModified', 'MaxCyclomaticStrict', 'MaxEssential',
    'AvgCyclomatic', 'AvgCyclomaticModified', 'AvgCyclomaticStrict', 'AvgEssential',
    'MinCyclomatic', 'MinCyclomaticModified', 'MinCyclomaticStrict', 'MinEssential',
    'SDCyclomatic', 'SDCyclomaticModified', 'SDCyclomaticStrict', 'SDEssential',
    'LogCyclomatic', 'LogCyclomaticStrict', 'LogCyclomaticModified', 'LogEssential',

    # 2.1.20-40. CSCC_NAMM
    'SumCyclomaticNAMM', 'SumCyclomaticModifiedNAMM', 'SumCyclomaticStrictNAMM', 'SumEssentialNAMM',
    'MaxCyclomaticNAMM', 'MaxCyclomaticModifiedNAMM', 'MaxCyclomaticStrictNAMM', 'MaxEssentialNAMM',
    'AvgCyclomaticNAMM', 'AvgCyclomaticModifiedNAMM', 'AvgCyclomaticStrictNAMM', 'AvgEssentialNAMM',
    'MinCyclomaticNAMM', 'MinCyclomaticModifiedNAMM', 'MinCyclomaticStrictNAMM', 'MinEssentialNAMM',
    'SDCyclomaticNAMM', 'SDCyclomaticModifiedNAMM', 'SDCyclomaticStrictNAMM', 'SDEssentialNAMM',  # Had bug!

    # 2.2. Nesting
    'MaxNesting', 'MinNesting', 'AvgNesting', 'SDNesting',

    # ------------------------------------------------
    # 3. Class cohesion metrics
    'PercentLackOfCohesion',  # LOCM

    # 4. Class coupling metrics
    'CountClassCoupled',  # CBO
    'RFC',  # RFC: Response for a class or # 'NumberOfFunctionCalls',
    'FANIN',  # Fan-in
    'FANOUT',  # Fan-out
    'ATFD',  # Access to foreign data
    'CFNAMM',  # Called foreign not accessor or mutator methods
    'DAC',  # Data Abstraction Coupling or MOA in QMOOD
    'NumberOfMethodCalls',

    # 5. Class visibility metrics
    'CountDeclMethodDefault',  # CSNODM
    'CountDeclMethodPrivate',  # CSNOPM
    'CountDeclMethodProtected',  # CSNOPRM
    'CountDeclMethodPublic',  # CSNOPLM
    'CSNOAMM',
    # NOAMM: Class number of accessor and mutator methods  # Replace with old NOAM which computed only getter methods

    # 6. Inheritance metrics
    'MaxInheritanceTree',  # DIT
    'CountClassDerived',  # NOC
    'CountClassBase',  # NOP for JAVA is 0 or 1
    'NIM',  # NIM: Number of inherited methods
    'NMO',  # NMO: Number of methods overridden
    'NOII',  # NOII: Number of implemented interfaces

    # 'CountDeclMethodAll', 'CountDeclMethod',  # Eliminated metric. Replace with 'NMO' + 'NIM' + '...' (version 0.3.0)

    # New added metric (version 0.3.0, dataset 0.5.0):
    'SumCountPath', 'MinCountPath', 'MaxCountPath', 'AvgCountPath', 'SDCountPath',
    'SumCountPathLog', 'MinCountPathLog', 'MaxCountPathLog', 'AvgCountPathLog', 'SDCountPathLog',
    'SumKnots', 'MinKnots', 'MaxKnots', 'AvgKnots', 'SDKnots',

    'NumberOfClassConstructors',
    'NumberOfDepends',
    'NumberOfDependsBy',
    'NumberOfClassInItsFile',

]

# Lexicon metrics class-level (version 0.3.0)
class_lexicon_metrics_names = [
    'NumberOfTokens', 'NumberOfUniqueTokens',
    'NumberOfIdentifies', 'NumberOfUniqueIdentifiers',
    'NumberOfKeywords', 'NumberOfUniqueKeywords',

    'NumberOfAssignments', 'NumberOfOperatorsWithoutAssignments', 'NumberOfUniqueOperators',

    'NumberOfSemicolons', 'NumberOfDots',

    # New added metric (version 0.3.0, dataset 0.5.0):
    'NumberOfReturnAndPrintStatements',
    'NumberOfConditionalJumpStatements',
    'NumberOfUnConditionalJumpStatements',
    'NumberOfExceptionStatements',
    'NumberOfNewStatements',
    'NumberOfSuperStatements',
]

# Package-level metrics (understand + j_code_odor + systematically created - version 0.3.0)
package_metrics_names = [
    # 1. Package size/count metrics
    # 2.1 PKLOC (15)
    'CountLineCode', 'CountLineCodeDecl', 'CountLineCodeExe',
    'AvgLineCode', 'AvgLineCodeDecl', 'AvgLineCodeExe',
    'MaxLineCode', 'MaxLineCodeDecl', 'MaxLineCodeExe',
    'MinLineCode', 'MinLineCodeDecl', 'MinLineCodeExe',
    'SDLineCode', 'SDLineCodeDecl', 'SDLineCodeExe',

    # 2.2 PKNOS (15)
    'CountStmt', 'CountStmtDecl', 'CountStmtExe',
    'AvgStmt', 'AvgStmtDecl', 'AvgStmtExe',
    'MaxStmt', 'MaxStmtDecl', 'MaxStmtExe',
    'MinStmt', 'MinStmtDecl', 'MinStmtExe',
    'SDStmt', 'SDStmtDecl', 'SDStmtExe',

    # 2.3. Other Size/Count method (understand built-in metrics)
    'CountDeclClassMethod',  # PKNOSM
    'CountDeclClassVariable',  # PKNOSA
    'CountDeclInstanceMethod',  # PKNOIM
    'CountDeclInstanceVariable',  # PKNOIA
    'PKNOMNAMM',  # PKNOMNAMM: Package number of not accessor or mutator methods
    'CountDeclClass',
    'CountDeclFile',

    # ------------------------------------------------
    # 2. Package complexity metrics
    # 2.1 PKCC (20)
    'SumCyclomatic', 'SumCyclomaticModified', 'SumCyclomaticStrict', 'SumEssential',
    'MaxCyclomatic', 'MaxCyclomaticModified', 'MaxCyclomaticStrict', 'MaxEssential',
    'AvgCyclomatic', 'AvgCyclomaticModified', 'AvgCyclomaticStrict', 'AvgEssential',
    'MinCyclomatic', 'MinCyclomaticModified', 'MinCyclomaticStrict', 'MinEssential',
    'SDCyclomatic', 'SDCyclomaticModified', 'SDCyclomaticStrict', 'SDEssential',

    # 2.2 PKNESTING (4)
    'MaxNesting', 'MinNesting', 'AvgNesting', 'SDNesting',

    # ------------------------------------------------
    # 3. Package visibility metrics
    'CountDeclMethodDefault',
    'CountDeclMethodPrivate',
    'CountDeclMethodProtected',
    'CountDeclMethodPublic',
    'PKNOAMM',  # Package number of accessor and mutator methods

    # ------------------------------------------------
    # 4. Package inheritance metrics
    'PKNOI',  # PKNOI: Package number of interfaces
    'PKNOAC',  # PKNOAC: Package number of abstract classes

    # 'CountSemicolon', Eliminated in new version of dataset (version 0.3.0)
]

# Project-level metrics (understand + j_code_odor + systematically created - version 0.3.0)
project_metrics_names = [
    # 1 Size/Count metrics
    # 1.1 Systematic count/size metrics
    'CountLineCode', 'CountLineCodeDecl', 'CountLineCodeExe',
    'AvgLineCode', 'AvgLineCodeDecl', 'AvgLineCodeExe',
    'MaxLineCode', 'MaxLineCodeDecl', 'MaxLineCodeExe',
    'MinLineCode', 'MinLineCodeDecl', 'MinLineCodeExe',
    'SDLineCode', 'SDLineCodeDecl', 'SDLineCodeExe',

    'CountStmt', 'CountStmtDecl', 'CountStmtExe',
    'AvgStmt', 'AvgStmtDecl', 'AvgStmtExe',
    'MaxStmt', 'MaxStmtDecl', 'MaxStmtExe',
    'MinStmt', 'MinStmtDecl', 'MinStmtExe',
    'SDStmt', 'SDStmtDecl', 'SDStmtExe',

    # 1.2 Other Count/Size metrics
    'NumberOfPackages',  # PJNOPK
    'CountDeclFile',  # PJNOFL
    'CountDeclClass',  # PJNOCS
    'CountDeclMethod',  # PJNOM
    'PJNOMNAMM',  # PJNOMNAMM

    # 2. Project Complexity
    # 2.1 PJCC (20)
    'SumCyclomatic', 'SumCyclomaticModified', 'SumCyclomaticStrict', 'SumEssential',
    'MaxCyclomatic', 'MaxCyclomaticModified', 'MaxCyclomaticStrict', 'MaxEssential',
    'AvgCyclomatic', 'AvgCyclomaticModified', 'AvgCyclomaticStrict', 'AvgEssential',
    'MinCyclomatic', 'MinCyclomaticModified', 'MinCyclomaticStrict', 'MinEssential',
    'SDCyclomatic', 'SDCyclomaticModified', 'SDCyclomaticStrict', 'SDEssential',

    # 2.2 PJNESTING(4)
    'MaxNesting', 'AvgNesting', 'MinNesting', 'SDNesting',
    'Knots',

    # 3 Inheritance metrics
    'PJNOI',  # Project number of interface
    'PJNAC',  # Project number of abstract classes

    # 'CountSemicolon', Eliminated in new version of dataset (version 0.3.0)

]

# Top 20 metrics based-on univariate feature selection (DS4)
top20_metrics2 = [
    # Five of this metrics are also available in Table 4.
    # Correlation coefficient between coverageability and source code metrics.
    'CSLOCNAMM', 'CSLOCDECNAMM', 'CSLOCEXENAMM', 'CSLOCNAMMAVG', 'CSLOCDECNAMMAVG', 'CSLOCEXENAMMAVG',
    'CSNOST', 'CSNOSTDEC', 'CSNOSTEXE', 'CSNOSTAVG', 'CSNOSTDECAVG', 'CSNOSTEXEAVG', 'CSNOSTNAMM', 'CSNOSTDECNAMM',
    'CSNOSTNAMMAVG', 'CSNOSTDECNAMMAVG', 'CSNOSM', 'CSNOSA', 'CSNOMNAMM', 'CSNOPNAMM',
]

# Top 20 metrics based-on univariate feature selection (DS4)
top20_metrics = [
    'CSLEX_NumberOfTokens', 'CSLEX_NumberOfUniqueTokens',
    'CSLEX_NumberOfIdentifies',
    'CSLEX_NumberOfUniqueOperators',
    'CSORD_LogLineCode', 'CSORD_LogLineCodeDecl',
    'CSORD_LogStmt', 'CSORD_LogStmtDecl', 'CSORD_LogStmtExe',
    'CSORD_LogCyclomatic', 'CSORD_LogCyclomaticStrict',
    'CSORD_LogCyclomaticModified', 'CSORD_LogEssential',
    'CSORD_CountClassCoupled', 'CSORD_ATFD'
]

# print number of all metrics in dataset version 0.3.0
# cs_metrics = len(class_ordinary_metrics_names) + len(class_lexicon_metrics_names)
# pk_metrics = len(package_metrics_names)
# pj_metric = len(project_metrics_names)
# all_metrics = cs_metrics + pk_metrics + pj_metric

# print('version 0.3.0')
# print('Number of class metrics:', cs_metrics,  # 151
#       '\nNumber of package metric:', pk_metrics,  # 68
#       '\nNumber of project metrics:', pj_metric,  # 62 ---> 61 in paper
#       '\nNumber of all metrics:', all_metrics)  # 281

# number of metric in version 0.2.0: 89
