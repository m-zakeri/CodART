from git import Repo, RemoteProgress
import logging
from os import getcwd
from os import system
import subprocess
from dotenv import dotenv_values


class Progress(RemoteProgress):
    def line_dropped(self, line):
        print(line)

    def update(self, *args):
        print(self._cur_line)


class DataSetsProvider:
    def __init__(self):
        logging.basicConfig(level=logging.INFO)
        # self.__extractor = URLExtract()
        self.__gitUrlList = open(file="Resources/urls_dataset.txt").readlines()
        self.__ResourcePath = dotenv_values().get("RESOURCES_PATH").split(" ")

    def get_datasets(self):
        # clone git rpoes in urls_dataset.txt and detch it to the true sha1 commit
        print(self.__gitUrlList)
        for item in self.__gitUrlList:
            print(item)
            try:
                Repo.clone_from(
                    url=item.split(" ")[0],
                    to_path="Resources/projects/" + item.split(" ")[2],
                    progress=Progress(),
                ).head.reset(commit=item.split(" ")[1])
            except Exception as e:
                print("ERROR : ", e)

    def get_resource_path(self):
        print(self.__ResourcePath)
        # return dir_path of projects
        return [direction.replace("\n", "") for direction in self.__ResourcePath]

    def refactoringminer(self, git_repo_folder):
        output = subprocess.check_output(
            ["git", "rev-list", "master"],
            cwd=getcwd() + f"/Resources/{git_repo_folder}",
        )
        mylist = output.decode("ascii").split("\n")
        mylist.pop()
        # RefactoringMiner -bc <git-repo-folder> <start-commit-sha1> <end-commit-sha1> -json <path-to-json-file>
        if len(mylist) >= 80:
            system(
                "refactoringminer -bc {0} {1} {2} -json {3}".format(
                    getcwd() + f"/Resources/{git_repo_folder}",
                    mylist[79],
                    mylist[39],
                    getcwd() + f"gorgeous/Resources/refactoring_files/{git_repo_folder}.json",
                )
            )
        else:
            print("warning : commit less than 80 !!")
