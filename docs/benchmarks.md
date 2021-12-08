# CodART benchmarks and testbed
To ensure CodART works properly, we are running it on many real-life software projects.
Refactorings are applied to the software systems listed in Table 3. Benchmark projects may update and extend in the future. For the time being, we use a set of well-known open-source Java projects that have been intensely studied in previous works. We have also added two new Java software programs, WEKA and ANTLR, to examine the versatility of CodART performance on real-life software projects. 


*Table 3. Software systems used as benchmarks in CodeART*

|     System            	|     Release                     	|     Previous releases    	|     Domain                                                       	|     Reference        	|
|-----------------------	|---------------------------------	|--------------------------	|------------------------------------------------------------------	|----------------------	|
|     [Xerces-J](https://github.com/apache/xerces2-j)            |     v2.7.0                        |        --          |   software packages for parsing XML                             |   [3], [6]
|     [Azureus](https://github.com/vuze/vuze-remote-for-android)             |     v2.3.0.6                      |      --                     |   Java BitTorrent client for handling multiple torrents         |     [3]             
|     [ArgoUML](https://github.com/argouml-tigris-org/argouml)             |     v0.26 and v0.3                |        --                   |   UML tool for object-oriented design                          	|     [3]               
|     [Apache Ant](https://github.com/apache/ant)         	|     v1.5.0 and v1.7.0           	|                 --         	|   Java build tool and library                                  	|     [3]              
|     [GanttProject](https://github.com/bardsoftware/ganttproject)      	|     v1.10.2 and v1.11.1         	|    --                      	|   project management                                            |     [3], [6], [5]    
|     [JHotDraw](https://github.com/wumpz/jhotdraw)          	|     v6.1 and v6.0b1 and v5.3    	|               --           	|   graphics tool                                                 |     [6], [5], [4]    
|     [JFreeChart](https://github.com/jfree/jfreechart)        	|     v1.0.9                      	|              --            	|   chart tool                                                    |     [6]              
|     [Beaver](https://github.com/svn2github/beaver-parser-generator-v09)            	|     v0.9.11 and v0.9.8          	|       --                   	|   parser generator                                              |     [5], [4]         
|     [Apache XML-RPC](https://ws.apache.org/xmlrpc/)    	|     v3.1.1                      	|           --               	|   B2B communications                                            |     [5], [4]         
|     [JRDF](http://jrdf.sourceforge.net/index.html)              	|     v0.3.4.3                    	|      --                    	|   semantic web (resource management)                            |     [5]              
|     [XOM](https://github.com/elharo/xom)               	|     v1.2.1                      	|             --             	|   XML tool                                                      |     [5]              
|     [JSON](https://github.com/stleary/JSON-java)              	|     v1.1                        	|      --                    	|   software packages for parsing JSON                            |     [4]              
|     [JFlex](https://github.com/jflex-de/jflex)            	  |     v1.4.1                      	|      --                    	|   lexical analyzer generator                                    |     [4]              
|     [Mango](https://github.com/jfaster/mango)             	|     v2.0.1                           	|      --                   	|              --                                                   |     [4]              
|     [Weka](https://github.com/Waikato/weka-3.8)              	|     v3.8                	|              --            	|   data mining tool                                              |     New              
|     [ANTLR](https://github.com/antlr/antlr4)             	|     v4.8.0                      	|             --             	|   parser generator tool                                         |     New              



## New projects

To be announced. 

## References

[3]	M. W. Mkaouer, M. Kessentini, S. Bechikh, M. Ó Cinnéide, and K. Deb, “On the use of many quality attributes for software refactoring: a many-objective search-based software engineering approach,” Empir. Softw. Eng., vol. 21, no. 6, pp. 2503–2545, Dec. 2016.

[4]	M. Mohan, D. Greer, and P. McMullan, “Technical debt reduction using search based automated refactoring,” J. Syst. Softw., vol. 120, pp. 183–194, Oct. 2016.

[5]	M. Mohan and D. Greer, “Using a many-objective approach to investigate automated refactoring,” Inf. Softw. Technol., vol. 112, pp. 83–101, Aug. 2019.

[6]	W. Mkaouer et al., “Many-Objective Software Remodularization Using NSGA-III,” ACM Trans. Softw. Eng. Methodol., vol. 24, no. 3, pp. 1–45, May 2015. 