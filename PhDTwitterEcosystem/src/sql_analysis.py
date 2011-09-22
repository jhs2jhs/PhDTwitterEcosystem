#! /usr/bin/python

# To change this template, choose Tools | Templates
# and open the template in the editor.

__author__="jianhuashao"
__date__ ="$Sep 13, 2011 11:43:15 AM$"

from my_util import cmd_p, db_conn
from analysis_util import db_execute, db_loop, db_loop_for_array
import analysis_util
import analysis_plot
from random import randrange
import color_util
conn = db_conn()
analysis_path = "../analysis/"
    

############ prepare developer index temp table, you can run it first before any action   
developer_index_mashups = '''
    SELECT 
        DISTINCT author_mashup.author_id, 
        COUNT(DISTINCT author_mashup.mashup_id) AS mashup_count
    FROM author_mashup
    GROUP BY
        author_mashup.author_id
'''
developer_index_api = '''
    SELECT 
        DISTINCT author_mashup.author_id, 
        COUNT(DISTINCT mashup_api.api_id) AS api_count
    FROM 
        author_mashup LEFT OUTER JOIN
        mashup_api
        ON
            author_mashup.mashup_id = mashup_api.mashup_id
    GROUP BY 
        author_mashup.author_id
'''
developer_index_tmp = '''
    SELECT 
        DISTINCT mashups.author_id, apis.author_id, mashups.mashup_count, apis.api_count
    FROM
        ('''+developer_index_mashups+''') AS mashups INNER JOIN
        ('''+developer_index_api+''') AS apis
        ON
            mashups.author_id = apis.author_id
    ORDER BY
        mashups.mashup_count DESC,
        apis.api_count DESC, 
        mashups.author_id
'''
def developer_index_tmp_table_prepare():
    global conn
    analysis_util.developer_index_tmp_table_init()
    sql_params = ( )
    #print developer_index_mashups
    i = 1
    rows = db_execute(developer_index_tmp, sql_params)
    author_id_rank = []
    for row in rows:
        author_id_rank.append(row[0])
    rows.close()
    for author_id in author_id_rank:
        #print author_id
        developer_index = i
        developer_id = author_id
        analysis_util.developer_index_tmp_table_update(developer_index, developer_id)
        i += 1
    analysis_util.developer_index_tmp_table_check()
############ prepare developer index temp table    

def arrange_developer_sql_length():
    index_sql = '''
    SELECT 
        COUNT(developer_index_temp.developer_index)
    FROM 
        developer_index_temp
        '''
    return index_sql
def arrange_developer_sql(content_name, temp_from_sql):
    index_sql = '''
    SELECT 
        developer_index_temp.developer_index,
        temp_table.'''+content_name+'''
    FROM 
        developer_index_temp LEFT OUTER JOIN
        ('''+temp_from_sql+''') AS temp_table
        ON
            developer_index_temp.developer_id = temp_table.author_id
    ORDER BY
        developer_index_temp.developer_index
        '''
    return index_sql
def get_developer_relationship(
        sql_params, 
        temp_sql, 
        temp_content_name, 
        file_name,
        plot_function = analysis_plot.developer_to_mashup_line_plot
        ):
    rows = db_execute(temp_sql, sql_params)
    db_loop(rows, file_name)
    sql = arrange_developer_sql(temp_content_name, temp_sql)
    rows = db_execute(sql, sql_params)
    developers = []
    contents = []
    for row in rows:
        #print row[0]
        developers.append(row[0])
        contents.append(row[1])
    #developers = range(len(mashups))
    #mashups = db_loop_for_array(rows, "developer_mashup_count_o", 2)
    #print developers
    #print
    #print mashups
    plot_function(developers, contents)
    #analysis_plot.show()
    

snapshot = '''
        developer_index_temp.developer_index BETWEEN 196 AND 433
'''
def arrange_developer_sql_length_snapshot():
    index_sql = '''
    SELECT 
        COUNT(developer_index_temp.developer_index)
    FROM 
        developer_index_temp
    WHERE
        '''+snapshot+'''
        '''
    return index_sql
def arrange_developer_sql_snapshot(content_name, temp_from_sql):
    index_sql = '''
    SELECT 
        developer_index_temp.developer_index,
        temp_table.'''+content_name+'''
    FROM 
        developer_index_temp LEFT OUTER JOIN
        ('''+temp_from_sql+''') AS temp_table
        ON
            developer_index_temp.developer_id = temp_table.author_id
    WHERE
        '''+snapshot+'''
    ORDER BY
        developer_index_temp.developer_index
        '''
    return index_sql
def get_developer_relationship_snapshot(
        sql_params, 
        temp_sql, 
        temp_content_name, 
        file_name,
        plot_function = analysis_plot.developer_to_mashup_line_plot
        ):
    rows = db_execute(temp_sql, sql_params)
    db_loop(rows, file_name)
    sql = arrange_developer_sql_snapshot(temp_content_name, temp_sql)
    rows = db_execute(sql, sql_params)
    developers = []
    contents = []
    for row in rows:
        #print row[0]
        developers.append(row[0])
        contents.append(row[1])
    #developers = range(len(mashups))
    #mashups = db_loop_for_array(rows, "developer_mashup_count_o", 2)
    #print developers
    #print
    #print mashups
    plot_function(developers, contents)
    #analysis_plot.show()




developer_mashup_count = '''
    SELECT 
        author_mashup.author_id, 
        COUNT(author_mashup.mashup_id) AS mashup_count
    FROM 
        author_mashup
    GROUP BY
        author_mashup.author_id
    ORDER BY 
        mashup_count DESC  
'''

def developer_mashup_count_o():
    sql_params = ( )
    get_developer_relationship(
        sql_params, 
        developer_mashup_count, 
        "mashup_count", 
        "developer_mashup_count_o",
        analysis_plot.developer_to_mashup_line_plot
        )
    #analysis_plot.show()
def developer_mashup_count_snapshot_o():
    sql_params = ( )
    get_developer_relationship_snapshot(
        sql_params, 
        developer_mashup_count, 
        "mashup_count", 
        "developer_mashup_count_snapshot_o",
        analysis_plot.developer_to_mashup_line_plot
        )
    #analysis_plot.show()
def developer_mashup_count_snapshot_dot_o():
    sql_params = ( )
    get_developer_relationship_snapshot(
        sql_params, 
        developer_mashup_count, 
        "mashup_count", 
        "developer_mashup_count_snapshot_o",
        analysis_plot.developer_to_mashup_dot_plot
        )
    #analysis_plot.show()
    

developer_api_count = '''
    SELECT 
        author_mashup.author_id, 
        COUNT(DISTINCT mashup_api.api_id) AS api_count
    FROM author_mashup, mashup_api
    WHERE
        author_mashup.mashup_id = mashup_api.mashup_id
    GROUP BY 
        author_mashup.author_id
    ORDER BY 
        api_count DESC
'''
def developer_api_count_o():
    sql_params = ( )
    get_developer_relationship(
        sql_params, 
        developer_api_count, 
        "api_count", 
        "developer_api_count_o",
        analysis_plot.developer_to_api_dot_plot
        )
    #analysis_plot.show()
def developer_api_count_snapshot_o():
    sql_params = ( )
    get_developer_relationship_snapshot(
        sql_params, 
        developer_api_count, 
        "api_count", 
        "developer_api_count_snapshot_o",
        analysis_plot.developer_to_api_dot_plot
        )
    #analysis_plot.show()
    




api_deploy_i = '''
    SELECT 
        author_mashup.author_id, 
        COUNT(mashup_api.api_id) AS api_count
    FROM author_mashup, mashup_api
    WHERE
        author_mashup.mashup_id = mashup_api.mashup_id AND 
        mashup_api.api_id = ?
    GROUP BY 
        author_mashup.author_id
    ORDER BY 
        author_id  
'''
api_deploy_other = '''
    SELECT 
        author_mashup.author_id, 
        COUNT(mashup_api.api_id) AS api_count
    FROM author_mashup, mashup_api
    WHERE
        author_mashup.mashup_id = mashup_api.mashup_id AND 
        mashup_api.api_id NOT IN %s
    GROUP BY 
        author_mashup.author_id
    ORDER BY 
        author_id  
'''
api_popularity_rank = '''
    SELECT 
        COUNT(DISTINCT author_mashup.author_id) AS author_count, 
        mashup_api.api_id,
        api.api_name
    FROM author_mashup, mashup_api, api
    WHERE
        author_mashup.mashup_id = mashup_api.mashup_id AND
        mashup_api.api_id = api.api_id
    GROUP BY 
        mashup_api.api_id
    ORDER BY 
        author_count DESC 
'''
api_popularity_rank_no_google_map = '''
    SELECT 
        COUNT(DISTINCT author_mashup.author_id) AS author_count, 
        mashup_api.api_id,
        api.api_name
    FROM author_mashup, mashup_api, api
    WHERE
        author_mashup.mashup_id = mashup_api.mashup_id AND
        mashup_api.api_id = api.api_id AND 
        mashup_api.api_id <> 1288
    GROUP BY 
        mashup_api.api_id
    ORDER BY 
        author_count DESC 
'''
def api_popularity_rank_o():
    sql_params = ( )
    rows = db_execute(api_popularity_rank, sql_params)
    #db_loop(rows, "api_popularity_rank_o")
    axx = analysis_plot.get_stacked_bar_axx(1, 1, 1)
    # get top apis list
    top_apis_id = list()
    top_apis_name = list()
    #print arrange_developer_sql_length()
    developer_count = analysis_util.get_developer_length(arrange_developer_sql_length(), 0)
    analysis_plot.set_stacked_bar_bottom(developer_count)
    index_count = 0
    index = range(index_count)
    color_util.create_rgbs(index_count)
    for i in index:
        row = rows.fetchone()
        api_id = row[1]
        api_name = row[2]
        top_apis_id.append(api_id)
        top_apis_name.append(api_name)
    # other apis plot
    other_developer_index = []
    other_apis = []
    api_count_other_sql = api_deploy_other % str(tuple(top_apis_id))
    api_count_other_sql = arrange_developer_sql("api_count", api_count_other_sql)
    #print api_count_other_sql
    api_count_other_rows = db_execute(api_count_other_sql, ())
    for api_count_other_row in api_count_other_rows:
        other_developer_index.append(api_count_other_row[0])
        if api_count_other_row[1] == None:
            #print "*********"
            other_apis.append(0)
        else: 
            other_apis.append(api_count_other_row[1])
    #print other_apis
    stack_color = 'w'
    print stack_color
    analysis_plot.developer_to_api_bar_plot(other_developer_index, other_apis, axx, stack_color, "APIs stack")
    # top api plot
    index = range(len(top_apis_id))
    for i in index:
        api_id = top_apis_id[i]
        api_name = top_apis_name[i]
        api_color = color_util.get_rgb(i)
        developer_index = []
        apis_is = []
        api_count_sql = arrange_developer_sql("api_count", api_deploy_i)
        api_count_rows = db_execute(api_count_sql, (api_id, ))
        for api_row in api_count_rows:
            #print api[0], api[1]
            developer_index.append(api_row[0])
            if api_row[1] == None:
                apis_is.append(0)
            else: 
                apis_is.append(api_row[1])
        analysis_plot.developer_to_api_bar_plot(developer_index, apis_is, axx, api_color, api_name)
    analysis_plot.developer_to_api_bar_legend(axx, top_apis_name)
def api_popularity_rank_snapshot_o():
    sql_params = ( )
    rows = db_execute(api_popularity_rank, sql_params)
    #db_loop(rows, "api_popularity_rank_o")
    axx = analysis_plot.get_stacked_bar_axx(1, 1, 1)
    # get top apis list
    top_apis_id = list()
    top_apis_name = list()
    #print arrange_developer_sql_length_snapshot()
    developer_count = analysis_util.get_developer_length(arrange_developer_sql_length_snapshot(), 0)
    analysis_plot.set_stacked_bar_bottom(developer_count)
    index_count = 21
    index = range(index_count)
    color_util.create_rgbs(index_count)
    for i in index:
        row = rows.fetchone()
        api_id = row[1]
        api_name = row[2]
        top_apis_id.append(api_id)
        top_apis_name.append(api_name)
    print top_apis_name
    # other apis plot
    other_developer_index = []
    other_apis = []
    api_count_other_sql = api_deploy_other % str(tuple(top_apis_id))
    api_count_other_sql = arrange_developer_sql_snapshot("api_count", api_count_other_sql)
    print api_count_other_sql
    api_count_other_rows = db_execute(api_count_other_sql, ())
    for api_count_other_row in api_count_other_rows:
        other_developer_index.append(api_count_other_row[0])
        if api_count_other_row[1] == None:
            #print "*********"
            other_apis.append(0)
        else: 
            other_apis.append(api_count_other_row[1])
    print other_apis
    stack_color = 'w'
    print stack_color
    analysis_plot.developer_to_api_bar_plot(other_developer_index, other_apis, axx, stack_color, "Other APIs")
    # top api plot
    index = range(len(top_apis_id))
    for i in index:
        api_id = top_apis_id[i]
        api_name = top_apis_name[i]
        api_color = color_util.get_rgb(i)
        developer_index = []
        apis_is = []
        api_count_sql = arrange_developer_sql_snapshot("api_count", api_deploy_i)
        api_count_rows = db_execute(api_count_sql, (api_id, ))
        for api_row in api_count_rows:
            #print api[0], api[1]
            developer_index.append(api_row[0])
            if api_row[1] == None:
                apis_is.append(0)
            else: 
                apis_is.append(api_row[1])
        analysis_plot.developer_to_api_bar_plot(developer_index, apis_is, axx, api_color, api_name)
    analysis_plot.developer_to_api_bar_legend(axx, top_apis_name)        




developer_to_mashup = '''
    SELECT 
        author_mashup.author_id, 
        author_mashup.mashup_id,
        mashup_api.api_id
    FROM author_mashup, mashup_api
    WHERE
        author_mashup.mashup_id = mashup_api.mashup_id
    ORDER BY 
        author_mashup.author_id,
        mashup_api.api_id,
        author_mashup.mashup_id
'''
developer_to_api = '''
    SELECT
        author_api.author_id,
        author_api.api_id,
        COUNT(author_api.api_id) AS api_count
    FROM
        ('''+developer_to_mashup+''') AS author_api
    GROUP BY
        author_api.author_id,
        author_api.api_id
    ORDER BY
        author_api.author_id
'''
def developer_to_api_o():
    sql_params = ( )
    rows = db_execute(developer_to_api, sql_params)
    db_loop(rows, "developer_to_api_o")
    


developer_to_mashup = '''
    SELECT 
        author_mashup.author_id, 
        author_mashup.mashup_id,
        mashup_api.api_id
    FROM author_mashup, mashup_api
    WHERE
        author_mashup.mashup_id = mashup_api.mashup_id
    ORDER BY 
        author_mashup.author_id,
        mashup_api.api_id,
        author_mashup.mashup_id
'''
apis_has_developer_count = '''
    SELECT
        author_api.api_id,
        COUNT (DISTINCT author_api.author_id) AS author_count
    FROM
        ('''+developer_to_mashup+''') AS author_api
    GROUP BY 
        author_api.api_id
    ORDER BY 
        author_count
'''
def apis_has_developer_count_o():
    sql_params = ( )
    rows = db_execute(apis_has_developer_count, sql_params)
    db_loop(rows, "apis_has_developer_count_o")






if __name__ == "__main__":
    print "Hello World";
