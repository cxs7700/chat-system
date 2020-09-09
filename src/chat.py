from src.swen344_db_utils import connect

def buildTables():
    conn = connect()
    cur = conn.cursor()
    
    sql = """
        CREATE TABLE users(
            id	            SERIAL PRIMARY KEY NOT NULL,
            username        VARCHAR(20) NOT NULL,
            email           TEXT NOT NULL UNIQUE,
            phone           TEXT NOT NULL,
            ssn             VARCHAR(11) NOT NULL UNIQUE,
            suspension      TIMESTAMP DEFAULT NULL
        );
        
        CREATE TABLE messages(
            id              SERIAL PRIMARY KEY,
            message         TEXT NOT NULL,
            sender          TEXT,
            receiver        TEXT,
            year            TEXT
        );
    """
    cur.execute(sql)
    conn.commit() 
    conn.close()
  
def rebuildTables():
    conn = connect()
    cur = conn.cursor()
    drop_sql = """
        DROP TABLE IF EXISTS users;
        DROP TABLE IF EXISTS messages;
        DROP TABLE IF EXISTS suspensions;
    """
    create_sql = """
        CREATE TABLE users(
            id	            SERIAL PRIMARY KEY NOT NULL,
            username        VARCHAR(20) NOT NULL,
            email           TEXT NOT NULL UNIQUE,
            phone           TEXT NOT NULL,
            ssn             VARCHAR(11) NOT NULL UNIQUE,
            suspension      TIMESTAMP DEFAULT NULL
        );
        
        CREATE TABLE messages(
            id              SERIAL PRIMARY KEY,
            message         TEXT NOT NULL,
            sender          TEXT,
            receiver        TEXT,
            year            TEXT
        );
    """
    cur.execute(drop_sql)
    cur.execute(create_sql)
    conn.commit()
    conn.close()