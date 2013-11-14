#!/usr/bin/env python
# -*- coding: utf-8 -*-

#######################################################################
#                                                                     #
#   mash.py                                                           #
#     Zach Lamberty                                                   #
#     10 - 17 - 2013                                                  #
#                                                                     #
#     Oh, the places you'll go                                        #
#                                                                     #
#######################################################################

import os
import scipy
import random

from MASHOptions import MASH_OPTIONS

#-----------------------#
#   Module Constants    #
#-----------------------#

MASHKeys = 'Advisor', 'Career', 'Publications', 'Hours of Free Time', 'Coffee Hour Snack'
L = len(MASHKeys)
Z = 5

#   Colors  #
BOLD = '\033[1m'
HEADER = BOLD + '\033[95m'
TRUE = BOLD + '\033[92m'
FALSE = '\033[91m'
END = '\033[0m'
COLOR_DIC = {True: TRUE, False: FALSE}

#   Printing
TRUNC_LEN = 35
FORMAT_STRING = '{:<' + str(TRUNC_LEN) + '}'

#-----------------------#
#   Whole Enchilada     #
#-----------------------#

def updateMASH(mashDic, N):
    """Take one update of the mashDic, using the "current" index

    """
    iNow = mashDic['index']
    mashKeyIndex = (iNow / L) % L
    subInd = iNow % Z

    stepsTaken = 0

    while stepsTaken < N:
        #   Increase iNow by 1 and see where we are
        iNow += 1
        iNow %= L * Z
        mashKeyIndex = (iNow / L) % L
        subInd = iNow % Z

        mashKeyNow = MASHKeys[mashKeyIndex]
        optNow = mashDic[mashKeyNow][subInd]

        if optNow[1] and not keyIsFinished(mashDic, mashKeyNow):
            stepsTaken += 1
        else:
            pass

    mashDic[mashKeyNow][subInd][1] = False


def keyIsFinished(mashDic, key):
    """See if all but one of the keys has been set to false

    """
    return scipy.sum([mashDic[key][i][1] for i in range(Z)]) == 1


def makeMASHDic():
    """Pick a random assortment of Z elements from each category and
    return a dictionary of the form
    { MASHKey : [[a0,True], [a1,True], ... [aZ,True]]}

    """
    mashDic = {'index': 0}
    for key in MASHKeys:
        mashDic[key] = [list(a) for a in zip(random.sample(MASH_OPTIONS[key], Z), [True] * Z)]

    return mashDic


def mashIsFinished(mashDic):
    """Check to see if every key is finished

    """
    return all(keyIsFinished(mashDic, key) for key in MASHKeys)


def printMash(mashDic):
    """Duh

    """
    #   Clear the screen
    os.system('cls' if os.name == 'nt' else 'clear')

    #   Make the print string
    s = ''.join( [HEADER + FORMAT_STRING.format(key) +END for key in MASHKeys] )
    s += '\n'
    for i in range(Z):
        s += ''.join( [COLOR_DIC[mashDic[key][i][1]] + FORMAT_STRING.format(truncateString(mashDic[key][i][0])) + END for key in MASHKeys] )
        s += '\n'

    print s


def truncateString(s):
    """Truncate the string at the length given by TRUNC_LEN

    """
    return s[: TRUNC_LEN - 1]



def main():
    mashDic = makeMASHDic()
    N = random.randint(7, 1000)

    while not mashIsFinished(mashDic):
        updateMASH(mashDic, N)
        printMash(mashDic)
        raw_input()

    return 0

if __name__ == '__main__':
    main()

