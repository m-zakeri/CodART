# Core refactoring development

The following proposal was initially prepared for the IUST Compiler and Advanced compiler courses in Fall 2020. 

Students must form groups of up to three persons, and each group must implement several refactoring operations. The exact list of refactoring will be assigned to each group subsequently. The refactoring operations in Table 1 may update during the semester. 

As an example of refactoring automation, we have implemented the EncapsulateField refactoring, illustrated in Figure 1. A naïve implementation is available on the project official Github page at [https://m-zakeri.github.io/CodART](https://m-zakeri.github.io/CodART). In addition, 26 refactoring operations in Table 1 have been implemented by [MultiRefactor](https://github.com/mmohan01/MultiRefactor) [7] based on [RECODER](http://sourceforge.net/projects/recoder), three of them have been implemented by JDeodrant [8], and other operations have been automated in  [3], [6]. RECODER extracts a model of the code that can be used to analyze and modify the code before the changes are applied and written to file. The tool takes Java source code as input and will output the modified source code to a specified folder. The input must be fully compilable and must be accompanied by any necessary library files as compressed jar files.


### Grading policy for BSc students
Table 4 shows the grading policy for the BSc students. It may change in the future. 

*Table 4. grading policy for BSc students*

|     Activity                                                |     Score   (100)          |
|-----------------------------------------------------------|----------------------------|
|     Refactoring   operations implementation (moderate level)              |     50                     |
|     Evaluation   of the tool on the benchmark projects    |     30                     |
|     Documentations                                        |     20                     |
|     Search-based   refactoring recommendation             |     30+   (extra bonus)    |


### Grading policy for MSc students
Table 5 shows the grading policy for the MSc students. It may change in the future. 

*Table 5. grading policy for MSc students*


|     Activity                                                |     Score   (100)          |
|-----------------------------------------------------------|----------------------------|
|     Refactoring   operations implementation (advanced level)              |     40                     |
|     Search-based   refactoring recommendation             |     30                     |
|     Evaluation   of the tool on the benchmark projects    |     20                     |
|     Documentations                                        |     10                     |
|     Improving   the state-of-the-arts papers              |     30+   (extra bonus)    |


To follow project's phases, refer to our next proposal: Core code smell development.

