import unittest
from src.chat import *
from src.swen344_db_utils import connect
import csv
import datetime

class TestChat(unittest.TestCase):
    def setUp(self):
        conn = connect()
        cur = conn.cursor()
        sql = """
            DROP TABLE IF EXISTS users, messages, communities, channels, communities_channels, communities_users, communities_moderators, channels_messages CASCADE;
            
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
        
            INSERT INTO users (username, email, phone, ssn, suspension) VALUES
                ('Abbott', 'abbott@gmail.com', '123-456-7890', '123-45-6789', NULL),
                ('Costello', 'costello@email.com', '123-456-7890', '123-54-6789', NULL),
                ('Moe', 'moe@email.com', '123-456-7890', '321-45-6789', NULL),
                ('Larry', 'larry@email.com', '123-456-7890', '123-45-9876', NULL),
                ('Curly', 'curly@email.com', '123-456-7890', '012-34-5678', '2060-01-01');    
            
            INSERT INTO communities (name) VALUES
                ('SWEN-331'),
                ('SWEN-440'),
                ('SWEN-344');
            
            INSERT INTO channels (name) VALUES
                ('General'),
                ('TAs'),
                ('Random');
                
            INSERT INTO communities_channels (community_id, channel_id) VALUES
                ('1', '1'),
                ('1', '2'),
                ('1', '3'),
                ('2', '1'),
                ('2', '2'),
                ('2', '3'),
                ('3', '1'),
                ('3', '2'),
                ('3', '3');
            
        """    
        cur.execute(sql)
        
        with open('test_data.csv', newline='') as f:
            data = csv.reader(f, delimiter=',', quotechar='"')
            for row in data:
                cur.execute(
                    "INSERT INTO messages (sender, receiver, message, year) VALUES (%s, %s, %s, %s);",
                    (row[0], row[1], row[2], row[3])
                )
            f.close()
        
        with open('whos_on_first.csv', newline='') as f:
            data = csv.reader(f, delimiter=',', quotechar='"')
            for row in data:
                cur.execute(
                    "INSERT INTO messages (sender, message) VALUES (%s, %s);",
                    (row[0], row[1])
                )
            f.close()
            
        with open('db3_populate_channels.csv', newline='') as f:
            data = csv.reader(f, delimiter=',', quotechar='"')
            for row in data:
                cur.execute(
                    "INSERT INTO channels_messages (community_id, channel_id, message, year) VALUES (%s, %s, %s, %s);",
                    (row[0], row[1], row[2], row[3])
                )
            f.close()
        
        conn.commit()
        conn.close()
    
    def tearDown(self):
        conn = connect()
        cur = conn.cursor()
        cur.execute("DROP TABLE IF EXISTS users, messages, communities, channels, communities_channels, communities_users, communities_moderators, channels_messages CASCADE;")
        conn.commit()
        conn.close()
        
    def test_build_tables(self):
        conn = connect()
        cur = conn.cursor()
        cur.execute("SELECT COUNT(*) FROM users;")
        conn.commit()
        self.assertEqual([(5,)], cur.fetchall(), "No rows in users table.")
        conn.close()
        
    def test_build_messages_table(self):
        conn = connect()
        cur = conn.cursor()
        cur.execute("SELECT * FROM messages;")
        conn.commit()
        self.assertIsNotNone(cur.fetchall(), "No rows in messages table.")
        conn.close()
      
    def test_rebuild_tables_is_idempotent(self):
        conn = connect()
        cur = conn.cursor()
        cur.execute("SELECT * FROM users, messages;")
        conn.commit()
        self.assertIsNotNone( cur.fetchall(), "No rows in any table.")
        conn.close()
        
    def test_abbott_is_a_user(self):
        conn = connect()
        cur = conn.cursor()
        cur.execute("SELECT username FROM users WHERE username = 'Abbott';")
        conn.commit()
        self.assertEqual([('Abbott',)], cur.fetchall(), "Abbott is not a user in this database.")
        
    def test_costello_is_a_user(self):
        conn = connect()
        cur = conn.cursor()
        cur.execute("SELECT username FROM users WHERE username = 'Costello';")
        conn.commit()
        self.assertEqual([('Costello',)], cur.fetchall(), "Costello is not a user in this database.")
        
    def test_total_number_of_users(self):
        conn = connect()
        cur = conn.cursor()
        cur.execute("SELECT COUNT(users) FROM users;")
        conn.commit()
        self.assertEqual([(5,)], cur.fetchall(), "Incorrect number of users.")
        conn.close()
        
    def test_total_number_of_messages(self):
        conn = connect()
        cur = conn.cursor()
        cur.execute("SELECT COUNT(message) - 2 FROM messages;")
        conn.commit()
        self.assertEqual([(368,)], cur.fetchall(), "Incorrect number of messages.")
        conn.close()
        
    def test_find_messages(self):
        conn = connect()
        cur = conn.cursor()
        sql = """
            DELETE FROM messages WHERE year = 'Year';
            SELECT COUNT(*) FROM messages 
                WHERE (CAST(year AS INTEGER) >= 1934 AND CAST(year AS INTEGER) <= 1946)
                AND (sender = 'Larry' OR sender = 'Moe' OR sender = 'Curly');
        """
        cur.execute(sql)
        conn.commit()
        self.assertEqual([(8,)], cur.fetchall(), "Incorrect number of messages.")
        conn.close()
        
    def test_suspended_account(self):
        conn = connect()
        cur = conn.cursor()
        cur.execute("SELECT suspension FROM users WHERE suspension = '2060-01-01';")
        conn.commit()
        self.assertEqual([(datetime.datetime(2060, 1, 1),)], cur.fetchall(), "Curly is not suspended until January 1, 2060.")
        conn.close()
        
    
    # DB2 Test Cases    
    def test_create_user_bob(self):
        conn = connect()
        cur = conn.cursor()
        createUser("Bob", "test", "12789", "890239028")
        cur.execute("SELECT * FROM users WHERE username = 'Bob';")
        self.assertEqual([(6, 'Bob', 'test', '12789', '890239028', None)], cur.fetchall(), "User was unsuccessfully created.")
        cur.execute("DELETE FROM users WHERE username = 'Bob';")
        conn.commit()
        conn.close()
        
    def test_update_user_bob(self):
        conn = connect()
        cur = conn.cursor()
        createUser("Bob", "test", "12789", "890239028")
        updateEmailByUsername('bob@gmail.com', 'Bob')
        deleteUserByUsername('Bob')
        cur.execute("SELECT * FROM users WHERE username = 'Bob';")
        conn.commit()
        self.assertEqual([], cur.fetchall(), "Bob is still a user.")
        conn.close()
        
    def test_suspend_curly(self):
        conn = connect()
        cur = conn.cursor()
        suspendUserByUsername('2061-01-01','Curly')
        sendMessage('Curly', 'Abbott', 'Am I suspended?', '2020')
        removeSuspensionByUsername('Curly')
        sendMessage('Curly', 'Abbott', 'I guess I was suspended', '2020')
        cur.execute("SELECT suspension FROM users WHERE username='Curly';")
        conn.commit()
        self.assertEqual([(None,)], cur.fetchall(), "Curly is still suspended.")
        conn.close()
        
    def test_get_messages_between_abbott_and_costello(self):
        conn = connect()
        cur = conn.cursor()
        sql = """
            SELECT COUNT(message) FROM messages 
                WHERE (
                    (sender = 'Abbott' AND receiver = 'Costello')
                    OR (sender = 'Costello' AND receiver = 'Abbott')
                    OR (sender = 'Abbott' AND receiver IS NULL)
                    OR (sender = 'Costello' AND receiver IS NULL)
                )
                AND (message LIKE '%Naturally%');
        """
        cur.execute(sql)
        conn.commit()
        self.assertEqual([(16,)], cur.fetchall(), "Incorrect number of messages.")
        conn.close()
        
    # # DB3 Test Cases
    def test_add_user_to_community(self):
        conn = connect()
        cur = conn.cursor()
        addUserToCommunity("Lex", "lex@gmail.com", "243123823", "987651234", "SWEN-344")
        makeModerator("SWEN-344", "Lex")
        sql = """
            SELECT username FROM users WHERE id IN (SELECT user_id FROM communities_users WHERE isMod = TRUE);
        """
        cur.execute(sql)
        conn.commit()
        self.assertEqual([("Lex",)], cur.fetchall(), "Incorrect name of moderator.")
        conn.close()
        
    def test_delete_message_is_not_mod(self):
        conn = connect()
        cur = conn.cursor()
        addUserToCommunity("Taylor", "taylor@gmail.com", "243123823", "987651234", "SWEN-344")
        cur.execute("SELECT id FROM users WHERE username='Taylor';")
        userID = cur.fetchall()
        cur.execute("SELECT id FROM communities WHERE name='SWEN-344';")
        communityID = cur.fetchall()
        cur.execute("SELECT id FROM channels WHERE name='General';")
        channelID = cur.fetchall()
        deleteMessageFromChannel(userID[0][0], 1, communityID[0][0], channelID[0][0])
        cur.execute("SELECT COUNT(*) FROM channels_messages")
        conn.commit()
        self.assertEqual([(90,)], cur.fetchall(), "Incorrect amount of messages left in the channel.")
        conn.close()
        
    def test_lex_delete_message(self):
        conn = connect()
        cur = conn.cursor()
        addUserToCommunity("Lex", "lex@gmail.com", "243123823", "987651234", "SWEN-344")
        cur.execute("SELECT id FROM users WHERE username='Lex';")
        userID = cur.fetchall()
        cur.execute("SELECT id FROM communities WHERE name='SWEN-331';")
        communityID = cur.fetchall()
        cur.execute("SELECT id FROM channels WHERE name='General';")
        channelID = cur.fetchall()
        deleteMessageFromChannel(userID[0][0], 1, communityID[0][0], channelID[0][0])
        cur.execute("SELECT COUNT(*) FROM channels_messages")
        conn.commit()
        self.assertEqual([(90,)], cur.fetchall(), "Incorrect amount of messages left in the channel.")
        conn.close()
        
    def test_create_channel(self):
        conn = connect()
        cur = conn.cursor()
        addUserToCommunity("Lex", "lex@gmail.com", "243123823", "987651234", "SWEN-344")
        makeModerator("SWEN-344", "Lex")
        cur.execute("SELECT id FROM users WHERE username='Lex';")
        userID = cur.fetchall()
        createChannel(userID[0][0], "SWEN-344", "Kill_Superman", False)
        createChannel(userID[0][0], "SWEN-440", "Kill_Superman", False)
        cur.execute("SELECT id FROM communities WHERE name='SWEN-344';")
        community1 = cur.fetchall()
        cur.execute("SELECT id FROM communities WHERE name='SWEN-440';")
        community2 = cur.fetchall()
        cur.execute("SELECT id FROM channels WHERE name='Kill_Superman';")
        channelID = cur.fetchall()
        sql = """
            SELECT COUNT(*) 
            FROM communities_channels 
            WHERE (community_id=%s OR community_id=%s) AND channel_id=%s;
        """
        cur.execute(sql, [community1[0][0], community2[0][0], channelID[0][0]])
        self.assertEqual([(2,)], cur.fetchall(), "Incorrect amount of channels.")
        conn.commit()
        conn.close()
        
    # def test_private_channel(self):
    #     conn = connect()
    #     cur = conn.cursor()
    #     # add user
    #     addUserToCommunity("i_told_u_1nce", "lex@gmail.com", "243123823", "987651234", "SWEN-344")
    #     cur.execute("SELECT id FROM users WHERE username='i_told_u_1nce';")
    #     userID = cur.fetchall()
    #     # create private channel
    #     createChannel(userID[0][0], "SWEN-344", "Argument Clinic", True)
    #     sql = """
            
    #     """
    #     conn.commit()
    #     conn.close()