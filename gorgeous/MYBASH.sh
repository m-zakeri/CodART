virtualenv venv
source venv/bin/activate
pip3 install -r requirements.txt
cd Resources/Grammars
antlr4 -Dlanguage=Python3 -visitor JavaLexer.g4 -o ../../gen/JavaLexer
antlr4 -Dlanguage=Python3 -visitor JavaLexer.g4 -o ../../gen/java
antlr4 -Dlanguage=Python3 -visitor JavaLexer.g4 -o ../../gen/java9
antlr4 -Dlanguage=Python3 -visitor JavaParserLabeled.g4 -lib ../../gen/javaLabeled -o ../../gen/javaLabeled
antlr4 -Dlanguage=Python3 -visitor Java9_v2.g4 -lib ../../gen/java9 -o ../../gen/java9
antlr4 -Dlanguage=Python3 -visitor JavaParser.g4 -lib ../../gen/java -o ../../gen/java

