# To change this template, choose Tools | Templates
# and open the template in the editor.

__author__="jianhuashao"
__date__ ="$Sep 6, 2011 12:39:30 AM$"

from my_util import cmd_p
import web_api 
import web_mashup 
import sqlite_init 

if __name__ == "__main__":
    sqlite_init.sqlite_init()
    web_api.apis_pages_read()
    web_api.apis_db_write()
    web_mashup.mashups_pages_read()
    print "Hello World"
