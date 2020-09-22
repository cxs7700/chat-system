from src.swen344_db_utils import connect

def buildTables():
    conn = connect()
    cur = conn.cursor()
    
    sql = """
        CREATE TABLE users(
            id	            SERIAL PRIMARY KEY NOT NULL,
            username        VARCHAR(20) UNIQUE NOT NULL,
            email           TEXT NOT NULL UNIQUE,
            phone           TEXT NOT NULL,
            ssn             VARCHAR(11) NOT NULL UNIQUE,
            suspension      TIMESTAMP DEFAULT NULL
        );
        
        CREATE TABLE messages(
                id              SERIAL PRIMARY KEY,
                chname          VARCHAR(15) NOT NULL UNIQUE,
                message         TEXT NOT NULL,
                sender          TEXT,
                receiver        TEXT,
                year            TEXT,
                FOREIGN KEY(chname)
                    REFERENCES channels(name)
            );
        
        CREATE TABLE communities(
            name	        VARCHAR(15) PRIMARY KEY NOT NULL UNIQUE
        );
        
        CREATE TABLE channels(
            id              SERIAL PRIMARY KEY NOT NULL,
            cname           VARCHAR(15) NOT NULL UNIQUE,
            name            VARCHAR(15) NOT NULL UNIQUE,
            FOREIGN KEY(cname) 
                REFERENCES communities(name)
        );
        
        CREATE TABLE privileges(
            cname           VARCHAR(15) NOT NULL UNIQUE,
            role            VARCHAR(11) NOT NULL UNIQUE,
            FOREIGN KEY(cname)
                REFERENCES communities(name)
        );
        
        CREATE TABLE admins(
            id              SERIAL PRIMARY KEY NOT NULL,
            uid             INTEGER NOT NULL UNIQUE,
            cname           VARCHAR(15) NOT NULL UNIQUE,
            FOREIGN KEY(cname)
                REFERENCES communities(name),
            FOREIGN KEY(uid)
                REFERENCES users(id)
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
            year            DATETIME DEFAULT NOW()
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
def createUser(username, email, phone, ssn):
    conn = connect()
    cur = conn.cursor()
    cur.execute("INSERT INTO users (username, email, phone, ssn) VALUES (%s, %s, %s, %s);", (username, email, phone, ssn))
    conn.commit()
    conn.close()
    
def getAllUsers():
    conn = connect()
    cur = conn.cursor()
    cur.execute("SELECT * FROM users;")
    conn.commit()
    conn.close()
    
def getUserByUserID(id):
    conn = connect()
    cur = conn.cursor()
    cur.execute("SELECT * FROM users WHERE id=%s;", id)
    conn.commit()
    conn.close()
    
def getUserByUsername(username):
    conn = connect()
    cur = conn.cursor()
    cur.execute("SELECT * FROM users WHERE username=%s;", username)
    conn.commit()
    conn.close()
    
def deleteUserByUserID(id):
    conn = connect()
    cur = conn.cursor()
    cur.execute("DELETE FROM users WHERE id=%s;", id)
    conn.commit()
    conn.close()
    
def deleteUserByUsername(username):
    conn = connect()
    cur = conn.cursor()
    cur.execute("DELETE FROM users WHERE username=%s;", [username])
    conn.commit()
    conn.close()

def updateUsernameByUserID(newUsername, id):
    conn = connect()
    cur = conn.cursor()
    cur.execute("UPDATE users SET username=%s WHERE id=%s;", (newUsername, id))
    conn.commit()
    conn.close()
    
def updateEmailByUserID(newEmail, id):
    conn = connect()
    cur = conn.cursor()
    cur.execute("UPDATE users SET email=%s WHERE id=%s;", (newEmail, id))
    conn.commit()
    conn.close()
    
def updateEmailByUsername(newEmail, username):
    conn = connect()
    cur = conn.cursor()
    cur.execute("UPDATE users SET email=%s WHERE username=%s;", (newEmail, username))
    conn.commit()
    conn.close()
    
def updatePhoneByUserID(newPhone, id):
    conn = connect()
    cur = conn.cursor()
    cur.execute("UPDATE users SET phone=%s WHERE id=%s", (newPhone, id))
    conn.commit()
    conn.close()
    
def removeSuspensionByUserID(id):
    conn = connect()
    cur = conn.cursor()
    cur.execute("UPDATE users SET suspension=%s WHERE id=%s;", (None, id))
    conn.commit()
    conn.close()
    
def removeSuspensionByUsername(username):
    conn = connect()
    cur = conn.cursor()
    cur.execute("UPDATE users SET suspension=%s WHERE username=%s;", (None, username))
    conn.commit()
    conn.close()
    
def suspendUserByUserID(suspension, id):
    conn = connect()
    cur = conn.cursor()
    cur.execute("UPDATE users SET suspension=%s WHERE id=%s", (suspension, id))
    conn.commit()
    conn.close()
    
def suspendUserByUsername(suspension, username):
    conn = connect()
    cur = conn.cursor()
    cur.execute("UPDATE users SET suspension=%s WHERE username=%s", (suspension, username))
    conn.commit()
    conn.close()

    
# MESSAGES
def sendMessage(sender, receiver, message, year):
    print("\nAttempting to send a message...")
    conn = connect()
    cur = conn.cursor()
    cur.execute("SELECT suspension FROM users WHERE username=%s", [sender])
    data = cur.fetchall()
    if data[0][0] != None:
        print("User is suspended from sending messages. The suspension ends on:", data[0][0])
    else:
        print("Message sent successfully.")
        cur.execute("INSERT INTO messages (message, sender, receiver, year) VALUES (%s, %s, %s, %s);", (message, sender, receiver, year))
    conn.commit()
    conn.close()
    
def getAllMessagesByUsername(username):
    conn = connect()
    cur = conn.cursor()
    cur.execute("SELECT * FROM messages WHERE sender=%s", [username])
    conn.commit()
    conn.close()
    
def deleteMessage(id):
    conn = connect()
    cur = conn.cursor()
    cur.execute("DELETE FROM messages WHERE id=%s", [id])
    conn.commit()
    conn.close()
    
def deleteAllMessages(username):
    conn = connect()
    cur = conn.cursor()
    cur.execute("DELETE * FROM messages;")
    conn.commit()
    conn.close()
    
def editMessage(newMessage, id):
    conn = connect()
    cur = conn.cursor()
    cur.execute("UPDATE messages SET message=%s WHERE id=%s", (newMessage, id))
    conn.commit()
    conn.close()
    