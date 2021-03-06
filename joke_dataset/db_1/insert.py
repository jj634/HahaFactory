import psycopg2
import json

# INSERTS: 
# 1. FINAL_NORM.JSON
# 2. INV_IDX_FREE.JSON
# 3. INV_IDX_CAT.JSON

try:
   connection = psycopg2.connect( 
                                  user = "winice",
                                  password = "password",
                                  host="localhost",
                                  port="5432",
                                  database="hahadata")
   cursor = connection.cursor()
   with open ('./final_norm.json') as f: 
       data = json.load(f)
       string = "\'" + json.dumps(data) + "\'"
       postgres_insert_query = "Insert into jokes (text, score, categories, norm) select text, score, categories, norm from json_populate_recordset(null::jokes, " + string + ");"
   cursor.execute(postgres_insert_query)

   connection.commit()
   count = cursor.rowcount
   print (count, "Records inserted successfully into Jokes table")
   
   with open ('./inv_idx_cat.json') as f: 
       data = json.load(f)
       string = "\'" + json.dumps(data) + "\'"
       postgres_insert_query = "Insert into categories (category, joke_ids) select category, joke_ids from json_populate_recordset(null::categories, " + string + ");"
   cursor.execute(postgres_insert_query)

   connection.commit()
   count = cursor.rowcount
   print (count, "Records inserted successfully into Categories table")

except (Exception, psycopg2.Error) as error :
    if(connection):
        print("Failed to insert record into mobile table", error)

finally:
    #closing database connection.
    if(connection):
        cursor.close()
        connection.close()
        print("PostgreSQL connection is closed")