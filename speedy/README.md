![version](https://img.shields.io/badge/version-1.0.0-green)

# Speedy module

Thanks to Speedy Antlr Tool, CodART is now using C++ in the backend to parse JAVA source codes. 
To use the speedy module, named `java9speedy` first, you must build and install `java9speedy` module using:

`python setup.py install` with the right privileges.

On windows  >= MVC++11 is required.


## Parse tree creation time

For the `/grammars/Test.java` the following parsing times are observed on a Windows machine with Intel CORE i7:

![ANTLR Python and C++](../docs/figs/parsetime/antlr_python_and_cpp.png)

![ANTLR Java](../docs/figs/parsetime/antlr_java.png)

![ANTLR Plugin for Intellij IDE](../docs/figs/parsetime/antlr_intellij-plugin-v4.png)

Please open an issue in case of any problem.
Thanks, Morteza