import subprocess
import os
from gorgeous.models.SimModelUse import SimilarityClassLevelModel, SimilarityMethodLevelModel


def git_restore(project_dir):
    """
    This function returns a git supported project back to the initial commit
    Args:
        project_dir (str): The absolute path of project's directory.
    Returns:
        None
    """
    assert os.path.isdir(project_dir)
    print("TEST PATH : ", os.path.join(project_dir, ".git"))
    assert os.path.isdir(os.path.join(project_dir, ".git"))
    subprocess.Popen(
        ["git", "restore", "."], cwd=project_dir, stdout=open(os.devnull, "wb")
    ).wait()
    subprocess.Popen(
        ["git", "clean", "-f", "-d"], cwd=project_dir, stdout=open(os.devnull, "wb")
    ).wait()


def getAttrOfActorListClassLevel(acrot_list: list = None) -> object:
    """
    mine data from actor list and init class level object to use  in similarity
    :param acrot_list:
    :return:
    """
    list_of_refactoring = []
    list_of_source = []
    list_of_target = []
    ec = "ExtractClass"
    mm = "MoveMethod"
    pu = "PushUpMethod"
    pd = "PullDownMethod"
    simClass = SimilarityClassLevelModel()
    for item in acrot_list:
        obj = item["obj"]
        if obj.refactoring.find("ERROR") != -1:
            if obj.refactoring == ec:
                list_of_refactoring.append("EC")
                list_of_source.append(obj.source)
                list_of_target.append(obj.target)
                simClass.ec = simClass.ec + 1
            elif obj.refactoring == mm:
                list_of_refactoring.append("MM")
                list_of_source.append(obj.source)
                list_of_target.append(obj.target)
                simClass.mm = simClass.mm + 1
            elif obj.refactoring == pu:
                list_of_refactoring.append("PU")
                list_of_source.append(obj.source)
                list_of_target.append(obj.target)
                simClass.pu = simClass.pu + 1
            elif obj.refactoring == pd:
                list_of_refactoring.append("PD")
                list_of_source.append(obj.source)
                list_of_target.append(obj.target)
                simClass.pd = simClass.pd + 1
    simClass.source = list_of_source
    simClass.target = list_of_target
    simClass.refactoring = list_of_refactoring
    return simClass


def getAttrOfActorListMethodLevel(acrot_list: list = None) -> object:
    """
    mine data from actor list and init Method level object to use  in similarity
    :param acrot_list:
    :return:
    """
    pass
