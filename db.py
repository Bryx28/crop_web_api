import psycopg2
import psycopg2.extras
#import datetime
#import arrow

#date = arrow.utcnow()

conn = psycopg2.connect(
    host='ec2-3-211-228-251.compute-1.amazonaws.com',
    database='dfqt1p61srvec0',
    user='kwqxcelviwbiyf',
    password='570b87e2f2fa138774cb2df0572e7359316ea44c17be8d7dcfe56192724c8f45',
    port=5432
)
cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

#cursor.execute("SELECT * FROM recommendations")
#for db in cursor.fetchall():
#    print(db)
#sql_query = """ CREATE TABLE IF NOT EXISTS book (
#        id integer PRIMARY KEY AUTO_INCREMENT,
#        author text NOT NULL,
#        language text NOT NULL,
#        title text  NOT NULL
#    )"""

#cursor.execute("""SELECT * 
#                    FROM pg_catalog.pg_tables 
#                    WHERE schemaname != 'pg_catalog' 
#                    AND schemaname != 'information_schema';""")
#for tables in cursor.fetchall():
#    print(tables)

#cursor.execute("""SELECT column_name 
#                    FROM INFORMATION_SCHEMA.COLUMNS WHERE 
#                    table_name = 'user';""")
#for tables in cursor.fetchall():
#    print(tables)

#cursor.execute("""SELECT * FROM public.\"user\"""")
#value = cursor.fetchall()
#for row in value:
#    print(row)

#cursor.execute("SELECT * FROM public.\"recommendations\" ORDER BY id DESC")
#value = cursor.fetchall()
#for row in value:
#    print(row)

cursor.execute("DELETE FROM public.\"recommendations\"")
conn.commit()

#cursor.execute("SELECT * FROM public.\"post\" ORDER BY date_posted DESC")
#value = cursor.fetchall()
#for row in value:
#    print(row)

"""
cursor.execute("SELECT id FROM book ORDER BY id DESC;")
new_id = cursor.fetchone()['id']
print(new_id)
conn.close()"""