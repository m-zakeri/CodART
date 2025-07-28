# ANTLR advanced tutorials


By: Morteza Zakeri

Last update: April 30, 2022



## Compiler background

We first define some terms used in compiler literature when analyzing the program based on the ANTLR vocabulary.

* **Compiler pass.**
Each time that the `walk` method of `ParseTreeWalker` class is called, it visits all nodes of the parse tree. In compiler literature, we called this process a pass. The ANTLR pass can be annotated with listener classes to perform specific analysis or transformation. An analysis pass refers to the pass in which some information is obtained from the source code, but the source code is not changed, or no new code is generated. A transformation pass refers to the pass in which the program source code is modified or new codes are generated. As we discussed in the next sections, refactoring automation consists of both the analysis and transformation passes.


* **Single v.s. multiple pass.** 
Often to perform specific analyses or transformations, the program should be visited multiple times. Indeed, such tasks required multiple passes. For instance, if a class attribute is defined after it is used in a method, which is possible in Java programming language, to find the definition of the field and then modify its usage, we should visit the program twice. The reason is that the program tokens are read from left to right, and then when traversing the parse tree, the node only is visited once in the order they appear in the program text. For a given task, if we visit a node and require the information obtained from the next nodes, we cannot complete the task in one pass. In such a case, a pass is required to obtain the necessary information from the next nodes, and another pass is required to use this information for the current node. Most refactoring operations we described in this chapter require multiple passes to complete the refactoring process. For each pass, we develop a separate listener class and pass it to `ParseTreeWalker` class.

