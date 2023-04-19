import sqlite3
from sqlite3 import Error

def create_connection(db_file):
   """ create a database connection to the SQLite database
       specified by db_file
   :param db_file: database file
   :return: Connection object or None
   """
   conn = None
   try:
       conn = sqlite3.connect(db_file)
       return conn
   except Error as e:
       print(e)

   return conn

def execute_sql(conn, sql):
   """ Execute sql
   :param conn: Connection object
   :param sql: a SQL script
   :return:
   """
   try:
       c = conn.cursor()
       c.execute(sql)
   except Error as e:
       print(e)


def add_exam(conn, exam):
   """
   Create a new exam into the exams table
   :param conn:
   :param exam:
   :return: exam id
   """
   sql = '''INSERT INTO exams(nazwa, start_date, end_date)
             VALUES(?,?,?)'''
   cur = conn.cursor()
   cur.execute(sql, exam)
   conn.commit()
   return cur.lastrowid

def add_candidate(conn, candidate):
   """
   Create a new candidate into the candidates table
   :param conn:
   :param candidate:
   :return: candidate id
   """
   sql = '''INSERT INTO candidates(exam_id,imię, nazwisko, obywatelstwo, birth_date, email)
             VALUES(?,?,?,?,?,?)'''
   cur = conn.cursor()
   cur.execute(sql,candidate)
   conn.commit()
   return cur.lastrowid

def select_all(conn, table):
   """
   Query all rows in the table
   :param conn: the Connection object
   :return:
   """
   cur = conn.cursor()
   cur.execute(f"SELECT * FROM {table}")
   rows = cur.fetchall()

   return rows


def delete_all(conn, table):
   """
   Delete all rows from table
   :param conn: Connection to the SQLite database
   :param table: table name
   :return:
   """
   sql = f'DELETE FROM {table}'
   cur = conn.cursor()
   cur.execute(sql)
   conn.commit()
   print("Deleted")

if __name__ == "__main__":

   create_exams_sql = """
   -- exams table
   CREATE TABLE IF NOT EXISTS exams (
      id integer PRIMARY KEY,
      nazwa text NOT NULL,
      start_date text,
      end_date text
   );
   """

   create_candidates_sql = """
   -- candidates table
   CREATE TABLE IF NOT EXISTS candidates (
      id integer PRIMARY KEY,
      exam_id integer NOT NULL,
      imię VARCHAR(250) NOT NULL,
      nazwisko VARCHAR(250) NOT NULL,
      obywatelstwo text NOT NULL,
      birth_date text NOT NULL,
      email text NOT NULL,
      FOREIGN KEY (exam_id) REFERENCES exams (id)
   );
   """

   db_file = "database.db"

   conn = create_connection(db_file)
   if conn is not None:
       execute_sql(conn, create_exams_sql)
       execute_sql(conn, create_candidates_sql)
       conn.close()
   

   exam = ("Egzamin  z JPJO", "2023-04-13 00:00:00", "2023-04-14 00:00:00")
   conn = create_connection("database.db")
   exam_id = add_exam(conn, exam)
   candidate = (
       exam_id,
       "Iaroslav",
       "Kanski",
       "Ukraina",
       "1974-03-02",
       "iar.kanski@gmail.com"
    )
   candidate_id = add_candidate(conn,candidate)
   print(exam_id, candidate_id)
   delete_all(conn, "candidates")
   conn.commit()
