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
import analysis_cacm
import analysis_pioneer_rate



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


def analysis_cacm_main():
    '''analysis_cacm.developer_mashup_api_category_dataformat_o(1)
    analysis_cacm.developer_mashup_api_category_dataformat_o(19)
    analysis_cacm.developer_mashup_api_category_dataformat_o(82)
    analysis_cacm.developer_mashup_api_category_dataformat_o(2720)
    #
    analysis_cacm.developer_mashup_o(1)
    analysis_cacm.developer_mashup_o(19)
    analysis_cacm.developer_mashup_o(82)
    analysis_cacm.developer_mashup_o(2720)
    #'''
    #analysis_cacm.api_usage_o(2720)
    #analysis_cacm.developer_api_count_o(2720)
    #analysis_cacm.developer_api_mashup_count_o(2720)
    analysis_cacm.api_usage_o(2720, 2)
    analysis_cacm.api_usage_o(2720, 3)
    analysis_cacm.api_usage_o(2720, 4)
    analysis_cacm.api_usage_o(2720, 5)
    analysis_cacm.api_usage_o(2720, 6)
    analysis_cacm.api_usage_o(2720, 7)
    analysis_cacm.api_usage_o(2720, 8)
    analysis_cacm.api_usage_o(2720, 9)
    analysis_cacm.api_usage_o(2720, 10)
    analysis_cacm.api_usage_o(2720, 11)
    
    
    
def analysis_pioneer_rate_main():
    analysis_util.pioneer_rate_tmp_table_init()
    analysis_pioneer_rate.developer_api_time_o()
    analysis_pioneer_rate.api_developer_index_o()
    analysis_pioneer_rate.pioneer_rate_o()
    analysis_pioneer_rate.pioneer_rate_mashups_o()


if __name__ == "__main__":
    #programableweb_page_read()
    #programable_sql_analysis()
    #get_gexf()
    #analysis_cacm_main()
    analysis_pioneer_rate_main()
    print "Hello World"
