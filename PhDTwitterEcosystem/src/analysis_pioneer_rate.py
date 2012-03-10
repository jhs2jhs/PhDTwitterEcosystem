#! /usr/bin/python

# To change this template, choose Tools | Templates
# and open the template in the editor.

__author__="jianhuashao"
__date__ ="$Dec 20, 2011 11:53:17 PM$"

from my_util import cmd_p, db_conn
conn = db_conn()
analysis_path = "../analysis/pioneer_rate/"
import analysis_util 
from analysis_util import db_execute, db_loop_for_array
from datetime import datetime
import operator

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
        api_id = row[0]
        developer_count = row[1]
        analysis_util.api_author_count_tmp_table_update(api_id, developer_count)
        out = str(i)
        for r in row:
            out = out+"\t"+str(r)
        print out
        txt.write(out+"\n")
        i = i+1
    


########################
def db_loop_time(c, file_name):
    global analysis_path
    txt = open(analysis_path+file_name+".txt", "w")
    head = "index"
    for colum_name in c.description:
        head = head + ", \t"+str(colum_name[0])
    print head
    txt.write(head+"\n")
    i = 1
    for row in c:
        api_id = row[2]
        developer_id = row[0]
        mashup_id = row[1]
        datestring = row[3]
        #print datestring
        dateobj = datetime.strptime(datestring, '%d %b %Y')
        datestring = dateobj.strftime('%s')
        #print dateobj, datestring
        analysis_util.api_developer_date_tmp_table_update(api_id, mashup_id, developer_id, datestring)
        #print dateobj.isoformat()
        #print dateobj.strftime('%s')
        #developer_count = row[1]
        #analysis_util.api_author_count_tmp_table_update(api_id, developer_count)
        out = str(i)
        for r in row:
            out = out+"\t"+str(r)
        print out
        txt.write(out+"\n")
        i = i+1
develop_mashup = '''
SELECT 
    author_mashup.author_id, 
    author_mashup.mashup_id, 
    mashup_api.api_id, 
    date.date
FROM author_mashup, mashup_api, date, date_mashup 
WHERE 
    author_mashup.mashup_id = mashup_api.mashup_id AND 
    mashup_api.mashup_id = date_mashup.mashup_id AND 
    date.date_id = date_mashup.date_id
ORDER BY 
    mashup_api.api_id,
    author_mashup.author_id,
    author_mashup.mashup_id
'''
def developer_api_time_o():
    sql_params = ( )
    rows = db_execute(develop_mashup, sql_params)
    db_loop_time(rows, "developer_api_time_o")



def db_loop_api_developer_index(c, file_name):
    global analysis_path
    api_developer_count = {}
    api_developer_rate = {}
    txt = open(analysis_path+file_name+".txt", "w")
    head = "index"
    for colum_name in c.description:
        head = head + ", \t"+str(colum_name[0])
    print head
    txt.write(head+"\n")
    i = 1
    for row in c:
        api_id = row[0]
        developer_id = row[1]
        developer_date = row[3]
        #
        if api_developer_count.get(api_id) == None :
            api_developer_count[api_id] = {}
        if api_developer_count[api_id].get(developer_id) == None :
            api_developer_count[api_id][developer_id] = 0
        api_developer_count[api_id][developer_id] = api_developer_count[api_id][developer_id] + 1
        #
        if api_developer_rate.get(api_id) == None :
            api_developer_rate[api_id] = {}
        if api_developer_rate[api_id].get(developer_id) == None :
            api_developer_rate[api_id][developer_id] = developer_date
        #print api_developer_rate[api_id][developer_id] >= developer_date, api_developer_rate[api_id][developer_id], developer_date
        if (api_developer_rate[api_id][developer_id] > developer_date):
            #print developer_date, type(developer_date), api_developer_rate[api_id][developer_id]
            api_developer_rate[api_id][developer_id] = developer_date
        # set up a index in array, or list or sequence, need to find out
        #analysis_util.api_author_count_tmp_table_update(api_id, developer_count)
        out = str(i)
        for r in row:
            out = out+"\t"+str(r)
        #print out
        txt.write(out+"\n")
        i = i+1
    #print api_developer_count
    #print api_developer_rate
    api_developer_rate_temp = []
    api_ids = api_developer_rate.keys()
    #print api_ids
    for api_id in api_ids:
        #print api_developer_rate[api_id]
        temp = api_developer_rate[api_id]
        temp1 = temp.iteritems()
        temp2 = sorted(temp1, key=operator.itemgetter(1))
        #print temp2
        i = 1 # index, index, index, developer_id, datestring
        api_develop_count = 0
        api_mashup_count = 0
        for developer_id, datestring in temp2:
            api_develop_count = api_develop_count + 1
            count = api_developer_count[api_id][developer_id]
            api_mashup_count = api_mashup_count + count
            #print developer_id, datestring, i, count
            analysis_util.developer_api_pioneer_rate_tmp_table_update(developer_id, api_id, i, count)
            i = i+1
        #api_developer_rate_temp.append(api_developer_count[api_id][developer_id])
        #print api_develop_count, api_mashup_count
        analysis_util.api_author_count_tmp_table_update(api_id, api_develop_count, api_mashup_count)
        #print "**********"
    #print api_developer_rate_temp
    #print len(api_developer_rate_temp)


api_developer_index = '''
SELECT 
    api_developer_date_temp.api_id,
    api_developer_date_temp.developer_id, 
    api_developer_date_temp.mashup_id, 
    api_developer_date_temp.date
FROM api_developer_date_temp
ORDER BY 
    api_developer_date_temp.api_id ASC,  
    api_developer_date_temp.developer_id ASC, 
    api_developer_date_temp.date ASC
'''
def api_developer_index_o():
    sql_params = ( )
    rows = db_execute(api_developer_index, sql_params)
    db_loop_api_developer_index(rows, "api_developer_index_o")




def db_loop_pioneer_rate(c, file_name):
    global analysis_path
    api_developer_count = {}
    api_developer_rate = {}
    txt = open(analysis_path+file_name+".txt", "w")
    head = "index"
    for colum_name in c.description:
        head = head + ", \t"+str(colum_name[0])
    print head
    txt.write(head+"\n")
    i = 1
    for row in c:
        developer_id = row[0]
        api_id = row[1]
        pioneer_position = row[2]
        mashup_counts = row[3]
        api_developer_count = row[4]
        api_mashup_count = row[5]
        api_pioneer_rate = 1.0 * (api_developer_count - pioneer_position) / api_developer_count
        api_mashup_rate = 1.0 * (mashup_counts) / api_mashup_count
        print developer_id, api_id
        print pioneer_position, api_developer_count, api_pioneer_rate
        print mashup_counts, api_mashup_count, api_mashup_rate
        print "*******************"
        out = str(i)
        for r in row:
            out = out+"\t"+str(r)
        #print out
        txt.write(out+"\n")
        i = i+1
    
# I should also be able to finger out the date of each API, and how long this API become popular when many people come to use it
pioneer_rate = '''
SELECT 
    developer_api_pioneer_rate_temp.developer_id, 
    developer_api_pioneer_rate_temp.api_id, 
    developer_api_pioneer_rate_temp.pioneer_position, 
    developer_api_pioneer_rate_temp.mashup_counts, 
    api_author_count_temp.developer_count,
    api_author_count_temp.mashup_count, 
    author.author_name,
    author.author_url,
    api.api_name, 
    api.api_url
FROM developer_api_pioneer_rate_temp, api_author_count_temp, api, author
WHERE 
    developer_api_pioneer_rate_temp.api_id = api_author_count_temp.api_id AND 
    developer_api_pioneer_rate_temp.api_id = api.api_id AND 
    developer_api_pioneer_rate_temp.developer_id = author.author_id  
ORDER BY 
    developer_api_pioneer_rate_temp.developer_id, 
    developer_api_pioneer_rate_temp.api_id
'''
def pioneer_rate_o():
    sql_params = ( )
    rows = db_execute(pioneer_rate, sql_params)
    db_loop_pioneer_rate(rows, "pioneer_rate_o")


############################################################
def db_loop_pioneer_rate_to_database(c, file_name):
    global analysis_path
    api_developer_count = {}
    api_developer_rate = {}
    txt = open(analysis_path+file_name+".txt", "w")
    head = "index"
    for colum_name in c.description:
        head = head + ", \t"+str(colum_name[0])
    print head
    txt.write(head+"\n")
    i = 1
    for row in c:
        developer_id = row[0]
        api_id = row[1]
        pioneer_position = row[2]
        mashup_counts = row[3]
        api_developer_count = row[4]
        api_mashup_count = row[5]
        api_pioneer_rate = 1.0 * (api_developer_count - pioneer_position) / api_developer_count
        api_mashup_rate = 1.0 * (mashup_counts) / api_mashup_count
        #print developer_id, api_id
        #print pioneer_position, api_developer_count, api_pioneer_rate
        #print mashup_counts, api_mashup_count, api_mashup_rate
        #print "*******************"
        analysis_util.developer_api_pioneer_rate_mashups_tmp_table_update(developer_id, api_id, mashup_counts, api_pioneer_rate, api_mashup_rate)
        out = str(i)
        for r in row:
            out = out+"\t"+str(r)
        #print out
        txt.write(out+"\n")
        i = i+1

pioneer_rate_apis_mashups = '''
SELECT 
    developer_api_pioneer_rate_mashups_temp.developer_id, 
    COUNT(developer_api_pioneer_rate_mashups_temp.api_id) AS apis, 
    SUM(developer_api_pioneer_rate_mashups_temp.mashup_counts) AS mashups, 
    AVG(developer_api_pioneer_rate_mashups_temp.pioneer_position_rate) AS avg_pioneer_position_rate, 
    MAX(developer_api_pioneer_rate_mashups_temp.pioneer_position_rate) AS max_pioneer_position_rate,
    MIN(developer_api_pioneer_rate_mashups_temp.pioneer_position_rate) AS min_pioneer_position_rate,
    AVG(developer_api_pioneer_rate_mashups_temp.pioneer_mashup_rate) AS avg_pioneer_mashup_rate,
    MAX(developer_api_pioneer_rate_mashups_temp.pioneer_mashup_rate) AS max_pioneer_mashup_rate,
    MIN(developer_api_pioneer_rate_mashups_temp.pioneer_mashup_rate) AS min_pioneer_mashup_rate
FROM developer_api_pioneer_rate_mashups_temp 
GROUP BY 
    developer_api_pioneer_rate_mashups_temp.developer_id
ORDER BY 
    developer_api_pioneer_rate_mashups_temp.developer_id 
'''

def db_loop_pioneer_rate_apis_mashups(c, file_name):
    global analysis_path
    api_developer_count = {}
    api_developer_rate = {}
    txt = open(analysis_path+file_name+".txt", "w")
    head = "index"
    for colum_name in c.description:
        head = head + ", \t"+str(colum_name[0])
    print head
    txt.write(head+"\n")
    i = 1
    for row in c:
        developer_id = row[0]
        apis = row[1]
        mashups = row[2]
        avg_pioneer_position_rate = row[3]
        avg_pioneer_mashup_rate = row[4]
        print developer_id, apis, mashups, avg_pioneer_position_rate, avg_pioneer_mashup_rate
        out = str(i)
        for r in row:
            out = out+"\t"+str(r)
        #print out
        txt.write(out+"\n")
        i = i+1
def pioneer_rate_mashups_o():
    sql_params = ( )
    rows = db_execute(pioneer_rate, sql_params)
    db_loop_pioneer_rate_to_database(rows, "pioneer_rate_apis_mashups_o")
    sql_params = ( )
    rows = db_execute(pioneer_rate_apis_mashups, sql_params)
    db_loop_pioneer_rate_apis_mashups(rows, "pioneer_rate_apis_mashups_o")
#####################################
    

if __name__ == "__main__":
    print "Hello World";
