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
          ssn           VARCHAR(11) NOT NULL,
          is_suspended  BOOLEAN NOT NULL DEFAULT FALSE
      );
      
    #    Use INSERT INTO for tests
      INSERT INTO users(username, email, phone, ssn, suspensions) VALUES
          ('Abbott', 'abbott@gmail.com', '123-456-7890', ),
          ('Costello', 'costello@email.com', '123-456-7890', ),
          ('Moe', 'moe@email.com', '123-456-7890', ),
          ('Larry', 'larry@email.com', '123-456-7890', ),
          ('Curly', 'curly@email.com', '123-456-7890', )
      );
      
      
      CREATE TABLE messages(
          id            SERIAL PRIMARY KEY,
          body          TEXT NOT NULL,
          to            INTEGER NOT NULL,
          from          INTEGER NOT NULL,
          time_sent     TIMESTAMP NOT NULL DEFAULT NOW(),
      );
      
      CREATE_TABLE suspensions(
          id            SERIAL PRIMARY KEY,
          user_id       INTEGER NOT NULL,
          expiration    TIMESTAMP NOT NULL
      );
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
          ssn           VARCHAR(11) NOT NULL,
          is_suspended  BOOLEAN NOT NULL DEFAULT FALSE
        );
    """
    cur.execute(drop_sql)
    cur.execute(create_sql)
    conn.commit()
    conn.close()