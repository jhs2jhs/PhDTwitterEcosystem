# To change this template, choose Tools | Templates
# and open the template in the editor.

__author__="jianhuashao"
__date__ ="$Sep 6, 2011 12:44:22 AM$"

import sqlite3


sqlite_file_path = "../db/programableweb.db"
sqlite_analysis_path = "../analysis/"

def db_conn(): 
    conn = sqlite3.connect(sqlite_file_path)
    return conn

def cmd_p(text):
    print "==",text,"=="


if __name__ == "__main__":
    print "Hello World"
