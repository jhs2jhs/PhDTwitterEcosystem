#! /usr/bin/python

# To change this template, choose Tools | Templates
# and open the template in the editor.

__author__="jianhuashao"
__date__ ="$Sep 21, 2011 10:28:00 PM$"


import colorsys

rgbs = []

def create_rgbs(n):
    global rgbs
    HSV_tuples = [(x*1.0/n, 1, 1) for x in range(n)]
    rgbs = map(lambda x: colorsys.hsv_to_rgb(*x), HSV_tuples)
    
def get_rgb(n):
    return rgbs[n]


if __name__ == "__main__":
    print "Hello World";
