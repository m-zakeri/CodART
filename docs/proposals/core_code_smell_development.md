# Core code smell development

The following proposal has been initially prepared for the **IUST Compiler** and **Advanced Software Engineering** courses in **Winter and Spring 2021**.

Note: Before reading this proposal ensure that you have read and understood the [CodART white-paper](../index.md).

Students may form groups of up to **three** persons. Each group must develop mechanisms for a subset of code smells listed in [Table 2](../code_smells_list.md). The exact list of code smells will be assigned to each group subsequently. The refactoring operations in [Table 1](../refactorings_list.md) and code smells in [Table 2](../code_smells_list.md) may update during the semester. 

To facilitate and organized the development process, this proposal defines the project in various phases. The project is divided into three separate phases.

In the first phase, students must read about refactoring and code smells and understand the current state of the CodART completely. As a practice, they are asked to fix the existing issues on the project repository about refactoring operations developed in the first proposal.

In the second phase, each group is asked to develop algorithms to automatically detect one or more code smells in a given Java project using [ANTLR tool](https://www.antlr.org/) and other compiler techniques. TA team frequently helps the students at this phase to develop their algorithms. 

In the third phase, each group is asked to connect the code smells detection scripts to the corresponding refactoring and automate the overall quality improvement process. 


### Grading policy for BSc students
Table 6 shows the grading policy for the BSc students. It may change in the future. 

*Table 6. grading policy for BSc students*


 |     Activity                                                                       |     Score   (100)          |
|-----------------------------------------------------------------------------------|----------------------------|
|     Understanding   the CodART project and Fix the existing issues                |     30                     |
|     Implementing   smell detection approaches                                     |     40                     |
|     Connecting   code smells to refactoring and harnessing the overall process    |     20                     |
|     Documenting   the new source codes and pushing them to GitHub                    |     10                     |
|     Testing   project on all projects available in CodART benchmarks              |     20+   (extra bonus)    |


### Grading policy for MSc students
Table 7 shows the grading policy for the MSc students. It may change in the future. 

*Table 7. grading policy for MSc students*

|     Activity                                                              |     Score   (100)          |
|-------------------------------------------------------------------------|----------------------------|
|     Understanding   the paper and presenting it                         |     20                     |
|     Implementing   the paper                                            |     30                     |
|     Evaluating   the implementation                                     |     30                     |
|     Documenting   the project                                           |     20                     |
|     Testing   project on all projects available in CodART benchmarks    |     20+   (extra bonus)    |


To follow project's future phases, meet our next proposal: Core search-based development.

