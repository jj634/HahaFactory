import psycopg2
import json

# INSERTS: 
# 1. final_sizes.json
# 2. inv_idx_cat.json

# final_sizes recipe
# 1. data scraping using ./getData/*.py
# 2. ml using ./ml_score/assign_scores.py
# 3. preprocessing - standardize, normalize, remove dups using ./preprocessing.py (makes final_score.json)
# 4. tokenize using ./tokenizer.py (makes final_toks.json)
# 5. precomputation - norms, sizes using ./precomputation.py (makes final_sizes.json)

# NOTE: you have to go to the final_sizes and replace all ' with '' (that is two apostrophes)
# this is because postgres is annoying

try:
   connection = psycopg2.connect( 
                                #   user = "winice",
                                #   password = "password",
                                  host="localhost",
                                  port="5432",
                                  database="hahadata")
   cursor = connection.cursor()
   with open ('./final_sizes.json') as f: 
       data = json.load(f)
       string = "\'" + json.dumps(data) + "\'"
       postgres_insert_query = "Insert into jokes (text, score, categories, norm, size, maturity) select text, score, categories, norm, size, maturity from json_populate_recordset(null::jokes, " + string + ");"
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
