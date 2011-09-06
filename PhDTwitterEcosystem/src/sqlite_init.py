# To change this template, choose Tools | Templates
# and open the template in the editor.

__author__="jianhuashao"
__date__ ="$Sep 6, 2011 12:50:17 AM$"

from my_util import cmd_p, db_conn

sql = '''
        -- create table category
        CREATE TABLE IF NOT EXISTS category (
            category_id  INTEGER PRIMARY KEY,
            category_name TEXT UNIQUE NOT NULL
        );
        CREATE TABLE IF NOT EXISTS api (
            api_id  INTEGER PRIMARY KEY,
            api_name TEXT NOT NULL, 
            api_description TEXT,
            api_url TEXT UNIQUE NOT NULL,
            api_date TEXT NOT NULL
        );
        CREATE TABLE IF NOT EXISTS api_category (
            api_category_id INTEGER PRIMARY KEY,
            api_id      INTEGER NOT NULL,
            category_id INTEGER NOT_NULL,
            FOREIGN KEY (api_id) REFERENCES api(api_id),
            FOREIGN KEY (category_id) REFERENCES category(category_id)
            UNIQUE (api_id, category_id)
        );
        
        CREATE TABLE IF NOT EXISTS mashup (
            mashup_id  INTEGER PRIMARY KEY,
            mashup_name TEXT NOT NULL, 
            mashup_description TEXT,
            mashup_url TEXT UNIQUE NOT NULL
        );
        CREATE TABLE IF NOT EXISTS mashup_api (
            mashup_api_id INTEGER PRIMARY KEY,
            mashup_id   INTEGER NOT NULL,
            api_id      INTEGER NOT_NULL,
            FOREIGN KEY (mashup_id) REFERENCES mshup(mashup_id),
            FOREIGN KEY (api_id) REFERENCES api(api_id)
            UNIQUE (mashup_id, api_id)
        );
        
        CREATE TABLE IF NOT EXISTS tag (
            tag_id  INTEGER PRIMARY KEY,
            tag_name TEXT UNIQUE NOT NULL
        );
        CREATE TABLE IF NOT EXISTS tag_api (
            tag_api_id INTEGER PRIMARY KEY,
            api_id      INTEGER NOT NULL,
            tag_id INTEGER NOT_NULL,
            FOREIGN KEY (api_id) REFERENCES api(api_id),
            FOREIGN KEY (tag_id) REFERENCES tag(tag_id),
            UNIQUE (api_id, tag_id)
        );
        CREATE TABLE IF NOT EXISTS tag_mashup (
            tag_mashup_id INTEGER PRIMARY KEY,
            mashup_id      INTEGER NOT NULL,
            tag_id INTEGER NOT_NULL,
            FOREIGN KEY (mashup_id) REFERENCES mashup(mashup_id),
            FOREIGN KEY (tag_id) REFERENCES tag(tag_id),
            UNIQUE (mashup_id, tag_id)
        );
        
        -- this description is from each api page, rather than from directory
        CREATE TABLE IF NOT EXISTS api_description_long (
            api_id INTEGER PRIMARY KEY,
            description TEXT NOT NULL,
            FOREIGN KEY (api_id) REFERENCES api(api_id)
        );
        
        CREATE TABLE IF NOT EXISTS protocol (
            protocol_id  INTEGER PRIMARY KEY,
            protocol_name TEXT UNIQUE NOT NULL
        );
        CREATE TABLE IF NOT EXISTS protocol_api (
            protocol_api_id INTEGER PRIMARY KEY,
            api_id INTEGER NOT NULL,
            protocol_id INTEGER NOT_NULL,
            FOREIGN KEY (api_id) REFERENCES api(api_id),
            FOREIGN KEY (protocol_id) REFERENCES protocol(protocol_id),
            UNIQUE (api_id, protocol_id)
        );
        CREATE TABLE IF NOT EXISTS protocol_mashup (
            protocol_mashup_id INTEGER PRIMARY KEY,
            mashup_id      INTEGER NOT NULL,
            protocol_id INTEGER NOT_NULL,
            FOREIGN KEY (mashup_id) REFERENCES mashup(mashup_id),
            FOREIGN KEY (protocol_id) REFERENCES protocol(protocol_id),
            UNIQUE (mashup_id, protocol_id)
        );
        
        CREATE TABLE IF NOT EXISTS dataformat (
            dataformat_id  INTEGER PRIMARY KEY,
            dataformat_name TEXT UNIQUE NOT NULL
        );
        CREATE TABLE IF NOT EXISTS dataformat_api (
            dataformat_api_id INTEGER PRIMARY KEY,
            api_id INTEGER NOT NULL,
            dataformat_id INTEGER NOT_NULL,
            FOREIGN KEY (api_id) REFERENCES api(api_id),
            FOREIGN KEY (dataformat_id) REFERENCES dataformat(dataformat_id),
            UNIQUE (api_id, dataformat_id)
        );
        CREATE TABLE IF NOT EXISTS dataformat_mashup (
            dataformat_mashup_id INTEGER PRIMARY KEY,
            mashup_id      INTEGER NOT NULL,
            dataformat_id INTEGER NOT_NULL,
            FOREIGN KEY (mashup_id) REFERENCES mashup(mashup_id),
            FOREIGN KEY (dataformat_id) REFERENCES dataformat(dataformat_id),
            UNIQUE (mashup_id, dataformat_id)
        );
        
        CREATE TABLE IF NOT EXISTS description (
            description_id  INTEGER PRIMARY KEY,
            description_name TEXT UNIQUE NOT NULL
        );
        CREATE TABLE IF NOT EXISTS description_api (
            description_api_id INTEGER PRIMARY KEY,
            api_id INTEGER NOT NULL,
            description_id INTEGER NOT_NULL,
            FOREIGN KEY (api_id) REFERENCES api(api_id),
            FOREIGN KEY (description_id) REFERENCES description(description_id),
            UNIQUE (api_id, description_id)
        );
        CREATE TABLE IF NOT EXISTS description_mashup (
            description_mashup_id INTEGER PRIMARY KEY,
            mashup_id      INTEGER NOT NULL,
            description_id INTEGER NOT_NULL,
            FOREIGN KEY (mashup_id) REFERENCES mashup(mashup_id),
            FOREIGN KEY (description_id) REFERENCES description(description_id),
            UNIQUE (mashup_id, description_id)
        );
        
        CREATE TABLE IF NOT EXISTS auth (
            auth_id  INTEGER PRIMARY KEY,
            auth_name TEXT UNIQUE NOT NULL
        );
        CREATE TABLE IF NOT EXISTS auth_api (
            auth_api_id INTEGER PRIMARY KEY,
            api_id INTEGER NOT NULL,
            auth_id INTEGER NOT_NULL,
            FOREIGN KEY (api_id) REFERENCES api(api_id),
            FOREIGN KEY (auth_id) REFERENCES auth(auth_id),
            UNIQUE (api_id, auth_id)
        );
        CREATE TABLE IF NOT EXISTS auth_mashup (
            auth_mashup_id INTEGER PRIMARY KEY,
            mashup_id      INTEGER NOT NULL,
            auth_id INTEGER NOT_NULL,
            FOREIGN KEY (mashup_id) REFERENCES mashup(mashup_id),
            FOREIGN KEY (auth_id) REFERENCES auth(auth_id),
            UNIQUE (mashup_id, auth_id)
        );
        
        CREATE TABLE IF NOT EXISTS date (
            date_id INTEGER PRIMARY KEY,
            date TEXT NOT NULL UNIQUE
        );
        CREATE TABLE IF NOT EXISTS date_mashup (
            date_mashup_id INTEGER PRIMARY KEY,
            mashup_id      INTEGER NOT NULL,
            date_id INTEGER NOT_NULL,
            FOREIGN KEY (mashup_id) REFERENCES mashup(mashup_id),
            FOREIGN KEY (date_id) REFERENCES date(date_id),
            UNIQUE (mashup_id, date_id)
        );
        
        CREATE TABLE IF NOT EXISTS author (
            author_id INTEGER PRIMARY KEY,
            author_name TEXT NOT NULL,
            author_url TEXT NOT NULL UNIQUE
        );
        CREATE TABLE IF NOT EXISTS author_mashup (
            author_mashup_id INTEGER PRIMARY KEY,
            mashup_id      INTEGER NOT NULL,
            author_id INTEGER NOT_NULL,
            FOREIGN KEY (mashup_id) REFERENCES mashup(mashup_id),
            FOREIGN KEY (author_id) REFERENCES author(author_id),
            UNIQUE (mashup_id, author_id)
        );
    '''

conn = db_conn()

def sqlite_init():
    global conn
    cmd_p("start to init the database")
    c = conn.cursor()
    c.executescript(sql)
    conn.commit()
    c.execute('''SELECT * FROM SQLITE_MASTER''')
    tables = c.fetchall()
    print ("database tables in total: ",len(tables))
    for row in tables:
        print "\t(["+row[0]+"],["+row[2]+"])"
    c.close()
    cmd_p("finish init databse")
        


if __name__ == "__main__":
    print "Hello World"
