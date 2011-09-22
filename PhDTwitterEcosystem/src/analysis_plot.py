#! /usr/bin/python

# To change this template, choose Tools | Templates
# and open the template in the editor.

__author__="jianhuashao"
__date__ ="$Sep 16, 2011 12:38:27 PM$"


import numpy as np
import matplotlib.pyplot as plt

figure = plt.figure()
stacked_bar_bottom = [0]*20
stacked_bars = []

def set_stacked_bar_bottom(index_count):
    global stacked_bar_bottom
    stacked_bar_bottom = [0]*index_count

def show():
    global plt
    plt.show()

def developer_to_mashup_line_plot(developers, mashups):
    global figure
    ax_developer_to_mashup = figure.add_subplot(1, 1, 1)
    ax_developer_to_mashup.plot(developers, mashups, lw=4, color='b', label="Mashups count")
def developer_to_mashup_dot_plot(developers, mashups):
    global figure
    ax_developer_to_mashup = figure.add_subplot(1, 1, 1)
    ax_developer_to_mashup.plot(developers, mashups, 'o', lw=4, color='k')

    
def developer_to_api_dot_plot(developers, mashups):
    global figure
    ax_developer_to_mashup = figure.add_subplot(1, 1, 1)
    ax_developer_to_mashup.plot(developers, mashups, lw=4, color='y', label="APIs count")
    
def get_stacked_bar_axx(x=1, y=1, z=1):
    global figure
    stacked_bar_axx = figure.add_subplot(x, y, z)
    return stacked_bar_axx

def developer_to_api_bar_plot(developers, apis, axx, stack_color, api_name):
    global stacked_bar_bottom
    print len(stacked_bar_bottom), len(apis), "***************"
    stacked_bar = axx.bar(
        developers, 
        apis, 
        1,
        bottom=stacked_bar_bottom,
        color=stack_color,
        facecolor=stack_color,
        label=api_name
        )
    stacked_bars.append(stacked_bar)
    stacked_bar_bottom = [y1+y2 for (y1, y2) in zip(stacked_bar_bottom, apis)]



    
def developer_to_api_bar_annotate(text, x1, y1, x2, y2):
    plt.annotate(
        text, 
        xy=(x1, y1), 
        xytext=(x2, y2), 
        arrowprops=dict(
            arrowstyle="simple",
            ),
        )

def set_max_y(max):
    plt.axis(ymax=max)
def set_max_x(max):
    plt.axis(xmax=max)
def set_min_y(max):
    plt.axis(ymin=max)
def set_min_x(max):
    plt.axis(xmin=max)

def developer_to_api_bar_legend(axx, api_names):
    #axx.legend(stacked_bars[0], "hello")
    #axx.legend((stacked_bars, api_names))
    axx.set_xlabel("Developer IDs")
    axx.legend()
    
def set_title(title):
    plt.title(title)
    

if __name__ == "__main__":
    main()
    print "Hello World";
