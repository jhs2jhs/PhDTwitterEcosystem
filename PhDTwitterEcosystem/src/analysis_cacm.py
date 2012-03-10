#! /usr/bin/python

# To change this template, choose Tools | Templates
# and open the template in the editor.

__author__="jianhuashao"
__date__ ="$Oct 5, 2011 11:14:15 PM$"


from my_util import cmd_p, db_conn
from analysis_util import db_execute, db_loop_for_array
import analysis_util
conn = db_conn()
analysis_path = "../analysis/CACM/"


def element_loop(c):
    global analysis_path
    out = ""
    i = 0
    for row in c:
        if (i > 0):
            out = out+", "
        out = out+str(row[0])
        i = i + 1
        #print out
    return out

def api_db_loop(c, file_name):
    global analysis_path
    txt = open(analysis_path+file_name+".txt", "w")
    head = "index"
    for colum_name in c.description:
        head = head + ", \t"+str(colum_name[0])
    head = head + ", \tprotocols"
    head = head + ", \tdataformats"
    head = head + ", \t"
    head = head + ", \tmashup_full_url"
    head = head + ", \tmashup_if_free"
    head = head + ", \tmashup_other_comments"
    print head
    txt.write(head+"\n")
    i = 1
    for row in c:
        out = str(i)
        for r in row:
            out = out+"\t"+str(r)
        api_id = row[5]
        sql_params = (api_id, )
        rows_p = db_execute(api_protocol, sql_params)
        protocols = element_loop(rows_p)
        out = out+"\t"+protocols
        rows_d = db_execute(api_dataformats, sql_params)
        dataformats = element_loop(rows_d)
        out = out+"\t"+dataformats
        print out
        out = out+"\t"
        mashup_part_url = row[3]
        mashup_full_url = "http://www.programmableweb.com"+row[3]
        out = out+"\t"+mashup_full_url
        out = out+"\t"
        out = out+"\t"
        print out
        txt.write(out+"\n")
        i = i+1
        
def db_loop(c, file_name):
    global analysis_path
    txt = open(analysis_path+file_name+".txt", "w")
    head = "index"
    for colum_name in c.description:
        head = head + ", \t"+str(colum_name[0])
    head = head + ", \t"
    head = head + ", \tmashup_full_url"
    head = head + ", \tmashup_if_free"
    head = head + ", \tmashup_other_comments"
    print head
    txt.write(head+"\n")
    i = 1
    for row in c:
        out = str(i)
        for r in row:
            out = out+"\t"+str(r)
        print out
        out = out+"\t"
        mashup_part_url = row[3]
        mashup_full_url = "http://www.programmableweb.com"+row[3]
        out = out+"\t"+mashup_full_url
        out = out+"\t"
        out = out+"\t"
        print out
        txt.write(out+"\n")
        i = i+1


api_dataformats = '''
SELECT 
    dataformat.dataformat_name 
FROM api, dataformat_api, dataformat
WHERE
    api.api_id = dataformat_api.api_id AND 
    dataformat_api.dataformat_id = dataformat.dataformat_id AND 
    api.api_id = ?
'''
api_protocol = '''
SELECT 
    protocol.protocol_name 
FROM api, protocol_api, protocol
WHERE
    api.api_id = protocol_api.api_id AND 
    protocol_api.protocol_id = protocol.protocol_id AND 
    api.api_id = ?
'''



developer_mashup_api_category_dataformat = '''
SELECT 
    developer_index_temp.developer_index,
    author.author_id, 
    author.author_url, 
    mashup.mashup_url,
    date.date AS mashup_date,
    api.api_id, 
    api.api_url,
    api.api_date AS api_date, 
    category.category_name
FROM 
    (SELECT * FROM developer_index_temp LIMIT ? ) AS developer_index_temp, author, 
    author_mashup, mashup, date_mashup, date,
    mashup_api, api, 
    api_category, category
WHERE
    developer_index_temp.developer_id = author.author_id AND 
    author.author_id = author_mashup.author_id AND 
    author_mashup.mashup_id = mashup.mashup_id AND 
    mashup.mashup_id = date_mashup.mashup_id AND 
    date_mashup.date_id = date.date_id AND
    mashup.mashup_id = mashup_api.mashup_id AND  
    mashup_api.api_id = api.api_id AND 
    api.api_id = api_category.api_id AND 
    api_category.category_id = category.category_id 
ORDER BY 
    developer_index_temp.developer_index
'''
def developer_mashup_api_category_dataformat_o(developer_number):
    sql_params = (developer_number, )
    rows = db_execute(developer_mashup_api_category_dataformat, sql_params)
    api_db_loop(rows, "CACM_developer_mashup_api_category_dataformat_"+str(developer_number)+"_o")




developer_mashup = '''
SELECT 
    developer_index_temp.developer_index,
    author.author_id, 
    author.author_url, 
    mashup.mashup_url,
    date.date AS mashup_date
FROM 
    (SELECT * FROM developer_index_temp LIMIT ? ) AS developer_index_temp, author, 
    author_mashup, mashup, date_mashup, date
WHERE
    developer_index_temp.developer_id = author.author_id AND 
    author.author_id = author_mashup.author_id AND 
    author_mashup.mashup_id = mashup.mashup_id AND 
    mashup.mashup_id = date_mashup.mashup_id AND 
    date_mashup.date_id = date.date_id 
ORDER BY 
    developer_index_temp.developer_index
'''
def developer_mashup_o(developer_number):
    sql_params = (developer_number, )
    rows = db_execute(developer_mashup, sql_params)
    db_loop(rows, "CACM_developer_mashup_"+str(developer_number)+"_o")





used_api_developer = '''
SELECT 
    developer_index_temp.developer_index,
    author.author_id,
    author.author_url, 
    api.api_id, 
    api.api_url
FROM 
    (SELECT * FROM developer_index_temp LIMIT ? ) AS developer_index_temp, author, 
    author_mashup, mashup, 
    mashup_api, api
WHERE
    developer_index_temp.developer_id = author.author_id AND 
    author.author_id = author_mashup.author_id AND 
    author_mashup.mashup_id = mashup.mashup_id AND 
    mashup.mashup_id = mashup_api.mashup_id AND  
    mashup_api.api_id = api.api_id 
ORDER BY 
    developer_index_temp.developer_index
'''
used_api = '''
SELECT 
    developer_api.api_id,
    developer_api.api_url
FROM 
    ('''+used_api_developer+''') AS developer_api
GROUP BY 
    developer_api.api_id
ORDER BY 
    developer_api.api_id
'''
api_developer_count_pre = '''
SELECT 
    author.author_id,
    author.author_url
FROM 
    author, 
    author_mashup, mashup, 
    mashup_api
WHERE
    author.author_id = author_mashup.author_id AND 
    author_mashup.mashup_id = mashup.mashup_id AND 
    mashup.mashup_id = mashup_api.mashup_id AND 
    mashup_api.api_id = ? 
'''
api_developer_count_middle = '''
SELECT 
    developer_api.author_id,
    developer_api.author_url
FROM 
    ('''+api_developer_count_pre+''') AS developer_api
GROUP BY 
    developer_api.author_url
ORDER BY 
    developer_api.author_url
'''
api_developer_count = '''
SELECT 
    COUNT (developer_api.author_url) AS developer_count
FROM 
    ('''+api_developer_count_middle+''') AS developer_api
'''
api_mashup_count_pre = '''
SELECT 
    mashup.mashup_id,
    mashup.mashup_url
FROM 
    author, 
    author_mashup, mashup, 
    mashup_api
WHERE
    author.author_id = author_mashup.author_id AND 
    author_mashup.mashup_id = mashup.mashup_id AND 
    mashup.mashup_id = mashup_api.mashup_id AND 
    mashup_api.api_id = ? 
'''
api_mashup_count_middle = '''
SELECT 
    developer_api.mashup_id,
    developer_api.mashup_url
FROM 
    ('''+api_mashup_count_pre+''') AS developer_api
GROUP BY 
    developer_api.mashup_url
ORDER BY 
    developer_api.mashup_url
'''
api_mashup_count = '''
SELECT 
    COUNT (developer_api.mashup_url) AS developer_count
FROM 
    ('''+api_mashup_count_middle+''') AS developer_api
'''

api_developer_mashup_count_condition_pre = '''
SELECT 
    mashup.mashup_id,
    COUNT (mashup_api.api_id) api_count
FROM 
    mashup, 
    mashup_api
WHERE
    mashup.mashup_id = mashup_api.mashup_id
GROUP BY 
    mashup.mashup_id
ORDER BY 
    mashup.mashup_id
'''
api_developer_mashup_count_condition_middle = '''
SELECT 
    author.author_id,
    author.author_url, 
    api_developer_mashup.mashup_id,
    api_developer_mashup.api_count
FROM 
    author, 
    author_mashup, 
    ('''+api_developer_mashup_count_condition_pre+''') AS api_developer_mashup,
    ('''+api_developer_count_middle+''') AS api_developer
WHERE 
    author.author_id = author_mashup.author_id AND 
    author_mashup.mashup_id = api_developer_mashup.mashup_id AND 
    api_developer.author_id = author.author_id 
GROUP BY 
    author.author_url
ORDER BY 
    author.author_url
'''
api_developer_count_condition_large = '''
SELECT 
    COUNT (developer_api.author_url) AS developer_count
FROM 
    ('''+api_developer_mashup_count_condition_middle+''') AS developer_api
WHERE 
    developer_api.api_count > ?
'''
api_developer_count_condition_small = '''
SELECT 
    COUNT (developer_api.author_url) AS developer_count
FROM 
    ('''+api_developer_mashup_count_condition_middle+''') AS developer_api
WHERE 
    developer_api.api_count <= ?
'''
def db_loop_api_usage(c, developer_number, cut_number, file_name):
    global analysis_path
    txt = open(analysis_path+file_name+".txt", "w")
    head = "index"
    for colum_name in c.description:
        head = head + ", \t"+str(colum_name[0])
    head = head + ", \tdeveloper_used"
    head = head + ", \tmashup_used"
    head = head + ", \tlow_end_mashup"
    head = head + ", \thigh_end_mashup"
    print head
    txt.write(head+"\n")
    i = 1
    for row in c:
        out = str(i)
        for r in row:
            out = out+"\t"+str(r)
        #print out
        api_id = row[0]
        #print api_id
        sql_params = (api_id, )
        rows = db_execute(api_developer_count, sql_params)
        developer_count = rows.fetchone()[0]
        sql_params = (api_id, )
        rows = db_execute(api_mashup_count, sql_params)
        mashup_count = rows.fetchone()[0]
        #print developer_count, mashup_count
        out = out+"\t"+str(developer_count)+"\t"+str(mashup_count)
        sql_params = (api_id, cut_number, )
        rows = db_execute(api_developer_count_condition_small, sql_params)
        api_developer_small = rows.fetchone()[0]
        sql_params = (api_id, cut_number, )
        rows = db_execute(api_developer_count_condition_large, sql_params)
        api_developer_large = rows.fetchone()[0]
        #print api_developer_small, api_developer_large
        out = out+"\t"+str(api_developer_small)+"\t"+str(api_developer_large)
        #print developer_condition_count
        print out
        txt.write(out+"\n")
        i = i+1
def api_usage_o(developer_number, cut_number):
    sql_params = (developer_number, )
    rows = db_execute(used_api, sql_params)
    db_loop_api_usage(rows, developer_number, cut_number, "CACM_api_usage_"+str(cut_number)+"_"+str(developer_number)+"_o")



developer_api_count = '''
    SELECT 
        author.author_url, 
        author_mashup.author_id, 
        COUNT(DISTINCT mashup_api.api_id) AS api_count,
        developer_index_temp.developer_index
    FROM 
        (SELECT * FROM developer_index_temp LIMIT ? ) AS developer_index_temp, author, 
        author_mashup, mashup_api
    WHERE
        developer_index_temp.developer_id = author.author_id AND 
        author.author_id = author_mashup.author_id AND 
        author_mashup.mashup_id = mashup_api.mashup_id
    GROUP BY 
        author_mashup.author_id
    ORDER BY 
        developer_index_temp.developer_index, api_count DESC
'''

def developer_api_count_o(developer_number):    
    sql_params = (developer_number, )
    rows = db_execute(developer_api_count, sql_params)
    analysis_util.db_loop(rows, "CACM_developer_api_count_"+str(developer_number)+"_o")

developer_mashup_api_count = '''
    SELECT 
        mashup_api.mashup_id, 
        COUNT (mashup_api.api_id) AS mashup_apis
    FROM mashup_api
    GROUP BY 
        mashup_api.mashup_id
'''
developer_mashup_count = '''
    SELECT 
        author_mashup.author_id, 
        COUNT(author_mashup.mashup_id) AS mashup_count,
        AVG (mashup_api_count.mashup_apis) AS mashup_api_avg
    FROM 
        ('''+developer_mashup_api_count+''') AS mashup_api_count,
        author_mashup
    WHERE 
        mashup_api_count.mashup_id = author_mashup.mashup_id
    GROUP BY
        author_mashup.author_id
    ORDER BY 
        mashup_count DESC
'''
developer_api_mashup_count = '''
    SELECT 
        developer_api.author_url, 
        developer_api.author_id, 
        developer_api.api_count, 
        developer_mashup.mashup_count, 
        developer_mashup.mashup_api_avg
    FROM 
        ('''+developer_api_count+''') AS developer_api,
        ('''+developer_mashup_count+''') AS developer_mashup
    WHERE
        developer_api.author_id = developer_mashup.author_id 
    ORDER BY 
        developer_api.developer_index
'''
def developer_api_mashup_count_o(developer_number):    
    sql_params = (developer_number, )
    rows = db_execute(developer_api_mashup_count, sql_params)
    analysis_util.db_loop(rows, "CACM_developer_api__mashup_count_"+str(developer_number)+"_o")


if __name__ == "__main__":
    print "Hello World";
    developer_mashup_api_category_dataformat_o()
