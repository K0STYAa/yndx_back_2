from pkg.store.postgres import postgres

conn = postgres.get_db_connection()

cur = conn.cursor()

cur.execute('DROP TABLE IF EXISTS files;')

cur.execute("CREATE TABLE files (type varchar(10) CHECK (type = 'FOLDER' OR type = 'FILE'),"
                                   'url varchar(100),'
                                   'id varchar(40) PRIMARY KEY,'
                                   'size integer CHECK (size >= 0),'
                                   'parentId varchar(40),'
                                   'date timestamp DEFAULT CURRENT_TIMESTAMP,'
                                   "children varchar(40)[] DEFAULT '{}');"
                                   )

conn.commit()

cur.close()
conn.close()