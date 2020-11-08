/*
 * [The "BSD license"]
 *  Copyright (c) 2014 Terence Parr
 *  Copyright (c) 2014 Sam Harwell
 *  Copyright (c) 2017 Chan Chung Kwong
 *  All rights reserved.
 *
 *  Redistribution and use in source and binary forms, with or without
 *  modification, are permitted provided that the following conditions
 *  are met:
 *
 *  1. Redistributions of source code must retain the above copyright
 *     notice, this list of conditions and the following disclaimer.
 *  2. Redistributions in binary form must reproduce the above copyright
 *     notice, this list of conditions and the following disclaimer in the
 *     documentation and/or other materials provided with the distribution.
 *  3. The name of the author may not be used to endorse or promote products
 *     derived from this software without specific prior written permission.
 *
 *  THIS SOFTWARE IS PROVIDED BY THE AUTHOR ``AS IS'' AND ANY EXPRESS OR
 *  IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES
 *  OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED.
 *  IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR ANY DIRECT, INDIRECT,
 *  INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT
 *  NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
 *  DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
 *  THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
 *  (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF
 *  THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
 */

/**
 * A Java 8 grammar for ANTLR 4 derived from the Java Language Specification
 * chapter 19.
 *
 * NOTE: This grammar results in a generated parser that is much slower
 *       than the Java 7 grammar in the grammars-v4/java directory. This
 *     one is, however, extremely close to the spec.
 *
 * You can test with
 *
 *  $ antlr4 Java9.g4
 *  $ javac *.java
 *  $ grun Java9 compilationUnit *.java
 *
 * Or,
~/antlr/code/grammars-v4/java9 $ java Test .
/Users/parrt/antlr/code/grammars-v4/java9/./Java9BaseListener.java
/Users/parrt/antlr/code/grammars-v4/java9/./Java9Lexer.java
/Users/parrt/antlr/code/grammars-v4/java9/./Java9Listener.java
/Users/parrt/antlr/code/grammars-v4/java9/./Java9Parser.java
/Users/parrt/antlr/code/grammars-v4/java9/./Test.java
Total lexer+parser time 30844ms.
~/antlr/code/grammars-v4/java9 $ java Test examples/module-info.java
/home/kwong/projects/grammars-v4/java9/examples/module-info.java
Total lexer+parser time 914ms.
~/antlr/code/grammars-v4/java9 $ java Test examples/TryWithResourceDemo.java
/home/kwong/projects/grammars-v4/java9/examples/TryWithResourceDemo.java
Total lexer+parser time 3634ms.
~/antlr/code/grammars-v4/java9 $ java Test examples/helloworld.java
/home/kwong/projects/grammars-v4/java9/examples/helloworld.java
Total lexer+parser time 2497ms.

 */

 /*
@revised by: Morteza Zakeri, (http://webpages.iust.ac.ir/morteza_zakeri/)
@date: 20201107

-Changelog:
-- v4.2
--- Add name for grammar rules extensions
--- Remove Java attributes from grammar file.

 */

grammar Java9_v2;

/*
 * Productions from §3 (Lexical Structure)
 */

literal
	:	IntegerLiteral
	|	FloatingPointLiteral
	|	BooleanLiteral
	|	CharacterLiteral
	|	StringLiteral
	|	NullLiteral
	;

/*
 * Productions from §4 (Types, Values, and Variables)
 */

primitiveType
	:	annotation* numericType #primitiveType1
	|	annotation* 'boolean' #primitiveType2
	;

numericType
	:	integralType #numericType1
	|	floatingPointType #numericType2
	;

integralType
	:	'byte'
	|	'short'
	|	'int'
	|	'long'
	|	'char'
	;

floatingPointType
	:	'float'
	|	'double'
	;

referenceType
	:	classOrInterfaceType #referenceType1
	|	typeVariable #referenceType2
	|	arrayType #referenceType3
	;

/*classOrInterfaceType
	:	classType
	|	interfaceType
	;
*/
classOrInterfaceType
	:	(	classType_lfno_classOrInterfaceType
		|	interfaceType_lfno_classOrInterfaceType
		)
		(	classType_lf_classOrInterfaceType
		|	interfaceType_lf_classOrInterfaceType
		)*
	;

classType
	:	annotation* identifier typeArguments? #classType1
	|	classOrInterfaceType '.' annotation* identifier typeArguments? #classType2
	;

classType_lf_classOrInterfaceType
	:	'.' annotation* identifier typeArguments?
	;

classType_lfno_classOrInterfaceType
	:	annotation* identifier typeArguments?
	;

interfaceType
	:	classType
	;

interfaceType_lf_classOrInterfaceType
	:	classType_lf_classOrInterfaceType
	;

interfaceType_lfno_classOrInterfaceType
	:	classType_lfno_classOrInterfaceType
	;

typeVariable
	:	annotation* identifier
	;

arrayType
	:	primitiveType dims #arrayType1
	|	classOrInterfaceType dims #arrayType2
	|	typeVariable dims #arrayTyp3
	;

dims
	:	annotation* '[' ']' (annotation* '[' ']')*
	;

typeParameter
	:	typeParameterModifier* identifier typeBound?
	;

typeParameterModifier
	:	annotation
	;

typeBound
	:	'extends' typeVariable #typeBound1
	|	'extends' classOrInterfaceType additionalBound* #typeBound2
	;

additionalBound
	:	'&' interfaceType
	;

typeArguments
	:	'<' typeArgumentList '>'
	;

typeArgumentList
	:	typeArgument (',' typeArgument)*
	;

typeArgument
	:	referenceType #typeArgument1
	|	wildcard #typeArgument2
	;

wildcard
	:	annotation* '?' wildcardBounds?
	;

wildcardBounds
	:	'extends' referenceType  #wildcardBounds1
	|	'super' referenceType #wildcardBound2
	;

/*
 * Productions from §6 (Names)
 */

moduleName
	:	identifier #moduleName1
	|	moduleName '.' identifier #moduleName2
	;

packageName
	:	identifier #packageName1
	|	packageName '.' identifier #packageName2
	;

typeName
	:	identifier #typeName1
	|	packageOrTypeName '.' identifier #typeName2
	;

packageOrTypeName
	:	identifier #packageOrTypeName1
	|	packageOrTypeName '.' identifier #packageOrTypeName2
	;

expressionName
	:	identifier #expressionName1
	|	ambiguousName '.' identifier #expressionName2
	;

methodName
	:	identifier
	;

ambiguousName
	:	identifier #ambiguousName1
	|	ambiguousName '.' identifier #ambiguousName2
	;

/*
 * Productions from §7 (Packages)
 */

/*
Grammar head:
compilationUnit
*/

compilationUnit
	:	ordinaryCompilation #compilationUnit1
	|	modularCompilation #compilationUnit2
	;

ordinaryCompilation
	:	packageDeclaration? importDeclaration* typeDeclaration* EOF
	;

modularCompilation
	:	importDeclaration* moduleDeclaration
	;

packageDeclaration
	:	packageModifier* 'package' packageName ';'
	;

packageModifier
	:	annotation
	;

importDeclaration
	:	singleTypeImportDeclaration #importDeclaration1
	|	typeImportOnDemandDeclaration #importDeclaration2
	|	singleStaticImportDeclaration #importDeclaration3
	|	staticImportOnDemandDeclaration #importDeclaration4
	;

singleTypeImportDeclaration
	:	'import' typeName ';'
	;

typeImportOnDemandDeclaration
	:	'import' packageOrTypeName '.' '*' ';'
	;

singleStaticImportDeclaration
	:	'import' 'static' typeName '.' identifier ';'
	;

staticImportOnDemandDeclaration
	:	'import' 'static' typeName '.' '*' ';'
	;

typeDeclaration
	:	classDeclaration #typeDeclaration1
	|	interfaceDeclaration #typeDeclaration2
	|	';' #typeDeclaration3
	;

moduleDeclaration
	:	annotation* 'open'? 'module' moduleName '{' moduleDirective* '}'
	;

moduleDirective
	:	'requires' requiresModifier* moduleName ';' #moduleDirective1
	|	'exports' packageName ('to' moduleName (',' moduleName)*)? ';' #moduleDirective2
	|	'opens' packageName ('to' moduleName (',' moduleName)*)? ';' #moduleDirectiv3
	|	'uses' typeName ';' #moduleDirective4
	|	'provides' typeName 'with' typeName (',' typeName)* ';' #moduleDirective5
	;

requiresModifier
	:	'transitive'
	|	'static'
	;

/*
 * Productions from §8 (Classes)
 */

classDeclaration
	:	normalClassDeclaration #classDeclaration1
	|	enumDeclaration #classDeclaration2
	;

normalClassDeclaration
	:	classModifier* 'class' identifier typeParameters? superclass? superinterfaces? classBody
	;

classModifier
	:	annotation
	|	'public'
	|	'protected'
	|	'private'
	|	'abstract'
	|	'static'
	|	'final'
	|	'strictfp'
	;

typeParameters
	:	'<' typeParameterList '>'
	;

typeParameterList
	:	typeParameter (',' typeParameter)*
	;

superclass
	:	'extends' classType
	;

superinterfaces
	:	'implements' interfaceTypeList
	;

interfaceTypeList
	:	interfaceType (',' interfaceType)*
	;

classBody
	:	'{' classBodyDeclaration* '}'
	;

classBodyDeclaration
	:	classMemberDeclaration #classBodyDeclaration1
	|	instanceInitializer #classBodyDeclaration2
	|	staticInitializer #classBodyDeclaration3
	|	constructorDeclaration #classBodyDeclaration4
	;

classMemberDeclaration
	:	fieldDeclaration #classMemberDeclaration1
	|	methodDeclaration #classMemberDeclaration2
	|	classDeclaration #classMemberDeclaration3
	|	interfaceDeclaration #classMemberDeclaration4
	|	';' #classMemberDeclaration5
	;

fieldDeclaration
	:	fieldModifier* unannType variableDeclaratorList ';'
	;

fieldModifier
	:	annotation
	|	'public'
	|	'protected'
	|	'private'
	|	'static'
	|	'final'
	|	'transient'
	|	'volatile'
	;

variableDeclaratorList
	:	variableDeclarator (',' variableDeclarator)*
	;

variableDeclarator
	:	variableDeclaratorId ('=' variableInitializer)?
	;

variableDeclaratorId
	:	identifier dims?
	;

variableInitializer
	:	expression #variableInitializer1
	|	arrayInitializer #variableInitializer2
	;

unannType
	:	unannPrimitiveType #unannType1
	|	unannReferenceType #unannType2
	;

unannPrimitiveType
	:	numericType #unannPrimitiveType1
	|	'boolean' # unannPrimitiveType2
	;

unannReferenceType
	:	unannClassOrInterfaceType #unannReferenceType1
	|	unannTypeVariable #unannReferenceType2
	|	unannArrayType #unannReferenceType3
	;

/*unannClassOrInterfaceType
	:	unannClassType
	|	unannInterfaceType
	;
*/

unannClassOrInterfaceType
	:	(	unannClassType_lfno_unannClassOrInterfaceType
		|	unannInterfaceType_lfno_unannClassOrInterfaceType
		)
		(	unannClassType_lf_unannClassOrInterfaceType
		|	unannInterfaceType_lf_unannClassOrInterfaceType
		)*
	;

unannClassType
	:	identifier typeArguments? #unannClassType1
	|	unannClassOrInterfaceType '.' annotation* identifier typeArguments? #unannClassType2
	;

unannClassType_lf_unannClassOrInterfaceType
	:	'.' annotation* identifier typeArguments?
	;

unannClassType_lfno_unannClassOrInterfaceType
	:	identifier typeArguments?
	;

unannInterfaceType
	:	unannClassType
	;

unannInterfaceType_lf_unannClassOrInterfaceType
	:	unannClassType_lf_unannClassOrInterfaceType
	;

unannInterfaceType_lfno_unannClassOrInterfaceType
	:	unannClassType_lfno_unannClassOrInterfaceType
	;

unannTypeVariable
	:	identifier
	;

unannArrayType
	:	unannPrimitiveType dims #unannArrayType1
	|	unannClassOrInterfaceType dims #unannArrayType2
	|	unannTypeVariable dims #unannArrayTyp3
	;

methodDeclaration
	:	methodModifier* methodHeader methodBody
	;

methodModifier
	:	annotation
	|	'public'
	|	'protected'
	|	'private'
	|	'abstract'
	|	'static'
	|	'final'
	|	'synchronized'
	|	'native'
	|	'strictfp'
	;

methodHeader
	:	result methodDeclarator throws_?
	|	typeParameters annotation* result methodDeclarator throws_?
	;

result
	:	unannType
	|	'void'
	;

methodDeclarator
	:	identifier '(' formalParameterList? ')' dims?
	;

formalParameterList
	:	formalParameters ',' lastFormalParameter #formalParameterList1
	|	lastFormalParameter #formalParameterList2
	|	receiverParameter #formalParameterList3
	;

formalParameters
	:	formalParameter (',' formalParameter)* #formalParameters1
	|	receiverParameter (',' formalParameter)* #formalParameters2
	;

formalParameter
	:	variableModifier* unannType variableDeclaratorId
	;

variableModifier
	:	annotation
	|	'final'
	;

lastFormalParameter
	:	variableModifier* unannType annotation* '...' variableDeclaratorId #lastFormalParameter1
	|	formalParameter #lastFormalParameter2
	;

receiverParameter
	:	annotation* unannType (identifier '.')? 'this'
	;

throws_
	:	'throws' exceptionTypeList
	;

exceptionTypeList
	:	exceptionType (',' exceptionType)*
	;

exceptionType
	:	classType #exceptionType1
	|	typeVariable #exceptionType2
	;

methodBody
	:	block
	|	';'
	;

instanceInitializer
	:	block
	;

staticInitializer
	:	'static' block
	;

constructorDeclaration
	:	constructorModifier* constructorDeclarator throws_? constructorBody
	;

constructorModifier
	:	annotation
	|	'public'
	|	'protected'
	|	'private'
	;

constructorDeclarator
	:	typeParameters? simpleTypeName '(' formalParameterList? ')'
	;

simpleTypeName
	:	identifier
	;

constructorBody
	:	'{' explicitConstructorInvocation? blockStatements? '}'
	;

explicitConstructorInvocation
	:	typeArguments? 'this' '(' argumentList? ')' ';' #explicitConstructorInvocation1
	|	typeArguments? 'super' '(' argumentList? ')' ';' #explicitConstructorInvocation2
	|	expressionName '.' typeArguments? 'super' '(' argumentList? ')' ';' #explicitConstructorInvocation3
	|	primary '.' typeArguments? 'super' '(' argumentList? ')' ';' #explicitConstructorInvocation4
	;

enumDeclaration
	:	classModifier* 'enum' identifier superinterfaces? enumBody
	;

enumBody
	:	'{' enumConstantList? ','? enumBodyDeclarations? '}'
	;

enumConstantList
	:	enumConstant (',' enumConstant)*
	;

enumConstant
	:	enumConstantModifier* identifier ('(' argumentList? ')')? classBody?
	;

enumConstantModifier
	:	annotation
	;

enumBodyDeclarations
	:	';' classBodyDeclaration*
	;

/*
 * Productions from §9 (Interfaces)
 */

interfaceDeclaration
	:	normalInterfaceDeclaration #interfaceDeclaration1
	|	annotationTypeDeclaration #interfaceDeclaration2
	;

normalInterfaceDeclaration
	:	interfaceModifier* 'interface' identifier typeParameters? extendsInterfaces? interfaceBody
	;

interfaceModifier
	:	annotation
	|	'public'
	|	'protected'
	|	'private'
	|	'abstract'
	|	'static'
	|	'strictfp'
	;

extendsInterfaces
	:	'extends' interfaceTypeList
	;

interfaceBody
	:	'{' interfaceMemberDeclaration* '}'
	;

interfaceMemberDeclaration
	:	constantDeclaration #interfaceMemberDeclaration1
	|	interfaceMethodDeclaration #interfaceMemberDeclaration2
	|	classDeclaration #interfaceMemberDeclaration3
	|	interfaceDeclaration #interfaceMemberDeclaration4
	|	';' #interfaceMemberDeclaration5
	;

constantDeclaration
	:	constantModifier* unannType variableDeclaratorList ';'
	;

constantModifier
	:	annotation
	|	'public'
	|	'static'
	|	'final'
	;

interfaceMethodDeclaration
	:	interfaceMethodModifier* methodHeader methodBody
	;

interfaceMethodModifier
	:	annotation
	|	'public'
	|	'private'//Introduced in Java 9
	|	'abstract'
	|	'default'
	|	'static'
	|	'strictfp'
	;

annotationTypeDeclaration
	:	interfaceModifier* '@' 'interface' identifier annotationTypeBody
	;

annotationTypeBody
	:	'{' annotationTypeMemberDeclaration* '}'
	;

annotationTypeMemberDeclaration
	:	annotationTypeElementDeclaration #annotationTypeMemberDeclaration1
	|	constantDeclaration #annotationTypeMemberDeclaration2
	|	classDeclaration #annotationTypeMemberDeclaration3
	|	interfaceDeclaration #annotationTypeMemberDeclaration4
	|	';' #annotationTypeMemberDeclaration5
	;

annotationTypeElementDeclaration
	:	annotationTypeElementModifier* unannType identifier '(' ')' dims? defaultValue? ';'
	;

annotationTypeElementModifier
	:	annotation
	|	'public'
	|	'abstract'
	;

defaultValue
	:	'default' elementValue
	;

annotation
	:	normalAnnotation #annotation1
	|	markerAnnotation #annotation2
	|	singleElementAnnotation #annotation3
	;

normalAnnotation
	:	'@' typeName '(' elementValuePairList? ')'
	;

elementValuePairList
	:	elementValuePair (',' elementValuePair)*
	;

elementValuePair
	:	identifier '=' elementValue
	;

elementValue
	:	conditionalExpression #elementValue1
	|	elementValueArrayInitializer #elementValue2
	|	annotation #elementValu3
	;

elementValueArrayInitializer
	:	'{' elementValueList? ','? '}'
	;

elementValueList
	:	elementValue (',' elementValue)*
	;

markerAnnotation
	:	'@' typeName
	;

singleElementAnnotation
	:	'@' typeName '(' elementValue ')'
	;

/*
 * Productions from §10 (Arrays)
 */

arrayInitializer
	:	'{' variableInitializerList? ','? '}'
	;

variableInitializerList
	:	variableInitializer (',' variableInitializer)*
	;

/*
 * Productions from §14 (Blocks and Statements)
 */

block
	:	'{' blockStatements? '}'
	;

blockStatements
	:	blockStatement+
	;

blockStatement
	:	localVariableDeclarationStatement #blockStatement1
	|	classDeclaration #blockStatement2
	|	statement #blockStatement3
	;

localVariableDeclarationStatement
	:	localVariableDeclaration ';'
	;

localVariableDeclaration
	:	variableModifier* unannType variableDeclaratorList
	;

statement
	:	statementWithoutTrailingSubstatement #statement1
	|	labeledStatement #statement2
	|	ifThenStatement #statement3
	|	ifThenElseStatement #statement4
	|	whileStatement #statement5
	|	forStatement #statement6
	;

statementNoShortIf
	:	statementWithoutTrailingSubstatement #statementNoShortIf1
	|	labeledStatementNoShortIf #statementNoShortIf2
	|	ifThenElseStatementNoShortIf #statementNoShortIf3
	|	whileStatementNoShortIf #statementNoShortIf4
	|	forStatementNoShortIf #statementNoShortIf5
	;

statementWithoutTrailingSubstatement
	:	block #statementWithoutTrailingSubstatement1
	|	emptyStatement #statementWithoutTrailingSubstatement2
	|	expressionStatement #statementWithoutTrailingSubstatement3
	|	assertStatement #statementWithoutTrailingSubstatement4
	|	switchStatement #statementWithoutTrailingSubstatement5
	|	doStatement #statementWithoutTrailingSubstatement6
	|	breakStatement #statementWithoutTrailingSubstatement7
	|	continueStatement #statementWithoutTrailingSubstatement8
	|	returnStatement #statementWithoutTrailingSubstatement9
	|	synchronizedStatement #statementWithoutTrailingSubstatement10
	|	throwStatement #statementWithoutTrailingSubstatement11
	|	tryStatement #statementWithoutTrailingSubstatement12
	;

emptyStatement
	:	';'
	;

labeledStatement
	:	identifier ':' statement
	;

labeledStatementNoShortIf
	:	identifier ':' statementNoShortIf
	;

expressionStatement
	:	statementExpression ';'
	;

statementExpression
	:	assignment #statementExpression1
	|	preIncrementExpression #statementExpression2
	|	preDecrementExpression #statementExpression3
	|	postIncrementExpression #statementExpression4
	|	postDecrementExpression #statementExpression5
	|	methodInvocation #statementExpression6
	|	classInstanceCreationExpression #statementExpression7
	;

ifThenStatement
	:	'if' '(' expression ')' statement
	;

ifThenElseStatement
	:	'if' '(' expression ')' statementNoShortIf 'else' statement
	;

ifThenElseStatementNoShortIf
	:	'if' '(' expression ')' statementNoShortIf 'else' statementNoShortIf
	;

assertStatement
	:	'assert' expression ';' #assertStatement1
	|	'assert' expression ':' expression ';' #assertStatement2
	;

switchStatement
	:	'switch' '(' expression ')' switchBlock
	;

switchBlock
	:	'{' switchBlockStatementGroup* switchLabel* '}'
	;

switchBlockStatementGroup
	:	switchLabels blockStatements
	;

switchLabels
	:	switchLabel+
	;

switchLabel
	:	'case' constantExpression ':' #switchLabel1
	|	'case' enumConstantName ':' #switchLabel2
	|	'default' ':' #switchLabel3
	;

enumConstantName
	:	identifier
	;

whileStatement
	:	'while' '(' expression ')' statement
	;

whileStatementNoShortIf
	:	'while' '(' expression ')' statementNoShortIf
	;

doStatement
	:	'do' statement 'while' '(' expression ')' ';'
	;

forStatement
	:	basicForStatement #forStatement1
	|	enhancedForStatement #forStatement2
	;

forStatementNoShortIf
	:	basicForStatementNoShortIf #forStatementNoShortIf3
	|	enhancedForStatementNoShortIf #forStatementNoShortIf4
	;

basicForStatement
	:	'for' '(' forInit? ';' expression? ';' forUpdate? ')' statement
	;

basicForStatementNoShortIf
	:	'for' '(' forInit? ';' expression? ';' forUpdate? ')' statementNoShortIf
	;

forInit
	:	statementExpressionList #forInit1
	|	localVariableDeclaration #forInit2
	;

forUpdate
	:	statementExpressionList
	;

statementExpressionList
	:	statementExpression (',' statementExpression)*
	;

enhancedForStatement
	:	'for' '(' variableModifier* unannType variableDeclaratorId ':' expression ')' statement
	;

enhancedForStatementNoShortIf
	:	'for' '(' variableModifier* unannType variableDeclaratorId ':' expression ')' statementNoShortIf
	;

breakStatement
	:	'break' identifier? ';'
	;

continueStatement
	:	'continue' identifier? ';'
	;

returnStatement
	:	'return' expression? ';'
	;

throwStatement
	:	'throw' expression ';'
	;

synchronizedStatement
	:	'synchronized' '(' expression ')' block
	;

tryStatement
	:	'try' block catches #tryStatement1
	|	'try' block catches? finally_ #tryStatement2
	|	tryWithResourcesStatement #tryStatement3
	;

catches
	:	catchClause+
	;

catchClause
	:	'catch' '(' catchFormalParameter ')' block
	;

catchFormalParameter
	:	variableModifier* catchType variableDeclaratorId
	;

catchType
	:	unannClassType ('|' classType)*
	;

finally_
	:	'finally' block
	;

tryWithResourcesStatement
	:	'try' resourceSpecification block catches? finally_?
	;

resourceSpecification
	:	'(' resourceList ';'? ')'
	;

resourceList
	:	resource (';' resource)*
	;

resource
	:	variableModifier* unannType variableDeclaratorId '=' expression #resource1
	|	variableAccess #resource2 //Introduced in Java 9
	;

variableAccess
	:	expressionName #variableAccess1
	|	fieldAccess #variableAccess2
	;

/*
 * Productions from §15 (Expressions)
 */

/*primary
	:	primaryNoNewArray
	|	arrayCreationExpression
	;
*/

primary
	:	(	primaryNoNewArray_lfno_primary
		|	arrayCreationExpression
		)
		(	primaryNoNewArray_lf_primary
		)*
	;

primaryNoNewArray
	:	literal #primaryNoNewArray1
	|	classLiteral #primaryNoNewArray2
	|	'this' #primaryNoNewArray3
	|	typeName '.' 'this' #primaryNoNewArray4
	|	'(' expression ')' #primaryNoNewArray5
	|	classInstanceCreationExpression #primaryNoNewArray6
	|	fieldAccess #primaryNoNewArray7
	|	arrayAccess #primaryNoNewArray8
	|	methodInvocation #primaryNoNewArray9
	|	methodReference #primaryNoNewArray10
	;

primaryNoNewArray_lf_arrayAccess
	:
	;

primaryNoNewArray_lfno_arrayAccess
	:	literal #primaryNoNewArray_lfno_arrayAccess1
	|	typeName ('[' ']')* '.' 'class' #primaryNoNewArray_lfno_arrayAccess2
	|	'void' '.' 'class' #primaryNoNewArray_lfno_arrayAccess3
	|	'this' #primaryNoNewArray_lfno_arrayAccess4
	|	typeName '.' 'this' #primaryNoNewArray_lfno_arrayAccess5
	|	'(' expression ')' #primaryNoNewArray_lfno_arrayAccess6
	|	classInstanceCreationExpression #primaryNoNewArray_lfno_arrayAccess7
	|	fieldAccess #primaryNoNewArray_lfno_arrayAccess8
	|	methodInvocation #primaryNoNewArray_lfno_arrayAccess9
	|	methodReference #primaryNoNewArray_lfno_arrayAccess10
	;

primaryNoNewArray_lf_primary
	:	classInstanceCreationExpression_lf_primary #primaryNoNewArray_lf_primary1
	|	fieldAccess_lf_primary #primaryNoNewArray_lf_primary2
	|	arrayAccess_lf_primary #primaryNoNewArray_lf_primary3
	|	methodInvocation_lf_primary #primaryNoNewArray_lf_primary4
	|	methodReference_lf_primary #primaryNoNewArray_lf_primary5
	;

primaryNoNewArray_lf_primary_lf_arrayAccess_lf_primary
	:
	;

primaryNoNewArray_lf_primary_lfno_arrayAccess_lf_primary
	:	classInstanceCreationExpression_lf_primary #primaryNoNewArray_lf_primary_lfno_arrayAccess_lf_primary1
	|	fieldAccess_lf_primary #primaryNoNewArray_lf_primary_lfno_arrayAccess_lf_primary2
	|	methodInvocation_lf_primary #primaryNoNewArray_lf_primary_lfno_arrayAccess_lf_primary3
	|	methodReference_lf_primary #primaryNoNewArray_lf_primary_lfno_arrayAccess_lf_primary4
	;

primaryNoNewArray_lfno_primary
	:	literal #primaryNoNewArray_lfno_primary1
	|	typeName ('[' ']')* '.' 'class' #primaryNoNewArray_lfno_primary2
	|	unannPrimitiveType ('[' ']')* '.' 'class' #primaryNoNewArray_lfno_primary3
	|	'void' '.' 'class' #primaryNoNewArray_lfno_primary4
	|	'this' #primaryNoNewArray_lfno_primary5
	|	typeName '.' 'this' #primaryNoNewArray_lfno_primary6
	|	'(' expression ')' #primaryNoNewArray_lfno_primary7
	|	classInstanceCreationExpression_lfno_primary #primaryNoNewArray_lfno_primary8
	|	fieldAccess_lfno_primary #primaryNoNewArray_lfno_primary9
	|	arrayAccess_lfno_primary #primaryNoNewArray_lfno_primary10
	|	methodInvocation_lfno_primary #primaryNoNewArray_lfno_primary11
	|	methodReference_lfno_primary #primaryNoNewArray_lfno_primary12
	;

primaryNoNewArray_lfno_primary_lf_arrayAccess_lfno_primary
	:
	;

primaryNoNewArray_lfno_primary_lfno_arrayAccess_lfno_primary
	:	literal #primaryNoNewArray_lfno_primary_lfno_arrayAccess_lfno_primary1
	|	typeName ('[' ']')* '.' 'class' #primaryNoNewArray_lfno_primary_lfno_arrayAccess_lfno_primary2
	|	unannPrimitiveType ('[' ']')* '.' 'class' #primaryNoNewArray_lfno_primary_lfno_arrayAccess_lfno_primary3
	|	'void' '.' 'class' #primaryNoNewArray_lfno_primary_lfno_arrayAccess_lfno_primary4
	|	'this' #primaryNoNewArray_lfno_primary_lfno_arrayAccess_lfno_primary5
	|	typeName '.' 'this' #primaryNoNewArray_lfno_primary_lfno_arrayAccess_lfno_primary6
	|	'(' expression ')' #primaryNoNewArray_lfno_primary_lfno_arrayAccess_lfno_primary7
	|	classInstanceCreationExpression_lfno_primary #primaryNoNewArray_lfno_primary_lfno_arrayAccess_lfno_primary8
	|	fieldAccess_lfno_primary #primaryNoNewArray_lfno_primary_lfno_arrayAccess_lfno_primary9
	|	methodInvocation_lfno_primary #primaryNoNewArray_lfno_primary_lfno_arrayAccess_lfno_primary10
	|	methodReference_lfno_primary #primaryNoNewArray_lfno_primary_lfno_arrayAccess_lfno_primary11
	;

classLiteral
	:	(typeName|numericType|'boolean') ('[' ']')* '.' 'class' #classLiteral1
	|	'void' '.' 'class' #classLiteral2
	;

classInstanceCreationExpression
	:	'new' typeArguments? annotation* identifier ('.' annotation* identifier)* typeArgumentsOrDiamond? '(' argumentList? ')' classBody? #classInstanceCreationExpression1
	|	expressionName '.' 'new' typeArguments? annotation* identifier typeArgumentsOrDiamond? '(' argumentList? ')' classBody? #classInstanceCreationExpression2
	|	primary '.' 'new' typeArguments? annotation* identifier typeArgumentsOrDiamond? '(' argumentList? ')' classBody? #classInstanceCreationExpression3
	;

classInstanceCreationExpression_lf_primary
	:	'.' 'new' typeArguments? annotation* identifier typeArgumentsOrDiamond? '(' argumentList? ')' classBody?
	;

classInstanceCreationExpression_lfno_primary
	:	'new' typeArguments? annotation* identifier ('.' annotation* identifier)* typeArgumentsOrDiamond? '(' argumentList? ')' classBody? #classInstanceCreationExpression_lfno_primary1
	|	expressionName '.' 'new' typeArguments? annotation* identifier typeArgumentsOrDiamond? '(' argumentList? ')' classBody? #classInstanceCreationExpression_lfno_primary2
	;

typeArgumentsOrDiamond
	:	typeArguments #typeArgumentsOrDiamond1
	|	'<' '>' #typeArgumentsOrDiamond2
	;

fieldAccess
	:	primary '.' identifier #fieldAccess1
	|	'super' '.' identifier #fieldAccess2
	|	typeName '.' 'super' '.' identifier #fieldAccess3
	;

fieldAccess_lf_primary
	:	'.' identifier
	;

fieldAccess_lfno_primary
	:	'super' '.' identifier #fieldAccess_lfno_primary1
	|	typeName '.' 'super' '.' identifier #fieldAccess_lfno_primary2
	;

/*arrayAccess
	:	expressionName '[' expression ']'
	|	primaryNoNewArray '[' expression ']'
	;
*/

arrayAccess
	:	(	expressionName '[' expression ']'
		|	primaryNoNewArray_lfno_arrayAccess '[' expression ']'
		)
		(	primaryNoNewArray_lf_arrayAccess '[' expression ']'
		)*
	;

arrayAccess_lf_primary
	:	(	primaryNoNewArray_lf_primary_lfno_arrayAccess_lf_primary '[' expression ']'
		)
		(	primaryNoNewArray_lf_primary_lf_arrayAccess_lf_primary '[' expression ']'
		)*
	;

arrayAccess_lfno_primary
	:	(	expressionName '[' expression ']'
		|	primaryNoNewArray_lfno_primary_lfno_arrayAccess_lfno_primary '[' expression ']'
		)
		(	primaryNoNewArray_lfno_primary_lf_arrayAccess_lfno_primary '[' expression ']'
		)*
	;


methodInvocation
	:	methodName '(' argumentList? ')' #methodInvocation1
	|	typeName '.' typeArguments? identifier '(' argumentList? ')' #methodInvocation2
	|	expressionName '.' typeArguments? identifier '(' argumentList? ')' #methodInvocation3
	|	primary '.' typeArguments? identifier '(' argumentList? ')' #methodInvocation4
	|	'super' '.' typeArguments? identifier '(' argumentList? ')' #methodInvocation5
	|	typeName '.' 'super' '.' typeArguments? identifier '(' argumentList? ')' #methodInvocation6
	;

methodInvocation_lf_primary
	:	'.' typeArguments? identifier '(' argumentList? ')'
	;

methodInvocation_lfno_primary
	:	methodName '(' argumentList? ')' #methodInvocation_lfno_primary1
	|	typeName '.' typeArguments? identifier '(' argumentList? ')' #methodInvocation_lfno_primary2
	|	expressionName '.' typeArguments? identifier '(' argumentList? ')' #methodInvocation_lfno_primary3
	|	'super' '.' typeArguments? identifier '(' argumentList? ')' #methodInvocation_lfno_primary4
	|	typeName '.' 'super' '.' typeArguments? identifier '(' argumentList? ')' #methodInvocation_lfno_primary5
	;

argumentList
	:	expression (',' expression)*
	;

methodReference
	:	expressionName '::' typeArguments? identifier #methodReference1
	|	referenceType '::' typeArguments? identifier  #methodReference2
	|	primary '::' typeArguments? identifier #methodReference3
	|	'super' '::' typeArguments? identifier #methodReference4
	|	typeName '.' 'super' '::' typeArguments? identifier #methodReference5
	|	classType '::' typeArguments? 'new'  #methodReference6
	|	arrayType '::' 'new' #methodReference7
	;

methodReference_lf_primary
	:	'::' typeArguments? identifier
	;

methodReference_lfno_primary
	:	expressionName '::' typeArguments? identifier #methodReference_lfno_primary1
	|	referenceType '::' typeArguments? identifier #methodReference_lfno_primary2
	|	'super' '::' typeArguments? identifier #methodReference_lfno_primary3
	|	typeName '.' 'super' '::' typeArguments? identifier #methodReference_lfno_primary4
	|	classType '::' typeArguments? 'new' #methodReference_lfno_primary5
	|	arrayType '::' 'new' #methodReference_lfno_primary6
	;

arrayCreationExpression
	:	'new' primitiveType dimExprs dims?  #arrayCreationExpression1
	|	'new' classOrInterfaceType dimExprs dims? #arrayCreationExpression2
	|	'new' primitiveType dims arrayInitializer #arrayCreationExpression3
	|	'new' classOrInterfaceType dims arrayInitializer #arrayCreationExpression4
	;

dimExprs
	:	dimExpr+
	;

dimExpr
	:	annotation* '[' expression ']'
	;

constantExpression
	:	expression
	;

expression
	:	lambdaExpression #expression1
	|	assignmentExpression #expression2
	;

lambdaExpression
	:	lambdaParameters '->' lambdaBody
	;

lambdaParameters
	:	identifier #lambdaParameters1
	|	'(' formalParameterList? ')' #lambdaParameters2
	|	'(' inferredFormalParameterList ')' #lambdaParameters3
	;

inferredFormalParameterList
	:	identifier (',' identifier)*
	;

lambdaBody
	:	expression #lambdaBody1
	|	block #lambdaBody2
	;

assignmentExpression
	:	conditionalExpression #assignmentExpression1
	|	assignment #assignmentExpression2
	;

assignment
	:	leftHandSide assignmentOperator expression
	;

leftHandSide
	:	expressionName #leftHandSide3
	|	fieldAccess #leftHandSide4
	|	arrayAccess #leftHandSide5
	;

assignmentOperator
	:	'='
	|	'*='
	|	'/='
	|	'%='
	|	'+='
	|	'-='
	|	'<<='
	|	'>>='
	|	'>>>='
	|	'&='
	|	'^='
	|	'|='
	;

conditionalExpression
	:	conditionalOrExpression #conditionalExpression1
	|	conditionalOrExpression '?' expression ':' (conditionalExpression|lambdaExpression) #conditionalExpression2
	;

conditionalOrExpression
	:	conditionalAndExpression #conditionalOrExpression1
	|	conditionalOrExpression '||' conditionalAndExpression #conditionalOrExpression2
	;

conditionalAndExpression
	:	inclusiveOrExpression #conditionalAndExpression1
	|	conditionalAndExpression '&&' inclusiveOrExpression #conditionalAndExpression2
	;

inclusiveOrExpression
	:	exclusiveOrExpression #inclusiveOrExpression1
	|	inclusiveOrExpression '|' exclusiveOrExpression #inclusiveOrExpression2
	;

exclusiveOrExpression
	:	andExpression #exclusiveOrExpression1
	|	exclusiveOrExpression '^' andExpression #exclusiveOrExpression2
	;

andExpression
	:	equalityExpression #andExpression1
	|	andExpression '&' equalityExpression #andExpression2
	;

equalityExpression
	:	relationalExpression #equalityExpression1
	|	equalityExpression '==' relationalExpression #equalityExpression2
	|	equalityExpression '!=' relationalExpression #equalityExpression3
	;

relationalExpression
	:	shiftExpression #relationalExpression1
	|	relationalExpression '<' shiftExpression #relationalExpression2
	|	relationalExpression '>' shiftExpression #relationalExpression3
	|	relationalExpression '<=' shiftExpression #relationalExpression4
	|	relationalExpression '>=' shiftExpression #relationalExpression5
	|	relationalExpression 'instanceof' referenceType #relationalExpression6
	;

shiftExpression
	:	additiveExpression #shiftExpression1
	|	shiftExpression '<' '<' additiveExpression #shiftExpression2
	|	shiftExpression '>' '>' additiveExpression #shiftExpression3
	|	shiftExpression '>' '>' '>' additiveExpression #shiftExpression4
	;

additiveExpression
	:	multiplicativeExpression #additiveExpression1
	|	additiveExpression '+' multiplicativeExpression #additiveExpressio2
	|	additiveExpression '-' multiplicativeExpression #additiveExpression3
	;

multiplicativeExpression
	:	unaryExpression #multiplicativeExpression1
	|	multiplicativeExpression '*' unaryExpression #multiplicativeExpression2
	|	multiplicativeExpression '/' unaryExpression #multiplicativeExpression3
	|	multiplicativeExpression '%' unaryExpression #multiplicativeExpression4
	;

unaryExpression
	:	preIncrementExpression #unaryExpression1
	|	preDecrementExpression #unaryExpression2
	|	'+' unaryExpression #unaryExpression3
	|	'-' unaryExpression #unaryExpression4
	|	unaryExpressionNotPlusMinus #unaryExpression5
	;

preIncrementExpression
	:	'++' unaryExpression
	;

preDecrementExpression
	:	'--' unaryExpression
	;

unaryExpressionNotPlusMinus
	:	postfixExpression #unaryExpressionNotPlusMinus1
	|	'~' unaryExpression #unaryExpressionNotPlusMinus2
	|	'!' unaryExpression #unaryExpressionNotPlusMinus3
	|	castExpression #unaryExpressionNotPlusMinus4
	;

/*postfixExpression
	:	primary
	|	expressionName
	|	postIncrementExpression
	|	postDecrementExpression
	;
*/

postfixExpression
	:	(	primary
		|	expressionName
		)
		(	postIncrementExpression_lf_postfixExpression
		|	postDecrementExpression_lf_postfixExpression
		)*
	;

postIncrementExpression
	:	postfixExpression '++'
	;

postIncrementExpression_lf_postfixExpression
	:	'++'
	;

postDecrementExpression
	:	postfixExpression '--'
	;

postDecrementExpression_lf_postfixExpression
	:	'--'
	;

castExpression
	:	'(' primitiveType ')' unaryExpression #castExpression1
	|	'(' referenceType additionalBound* ')' unaryExpressionNotPlusMinus #castExpression2
	|	'(' referenceType additionalBound* ')' lambdaExpression #castExpression3
	;

// LEXER

identifier : Identifier | 'to' | 'module' | 'open' | 'with' | 'provides' | 'uses' | 'opens' | 'requires' | 'exports';

// §3.9 Keywords

ABSTRACT : 'abstract';
ASSERT : 'assert';
BOOLEAN : 'boolean';
BREAK : 'break';
BYTE : 'byte';
CASE : 'case';
CATCH : 'catch';
CHAR : 'char';
CLASS : 'class';
CONST : 'const';
CONTINUE : 'continue';
DEFAULT : 'default';
DO : 'do';
DOUBLE : 'double';
ELSE : 'else';
ENUM : 'enum';
EXTENDS : 'extends';
FINAL : 'final';
FINALLY : 'finally';
FLOAT : 'float';
FOR : 'for';
IF : 'if';
GOTO : 'goto';
IMPLEMENTS : 'implements';
IMPORT : 'import';
INSTANCEOF : 'instanceof';
INT : 'int';
INTERFACE : 'interface';
LONG : 'long';
NATIVE : 'native';
NEW : 'new';
PACKAGE : 'package';
PRIVATE : 'private';
PROTECTED : 'protected';
PUBLIC : 'public';
RETURN : 'return';
SHORT : 'short';
STATIC : 'static';
STRICTFP : 'strictfp';
SUPER : 'super';
SWITCH : 'switch';
SYNCHRONIZED : 'synchronized';
THIS : 'this';
THROW : 'throw';
THROWS : 'throws';
TRANSIENT : 'transient';
TRY : 'try';
VOID : 'void';
VOLATILE : 'volatile';
WHILE : 'while';
UNDER_SCORE : '_';//Introduced in Java 9

// §3.10.1 Integer Literals

IntegerLiteral
	:	DecimalIntegerLiteral
	|	HexIntegerLiteral
	|	OctalIntegerLiteral
	|	BinaryIntegerLiteral
	;

fragment
DecimalIntegerLiteral
	:	DecimalNumeral IntegerTypeSuffix?
	;

fragment
HexIntegerLiteral
	:	HexNumeral IntegerTypeSuffix?
	;

fragment
OctalIntegerLiteral
	:	OctalNumeral IntegerTypeSuffix?
	;

fragment
BinaryIntegerLiteral
	:	BinaryNumeral IntegerTypeSuffix?
	;

fragment
IntegerTypeSuffix
	:	[lL]
	;

fragment
DecimalNumeral
	:	'0'
	|	NonZeroDigit (Digits? | Underscores Digits)
	;

fragment
Digits
	:	Digit (DigitsAndUnderscores? Digit)?
	;

fragment
Digit
	:	'0'
	|	NonZeroDigit
	;

fragment
NonZeroDigit
	:	[1-9]
	;

fragment
DigitsAndUnderscores
	:	DigitOrUnderscore+
	;

fragment
DigitOrUnderscore
	:	Digit
	|	'_'
	;

fragment
Underscores
	:	'_'+
	;

fragment
HexNumeral
	:	'0' [xX] HexDigits
	;

fragment
HexDigits
	:	HexDigit (HexDigitsAndUnderscores? HexDigit)?
	;

fragment
HexDigit
	:	[0-9a-fA-F]
	;

fragment
HexDigitsAndUnderscores
	:	HexDigitOrUnderscore+
	;

fragment
HexDigitOrUnderscore
	:	HexDigit
	|	'_'
	;

fragment
OctalNumeral
	:	'0' Underscores? OctalDigits
	;

fragment
OctalDigits
	:	OctalDigit (OctalDigitsAndUnderscores? OctalDigit)?
	;

fragment
OctalDigit
	:	[0-7]
	;

fragment
OctalDigitsAndUnderscores
	:	OctalDigitOrUnderscore+
	;

fragment
OctalDigitOrUnderscore
	:	OctalDigit
	|	'_'
	;

fragment
BinaryNumeral
	:	'0' [bB] BinaryDigits
	;

fragment
BinaryDigits
	:	BinaryDigit (BinaryDigitsAndUnderscores? BinaryDigit)?
	;

fragment
BinaryDigit
	:	[01]
	;

fragment
BinaryDigitsAndUnderscores
	:	BinaryDigitOrUnderscore+
	;

fragment
BinaryDigitOrUnderscore
	:	BinaryDigit
	|	'_'
	;

// §3.10.2 Floating-Point Literals

FloatingPointLiteral
	:	DecimalFloatingPointLiteral
	|	HexadecimalFloatingPointLiteral
	;

fragment
DecimalFloatingPointLiteral
	:	Digits '.' Digits? ExponentPart? FloatTypeSuffix?
	|	'.' Digits ExponentPart? FloatTypeSuffix?
	|	Digits ExponentPart FloatTypeSuffix?
	|	Digits FloatTypeSuffix
	;

fragment
ExponentPart
	:	ExponentIndicator SignedInteger
	;

fragment
ExponentIndicator
	:	[eE]
	;

fragment
SignedInteger
	:	Sign? Digits
	;

fragment
Sign
	:	[+-]
	;

fragment
FloatTypeSuffix
	:	[fFdD]
	;

fragment
HexadecimalFloatingPointLiteral
	:	HexSignificand BinaryExponent FloatTypeSuffix?
	;

fragment
HexSignificand
	:	HexNumeral '.'?
	|	'0' [xX] HexDigits? '.' HexDigits
	;

fragment
BinaryExponent
	:	BinaryExponentIndicator SignedInteger
	;

fragment
BinaryExponentIndicator
	:	[pP]
	;

// §3.10.3 Boolean Literals

BooleanLiteral
	:	'true'
	|	'false'
	;

// §3.10.4 Character Literals

CharacterLiteral
	:	'\'' SingleCharacter '\''
	|	'\'' EscapeSequence '\''
	;

fragment
SingleCharacter
	:	~['\\\r\n]
	;

// §3.10.5 String Literals

StringLiteral
	:	'"' StringCharacters? '"'
	;

fragment
StringCharacters
	:	StringCharacter+
	;

fragment
StringCharacter
	:	~["\\\r\n]
	|	EscapeSequence
	;

// §3.10.6 Escape Sequences for Character and String Literals

fragment
EscapeSequence
	:	'\\' [btnfr"'\\]
	|	OctalEscape
    |   UnicodeEscape // This is not in the spec but prevents having to preprocess the input
	;

fragment
OctalEscape
	:	'\\' OctalDigit
	|	'\\' OctalDigit OctalDigit
	|	'\\' ZeroToThree OctalDigit OctalDigit
	;

fragment
ZeroToThree
	:	[0-3]
	;

// This is not in the spec but prevents having to preprocess the input
fragment
UnicodeEscape
    :   '\\' 'u'+ HexDigit HexDigit HexDigit HexDigit
    ;

// §3.10.7 The Null Literal

NullLiteral
	:	'null'
	;

// §3.11 Separators

LPAREN : '(';
RPAREN : ')';
LBRACE : '{';
RBRACE : '}';
LBRACK : '[';
RBRACK : ']';
SEMI : ';';
COMMA : ',';
DOT : '.';
ELLIPSIS : '...';
AT : '@';
COLONCOLON : '::';


// §3.12 Operators

ASSIGN : '=';
GT : '>';
LT : '<';
BANG : '!';
TILDE : '~';
QUESTION : '?';
COLON : ':';
ARROW : '->';
EQUAL : '==';
LE : '<=';
GE : '>=';
NOTEQUAL : '!=';
AND : '&&';
OR : '||';
INC : '++';
DEC : '--';
ADD : '+';
SUB : '-';
MUL : '*';
DIV : '/';
BITAND : '&';
BITOR : '|';
CARET : '^';
MOD : '%';
//LSHIFT : '<<';
//RSHIFT : '>>';
//URSHIFT : '>>>';

ADD_ASSIGN : '+=';
SUB_ASSIGN : '-=';
MUL_ASSIGN : '*=';
DIV_ASSIGN : '/=';
AND_ASSIGN : '&=';
OR_ASSIGN : '|=';
XOR_ASSIGN : '^=';
MOD_ASSIGN : '%=';
LSHIFT_ASSIGN : '<<=';
RSHIFT_ASSIGN : '>>=';
URSHIFT_ASSIGN : '>>>=';

// §3.8 Identifiers (must appear after all keywords in the grammar)

Identifier
	:	JavaLetter JavaLetterOrDigit*
	;

fragment
JavaLetter
	:	[a-zA-Z$_] // these are the "java letters" below 0x7F
	|	// covers all characters above 0x7F which are not a surrogate
		~[\u0000-\u007F\uD800-\uDBFF]

	|	// covers UTF-16 surrogate pairs encodings for U+10000 to U+10FFFF
		[\uD800-\uDBFF] [\uDC00-\uDFFF]

	;

fragment
JavaLetterOrDigit
	:	[a-zA-Z0-9$_] // these are the "java letters or digits" below 0x7F
	|	// covers all characters above 0x7F which are not a surrogate
		~[\u0000-\u007F\uD800-\uDBFF]

	|	// covers UTF-16 surrogate pairs encodings for U+10000 to U+10FFFF
		[\uD800-\uDBFF] [\uDC00-\uDFFF]

	;

//
// Whitespace and comments
//

WS  :  [ \t\r\n\u000C]+ -> channel(HIDDEN)
    ;

COMMENT
    :   '/*' .*? '*/' -> channel(HIDDEN)
    ;

LINE_COMMENT
    :   '//' ~[\r\n]* -> channel(HIDDEN)
    ;
