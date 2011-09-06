#! /usr/bin/python

# To change this template, choose Tools | Templates
# and open the template in the editor.

__author__="jianhuashao"
__date__ ="$Sep 6, 2011 1:27:38 AM$"

import httplib2
from my_util import cmd_p, db_conn
from BeautifulSoup import Tag, NavigableString, BeautifulSoup

conn = db_conn()
url_root = "http://www.programmableweb.com"


def mashup_exist(mashup_name):
    global conn
    c = conn.cursor()
    c.execute("SELECT mashup_id FROM mashup WHERE mashup_name = ? ", (mashup_name,))
    result = c.fetchone()
    c.close()
    if result == None:
        return -1
    else: 
        return result[0]


def mashups_page_read(url):
    global mashups
    mashups = []
    h = httplib2.Http()
    resp, content = h.request(url) #, "PUT", headers={"Content-Type":"text/plain"}
    cmd_p("reading page: "+url)
    #print type(content)
    #print content
    soup = BeautifulSoup(content)
    #print type(soup)
    lists = soup.findAll("table", attrs={"summary":"Web 2.0 Mashups", "id":"mashups"})
    #print type(lists[0].contents)
    i = -2
    #print i
    for list in lists[0].contents:
        #print list
        if isinstance(list, Tag) :
            i = i+1
            #print i
            if i == -1:
                i = 0
                continue
            #for l in list.contents:
            #    print type(l), l
            #print len(list.contents)
            if len(list.contents) != 6:
                sys.exit("api length is not equal to 4")
            mashup_name = ""
            mashup_url = ""
            mashup_desc = ""
            mashup_category = ""
            mashup_name = list.contents[3].contents[0].contents[0].strip().encode("ascii", 'ignore').lower()
            if mashup_exist(mashup_name) != -1:
                continue
            mashup_url = list.contents[1].contents[0]["href"].encode("ascii", 'ignore').strip().lower()
            mashup_desc = list.contents[3].contents[1].contents[0].strip()
            mashup = {
                "name": mashup_name,
                "url": mashup_url,
                "desc": mashup_desc,
                #"apis": mashup_apis
                }
            print mashup
            mashups.append(mashup)
    #print apis
    pages = soup.findAll("img", attrs={"src":"/images/listnav_next.png"})
    if len(pages) == 0:
        return False
    else:
        return True
    
    
def description_mashup_db_write(elements, mashup_id, highlight):
    global conn
    #cmd_p("write "+highlight+" into database")
    c = conn.cursor()
    c.execute("SELECT "+highlight+"_id FROM "+highlight+"_mashup WHERE mashup_id = ?", (mashup_id, ))
    if c.fetchone() == None:
        c.execute("INSERT OR IGNORE INTO "+highlight+" ("+highlight+"_name) VALUES (?)", (elements,) )
        conn.commit()
        c.execute("SELECT MAX("+highlight+"_id) FROM "+highlight, )
        element_id = c.fetchone()[0]
        c.execute ("INSERT OR IGNORE INTO "+highlight+"_mashup (mashup_id, "+highlight+"_id) VALUES (?, ?)", (mashup_id, element_id, ))
        conn.commit()
    c.execute("SELECT COUNT("+highlight+"_id) FROM "+highlight+"", )
    element_total = c.fetchone()[0]
    cmd_p(""+highlight+"s total: "+str(element_total))
    c.close()



def description_mashup_page_read(soup, mashup_id):
    description = ""
    lists = soup.findAll("div", attrs={"class":"span-8 last"})
    jump = 0
    for list in lists:
        #print list
        if jump == 2:
            break
        for l in list.contents:
            #print l
            if jump == 2:
                break
            if isinstance(l, Tag):
                if l.contents[0].strip().lower() == "description":
                    jump = 1
                elif jump == 1:
                    jump = 2
                    description = l.contents[0].strip()
                else:
                    break
                #break
            #break
        break
    #print "cool", description.encode("ascii", 'ignore')
    description_mashup_db_write(description, mashup_id, "description")


def tags_mashup_db_write(tags, mashup_id):
    global conn
    #cmd_p("write tags into database")
    c = conn.cursor()
    for tag_name in tags:
        c.execute("INSERT OR IGNORE INTO tag (tag_name) VALUES (?)", (tag_name,) )
        conn.commit()
        c.execute("SELECT tag_id FROM tag WHERE tag_name=?", (tag_name,))
        tag_id = c.fetchone()[0]
        c.execute ("INSERT OR IGNORE INTO tag_mashup (mashup_id, tag_id) VALUES (?, ?)", (mashup_id, tag_id, ))
        conn.commit()
    c.execute("SELECT COUNT(tag_id) FROM tag", )
    tag_total = c.fetchone()[0]
    cmd_p("tags total: "+str(tag_total))
    c.close()


def tags_mashup_page_read(soup, mashup_id):
    tags = []
    lists = soup.findAll("dl", attrs={"class":"inline dt40 mB15"})
    for list in lists:
        #print list.contents[0], list.contents[1:]
        dt = list.contents[0]
        dd = list.contents[1:]
        #print dt.contents[0].strip().lower()
        if dt.contents[0].strip().lower() == "tags":
            #print type(dd)
            #print dd
            for d in dd:
                if isinstance(d, Tag) and len(d.contents)>0 and len(d.contents[0])>0 and len(d.contents[0].contents)>0:
                    #print d.contents[0].contents
                    tag = d.contents[0].contents[0].strip().lower()
                    tags.append(tag)
        #print ""
    #print tags
    tags_mashup_db_write(tags, mashup_id)
    

def api_mashup_db_write(apis, mashup_id):
    global conn
    #cmd_p("write apis into database")
    c = conn.cursor()
    for api in apis:
        #print "api:", api
        c.execute("SELECT api_id FROM api WHERE api_url = ?", (api,))
        result = c.fetchone()
        #print result
        if result == None:
            cmd_p("error:api("+api+") is not exist for mashup("+str(mashup_id)+")")
            #sys.exit(mashup_name)
            continue
        api_id = result[0]
        c.execute ("INSERT OR IGNORE INTO mashup_api (mashup_id, api_id) VALUES (?, ?)", (mashup_id, api_id, ))
        conn.commit()
    cmd_p("apis total: "+str(len(apis)))
    c.close()    
    

def date_mashup_db_write(elements, mashup_id, highlight):
    global conn
    #cmd_p("write "+highlight+" into database")
    c = conn.cursor()
    for element_name in elements:
        c.execute("INSERT OR IGNORE INTO "+highlight+" ("+highlight+") VALUES (?)", (element_name,) )
        conn.commit()
        c.execute("SELECT "+highlight+"_id FROM "+highlight+" WHERE "+highlight+" = ?", (element_name,))
        element_id = c.fetchone()[0]
        c.execute ("INSERT OR IGNORE INTO "+highlight+"_mashup (mashup_id, "+highlight+"_id) VALUES (?, ?)", (mashup_id, element_id, ))
        conn.commit()
    c.execute("SELECT COUNT("+highlight+"_id) FROM "+highlight+"", )
    element_total = c.fetchone()[0]
    cmd_p(""+highlight+"s total: "+str(element_total))
    c.close()


def author_mashup_db_write(elements, mashup_id, highlight):
    global conn
    #cmd_p("write "+highlight+" into database")
    c = conn.cursor()
    for element in elements:
        #print element["url"], "hello"
        if element["url"] != None:
            c.execute("INSERT OR IGNORE INTO "+highlight+" ("+highlight+"_name, "+highlight+"_url) VALUES (?, ?)", (element["name"], element["url"], ) )
            conn.commit()
            c.execute("SELECT "+highlight+"_id FROM "+highlight+" WHERE "+highlight+"_url = ?", (element["url"],))
            element_id = c.fetchone()[0]
            c.execute ("INSERT OR IGNORE INTO "+highlight+"_mashup (mashup_id, "+highlight+"_id) VALUES (?, ?)", (mashup_id, element_id, ))
            conn.commit()        
    c.execute("SELECT COUNT("+highlight+"_id) FROM "+highlight+"", )
    element_total = c.fetchone()[0]
    cmd_p(""+highlight+"s total: "+str(element_total))
    c.close()


def summary_mashup_page_read(soup, mashup_id):
    apis = []
    dates = []
    authors = []
    lists = soup.findAll("dl", attrs={"class":"inline dt40"})
    for list in lists:
        #print list.contents[0], list.contents[1:]
        dt = list.contents[0]
        dd = list.contents[1:]
        #print dt.contents[0].strip().lower()
        if dt.contents[0].strip().lower() == "apis":
            #print type(dd)
            #print dd
            for d in dd:
                if isinstance(d, Tag) and len(d.contents)>0 and len(d.contents[0])>0:
                    #print d.contents[0]["href"].strip().lower()
                    api = d.contents[0]["href"].encode("ascii", 'ignore').strip().lower()
                    apis.append(api)
        if dt.contents[0].strip().lower() == "added":
            #print type(dd)
            #print dd
            for d in dd:
                if isinstance(d, Tag) and len(d.contents)>0 :
                    #print d.contents[0]
                    date = d.contents[0].strip().lower()
                    dates.append(date)
        if dt.contents[0].strip().lower() == "who":
            #print type(dd)
            #print dd
            for d in dd:
                if isinstance(d, Tag) and isinstance(d.contents[0], Tag) :
                    #print d, "hello"
                    #print type(d.contents[0]['href'])
                    #print type(d.contents[0])
                    #print d.contents[0].contents
                    author_name = "noname"
                    if len(d.contents[0].contents) != 0:
                        #print d.contents[0].contents[0].encode("ascii", 'ignore').strip().lower()
                        author_name = d.contents[0].contents[0].encode("ascii", 'ignore').strip().lower()
                    author_url = d.contents[0]["href"].encode("ascii", 'ignore').strip().lower()
                    author = {
                        "name": author_name,
                        "url": author_url
                        }
                    authors.append(author)
                    #print author
    api_mashup_db_write(apis, mashup_id)   
    date_mashup_db_write(dates, mashup_id, "date")
    author_mashup_db_write(authors, mashup_id, "author")


def mashup_page_read(url, mashup_id):
    h = httplib2.Http()
    resp, content = h.request(url) #, "PUT", headers={"Content-Type":"text/plain"}
    cmd_p("reading page: "+url)
    soup = BeautifulSoup(content)
    description_mashup_page_read(soup, mashup_id)
    tags_mashup_page_read(soup, mashup_id)
    summary_mashup_page_read(soup, mashup_id)
    
    
def mashups_db_write():
    global conn, mashups
    cmd_p("writing mashup to database")
    c = conn.cursor()
    cool = conn.cursor()
    for mashup in mashups:
        #print api
        mashup_name = mashup["name"]
        mashup_url = mashup["url"]
        mashup_desc = mashup["desc"]
        #mashup_apis = mashup["apis"]
        # mashup
        #print ((mashup_name, mashup_url, mashup_desc,) )
        c.execute("INSERT OR IGNORE INTO mashup (mashup_name, mashup_url, mashup_description) VALUES (?, ?, ?)", (mashup_name, mashup_url, mashup_desc,) )
        conn.commit()
        c.execute("SELECT mashup_id FROM mashup WHERE mashup_url = ? ", (mashup_url,))
        #p = c.fetchone()
        #print p, mashup_name
        mashup_id = c.fetchone()[0]
        # api_category
        mashup_page_read("http://www.programmableweb.com"+mashup_url, mashup_id)
    c.execute("SELECT COUNT(mashup_id) FROM mashup", )
    mashup_total = c.fetchone()[0]
    cmd_p("mashup total: "+str(mashup_total))
    c.close()    
    

def mashups_pages_read():
    global mashups, url_root
    mashups = []
    url = url_root+"/mashups/directory/"
    i = 0
    next = True
    while next:
        i = i+1
        u = url+str(i)
        #print u
        next = mashups_page_read(u)
        mashups_db_write()

if __name__ == "__main__":
    mashups_pages_read()
    print "Hello World";
