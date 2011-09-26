#! /usr/bin/python

# To change this template, choose Tools | Templates
# and open the template in the editor.

__author__="jianhuashao"
__date__ ="$Sep 26, 2011 11:10:54 AM$"

from gexf import Gexf
from my_util import cmd_p, db_conn
conn = db_conn()
gexf_path = "../gexf/"


developer_to_api_distinct_developer='''
    SELECT 
        DISTINCT author_mashup.author_id,
        author.author_name
    FROM author_mashup, mashup_api, author, api
    WHERE 
        author_mashup.mashup_id = mashup_api.mashup_id
        AND author_mashup.author_id = author.author_id
        AND mashup_api.api_id = api.api_id 
    ORDER BY
        author_mashup.author_id
'''
developer_to_api_distinct_api='''
    SELECT 
        DISTINCT mashup_api.api_id,
        api.api_name
    FROM author_mashup, mashup_api, author, api
    WHERE 
        author_mashup.mashup_id = mashup_api.mashup_id
        AND author_mashup.author_id = author.author_id
        AND mashup_api.api_id = api.api_id 
    ORDER BY
        mashup_api.api_id
'''
developer_to_api='''
    SELECT 
        author_mashup.author_id,
        author.author_name,
        mashup_api.api_id,
        api.api_name
    FROM author_mashup, mashup_api, author, api
    WHERE 
        author_mashup.mashup_id = mashup_api.mashup_id
        AND author_mashup.author_id = author.author_id
        AND mashup_api.api_id = api.api_id 
    ORDER BY
        author_mashup.author_id,
        mashup_api.api_id
'''

def gexf_node_developer(sql, param, graph, attr_node):
    global conn
    c = conn.cursor()
    c.execute(sql, param)
    for row in c.fetchall():
        n = graph.addNode('d_'+str(row[0]), row[1].encode("ascii", "ignore"))
        n.addAttribute(attr_node, 'developer')
    c.close()
        
def gexf_node_api(sql, param, graph, attr_node):
    global conn
    c = conn.cursor()
    c.execute(sql, param)
    for row in c.fetchall():
        n = graph.addNode('a_'+str(row[0]), row[1].encode("ascii", "ignore"))
        n.addAttribute(attr_node, 'api')
    c.close()
        
def gexf_edge_developer_to_api(sql, param, graph):
    global conn
    c = conn.cursor()
    c.execute(sql, param)
    i = 1
    for row in c.fetchall():
        e = graph.addEdge(str(i), 'd_'+str(row[0]), 'a_'+str(row[2]))
        i += 1
    c.close()
    
def developer_to_api_o():
    global conn
    gexf = Gexf("Jianhua Shao", "programaleweb developer to api")
    graph = gexf.addGraph("directed", "static", "ecosystem")
    attr_node = graph.addNodeAttribute("n_type", "mashup", "string")
    gexf_node_developer(
        developer_to_api_distinct_developer, 
        (), 
        graph, 
        attr_node)
    gexf_node_api(
        developer_to_api_distinct_api, 
        (), 
        graph, 
        attr_node)
    gexf_edge_developer_to_api(
        developer_to_api, 
        (), 
        graph)
    output_file = open(gexf_path+"pgw_developer_to_api.gexf", 'w')
    gexf.write(output_file)


if __name__ == "__main__":
    print "Hello World";
    
