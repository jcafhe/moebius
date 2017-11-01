# -*- coding: utf-8 -*-
"""
Created on Sat Oct 28 19:32:22 2017
@author: Jérémie Fache
"""
import sys

def main(args=None):
    print("Lauching moebius")
    if args is None:
        args = sys.argv[1:]

        print('sys.argv:')
        for arg in args:
            print(arg)

    else:
        print('main args')
        for arg in args:
            print(arg)


    print("Exiting moebius")



if __name__ == "__main__":
    print("moebius called from python -m")
    main()
