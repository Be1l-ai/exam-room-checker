import sqlite3

def connect_db(db_path):
    try:
        connection = sqlite3.connect(db_path)
        return connection
    except sqlite3.Error as e:
        print(f"Error connecting to database: {e}")
        return None
    
def init_db(db_path, db_schema): # initialize the database with schema
    connection = connect_db(db_path)
    if connection is not None:
        try: 
            with open(db_schema, 'r') as f:
                schema_sql = f.read()
            cursor = connection.cursor()
            cursor.executescript(schema_sql)
            connection.commit()
            print("Database initialized successfully.")
        except sqlite3.Error as e:
            print(f"Error initializing database: {e}")
        finally:
            connection.close()
