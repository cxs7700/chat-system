import unittest
from src.chat import *
from src.swen344_db_utils import connect
import csv

class TestChat(unittest.TestCase):

    def test_build_users_table(self):
        conn = connect()
        cur = conn.cursor()
        rebuildTables()
        
        sql_str = """
            INSERT INTO users (username, email, phone, ssn, suspension) VALUES
                ('Abbott', 'abbott@gmail.com', '123-456-7890', '123-45-6789', NULL),
                ('Costello', 'costello@email.com', '123-456-7890', '123-54-6789', NULL),
                ('Moe', 'moe@email.com', '123-456-7890', '321-45-6789', NULL),
                ('Larry', 'larry@email.com', '123-456-7890', '123-45-9876', NULL),
                ('Curly', 'curly@email.com', '123-456-7890', '012-34-5678', NULL);
            """
        cur.execute(sql_str)
        sql_str = "SELECT * FROM users"
        cur.execute(sql_str)
        conn.commit()
        self.assertEqual([], cur.fetchall(), "No rows in users table")
        conn.close()
        
    def test_build_messages_table(self):
        conn = connect()
        cur = conn.cursor()
        rebuildTables()
        
        with open('test_data.csv', 'r') as f:
            reader = csv.DictReader(f, delimiter=",", quotechar='"')
            # next(reader)
            for row in reader:
                # cur.execute(
                #     "INSERT INTO messages (sender, receiver, message, year) VALUES (%s, %s, %s, %s);",
                #     row
                # )
                
                sql = "INSERT INTO messages(sender, receiver, message, year) VALUES (%(Sender)s, %(Receiver)s, %( Message)s, %(Year)s);"
                # print(row)
                cur.execute(sql, row)
        conn.commit()
        cur.execute("SELECT * FROM messages")
        self.assertEqual([], cur.fetchall(), "No rows in messages table")
        conn.close()
      
    def test_rebuild_tables_is_idempotent(self):
        rebuildTables()
        rebuildTables()
        conn = connect()
        cur = conn.cursor()
        sql1 = "SELECT * FROM users"

        # self.assertEqual([], cur.fetchall(), "no rows in example_table")
        conn.close()
        
    # def test_abbott_costello(self):
        
    # def test_number_of_users(self):
        
    # def test_number_of_messages(self):
        
    # def test_find_messages(self):
        
    # def test_suspended_account(self):
        