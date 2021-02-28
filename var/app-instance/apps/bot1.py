#!/usr/bin/env python
# -*- coding: utf8 -*-
'''
A simple example application that adds a line to a file at regular intervals.
'''

import sys, time

def main():
    name = sys.argv[-1]
    while True:
        print("tik tok")

        with open('sample.txt', 'a') as fp:
            fp.write(f'greetings to {name}\n')
        time.sleep(2)

if __name__ == '__main__':
    main()
