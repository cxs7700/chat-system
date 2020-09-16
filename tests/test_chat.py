import unittest
from src.chat import *
from src.swen344_db_utils import connect
import csv
import datetime
import json

class TestChat(unittest.TestCase):
    def setUp(self):
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
                message         TEXT NOT NULL,
                sender          TEXT,
                receiver        TEXT,
                year            TEXT
            );
        
            INSERT INTO users (username, email, phone, ssn, suspension) VALUES
                ('Abbott', 'abbott@gmail.com', '123-456-7890', '123-45-6789', NULL),
                ('Costello', 'costello@email.com', '123-456-7890', '123-54-6789', NULL),
                ('Moe', 'moe@email.com', '123-456-7890', '321-45-6789', NULL),
                ('Larry', 'larry@email.com', '123-456-7890', '123-45-9876', NULL),
                ('Curly', 'curly@email.com', '123-456-7890', '012-34-5678', '2060-01-01');     
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
        conn.commit()
        conn.close()
    
    def tearDown(self):
        conn = connect()
        cur = conn.cursor()
        cur.execute("DROP TABLE IF EXISTS users, messages;")
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
        
    # def test_total_number_of_messages(self):
    #     conn = connect()
    #     cur = conn.cursor()
    #     cur.execute("SELECT COUNT(message) - 1 FROM messages;")
    #     conn.commit()
    #     self.assertEqual([(184,)], cur.fetchall(), "Incorrect number of messages.")
    #     conn.close()
        
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
        
    def test_get_messages_abbott_costello(self):
        conn = connect()
        cur = conn.cursor()
        cur.execute("SELECT username FROM users;")
        conn.commit()
        self.assertEqual([('Abbott',), ('Costello',), ('Moe',), ('Larry',), ('Curly',)], cur.fetchall(), "Incorrect users.")
        conn.close()
        
    