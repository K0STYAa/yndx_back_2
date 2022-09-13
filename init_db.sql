DROP TABLE IF EXISTS files;

CREATE TABLE files (type varchar(10) CHECK (type = 'FOLDER' OR type = 'FILE'),
                    url varchar(100) NOT NULL,
                    id varchar(40) PRIMARY KEY,
                    size integer CHECK (size >= 0),
                    parentId varchar(40),
                    date timestamp DEFAULT CURRENT_TIMESTAMP,
                    children varchar(40)[] DEFAULT '{}');