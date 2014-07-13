#! /bin/python3
# -*- coding : utf-8 -*-

from i3 import command, get_workspaces, i3Exception
from argparse import ArgumentParser
from logging import INFO, WARNING, basicConfig, info, critical


# only workspaces with numbers are managed (binded to super+nb by default)
ALLOWED = [str(i+1) for i in range(10)]   

def parseArguments() :
    """
    Parse the command line arguments.

    return : (count, right), verbose
           : shiftworkspaces_parameters, verbose
    """

    parser = ArgumentParser()
    parser.add_argument('-c', '--count', type=int, default=9, choices=range(10), help='Maximum shift allowed')
    parser.add_argument('-r', '--right', action='store_true', help='Reverse shift direction')
    parser.add_argument('-v', '--verbose', action='store_true')
    args = parser.parse_args()

    return (args.count, args.right), args.verbose


def shift_workspaces(count, right):
    """
    Shift the workspaces. 

    count : maximum shift allowed (typically between 0 and 9)
    right : reverse shift direction if True
    return : 0 on success, 1 on error
    """

    # initial workspace setup
    workspaces = [None] * 10
    for name in [w['name'] for w in get_workspaces()]:
        if name in ALLOWED :
            workspaces[int(name)-1] = name 
    info('Initial workspaces={}' .format(workspaces))

    # optimal workspace setup 
    changes = [ws for ws in workspaces if ws!= None]
    info('Optimal workspaces={}' .format(changes))

    # deduce swaps to make (considering count parameter)
    commits= []
    offset = 10-len(changes) if right else 0
    
    for index, ws in enumerate(changes):
        src, target = int(ws), index + 1 + offset
        if src != target:
            if right :
                final = src +(min(count,target - src))
            else :
                final = src - (min(count,src - target))
            commits.append( (src,final) )

    # apply changes in right order
    if right:
        commits.reverse()
    try :
        for (src,final) in commits:        
            info('Moving workspace {}->{}'.format(src, final))
            command('rename workspace {} to {}'.format(src, final))
    except i3Exception:
        critical('Communication with i3 failed')
        return 1
    info('{} swaps were made.'.format(len(commits)))
    return 0


def leftshift_possible():
    """
    Check that a default left shift is useful

    return: True if a default shift would change anything
    """
    
    # Get workspaces setup
    ws = [None] * 10
    for name in [w['name'] for w in get_workspaces()]:
        if name in ALLOWED :
            ws[int(name)-1] = name 

    # Verify
    if len(set(ws[-ws.count(None):]))==1:
        return False
    return True



if __name__=='__main__':
    params, verbose = parseArguments()
    basicConfig(level=INFO if verbose else WARNING)
    exit_code = shift_workspaces( *params )
    exit(exit_code)

