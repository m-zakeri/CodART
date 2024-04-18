## Overview
The goal of this project is to implement a software to mimic the functionality of Contain, ContainIn, Extend, and ExtendBy queries in the [SciTools Understand](https://www.scitools.com/) software analysis toolkit. I used ANTLRv4 in C# runtime along with SQLite databse to save the results. To find more information about Understand, the database schemas and the terminology visit [here](https://m-zakeri.github.io/OpenUnderstand/).

## What I have done
- Used ANTLRv4 java grammars and its C# library to find entities in java files.
- Detected Classes, Enums, Interfaces, and Annotation Types that are defined in a package.
- Used SQLite and Dapper ORM to save the extracted entities and references.
