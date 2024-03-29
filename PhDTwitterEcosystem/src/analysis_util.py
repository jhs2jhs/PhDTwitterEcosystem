#! /usr/bin/python

# To change this template, choose Tools | Templates
# and open the template in the editor.

__author__="jianhuashao"
__date__ ="$Sep 17, 2011 8:16:54 PM$"

from my_util import cmd_p, db_conn
conn = db_conn()
analysis_path = "../analysis/"

def db_execute(sql, params):
    global conn
    c = conn.cursor()
    #print sql
    c.execute(sql, params)
    return c

def db_loop(c, file_name):
    global analysis_path
    txt = open(analysis_path+file_name+".txt", "w")
    head = "index"
    for colum_name in c.description:
        head = head + ", \t"+str(colum_name[0])
    print head
    txt.write(head+"\n")
    i = 1
    for row in c:
        out = str(i)
        for r in row:
            out = out+"\t"+str(r)
        print out
        txt.write(out+"\n")
        i = i+1

def db_loop_for_array(c, file_name, element_index):
    global analysis_path
    lists = []
    txt = open(analysis_path+file_name+".txt", "w")
    head = "index"
    for colum_name in c.description:
        head = head + ", \t"+str(colum_name[0])
    print head
    txt.write(head+"\n")
    i = 1
    for row in c:
        out = str(i)
        lists.append(row[element_index])
        for r in row:
            out = out+"\t"+str(r)
        print out
        txt.write(out+"\n")
        i = i+1
    return lists


def template():
    sql_params = (1, )
    rows = db_execute(developer_to_mashup, sql_params)
    db_loop(rows, "template_o")


############# developer_index_temp ############# 
developer_index_table_dropx = '''
    DROP TABLE IF EXISTS developer_index_temp
'''
developer_index_table_create = '''
    CREATE TABLE developer_index_temp (
        developer_index INTEGER PRIMARY KEY ,
        developer_id INTEGER NOT NULL,
        UNIQUE (developer_index, developer_id)
    )
'''
def developer_index_tmp_table_init():
    global conn
    c = conn.cursor()
    c.execute(developer_index_table_dropx, )
    conn.commit()
    c.execute(developer_index_table_create, )
    conn.commit()
    
   

developer_index_table_update = '''
    INSERT OR IGNORE INTO developer_index_temp (developer_index, developer_id) VALUES (?, ?)
'''
def developer_index_tmp_table_update(developer_index, developer_id):
    global conn
    c = conn.cursor()
    c.execute(developer_index_table_update, (developer_index, developer_id, ))
    print developer_id
    conn.commit()

develop_index_table_check = '''
    SELECT 
        developer_index_temp.developer_index, 
        developer_index_temp.developer_id
    FROM developer_index_temp
    ORDER BY developer_index_temp.developer_index
'''
def developer_index_tmp_table_check():
    global conn
    c = conn.cursor()
    c.execute(develop_index_table_check, )
    db_loop(c, "developer_index_tmp_table_check_o")
############# developer_index_temp ############# 



def get_developer_length(arrange_developer_sql_length, i):
    global conn
    c = conn.cursor()
    #print arrange_developer_sql_length
    c.execute(arrange_developer_sql_length, )
    developer_length = c.fetchone()[i]
    return developer_length


############# sqlite3 self defined function ############# 
sqlite_function_create_test = '''
    SELECT 
        author_mashup.author_id, 
        COUNT(author_mashup.mashup_id) AS mashup_count
    FROM author_mashup
    GROUP BY
        author_mashup.author_id
    ORDER BY 
        mashup_count DESC
'''
sqlite_function_create_test_test = '''
    SELECT 
        test.author_id,
        test.mashup_count,
        auto_index(test.mashup_count) AS i_index
    FROM ('''+sqlite_function_create_test+''') AS test
    ORDER BY
        test.mashup_count DESC
'''
i_index = 0
def auto_index(s):
    global i_index
    i_index += 1
    print  i_index, s
    return i_index
def sqlite_function_create_test_o():
    global conn, i_index
    i_index = 0
    conn.create_function('auto_index', 1, auto_index)
    c = conn.cursor()
    print sqlite_function_create_test_test
    c.execute(sqlite_function_create_test_test, )
    db_loop(c, "sqlite_function_create_test_o")


sqlite_function_aggreation_test = '''
    SELECT 
        author_mashup.author_id, 
        COUNT(author_mashup.mashup_id) AS mashup_count,
        auto_index(author_mashup.author_id) AS i_index
    FROM author_mashup
    GROUP BY
        author_mashup.author_id
    ORDER BY 
        mashup_count DESC
'''
i_index = 0
class AutoIndex(object):
    #global i_index
    def __init__(self):
        global i_index 
        self.i = i_index
    def step(self, value):
        print value
        #self.i += 1
    def finalize(self):
        global i_index
        i_index += 1
        return i_index + 1
def sqlite_function_aggreation_test_o():
    global conn, i_index
    i_index = 0
    conn.create_aggregate('auto_index', 1, AutoIndex)
    c = conn.cursor()
    print sqlite_function_aggreation_test
    c.execute(sqlite_function_aggreation_test, )
    db_loop(c, "sqlite_function_aggreation_test_o")

############# sqlite3 self defined function ############# 











############# develop pioneer rate ######################
############# developer_api_pioneer_rate ############# 
api_author_count_table_dropx = '''
    DROP TABLE IF EXISTS api_author_count_temp
'''
api_author_count_table_create = '''
    CREATE TABLE api_author_count_temp (
        id INTEGER PRIMARY KEY,
        api_id INTEGER NOT NULL ,
        developer_count INTEGER NOT NULL,
        mashup_count INTEGER NOT NULL,
        FOREIGN KEY (api_id) REFERENCES api(api_id)
    )
'''
api_developer_date_table_dropx = '''
    DROP TABLE IF EXISTS api_developer_date_temp
'''
api_developer_date_table_create = '''
    CREATE TABLE api_developer_date_temp (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        api_id INTEGER NOT NULL ,
        mashup_id INTEGER NOT NULL, 
        developer_id INTEGER NOT NULL,
        date INTEGER NOT NULL,
        FOREIGN KEY (developer_id) REFERENCES author(author_id),
        FOREIGN KEY (api_id) REFERENCES api(api_id),
        FOREIGN KEY (mashup_id) REFERENCES mashup(mashup_id)
    )
'''
developer_api_pioneer_rate_table_dropx = '''
    DROP TABLE IF EXISTS developer_api_pioneer_rate_temp
'''
developer_api_pioneer_rate_table_create = '''
    CREATE TABLE developer_api_pioneer_rate_temp (
        id INTEGER PRIMARY KEY,
        developer_id INTEGER NOT NULL ,
        api_id INTEGER NOT NULL,
        pioneer_position INTEGER NOT NULL,
        mashup_counts INTEGER NOT NULL, 
        FOREIGN KEY (developer_id) REFERENCES author(author_id),
        FOREIGN KEY (api_id) REFERENCES api(api_id),
        UNIQUE (developer_id, api_id)
    )
'''
developer_api_pioneer_rate_mashups_table_dropx = '''
    DROP TABLE IF EXISTS developer_api_pioneer_rate_mashups_temp
'''
developer_api_pioneer_rate_mashups_table_create = '''
    CREATE TABLE developer_api_pioneer_rate_mashups_temp (
        id INTEGER PRIMARY KEY,
        developer_id INTEGER NOT NULL ,
        api_id INTEGER NOT NULL,
        mashup_counts INTEGER NOT NULL, 
        pioneer_position_rate REAL NOT NULL,
        pioneer_mashup_rate REAL NOT NULL,
        FOREIGN KEY (developer_id) REFERENCES author(author_id),
        FOREIGN KEY (api_id) REFERENCES api(api_id),
        UNIQUE (developer_id, api_id)
    )
'''
def pioneer_rate_tmp_table_init():
    global conn
    c = conn.cursor()
    #
    c.execute(api_author_count_table_dropx, )
    conn.commit()
    c.execute(api_author_count_table_create, )
    conn.commit()
    #
    c.execute(api_developer_date_table_dropx, )
    conn.commit()
    c.execute(api_developer_date_table_create, )
    conn.commit()
    #
    c.execute(developer_api_pioneer_rate_table_dropx, )
    conn.commit()
    c.execute(developer_api_pioneer_rate_table_create, )
    conn.commit()
    #
    c.execute(developer_api_pioneer_rate_mashups_table_dropx, )
    conn.commit()
    c.execute(developer_api_pioneer_rate_mashups_table_create, )
    conn.commit()
    print "init finish"
    
api_author_count_table_update = '''
    INSERT OR IGNORE INTO api_author_count_temp (api_id, developer_count, mashup_count) VALUES (?, ?, ?)
'''
def api_author_count_tmp_table_update(api_id, developer_count, mashup_count):
    global conn
    c = conn.cursor()
    c.execute(api_author_count_table_update, (api_id, developer_count, mashup_count, ))
    #print developer_count
    conn.commit()
api_developer_date_table_update = '''
    INSERT OR IGNORE INTO api_developer_date_temp (api_id, mashup_id, developer_id, date) VALUES (?, ?, ?, ?)
'''
def api_developer_date_tmp_table_update(api_id, mashup_id, developer_id, datestring):
    global conn
    c = conn.cursor()
    c.execute(api_developer_date_table_update, (api_id, mashup_id, developer_id, datestring, ))
    #print "cool: "+str(datestring)
    conn.commit()
developer_api_pioneer_rate_table_update = '''
    INSERT OR IGNORE INTO developer_api_pioneer_rate_temp (developer_id, api_id, pioneer_position, mashup_counts) VALUES (?, ?, ?, ?)
'''
def developer_api_pioneer_rate_tmp_table_update(developer_id, api_id, pioneer_position, mashup_counts):
    global conn
    c = conn.cursor()
    c.execute(developer_api_pioneer_rate_table_update, (developer_id, api_id, pioneer_position, mashup_counts, ))
    #print "cool: "+str(mashup_counts)
    conn.commit()
developer_api_pioneer_rate_mashups_table_update = '''
    INSERT OR IGNORE INTO developer_api_pioneer_rate_mashups_temp (developer_id, api_id, mashup_counts, pioneer_position_rate, pioneer_mashup_rate) VALUES (?, ?, ?, ?, ?)
'''
def developer_api_pioneer_rate_mashups_tmp_table_update(developer_id, api_id, mashup_counts, pioneer_position_rate, pioneer_mashup_rate):
    global conn
    c = conn.cursor()
    c.execute(developer_api_pioneer_rate_mashups_table_update, (developer_id, api_id, mashup_counts, pioneer_position_rate, pioneer_mashup_rate, ))
    #print "cool: "+str(mashup_counts)
    conn.commit()
############# develop pioneer rate ######################



if __name__ == "__main__":
    print "Hello World";
