
from gorgeous.dependencies.DatasetsProvider import DataSetsProvider
from gorgeous.dependencies.ClsUDBMetrics import ClsUDB_Metrics
from gorgeous.dependencies.GenBase import GenBase
import os

os.add_dll_directory("C:\\Program Files\\SciTools\\bin\\pc-win64")


ds_instance = DataSetsProvider()
cu_instance = ClsUDB_Metrics()


def state(arg):
    if arg == 0:
        # GENBASE
        print("RUN GENETIC ALG \n")
        a = GenBase()
        a.run()
        return 1
    elif arg == 1:
        # clone projects
        print("CLONE PROJECTS\n")
        try:
            ds_instance.get_datasets()
        except Exception as e:
            print("ERROR : ", e)
        return 1
    elif arg == 2:
        print("EXIT\n")
        return -1
    else:
        print("WRONG INPUT TRY AGAIN !!!\n")
        return 1


def main():
    while True:
        inp = int(
            input(
                "INTER NUMBER TO DO : \n 0 - RUN GORGEOUS \n 1 - CLONE PROJECTS \n 2 - EXIT \n\n =====>> \t"
            )
        )
        o = state(inp)
        if o == -1:
            break


if __name__ == "__main__":
    main()


# create .und db and refactoring .json file
# for item in ds_instance.get_resource_path():
#     cu_instance.create_understand_database_from_project(root_path=item)
#     ds_instance.refactoringminer(git_repo_folder=item)


# METHOD METRICS
# for item in ds_instance.get_resource_path():
#     cu_instance.get_metrics_of_each_function(my_path=item)

# CLASS METRICS
# for item in ds_instance.get_resource_path():
#     cu_instance.get_metrics_of_each_class(my_path=item)

# DEP CLASSES
# for item in ds_instance.get_resource_path():
#     cu_instance.get_dep_of_each_class(db_path=item, csv_path="Resources/csv_files/")
