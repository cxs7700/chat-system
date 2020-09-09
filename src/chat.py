from src.swen344_db_utils import connect

def buildTables():
  conn = connect()
  cur = conn.cursor()
  sql = """
      CREATE TABLE example_table(
          example_col VARCHAR(40)
      )
  """
  cur.execute(sql)
  conn.commit() # don't forget this!
  conn.close()
  
def rebuildTables():
    conn = connect()
    cur = conn.cursor()
    drop_sql = """
        DROP TABLE IF EXISTS example_table
    """
    create_sql = """
        CREATE TABLE example_table(
            example_col VARCHAR(40)
        )
    """
    cur.execute(drop_sql)
    cur.execute(create_sql)
    conn.commit()
    conn.close()