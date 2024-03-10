import os
import psycopg2

# Connect to your postgres DB
conn = psycopg2.connect(host=os.environ['HOST'], database=os.environ['DATABASE'],
                        user=os.environ['USER'], password=os.environ['PASSWORD'])

# Open a cursor to perform database operations
cur = conn.cursor()

# Execute a query
cur.execute("SELECT * FROM scifile")

# Recorremos los resultados y los mostramos
for i in cur.fetchall():
    print(f'{i}')

conn.close()
