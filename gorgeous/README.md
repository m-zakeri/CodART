# Generation of refactoring algorithms by grammatical evolution

******************************************
### Requirements : 
- install Understand from : https://scitools.com/features/
- run script "bash MYBASH.sh" in terminal to install Prerequisites
- init git ssh on github
### Prerequisites : 
###### create .env file in root dir and add these entities to it :
  - LIST_METRICS_CLASS = "CountClassBase CountClassCoupled CountClassDerived CountDeclMethod CountDeclMethodAll MaxInheritanceTree CountLineCode CountLineComment"
  - LIST_METRICS_METHOD = "CountLineCode CountLineComment"
  - LIST_METRICS_QM = ""
  - RESOURCES_PATH = "Activity"
  - MODE = "2"
  - MODE_SIM = "1" 
###### add projects git address and sha1 commit and name and version like following in the Resources/urls_dataset.txt address in project root directory 
-   git@github.com:Activiti/Activiti.git aba6f941f8f8d42f767c3ea0ae65ddc18b7f1e8b Activity version:5.17.0
### Run project :
  - run understand
  - python3 main.py