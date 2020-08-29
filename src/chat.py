from src.swen344_db_utils import connect

def buildTables():
    conn = connect()
    cur = conn.cursor()
    
    # CREATE TABLE for users, etc. with basic information, set up columns
    # INSERT INTO table with dummy data (email, phone number, social security)
    sql = """
        CREATE TABLE users(
            id	        SERIAL PRIMARY KEY NOT NULL,
            username      VARCHAR(20) NOT NULL,
            email         TEXT NOT NULL UNIQUE,
            phone         TEXT NOT NULL,
            ssn           VARCHAR(11) NOT NULL UNIQUE,
            is_suspended  BOOLEAN NOT NULL DEFAULT FALSE
        );
        
        INSERT INTO users(username, email, phone, ssn, suspensions) VALUES
            ('Abbott', 'abbott@gmail.com', '123-456-7890', '123-45-6789', TRUE),
            ('Costello', 'costello@email.com', '123-456-7890', '123-54-6789', FALSE),
            ('Moe', 'moe@email.com', '123-456-7890', '321-45-6789', TRUE),
            ('Larry', 'larry@email.com', '123-456-7890', '123-45-9876', FALSE),
            ('Curly', 'curly@email.com', '123-456-7890', '012-34-5678', TRUE)
        ;
        
        
        CREATE TABLE messages(
            id            SERIAL PRIMARY KEY,
            body          TEXT NOT NULL,
            to            INTEGER NOT NULL,
            from          INTEGER NOT NULL,
            time_sent     TIMESTAMP NOT NULL DEFAULT NOW(),
        );
        
        INSERT INTO messages(body, to, from, time_sent) VALUES
            ('Hello', 1, 2, '2020-2-19 10:23:54+02'),
            ('Bye', 2, 1, '2020-1-19 10:23:54+02'),
            ('I have a crush on u bro', 3, 4, '2020-3-19 10:23:54+02'),
            ('Nice meme yesterday', 4, 3, '2020-4-19 10:23:54+02'),
            ('WHITE CLAWS BABY!', 5, 1, '2020-5-19 10:23:54+02')
        ;
        
        
        CREATE TABLE suspensions(
            id            SERIAL PRIMARY KEY,
            user_id       INTEGER NOT NULL,
            expiration    TIMESTAMP NOT NULL
        );
        
        INSERT INTO suspensions(user_id, expiration) VALUES
            (1, '2020-10-19 10:23:54+02'),
            (2, '2020-11-19 10:23:54+02'),
            (3, '2020-11-19 11:23:54+02'),
            (4, '2020-11-19 12:23:54+02'),
            (5, '2020-11-19 1:23:54+02')
        ;
    """
    cur.execute(sql)
    conn.commit() # don't forget this!
    conn.close()
  
def rebuildTables():
    conn = connect()
    cur = conn.cursor()
    drop_sql = """
        DROP TABLE IF EXISTS users
    """
    create_sql = """
        CREATE TABLE users(
          id	        SERIAL PRIMARY KEY NOT NULL,
          username      VARCHAR(20) NOT NULL,
          email         TEXT NOT NULL UNIQUE,
          phone         TEXT NOT NULL,
          ssn           VARCHAR(11) NOT NULL UNIQUE,
          is_suspended  BOOLEAN NOT NULL DEFAULT FALSE
        );
    """
    cur.execute(drop_sql)
    cur.execute(create_sql)
    conn.commit()
    conn.close()