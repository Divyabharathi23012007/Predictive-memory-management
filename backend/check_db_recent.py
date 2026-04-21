import mysql.connector
from database import DB_CONFIG

conn = mysql.connector.connect(**DB_CONFIG)
cur = conn.cursor()
cur.execute('SELECT NOW(), DATABASE(), @@hostname')
print('server info',cur.fetchone())

cur.execute('SELECT id, timestamp, current_used_mb FROM memory_samples ORDER BY timestamp DESC LIMIT 5')
print('latest samples:')
for row in cur.fetchall():
    print(row)

conn.commit()
cur.close()
conn.close()
