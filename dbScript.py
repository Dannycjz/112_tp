import sqlite3
import pandas as pd

db = sqlite3.connect('chess') 
cursor = db.cursor()

# cursor.execute('''
#           CREATE TABLE IF NOT EXISTS users
#           ([user_id] INTEGER PRIMARY KEY, [user_name] TEXT, 
#           [password] TEXT)
#           ''')
    
# # cursor.execute('''
# #         INSERT INTO users (user_id, user_name, password)
# #         VALUES
# #         (1, 'Danny', '123'),
# #         (2, 'Daniel', '456')
# #         ''')

cursor.execute('''
                SELECT * FROM users
                ''')

df=pd.DataFrame(cursor.fetchall(), columns=['user_id', 'user_name', 'password'])

# db.commit()
print(df)