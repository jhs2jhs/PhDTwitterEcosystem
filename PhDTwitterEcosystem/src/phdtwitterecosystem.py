# To change this template, choose Tools | Templates
# and open the template in the editor.

__author__="jianhuashao"
__date__ ="$Sep 6, 2011 12:39:30 AM$"

from my_util import cmd_p
import web_api 
import web_mashup 
import sqlite_init 
import sql_analysis
import analysis_util
import analysis_plot
import sql_gexf



def programableweb_page_read():
    sqlite_init.sqlite_init()
    web_api.apis_pages_read()
    web_api.apis_db_write()
    web_mashup.mashups_pages_read()

def programable_sql_analysis():
    #sql_analysis.developer_index_tmp_table_prepare()
    is_snapshot = 1
    if is_snapshot == 0:
        sql_analysis.developer_api_count_o()
        sql_analysis.developer_mashup_count_o()
        sql_analysis.api_popularity_rank_o()
        analysis_plot.set_title("All developers")
        analysis_plot.set_max_y(85)
        analysis_plot.set_max_x(2721)
        analysis_plot.developer_to_api_bar_annotate(
            "2 mashups", 
            315, 2, 
            815, 20)
        analysis_plot.developer_to_api_bar_annotate(
            "1 mashup", 
            1600, 1, 
            2100, 20)
    #analysis_plot.show()
    else:
        sql_analysis.developer_api_count_snapshot_o()
        sql_analysis.developer_mashup_count_snapshot_o()
        #sql_analysis.developer_mashup_count_snapshot_dot_o()
        sql_analysis.api_popularity_rank_snapshot_o()
        analysis_plot.set_max_y(20)
        analysis_plot.set_min_x(197)
        analysis_plot.set_max_x(432)
        '''analysis_plot.developer_to_api_bar_annotate(
            "2 mashups", 
            315, 2, 
            315, 20)'''
        analysis_plot.set_title("Developers who created only 2 mashups")
    analysis_plot.show()
    #sql_analysis.developer_to_api_o()
    #sql_analysis.apis_has_developer_count_o()
    #analysis_util.sqlite_function_create_test_o()
    #analysis_util.sqlite_function_aggreation_test_o()


def get_gexf():
    sql_gexf.developer_to_api_o()


if __name__ == "__main__":
    #programableweb_page_read()
    #programable_sql_analysis()
    get_gexf()
    print "Hello World"
