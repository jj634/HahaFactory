import json
import nltk

###### ORIGINAL CODE FOR REMOVING EXACT DUPLICATES -- JACCARD SIMILARITY SHOULD REMOVE THEM #####
# joke_list = {}
# final = []
# with open ('./final_sizes.json') as f:
#     data = json.load(f)
#     for joke in data:
#         text = joke['text'].lower()
#         if text not in joke_list.keys():
#             joke_list[text] = len(final) 
#             final.append(joke)
#         else: 
#             duplicate_index = joke_list[text]
#             duplicate_score = final[duplicate_index]['score']
#             duplicate_categories = final[duplicate_index]['categories']

#             curr_score = joke['score']
#             curr_categories = joke['categories']

#             new_categories = list(set(duplicate_categories + curr_categories))
#             new_score = (duplicate_score + curr_score) / 2

#             final[duplicate_index]['categories'] = new_categories
#             final[duplicate_index]['score'] = new_score
#     f.close()

# with open ('./final_sizes_nodups.json', "w") as f:
#     json.dump(final, f, indent = 4)








# LOOOL pls don't look at this code; its atrocious, slow and awful. do not run. it does not use tfidfvectorizer. 
# if you want to try to remove similar jokes, i would recommend rewriting using sklearn lol (: sorry 

from nltk.tokenize import TreebankWordTokenizer

tokenizer = TreebankWordTokenizer()

with open ('./final_sizes_nodups.json') as f:
    data = json.load(f)
f.close()

# Only checks for duplicates among jokes with length < 50; assumption is that that the longer the joke, the less similar it will be with other jokes 
short_jokes = [idx for idx, joke in enumerate(data) if joke['size'] < 225] 
sim_jokes = []
deletejokes_indexes = []

for i in range(0, len(short_jokes)):
    index_1 = short_jokes[i]
    joke = data[index_1]['text']
    tokens_1 = set(tokenizer.tokenize(joke))
    # print(joke)

    for j in range (i+1, len(short_jokes)):
        index_2 = short_jokes[j]
        joke_2 = data[index_2]['text']
        tokens_2 = set(tokenizer.tokenize(joke_2))
        # print(joke_2)

        jd_sent_1_2 = nltk.jaccard_distance(tokens_1, tokens_2)

        ############# Jaccard distance threshold ##############
        if(jd_sent_1_2 < 0.4): 
            
            # note: "If you were a ..., you'd be a ...." jokes need a smaller threshold

            # some other possible cases to catch: [seems to be fine, since it usually has a reply that differs. could manually change too]
                # What did the .... say to the ...? 
                # How many .... does it take to change a light bulb?
                # Did you hear about the .....?
                # What do you get when you cros a ....?
            if ("if you were a " in joke.lower() and jd_sent_1_2 > 0.30):
                continue
            
            new_score = (data[index_1]['score'] + data[index_2]['score']) /2 
            new_categories = list(set(data[index_1]['categories'] + data[index_2]['categories']))

            data[index_2]['score'] = new_score
            data[index_2]['categories'] = new_categories

            deletejokes_indexes.append(index_1)
            print([(data[index_1]['text'], data[index_2]['text']), jd_sent_1_2, (index_1, index_2)])

            sim_jokes.append([(joke, joke_2), jd_sent_1_2, (index_1, index_2)])

with open ('./simjokes_jaccard.json', "w") as f:
    json.dump(sim_jokes, f, indent = 4)
f.close()
 
# deletejokes_indexes = []
# with open ('./final_sizes_nodups.json') as f:
#     data = json.load(f)
# f.close()

# with open ('./simjokes_jaccard.json') as f:
#     sim_jokes = json.load(f)
# f.close()

# indexes = [sim[2] for sim in sim_jokes] 

# for tup in indexes:
#     print(tup)
#     joke = data[tup[0]]
#     joke_2 = data[tup[1]]
#     print(joke)
#     print(joke_2)
    
#     new_score = (joke['score'] + joke_2['score']) /2
#     new_categories = list(set(joke['categories'] + joke_2['categories']))

#     data[tup[1]]['score'] = new_score
#     data[tup[1]]['categories'] = new_categories
#     deletejokes_indexes.append(tup[0])

for ele in sorted(deletejokes_indexes, reverse = True):  
    del data[ele] 
  
with open ('./final_nosimjokes.json', "w") as f:
    json.dump(data, f, indent = 4)
