import requests, time, mysql.connector
from database import DB_CONFIG

# call scan a few times
for i in range(3):
    r=requests.get('http://127.0.0.1:8000/scan')
    print('scan',i,r.json())
    time.sleep(1)

# check DB entries
conn=mysql.connector.connect(**DB_CONFIG)
cursor=conn.cursor()
cursor.execute('SELECT COUNT(*) FROM memory_samples')
print('count samples',cursor.fetchone())
cursor.execute('SELECT MAX(id) FROM memory_samples')
print('max id',cursor.fetchone())
cursor.execute('SELECT COUNT(*) FROM process_snapshots')
print('count procs',cursor.fetchone())
conn.close()
