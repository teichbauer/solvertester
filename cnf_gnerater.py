# -----------------------------------------------------------------------------
# 2020-04-21
# ------------ Raymond Wei ----------------------------------------------------
# https://fairmut3x.wordpress.com/2011/07/29
#       /cnf-conjunctive-normal-form-dimacs-format-explained/
# cnf file format
# comment lines start with a 'c'
# parameter line starts with a 'p'
# every clause line ends with a 0
# n variables are represented by 1..n
# Example, for expression
#
#     (A v ¬B v C) ^ (B v D v E) ^ (D V F)
#
#     A,B,C,D,E,F  are represented by
#     1,2,3,4,5,6
#
# negative number represent NOT/¬
#     c This is a comment
#     c This is another comment
#     p cnf 6 3
#     1 -2 3 0
#     2 4 5 0
#     4 6 0
# =============================================================================
# the class Generator generates such a file, by taking
# nov : number of variables (n in above), and
# nok : number of clauses
# output files are stored under ./data/
# =============================================================================

import random


class Generator:
    def __init__(self, nov, nok):
        self.nov = nov
        self.nok = nok
        self.datadir = 'data'

    def generate(self):
        pass
