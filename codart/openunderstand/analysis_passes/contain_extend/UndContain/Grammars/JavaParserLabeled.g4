/*
 [The "BSD licence"]
 Copyright (c) 2013 Terence Parr, Sam Harwell
 Copyright (c) 2017 Ivan Kochurkin (upgrade to Java 8)
 All rights reserved.

 Redistribution and use in source and binary forms, with or without
 modification, are permitted provided that the following conditions
 are met:
 1. Redistributions of source code must retain the above copyright
    notice, this list of conditions and the following disclaimer.
 2. Redistributions in binary form must reproduce the above copyright
    notice, this list of conditions and the following disclaimer in the
    documentation and/or other materials provided with the distribution.
 3. The name of the author may not be used to endorse or promote products
    derived from this software without specific prior written permission.

 THIS SOFTWARE IS PROVIDED BY THE AUTHOR ``AS IS'' AND ANY EXPRESS OR
 IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES
 OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED.
 IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR ANY DIRECT, INDIRECT,
 INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT
 NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
 DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
 THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
 (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF
 THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
*/

parser grammar JavaParserLabeled;

options { tokenVocab=JavaLexer; }

compilationUnit
    : packageDeclaration? importDeclaration* typeDeclaration* EOF
    ;

packageDeclaration
    : annotation* PACKAGE qualifiedName ';'
    ;

importDeclaration
    : IMPORT STATIC? qualifiedName ('.' '*')? ';'
    ;

typeDeclaration
    : classOrInterfaceModifier*
      (classDeclaration | enumDeclaration | interfaceDeclaration | annotationTypeDeclaration)
    | ';'
    ;

modifier
    : classOrInterfaceModifier
    | NATIVE
    | SYNCHRONIZED
    | TRANSIENT
    | VOLATILE
    ;

classOrInterfaceModifier
    : annotation
    | PUBLIC
    | PROTECTED
    | PRIVATE
    | STATIC
    | ABSTRACT
    | FINAL    // FINAL for class only -- does not apply to interfaces
    | STRICTFP
    ;

variableModifier
    : FINAL
    | annotation
    ;

classDeclaration
    : CLASS IDENTIFIER typeParameters?
      (EXTENDS typeType)?
      (IMPLEMENTS typeList)?
      classBody
    ;

typeParameters
    : '<' typeParameter (',' typeParameter)* '>'
    ;

typeParameter
    : annotation* IDENTIFIER (EXTENDS annotation* typeBound)?
    ;

typeBound
    : typeType ('&' typeType)*
    ;

enumDeclaration
    : ENUM IDENTIFIER (IMPLEMENTS typeList)? '{' enumConstants? ','? enumBodyDeclarations? '}'
    ;

enumConstants
    : enumConstant (',' enumConstant)*
    ;

enumConstant
    : annotation* IDENTIFIER arguments? classBody?
    ;

enumBodyDeclarations
    : ';' classBodyDeclaration*
    ;

interfaceDeclaration
    : INTERFACE IDENTIFIER typeParameters? (EXTENDS typeList)? interfaceBody
    ;

classBody
    : '{' classBodyDeclaration* '}'
    ;

interfaceBody
    : '{' interfaceBodyDeclaration* '}'
    ;

classBodyDeclaration
    : ';' #classBodyDeclaration0
    | STATIC? block #classBodyDeclaration1
    | modifier* memberDeclaration #classBodyDeclaration2
    ;

memberDeclaration
    : methodDeclaration #memberDeclaration0
    | genericMethodDeclaration #memberDeclaration1
    | fieldDeclaration #memberDeclaration2
    | constructorDeclaration #memberDeclaration3
    | genericConstructorDeclaration #memberDeclaration4
    | interfaceDeclaration #memberDeclaration5
    | annotationTypeDeclaration #memberDeclaration6
    | classDeclaration #memberDeclaration7
    | enumDeclaration #memberDeclaration8
    ;

/* We use rule this even for void methods which cannot have [] after parameters.
   This simplifies grammar and we can consider void to be a type, which
   renders the [] matching as a context-sensitive issue or a semantic check
   for invalid return type after parsing.
 */
methodDeclaration
    : typeTypeOrVoid IDENTIFIER formalParameters ('[' ']')*
      (THROWS qualifiedNameList)?
      methodBody
    ;

methodBody
    : block
    | ';'
    ;

typeTypeOrVoid
    : typeType
    | VOID
    ;

genericMethodDeclaration
    : typeParameters methodDeclaration
    ;

genericConstructorDeclaration
    : typeParameters constructorDeclaration
    ;

constructorDeclaration
    : IDENTIFIER formalParameters (THROWS qualifiedNameList)? constructorBody=block
    ;

fieldDeclaration
    : typeType variableDeclarators ';'
    ;

interfaceBodyDeclaration
    : modifier* interfaceMemberDeclaration
    | ';'
    ;

interfaceMemberDeclaration
    : constDeclaration #interfaceMemberDeclaration0
    | interfaceMethodDeclaration #interfaceMemberDeclaration1
    | genericInterfaceMethodDeclaration #interfaceMemberDeclaration2
    | interfaceDeclaration #interfaceMemberDeclaration3
    | annotationTypeDeclaration #interfaceMemberDeclaration4
    | classDeclaration #interfaceMemberDeclaration5
    | enumDeclaration #interfaceMemberDeclaration6
    ;

constDeclaration
    : typeType constantDeclarator (',' constantDeclarator)* ';'
    ;

constantDeclarator
    : IDENTIFIER ('[' ']')* '=' variableInitializer
    ;

// see matching of [] comment in methodDeclaratorRest
// methodBody from Java8
interfaceMethodDeclaration
    : interfaceMethodModifier* (typeTypeOrVoid | typeParameters annotation* typeTypeOrVoid)
      IDENTIFIER formalParameters ('[' ']')* (THROWS qualifiedNameList)? methodBody
    ;

// Java8
interfaceMethodModifier
    : annotation
    | PUBLIC
    | ABSTRACT
    | DEFAULT
    | STATIC
    | STRICTFP
    ;

genericInterfaceMethodDeclaration
    : typeParameters interfaceMethodDeclaration
    ;

variableDeclarators
    : variableDeclarator (',' variableDeclarator)*
    ;

variableDeclarator
    : variableDeclaratorId ('=' variableInitializer)?
    ;

variableDeclaratorId
    : IDENTIFIER ('[' ']')*
    ;

variableInitializer
    : arrayInitializer #variableInitializer0
    | expression #variableInitializer1
    ;

arrayInitializer
    : '{' (variableInitializer (',' variableInitializer)* (',')? )? '}'
    ;

classOrInterfaceType
    : IDENTIFIER typeArguments? ('.' IDENTIFIER typeArguments?)*
    ;

typeArgument
    : typeType #typeArgument0
    | annotation* '?' ((EXTENDS | SUPER) typeType)? #typeArgument0
    ;

qualifiedNameList
    : qualifiedName (',' qualifiedName)*
    ;

formalParameters
    : '(' formalParameterList? ')'
    ;

formalParameterList
    : formalParameter (',' formalParameter)* (',' lastFormalParameter)? #formalParameterList0
    | lastFormalParameter #formalParameterList1
    ;

formalParameter
    : variableModifier* typeType variableDeclaratorId
    ;

lastFormalParameter
    : variableModifier* typeType annotation* '...' variableDeclaratorId
    ;

qualifiedName
    : IDENTIFIER ('.' IDENTIFIER)*
    ;

literal
    : integerLiteral #literal0
    | floatLiteral #literal1
    | CHAR_LITERAL #literal2
    | STRING_LITERAL #literal3
    | BOOL_LITERAL #literal4
    | NULL_LITERAL #literal5
    ;

integerLiteral
    : DECIMAL_LITERAL
    | HEX_LITERAL
    | OCT_LITERAL
    | BINARY_LITERAL
    ;

floatLiteral
    : FLOAT_LITERAL
    | HEX_FLOAT_LITERAL
    ;

// ANNOTATIONS
altAnnotationQualifiedName
    : (IDENTIFIER DOT)* '@' IDENTIFIER
    ;

annotation
    : ('@' qualifiedName | altAnnotationQualifiedName) ('(' ( elementValuePairs | elementValue )? ')')?
    ;

elementValuePairs
    : elementValuePair (',' elementValuePair)*
    ;

elementValuePair
    : IDENTIFIER '=' elementValue
    ;

elementValue
    : expression #elementValue0
    | annotation #elementValue1
    | elementValueArrayInitializer #elementValue2
    ;

elementValueArrayInitializer
    : '{' (elementValue (',' elementValue)*)? (',')? '}'
    ;

annotationTypeDeclaration
    : '@' INTERFACE IDENTIFIER annotationTypeBody
    ;

annotationTypeBody
    : '{' (annotationTypeElementDeclaration)* '}'
    ;

annotationTypeElementDeclaration
    : modifier* annotationTypeElementRest
    | ';' // this is not allowed by the grammar, but apparently allowed by the actual compiler
    ;

annotationTypeElementRest
    : typeType annotationMethodOrConstantRest ';' #annotationTypeElementRest0
    | classDeclaration ';'? #annotationTypeElementRest1
    | interfaceDeclaration ';'? #annotationTypeElementRest2
    | enumDeclaration ';'? #annotationTypeElementRest3
    | annotationTypeDeclaration ';'? #annotationTypeElementRest4
    ;

annotationMethodOrConstantRest
    : annotationMethodRest #annotationMethodOrConstantRest0
    | annotationConstantRest #annotationMethodOrConstantRest1
    ;

annotationMethodRest
    : IDENTIFIER '(' ')' defaultValue?
    ;

annotationConstantRest
    : variableDeclarators
    ;

defaultValue
    : DEFAULT elementValue
    ;

// STATEMENTS / BLOCKS

block
    : '{' blockStatement* '}'
    ;

blockStatement
    : localVariableDeclaration ';' #blockStatement0
    | statement #blockStatement1
    | localTypeDeclaration #blockStatement2
    ;

localVariableDeclaration
    : variableModifier* typeType variableDeclarators
    ;

localTypeDeclaration
    : classOrInterfaceModifier*
      (classDeclaration | interfaceDeclaration)
    | ';'
    ;

statement
    : blockLabel=block #statement0
    | ASSERT expression (':' expression)? ';' #statement1
    | IF parExpression statement (ELSE statement)? #statement2
    | FOR '(' forControl ')' statement #statement3
    | WHILE parExpression statement #statement4
    | DO statement WHILE parExpression ';' #statement5
    | TRY block (catchClause+ finallyBlock? | finallyBlock) #statement6
    | TRY resourceSpecification block catchClause* finallyBlock? #statement7
    | SWITCH parExpression '{' switchBlockStatementGroup* switchLabel* '}' #statement8
    | SYNCHRONIZED parExpression block #statement9
    | RETURN expression? ';' #statement10
    | THROW expression ';' #statement11
    | BREAK IDENTIFIER? ';' #statement12
    | CONTINUE IDENTIFIER? ';' #statement13
    | SEMI #statement14
    | statementExpression=expression ';' #statement15
    | identifierLabel=IDENTIFIER ':' statement #statement16
    ;

catchClause
    : CATCH '(' variableModifier* catchType IDENTIFIER ')' block
    ;

catchType
    : qualifiedName ('|' qualifiedName)*
    ;

finallyBlock
    : FINALLY block
    ;

resourceSpecification
    : '(' resources ';'? ')'
    ;

resources
    : resource (';' resource)*
    ;

resource
    : variableModifier* classOrInterfaceType variableDeclaratorId '=' expression
    ;

/** Matches cases then statements, both of which are mandatory.
 *  To handle empty cases at the end, we add switchLabel* to statement.
 */
switchBlockStatementGroup
    : switchLabel+ blockStatement+
    ;

switchLabel
    : CASE (constantExpression=expression | enumConstantName=IDENTIFIER) ':'
    | DEFAULT ':'
    ;

forControl
    : enhancedForControl #forControl0
    | forInit? ';' expression? ';' forUpdate=expressionList? #forControl1
    ;

forInit
    : localVariableDeclaration #forInit0
    | expressionList #forInit1
    ;

enhancedForControl
    : variableModifier* typeType variableDeclaratorId ':' expression
    ;

// EXPRESSIONS

parExpression
    : '(' expression ')'
    ;

expressionList
    : expression (',' expression)*
    ;

methodCall
    : IDENTIFIER '(' expressionList? ')' #methodCall0
    | THIS '(' expressionList? ')' #methodCall1
    | SUPER '(' expressionList? ')' #methodCall2
    ;

expression
    : primary #expression0
    | expression bop='.'
      ( IDENTIFIER
      | methodCall
      | THIS
      | NEW nonWildcardTypeArguments? innerCreator
      | SUPER superSuffix
      | explicitGenericInvocation
      ) #expression1
    | expression '[' expression ']' #expression2
    | methodCall #expression3
    | NEW creator #expression4
    | '(' annotation* typeType ')' expression #expression5
    | expression postfix=('++' | '--') #expression6
    | prefix=('+'|'-'|'++'|'--') expression #expression7
    | prefix=('~'|'!') expression #expression8
    | expression bop=('*'|'/'|'%') expression #expression9
    | expression bop=('+'|'-') expression #expression10
    | expression ('<' '<' | '>' '>' '>' | '>' '>') expression #expression11
    | expression bop=('<=' | '>=' | '>' | '<') expression #expression12
    | expression bop=INSTANCEOF typeType #expression13
    | expression bop=('==' | '!=') expression #expression14
    | expression bop='&' expression #expression15
    | expression bop='^' expression #expression16
    | expression bop='|' expression #expression17
    | expression bop='&&' expression #expression18
    | expression bop='||' expression #expression19
    | <assoc=right> expression bop='?' expression ':' expression #expression20
    | <assoc=right> expression
      bop=('=' | '+=' | '-=' | '*=' | '/=' | '&=' | '|=' | '^=' | '>>=' | '>>>=' | '<<=' | '%=')
      expression #expression21
    | lambdaExpression #expression22 // Java8

    // Java 8 methodReference
    | expression '::' typeArguments? IDENTIFIER #expression23
    | typeType '::' (typeArguments? IDENTIFIER | NEW) #expression24
    | classType '::' typeArguments? NEW #expression25
    ;

// Java8
lambdaExpression
    : lambdaParameters '->' lambdaBody
    ;

// Java8
lambdaParameters
    : IDENTIFIER #lambdaParameters0
    | '(' formalParameterList? ')' #lambdaParameters1
    | '(' IDENTIFIER (',' IDENTIFIER)* ')' #lambdaParameters2
    ;

// Java8
lambdaBody
    : expression #lambdaBody0
    | block #lambdaBody1
    ;

primary
    : '(' expression ')' #primary0
    | THIS #primary1
    | SUPER #primary2
    | literal #primary3
    | IDENTIFIER #primary4
    | typeTypeOrVoid '.' CLASS #primary5
    | nonWildcardTypeArguments (explicitGenericInvocationSuffix | THIS arguments) #primary6
    ;

classType
    : (classOrInterfaceType '.')? annotation* IDENTIFIER typeArguments?
    ;

creator
    : nonWildcardTypeArguments createdName classCreatorRest #creator0
    | createdName (arrayCreatorRest | classCreatorRest) #creator1
    ;

createdName
    : IDENTIFIER typeArgumentsOrDiamond? ('.' IDENTIFIER typeArgumentsOrDiamond?)* #createdName0
    | primitiveType #createdName1
    ;

innerCreator
    : IDENTIFIER nonWildcardTypeArgumentsOrDiamond? classCreatorRest
    ;

arrayCreatorRest
    : '[' (']' ('[' ']')* arrayInitializer | expression ']' ('[' expression ']')* ('[' ']')*)
    ;

classCreatorRest
    : arguments classBody?
    ;

explicitGenericInvocation
    : nonWildcardTypeArguments explicitGenericInvocationSuffix
    ;

typeArgumentsOrDiamond
    : '<' '>'
    | typeArguments
    ;

nonWildcardTypeArgumentsOrDiamond
    : '<' '>'
    | nonWildcardTypeArguments
    ;

nonWildcardTypeArguments
    : '<' typeList '>'
    ;

typeList
    : typeType (',' typeType)*
    ;

typeType
    : annotation* (classOrInterfaceType | primitiveType) (annotation* '[' ']')*
    ;

primitiveType
    : BOOLEAN
    | CHAR
    | BYTE
    | SHORT
    | INT
    | LONG
    | FLOAT
    | DOUBLE
    ;

typeArguments
    : '<' typeArgument (',' typeArgument)* '>'
    ;

superSuffix
    : arguments #superSuffix0
    | '.' IDENTIFIER arguments? #superSuffix1
    ;

explicitGenericInvocationSuffix
    : SUPER superSuffix #explicitGenericInvocationSuffix0
    | IDENTIFIER arguments #explicitGenericInvocationSuffix1
    ;

arguments
    : '(' expressionList? ')'
    ;
