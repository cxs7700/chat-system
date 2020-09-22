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
        
        CREATE TABLE communities(
                name	        VARCHAR(15) PRIMARY KEY UNIQUE
            );
        
        CREATE TABLE channels(
            id              SERIAL PRIMARY KEY NOT NULL,
            cname           VARCHAR(15) UNIQUE,
            name            VARCHAR(15) UNIQUE,
            FOREIGN KEY(cname) 
                REFERENCES communities(name)
        );
        
        CREATE TABLE messages(
            id              SERIAL PRIMARY KEY,
            chname          VARCHAR(15) UNIQUE,
            message         TEXT NOT NULL,
            sender          TEXT,
            receiver        TEXT,
            year            TEXT,
            FOREIGN KEY(chname)
                REFERENCES channels(name)
        );
        
        INSERT INTO channels (cname, name) VALUES
                ('SWEN-331', 'General'),
                ('SWEN-440', 'TAs'),
                ('SWEN-344', 'Random'),
                ('SWEN-331', 'General'),
                ('SWEN-440', 'TAs'),
                ('SWEN-344', 'Random'),
                ('SWEN-331', 'General'),
                ('SWEN-440', 'TAs'),
                ('SWEN-344', 'Random');
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
    
# DB3 CRUD Operations
def addUserToCommunity(username, email, phone, ssn, community):
    conn = connect()
    cur = conn.cursor()
    createUser(username, email, phone, ssn)
    sql = """
        INSERT INTO communities_users (community_id, user_id)
            SELECT communities.id, users.id
            FROM communities, users 
            WHERE users.username=%s AND communities.name=%s
    """
    cur.execute(sql, (username, community))
    conn.commit()
    conn.close()
    
def makeModerator(community, username):
    conn = connect()
    cur = conn.cursor()
    cur.execute("SELECT * FROM users WHERE username=%s", [username])
    data = cur.fetchall()
    if data[0][0] != None:
        cur.execute("UPDATE communities_users SET isMod=TRUE WHERE user_id=%s", [data[0][0]])
    print("Successfully made %s a moderator of %s." % (username, community))
    conn.commit()
    conn.close()
    
def deleteMessageFromChannel(userID, messageID, communityID, channelID):
    conn = connect()
    cur = conn.cursor()
    sql = """
        SELECT EXISTS 
        (SELECT * FROM communities_users 
        WHERE community_id = %s AND user_id = %s AND isMod = TRUE);
    """
    cur.execute(sql, [communityID, userID])
    data = cur.fetchall()
    if data[0][0] == False:
        print("Insufficient permissions to delete messages.")
    else:
        cur.execute("DELETE FROM channels_messages WHERE id = %s", [messageID])
        print("Successfully deleted message.")
    conn.commit()
    conn.close()
    # Provide checks to see if the user is a moderator of the community

# def createChannel(username, community, newChannelName):
#     print()
#     # Any user can create a channel
    
# def createPrivateChannel():
#     print()
    