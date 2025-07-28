"""
This module map code smells to their corresponding refactorings.
A graph of code/design smells and strategies to identify/remove/mitigate

"""

__version__ = '0.1.0'
__author__ = 'Morteza'

import os
import networkx as nx


class Mapper:
    def __init__(self):
        G = nx.DiGraph()

        # 1
        G.add_edge('Move field', 'SHOTGUN SURGERY')
        G.add_edge('Move field', 'BROKEN MODULARIZATION')  # Design smell
        G.add_edge('Move field', 'CYCLICALLY-DEPENDENT MODULARIZATION')  # Design smell

        G.add_edge('Move method', 'MUTABLE DATA')
        G.add_edge('Move method', 'DIVERGENT CHANGE')
        G.add_edge('Move method', 'SHOTGUN SURGERY')
        G.add_edge('Move method', 'FEATURE ENVY')
        G.add_edge('Move method', 'MESSAGE CHAINS')
        G.add_edge('Move method', 'BROKEN MODULARIZATION')  # Design smell
        G.add_edge('Move method', 'CYCLICALLY-DEPENDENT MODULARIZATION')  # Design smell
        G.add_edge('Move method', 'HUB-LIKE MODULARIZATION')  # Design smell
        G.add_edge('Move method', 'CYCLIC HIERARCHY')  # Design smell

        G.add_edge('Move class', 'MISPLACED CLASS')  # TACO

        G.add_edge('Push down field', 'REFUSED BEQUEST')
        G.add_edge('Push down method', 'REFUSED BEQUEST')
        G.add_edge('Pull-up field', 'UNFACTORED HIERARCHY')  # Design smell
        G.add_edge('Pull-up method', 'UNFACTORED HIERARCHY')  # Design smell
        G.add_edge('Pull-up method', 'DUPLICATED CODE')
        G.add_edge('Pull-up constructor body', 'DUPLICATED CODE')

        # 2
        G.add_edge('Extract method', 'DUPLICATED CODE')
        G.add_edge('Extract method', 'MUTABLE DATA')
        G.add_edge('Extract method', 'DIVERGENT CHANGE')
        G.add_edge('Extract method', 'FEATURE ENVY')
        G.add_edge('Extract method', 'MESSAGE CHAINS')
        G.add_edge('Extract method', 'LONG METHOD')

        G.add_edge('Inline method', 'SHOTGUN SURGERY')
        G.add_edge('Inline method', 'MIDDLE MAN')
        G.add_edge('Inline method', 'SPECULATIVE GENERALITY')

        G.add_edge('Extract class', 'LONG PARAMETER LIST')
        G.add_edge('Extract class', 'DIVERGENT CHANGE')
        G.add_edge('Extract class', 'DATA CLUMPS')
        G.add_edge('Extract class', 'PRIMITIVE OBSESSION ')
        G.add_edge('Extract class', 'TEMPORARY FIELD')
        G.add_edge('Extract class', 'LARGE CLASS/MULTIFACETED ABSTRACTION')  # Design smell
        G.add_edge('Extract class', 'CYCLIC HIERARCHY')  # Design smell

        G.add_edge('Extract subclass', 'DUPLICATED CODE')
        G.add_edge('Extract subclass', 'PRIMITIVE OBSESSION')

        G.add_edge('Inline class', 'SHOTGUN SURGERY')
        G.add_edge('Inline class', 'SPECULATIVE GENERALITY')
        G.add_edge('Inline class', 'UNNECESSARY ABSTRACTION')  # Design smell

        G.add_edge('Extract/Split package', 'PROMISCUOUS PACKAGE')  # TACO
        G.add_edge('Merge packages', 'SPECULATIVE GENERALITY')  # Introduce by Morteza

        # 3
        G.add_edge('Collapse hierarchy', 'SPECULATIVE HIERARCHY')  # Design smell
        G.add_edge('Collapse hierarchy', 'DEEP HIERARCHY')  # Design smell

        # 4
        G.add_edge('Encapsulate field', 'GLOBAL DATA')
        G.add_edge('Encapsulate field', 'MUTABLE DATA')

        # 5
        G.add_edge('Remove control flag', 'LONG METHOD')
        G.add_edge('Remove control flag', 'LONG PARAMETER LIST')
        G.add_edge('Remove flag argument', 'LONG PARAMETER LIST')
        G.add_edge('Remove field', 'MYSTERIOUS NAME')
        G.add_edge('Remove field', 'LONG PARAMETER LIST')
        G.add_edge('Remove method', 'REBELLIOUS HIERARCHY')  # Design smell
        G.add_edge('Remove Dead Code', 'DEAD CODE')

        # 6
        G.add_edge('Rename entity', 'MYSTERIOUS NAME')

        # 7
        G.add_edge('Replace conditional with polymorphism', 'REPEATED SWITCHES')
        G.add_edge('Replace parameter with query', 'LONG METHOD')
        G.add_edge('Replace parameter with query', 'LONG PARAMETER LIST')

        G.add_edge('Replace constructor with factory function', 'NULL')  # Not set!
        G.add_edge('Replace exception with test (prechek)', 'NULL')  # Not set!
        G.add_edge('Replace nested conditional with guard clauses', 'NULL')  # Not set!
        G.add_edge('Replace control flag with break', 'NULL')  # Not set!

        # 8
        G.add_edge('Decrease field visibility', 'DEFICIENT ENCAPSULATION')  # Design smell
        G.add_edge('Increase field visibility', 'NULL')  # Not set!
        G.add_edge('Decrease method visibility', 'NULL')  # Not set!
        G.add_edge('Increase method visibility', 'NULL')  # Not set!

        # 9
        G.add_edge('Extract interface', 'NULL')  # Not set!
        G.add_edge('Make class abstract', 'NULL')  # Not set!
        G.add_edge('Make class concrete', 'NULL')  # Not set!

        # 10
        G.add_edge('Make field static', 'NULL')  # Not set!
        G.add_edge('Make field non-static', 'NULL')  # Not set!
        G.add_edge('Make method static', 'NULL')  # Not set!
        G.add_edge('Make method non- static', 'NULL')  # Not set!
        G.add_edge('Make field final', 'NULL')  # Not set!
        G.add_edge('Make field non-final', 'NULL')  # Not set!
        G.add_edge('Make method final', 'NULL')  # Not set!
        G.add_edge('Make method non-final', 'NULL')  # Not set!
        G.add_edge('Make class-final', 'NULL')  # Not set!
        G.add_edge('Make class non-final', 'NULL')  # Not set!



        # Get all refactorings-smells pairs
        print('all refactorings-smells pairs', G.edges)
        print('nodes', G.nodes)
        print('Number all refactorings-smells pairs', len(G.edges))

        # Get refactorings without specific smells
        print('refactorings without specific smells', G.in_degree(['NULL']))

        nx.write_edgelist(G=G, path='RefactoringSmells.csv', delimiter=',')

map = Mapper()
