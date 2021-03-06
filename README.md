# CodART

![CodART](docs/figs/logo.png)


Source Code Automated Refactoring Toolkit (CodART) is a research project at [IUST reverse engineering laboratory](http://reverse.iust.ac.ir/).
We have currently focused on automating the [various refactoring operations](https://refactoring.com/catalog/) for Java source codes. The CodART repository is under active development, and it is not a ready-to-use tool. A complete list of refactoring supported by CodART can be found at [CodART refactorings list](https://m-zakeri.github.io/CodART/refactorings_list/).



## Getting started

To start working on CodART you must first read the [CodART white-paper](https://m-zakeri.github.io/CodART).
In addition, a summary of CodART architecture is discussed in the following:

### CodART architecture

The high-level architecture of CodART is shown in Figure 1. The source code consists of several Python packages and directories. We briefly describe each component in CodART. 

![CodART__Architecture](docs/figs/CodART_architecture__v0.1.1.png)

*Figure 1. CodART architecture*


I. `grammars`: This directory contains three ANTLR4 grammars for the Java programming language: 

1.	`Java9_v2.g4`: This grammar was used in the initial version of CodART. The main problem of this grammar is that parsing large source code files is performed very slow due to some decisions used in grammar design. We have switched to the fast grammar `JavaParserLabled.g4`.
      
2.	`JavaLexer.g4`: The lexer of Java fast grammar. This lexer is used for both fast parsers, i.e., `JavaParser.g4` and JavaParserLabeled.
      
3.	`JavaParser.g4`: The original parser of Java fast grammar. This parser is currently used in some refactoring. In the future release, this grammar will be replaced with `JavaPaseredLabled.g4`.
      
4.	`JavaParserLabeled.g4`: This file contains the same `JavaParsar.g4` grammar. The only difference is that the rules with more than one extension are labled with a specific name. The ANTLR parser generator thus generates separate visitor and listener methods for each extension. This grammar facilitates the development of some refactoring. It is the preferred parser in CodART project.


II. `gen`: The `gen` packages contain all generated source code for the parser, lexer, visitor, and listener for different grammars available in the grammars directory. To develop refactorings and code smells, `gen.JavaLabled` package, which contains `JavaParserLabled.g4` generated source code, must be used. The content of this package is generated _automatically_, and therefore it should _not_ be modified _manually_. Modules within this gen package are just for importing and using in other modules.


III. `speedy`: The python implementation for ANTLR is less efficient than Java or C++ implementation. The `speedy` module implements a Java parser with a C++ back-end, improving the efficiency and speed of parsing. It uses speedy-antlr implementation with some minor changes.  The current version of the speedy module use `java9_v2.g4` grammar, which inherently slow as described. To switch to C++ back-end, first, the speedy module must be installed on the client system. It requires a C++ compiler. We _recommended_ to CodART developers using the Python back-end as switching to C++ back-end would be done transparently in the future release. The Python back-end saves debugging and developing time.


IV. `refactorings`: The `refactorings` package is the main package in the CodART project and contains numerous Python modules that form the kernel functionalities of CodART. Each module implements the automation of one refactoring operation according to standard practices. The modules may include several classes which _inherit_ from ANTLR listeners. Sub-packages in this module contain refactorings, which are in an early step of development or deprecated version of an existing refactoring. This package is under active development and testing. The module in the root packages can be used for testing purposes.


V. `refactoring_design_patters`: The refactoring_design_pattern packages contain modules that implement refactoring to a specific design pattern automatically. 


VI. `smells`: The smell package implements the automatic detection of software code and design smells relevant to the refactoring operation supported by CodART. Each smell corresponds to one or more refactoring in the refactoring package.


VII. `metrics`: The metrics packages contain several modules that implement the computation of the most well-known source code metrics. These metrics used to detect code smells and measuring the quality of software in terms of quality attributed. 


VIII. `tests`: The test directory contains individual test data and test cases that are used for developing specific refactorings. Typically, each test case is a single Java file that contains one or more Java classes.


IX. `benchmark_projects`: This directory contains several open-source Java projects formerly used in automated refactoring researches by many researchers. Once the implementation of refactoring is completed, it will be executed and tested on all projects in this benchmark to ensure the generalization of functionality proposed by the implementation.  

X. **Other packages**: The information of other packages will be announced in the future.  
 


### Read more

 * [CodART official website and documentation](https://m-zakeri.github.io/CodART)
 * [CodART refactoring list](https://m-zakeri.github.io/CodART/refactorings_list/)
 * [CodART code smells list](https://m-zakeri.github.io/CodART/code_smells_list/)
 * [CodART benchmark projects](https://m-zakeri.github.io/CodART/benchmarks/)
 * [CodART team members and contributors](https://m-zakeri.github.io/CodART/about/)
 * [CodART issues](https://github.com/m-zakeri/CodART/issues)
   


 * [Catalog of refactorings by Martin Fowler](https://refactoring.com/catalog/)
 * [Refactoring.Guru](https://refactoring.guru/)

Follow us!