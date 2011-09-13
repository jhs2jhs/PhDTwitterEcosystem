#! /usr/bin/python

# To change this template, choose Tools | Templates
# and open the template in the editor.

__author__="jianhuashao"
__date__ ="$Sep 6, 2011 12:56:07 AM$"

import httplib2
from my_util import cmd_p, db_conn
from BeautifulSoup import Tag, NavigableString, BeautifulSoup

conn = db_conn()
url_root = "http://www.programmableweb.com"
apis = []

def api_exist(api_name):
    global conn
    c = conn.cursor()
    c.execute("SELECT api_id FROM api WHERE api_name = ? ", (api_name,))
    result = c.fetchone()
    if result == None:
        return -1
    else: 
        return result[0]

def apis_directory_page_read(url):
    global conn, apis
    h = httplib2.Http()
    resp, content = h.request(url) #, "PUT", headers={"Content-Type":"text/plain"}
    cmd_p("reading page: "+url)
    #print type(content)
    #print content
    soup = BeautifulSoup(content)
    #print type(soup)
    lists = soup.findAll("table", attrs={"summary":"API", "id":"apis"})
    #print type(lists[0].contents)
    i = -2
    #print i
    for list in lists[0].contents:
        if isinstance(list, Tag) :
            i = i+1
            #print i
            if i == -1:
                i = 0
                continue
            if len(list.contents) != 4:
                sys.exit("api length is not equal to 4")
            api_name = ""
            api_url = ""
            api_desc = ""
            api_category = ""
            api_date = ""
            api_name = list.contents[0].contents[0].contents[0].strip().encode("ascii", 'ignore').lower()
            if api_exist(api_name) != -1:
                continue
            api_url = list.contents[0].contents[0]["href"].encode("ascii", 'ignore').strip().lower()
            api_desc = list.contents[1].contents[0].strip()
            api_category = list.contents[2].contents[0].strip().encode("ascii", 'ignore').lower()
            api_date = list.contents[3].contents[0].strip().encode("ascii", 'ignore').lower()
            api = {
                "name": api_name,
                "url": api_url,
                "desc": api_desc,
                "category": api_category,
                "date": api_date
                }
            print api
            apis.append(api)
            #print api_date
    #print apis
    pages = soup.findAll("img", attrs={"src":"/images/listnav_next.png"})
    if len(pages) == 0:
        return False
    else:
        return True

def apis_pages_read():
    global conn, apis, url_root
    apis = []
    i = 0
    next = True
    while next:
        i = i+1
        u = url_root+"/apis/directory/"+str(i)
        print u
        next = apis_directory_page_read(u)
    cmd_p("apis list length: "+str(len(apis)))


def highlight_api_db_write(elements, api_id, highlight):
    global conn
    #cmd_p("write "+highlight+" into database")
    c = conn.cursor()
    for element_name in elements:
        c.execute("INSERT OR IGNORE INTO "+highlight+" ("+highlight+"_name) VALUES (?)", (element_name,) )
        conn.commit()
        c.execute("SELECT "+highlight+"_id FROM "+highlight+" WHERE "+highlight+"_name=?", (element_name,))
        element_id = c.fetchone()[0]
        c.execute ("INSERT OR IGNORE INTO "+highlight+"_api (api_id, "+highlight+"_id) VALUES (?, ?)", (api_id, element_id, ))
        conn.commit()
    c.execute("SELECT COUNT("+highlight+"_id) FROM "+highlight+"", )
    element_total = c.fetchone()[0]
    cmd_p(""+highlight+"s total: "+str(element_total))
    c.close()


def highlight_api_page_read(soup, api_id):
    #global tags
    tags = []
    protocols = []
    dataformats = []
    lists = soup.findAll("dl", attrs={"class":"inline dt90"})
    #print type(lists[0].contents)
    #print lists[0]
    #i = 0
    #print i
    for list in lists:
        #print list.contents[0], list.contents[1]
        dt = list.contents[0]
        dd = list.contents[1]
        #print dt.contents[0].strip().lower()
        if dt.contents[0].strip().lower() == "tags" :
            #print type(dd)
            #print dd.contents
            for d in dd.contents:
                if isinstance(d, Tag) and len(d) > 0 and len(d.contents[0]) > 0:
                    #print d
                    tag = d.contents[0].strip().lower()
                    tags.append(tag)
                    #print tag
        #print ""
        if dt.contents[0].strip().lower() == "protocols" :
            #print type(dd)
            #print dd.contents
            for d in dd.contents:
                if isinstance(d, Tag) and len(d) > 0 and len(d.contents[0]) > 0:
                    #print d
                    protocol = d.contents[0].strip().lower()
                    protocols.append(protocol)
                    #print protocol
        #print ""
        if dt.contents[0].strip().lower() == "data formats" :
            #print type(dd)
            #print dd.contents
            for d in dd.contents:
                if isinstance(d, Tag) and len(d) > 0 and len(d.contents[0]) > 0:
                    #print d
                    dataformat = d.contents[0].strip().lower()
                    dataformats.append(dataformat)
                    #print dataformat
        #print ""
    highlight_api_db_write(tags, api_id, "tag")
    highlight_api_db_write(protocols, api_id, "protocol")
    highlight_api_db_write(dataformats, api_id, "dataformat")



def description_api_db_write(elements, api_id, highlight):
    global conn
    #cmd_p("write "+highlight+" into database")
    c = conn.cursor()
    c.execute("SELECT "+highlight+"_id FROM "+highlight+"_api WHERE api_id = ?", (api_id, ))
    if c.fetchone() == None:
        c.execute("INSERT OR IGNORE INTO "+highlight+" ("+highlight+"_name) VALUES (?)", (elements,) )
        conn.commit()
        c.execute("SELECT MAX("+highlight+"_id) FROM "+highlight, )
        element_id = c.fetchone()[0]
        c.execute ("INSERT OR IGNORE INTO "+highlight+"_api (api_id, "+highlight+"_id) VALUES (?, ?)", (api_id, element_id, ))
        conn.commit()
    c.execute("SELECT COUNT("+highlight+"_id) FROM "+highlight+"", )
    element_total = c.fetchone()[0]
    cmd_p(""+highlight+"s total: "+str(element_total))
    c.close()
         
def description_api_page_read(soup, api_id):
    description = ""
    lists = soup.findAll("div", attrs={"class":"span-10"})
    for list in lists:
        #print list.contents[0].contents[0]
        if isinstance(list, Tag) == False:
            break
        if isinstance(list.contents[0], Tag) == False:
            break
        description = list.contents[0].contents[0].strip()
        if description != "":
            #print description
            description_api_db_write(description, api_id, "description")

def specification_api_page_read(soup, api_id):
    auths = []
    lists = soup.findAll("dl", attrs={"class":"tabular dt145"})
    for list in lists:
        #print list.contents[0], list.contents[1]
        dt = list.contents[0]
        dd = list.contents[1]
        #print dt.contents[0].strip().lower()
        if dt.contents[0].strip().lower() == "authentication model" :
            #print dd.contents[0]
            #print "hello", len(dd.contents[0].contents)
            for d in dd.contents:
                if isinstance(d, Tag) and len(d) > 0 and len(d.contents[0]) > 0:
                    #print "world", d
                    auth = d.contents[0].strip().lower()
                    auths.append(auth)
                    #print auth
        #print """"
    highlight_api_db_write(auths, api_id, "auth")

def api_page_read(api_id, url):
    h = httplib2.Http()
    resp, content = h.request(url) #, "PUT", headers={"Content-Type":"text/plain"}
    cmd_p("reading page: "+url)
    soup = BeautifulSoup(content)
    highlight_api_page_read(soup, api_id)
    description_api_page_read(soup, api_id)
    specification_api_page_read(soup, api_id)

def apis_db_write():
    global conn, apis
    #cmd_p("writing api to database")
    c = conn.cursor()
    for api in apis:
        #print api
        api_name = api["name"]
        api_url = api["url"]
        api_desc = api["desc"]
        api_category = api["category"]
        api_date = api["date"]
        # category 
        c.execute("INSERT OR IGNORE INTO category (category_name) VALUES (?)", (api_category,) )
        conn.commit()
        c.execute("SELECT category_id FROM category WHERE category_name = ?", (api_category,))
        category_id = c.fetchone()[0]
        # api
        c.execute("INSERT OR IGNORE INTO api (api_name, api_url, api_description, api_date) VALUES (?, ?, ?, ?)", (api_name, api_url, api_desc, api_date, ) )
        conn.commit()
        c.execute("SELECT api_id FROM api WHERE api_url = ?", (api_url,))
        api_id = c.fetchone()[0]
        # api_category
        c.execute ("INSERT OR IGNORE INTO api_category (api_id, category_id) VALUES (?, ?)", (api_id, category_id, ))
        conn.commit()
        api_page_read(api_id, "http://www.programmableweb.com"+api_url)
        #print "api: "+str(api_name)
    c.execute("SELECT COUNT(api_id) FROM api", )
    apis_total = c.fetchone()[0]
    cmd_p("apis total: "+str(apis_total))
    c.close()




if __name__ == "__main__":
    apis_pages_read("kk")
    print "Hello World";
