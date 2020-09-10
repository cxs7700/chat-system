import unittest
from src.chat import *
from src.swen344_db_utils import connect
import csv
import datetime

class TestChat(unittest.TestCase):

    def test_build_tables(self):
        """Build the tables"""
        conn = connect()
        cur = conn.cursor()
        rebuildTables()
        cur.execute("SELECT * FROM users")
        conn.commit()
        self.assertEqual([], cur.fetchall(), "No rows in users table.")
        conn.close()
        
    def test_build_messages_table(self):
        conn = connect()
        cur = conn.cursor()
        rebuildTables()
        cur.execute("SELECT * FROM messages")
        conn.commit()
        self.assertEqual([], cur.fetchall(), "No rows in messages table.")
        conn.close()
      
    def test_rebuild_tables_is_idempotent(self):
        rebuildTables()
        rebuildTables()
        conn = connect()
        cur = conn.cursor()
        sql = """
            SELECT * FROM users, messages;
        """
        cur.execute(sql)
        conn.commit()
        self.assertEqual([], cur.fetchall(), "No rows in any table.")
        conn.close()
        
    def test_abbott_is_a_user(self):
        conn = connect()
        cur = conn.cursor()
        rebuildTables()
        sql = """
            INSERT INTO users (username, email, phone, ssn, suspension) VALUES
                ('Abbott', 'abbott@gmail.com', '123-456-7890', '123-45-6789', NULL),
                ('Costello', 'costello@email.com', '123-456-7890', '123-54-6789', NULL),
                ('Moe', 'moe@email.com', '123-456-7890', '321-45-6789', NULL),
                ('Larry', 'larry@email.com', '123-456-7890', '123-45-9876', NULL),
                ('Curly', 'curly@email.com', '123-456-7890', '012-34-5678', NULL);
                
            SELECT username FROM users WHERE username = 'Abbott';
        """
        cur.execute(sql)
        conn.commit()
        self.assertEqual([('Abbott',)], cur.fetchall(), "Abbott is not a user in this database.")
        
    def test_costello_is_a_user(self):
        conn = connect()
        cur = conn.cursor()
        rebuildTables()
        sql = """
            INSERT INTO users (username, email, phone, ssn, suspension) VALUES
                ('Abbott', 'abbott@gmail.com', '123-456-7890', '123-45-6789', NULL),
                ('Costello', 'costello@email.com', '123-456-7890', '123-54-6789', NULL),
                ('Moe', 'moe@email.com', '123-456-7890', '321-45-6789', NULL),
                ('Larry', 'larry@email.com', '123-456-7890', '123-45-9876', NULL),
                ('Curly', 'curly@email.com', '123-456-7890', '012-34-5678', NULL);
                
            SELECT username FROM users WHERE username = 'Costello';
        """
        cur.execute(sql)
        conn.commit()
        self.assertEqual([('Costello',)], cur.fetchall(), "Costello is not a user in this database.")
        
    def test_total_number_of_users(self):
        conn = connect()
        cur = conn.cursor()
        rebuildTables()
        sql = """
            INSERT INTO users (username, email, phone, ssn, suspension) VALUES
                ('Abbott', 'abbott@gmail.com', '123-456-7890', '123-45-6789', NULL),
                ('Costello', 'costello@email.com', '123-456-7890', '123-54-6789', NULL),
                ('Moe', 'moe@email.com', '123-456-7890', '321-45-6789', NULL),
                ('Larry', 'larry@email.com', '123-456-7890', '123-45-9876', NULL),
                ('Curly', 'curly@email.com', '123-456-7890', '012-34-5678', NULL);
                
            SELECT COUNT(users) FROM users;
        """
        cur.execute(sql)
        conn.commit()
        self.assertEqual([(5,)], cur.fetchall(), "Incorrect number of users.")
        conn.close()
        
    def test_total_number_of_messages(self):
        conn = connect()
        cur = conn.cursor()
        rebuildTables()
        
        with open('test_data.csv', newline='') as f:
            data = csv.reader(f, delimiter=',', quotechar='|')
            for row in data:
                cur.execute(
                    "INSERT INTO messages (sender, receiver, message, year) VALUES (%s, %s, %s, %s);",
                    (row[0], row[1], row[2], row[3])
                )
            f.close()
            
        cur.execute("SELECT COUNT(message) - 1 FROM messages;")
        conn.commit()
        self.assertEqual([(184,)], cur.fetchall(), "Incorrect number of messages.")
        conn.close()
        
    def test_find_messages(self):
        conn = connect()
        cur = conn.cursor()
        rebuildTables()
        with open('test_data.csv', newline='') as f:
            data = csv.reader(f, delimiter=',', quotechar='"')
            for row in data:
                cur.execute(
                    "INSERT INTO messages (sender, receiver, message, year) VALUES (%s, %s, %s, %s);",
                    (row[0], row[1], row[2], row[3])
                )
            f.close()
            
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
        rebuildTables()
        sql = """
            INSERT INTO users (username, email, phone, ssn, suspension) VALUES
                ('Abbott', 'abbott@gmail.com', '123-456-7890', '123-45-6789', NULL),
                ('Costello', 'costello@email.com', '123-456-7890', '123-54-6789', NULL),
                ('Moe', 'moe@email.com', '123-456-7890', '321-45-6789', NULL),
                ('Larry', 'larry@email.com', '123-456-7890', '123-45-9876', NULL),
                ('Curly', 'curly@email.com', '123-456-7890', '012-34-5678', '2060-01-01');
                
            
            SELECT suspension FROM users WHERE suspension = '2060-01-01';
        """
        cur.execute(sql)
        conn.commit()
        self.assertEqual([(datetime.datetime(2060, 1, 1),)], cur.fetchall(), "Curly is not suspended until January 1, 2060.")
        conn.close()
        