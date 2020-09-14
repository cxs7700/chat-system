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
    
    
##############################
#       CRUD OPERATIONS      #
##############################
    
# USERS
def createUser(username, email, phone, ssn, suspension):
    conn = connect()
    cur = conn.cursor()
    cur.execute("INSERT INTO users VALUES (%s, %s, %s, %s, %s);", (username, email, phone, ssn, suspension))
    conn.commit()
    conn.close
    
def getAllUsers():
    conn = connect()
    cur = conn.cursor()
    cur.execute("SELECT * FROM users;")
    conn.commit()
    conn.close
    
def getUserByUserID(id):
    conn = connect()
    cur = conn.cursor()
    cur.execute("SELECT * FROM users WHERE id=%s;", id)
    conn.commit()
    conn.close
    
def getUsersByUsername(username):
    conn = connect()
    cur = conn.cursor()
    cur.execute("SELECT * FROM users WHERE username=%s;", username)
    conn.commit()
    conn.close
    
def deleteUserByUserID(id):
    conn = connect()
    cur = conn.cursor()
    cur.execute("DELETE FROM users WHERE id=%s;", id)
    conn.commit()
    conn.close

def changeUsernameByUserID(newUsername, id):
    conn = connect()
    cur = conn.cursor()
    cur.execute("UPDATE users SET username=%s WHERE id=%s;", (newUsername, id))
    conn.commit()
    conn.close
    
def changeEmailByUserID(newEmail, id):
    conn = connect()
    cur = conn.cursor()
    cur.execute("UPDATE users SET email=%s WHERE id=%s;", (newEmail, id))
    conn.commit()
    conn.close
    
def changePhoneByUserID(newPhone, id):
    conn = connect()
    cur = conn.cursor()
    cur.execute("UPDATE users SET phone=%s WHERE id=%s", (newPhone, id))
    conn.commit()
    conn.close
    
def removeSuspensionByUserID(id):
    conn = connect()
    cur = conn.cursor()
    cur.execute("UPDATE users SET suspension=%s WHERE id=%s;", (NULL, id))
    conn.commit()
    conn.close
    
def suspendUserByUserID(suspension, id):
    conn = connect()
    cur = conn.cursor()
    cur.execute("UPDATE users SET suspension=%s WHERE id=%s", (suspension, id))
    conn.commit()
    conn.close

    
# MESSAGES
def createMessage():
    conn = connect()
    cur = conn.cursor()
    
    conn.commit()
    conn.close

def getAllMessages():
    conn = connect()
    cur = conn.cursor()
    
    conn.commit()
    conn.close
    
def deleteMessage():
    conn = connect()
    cur = conn.cursor()
    
    conn.commit()
    conn.close
    
def deleteAllMessages():
    conn = connect()
    cur = conn.cursor()
    
    conn.commit()
    conn.close
    
def editMessage():
    conn = connect()
    cur = conn.cursor()
    
    conn.commit()
    conn.close
    
def x():
    conn = connect()
    cur = conn.cursor()
    
    conn.commit()
    conn.close