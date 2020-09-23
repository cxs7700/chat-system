from src.swen344_db_utils import connect

def buildTables():
    conn = connect()
    cur = conn.cursor()
    
    sql = """
        CREATE TABLE users(
                id	            SERIAL PRIMARY KEY NOT NULL,
                username        VARCHAR(25) UNIQUE NOT NULL,
                email           TEXT NOT NULL UNIQUE,
                phone           TEXT NOT NULL,
                ssn             VARCHAR(11) NOT NULL UNIQUE,
                suspension      TIMESTAMP DEFAULT NULL
            );
            
        CREATE TABLE communities(
            id	            SERIAL PRIMARY KEY NOT NULL,
            name	        VARCHAR(15) UNIQUE
        );
    
        CREATE TABLE channels(
            id              SERIAL PRIMARY KEY NOT NULL,
            name            VARCHAR(20) UNIQUE,
            is_private      BOOLEAN DEFAULT FALSE
        );
        
        CREATE TABLE communities_channels(
            id              SERIAL PRIMARY KEY,
            community_id    INTEGER NOT NULL,
            channel_id      INTEGER NOT NULL,
            FOREIGN KEY (community_id) REFERENCES communities(id) ON DELETE CASCADE,
            FOREIGN KEY (channel_id) REFERENCES channels(id) ON DELETE CASCADE
        );
        
        CREATE TABLE communities_users (
            id              SERIAL PRIMARY KEY NOT NULL,
            community_id    INTEGER NOT NULL,
            user_id         INTEGER NOT NULL,
            isMod           BOOLEAN NOT NULL DEFAULT FALSE,
            FOREIGN KEY (community_id) REFERENCES communities(id) ON DELETE CASCADE,
            FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
        );
        
        CREATE TABLE messages(
            id              SERIAL PRIMARY KEY,
            chname          VARCHAR(15) UNIQUE,
            message         TEXT NOT NULL,
            sender          TEXT,
            receiver        TEXT,
            year            TEXT
        );
        
        CREATE TABLE channels_messages (
            id              SERIAL PRIMARY KEY NOT NULL,
            community_id    INTEGER NOT NULL,
            channel_id      INTEGER NOT NULL,
            message         TEXT NOT NULL,
            year            TEXT,
            FOREIGN KEY (community_id) REFERENCES communities(id) ON DELETE CASCADE,
            FOREIGN KEY (channel_id) REFERENCES channels(id) ON DELETE CASCADE
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
        print("\nUser is suspended from sending messages. The suspension ends on:", data[0][0])
    else:
        print("\nMessage sent successfully.")
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
    
def addUserToChannel():
    print()
    
def makeModerator(community, username):
    conn = connect()
    cur = conn.cursor()
    cur.execute("SELECT * FROM users WHERE username=%s", [username])
    data = cur.fetchall()
    if data[0][0] != None:
        cur.execute("UPDATE communities_users SET isMod=TRUE WHERE user_id=%s", [data[0][0]])
    print("\nYou have successfully made %s a moderator of Community %s." % (username, community))
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
        print("\nUser of ID #%s has insufficient permissions to delete messages." % userID)
    else:
        cur.execute("DELETE FROM channels_messages WHERE id = %s", [messageID])
        print("\nUser of ID #%s has successfully deleted a message." % userID)
    conn.commit()
    conn.close()

def createChannel(userID, community, newChannelName, isPrivate):
    conn = connect()
    cur = conn.cursor()
    cur.execute("SELECT * FROM users WHERE id=%s", [userID])
    data = cur.fetchall()
    if data[0][0] != None:
        cur.execute("SELECT id FROM communities WHERE name = %s;", [community])
        cid = cur.fetchall()
        cur.execute("SELECT COUNT(*) FROM channels WHERE name = %s;", [newChannelName])
        total = cur.fetchall()
        if (total[0][0] < 1): # checks if there is already a channel with the same name
            cur.execute("INSERT INTO channels (name, is_private) VALUES (%s, %s);", [newChannelName, isPrivate])
        cur.execute("SELECT id FROM channels WHERE name = %s;", [newChannelName])
        chid = cur.fetchall()
        cur.execute("INSERT INTO communities_channels (community_id, channel_id) VALUES (%s, %s);", (cid[0][0], chid[0][0]))
        print("\nUser of ID #%s has successfully created channel %s in %s" % (userID, newChannelName, community))
    else: 
        print("\nUser of ID #%s has insufficient permissions to create a channel in this community." % userID)
    conn.commit()
    conn.close()
