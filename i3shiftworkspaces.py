#! /bin/python3
# -*- coding : utf-8 -*-

from i3 import command, get_workspaces, i3Exception
from argparse import ArgumentParser
import logging


def parseArguments() :
    parser = ArgumentParser()
    parser.add_argument('-c', '--count', type=int, default=9, choices=range(10), 
                        help='Shifts number (>=0)')
    parser.add_argument('-r', '--right', action='store_true', 
                        help='Shift to the right side')
    parser.add_argument('-v', '--verbose', action='store_true')

    args = parser.parse_args()

    return (args.count, args.right), args.verbose


def shift_workspaces(count, right):

    # only workspaces with numbers are managed (binded to super+nb by default)
    allowed = [str(i+1) for i in range(10)]   

    # initial workspace setup
    workspaces = [None]*10
    for ws in get_workspaces():
        name = ws['name']
        if name in allowed:
            workspaces[int(name)-1] = name
    logging.info('Initial workspaces={}' .format(workspaces))

    # optimal workspace setup 
    changes = [ws for ws in workspaces if ws!= None]
    logging.info('Wanted workspaces={}' .format(changes))

    # deduce swaps to make (considering count parameter)
    commits= []
    offset = 10-len(changes) if right else 0
    
    for index, ws in enumerate(changes):
        src, target = int(ws), index + 1 + offset
        if src != target:
            delta = src - target
            if right==False :
                final = src - (min(count,src - target))
            else :
                final = src +(min(count,target - src))
            commits.append( (src,final) )

    # apply changes in right order
    if right:
        commits.reverse()
    for (src,final) in commits:        
        logging.info('Moving workspace {}->{}'.format(src, final))
        command('rename workspace {} to {}'.format(src, final))


if __name__=='__main__':
    params, verbose = parseArguments()
    if verbose:
        logging.basicConfig(level=logging.INFO)
    
    try :
        shift_workspaces( *params )
    except i3Exception:
        logging.critical('Communication with i3 failed')
        exit(1)
    exit(0)

