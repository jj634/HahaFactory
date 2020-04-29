import json
import nltk

# please don't run ----- it takes forever because it doesn't use a tfidf matrix rn loool 
# duplicate jokes identified are in sim_jokes.json, they have been deleted

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

# from nltk.tokenize import TreebankWordTokenizer

# tokenizer = TreebankWordTokenizer()

# with open ('./final_sizes_nodups.json') as f:
#     data = json.load(f)
# f.close()

# #indexes/joke_ids of jokes with length < 50; assumption that longer jokes won't have similar jokes
# short_jokes = [idx for idx, joke in enumerate(data) if joke['size'] < 50] 
# sim_jokes = []
# deletejokes_indexes = []

# for i in range(0, len(short_jokes)):
#     joke = data[i]['text']
#     tokens_1 = set(tokenizer.tokenize(joke))

#     for j in range (i+1, len(short_jokes)):
#         joke_2 = data[j]['text']
#         tokens_2 = set(tokenizer.tokenize(joke_2))

#         jd_sent_1_2 = nltk.jaccard_distance(tokens_1, tokens_2)

#         if(jd_sent_1_2 < 0.4): 
#             # note: "If you were a ..., you'd be a ...." jokes need a smaller threshold
#             if ("if you were a " in joke.lower() and jd_sent_1_2 > 0.30):
#                 continue
#             new_score = (data[i]['score'] + data[j]['score']) /2 
#             new_categories = list(set(data[i]['categories'] + data[j]['categories']))

#             data[j]['score'] = new_score
#             data[j]['categories'] = new_categories

#             deletejokes_indexes.append(short_jokes[i])
#             print([(joke, joke_2), jd_sent_1_2, (short_jokes[i], short_jokes[j])])

#             sim_jokes.append([(joke, joke_2), jd_sent_1_2, (short_jokes[i], short_jokes[j])])

# with open ('./simjokes_jaccard.json', "w") as f:
#     json.dump(sim_jokes, f, indent = 4)
# f.close()
 
# print(sim_jokes)
# print(deletejokes_indexes)

deletejokes_indexes = []
with open ('./final_sizes_nodups.json') as f:
    data = json.load(f)
f.close()

with open ('./simjokes_jaccard.json') as f:
    sim_jokes = json.load(f)
f.close()

# short_jokes = [idx for idx, joke in enumerate(data) if joke['size'] < 50] 

indexes = [sim[2] for sim in sim_jokes] 

for tup in indexes:
    print(tup)
    joke = data[tup[0]]
    joke_2 = data[tup[1]]
    print(joke)
    print(joke_2)
    
#     new_score = (joke['score'] + joke_2['score']) /2
#     new_categories = list(set(joke['categories'] + joke_2['categories']))

#     data[short_jokes[tup[1]]]['score'] = new_score
#     data[short_jokes[tup[1]]]['categories'] = new_categories
#     deletejokes_indexes.append(tup[0])

# for ele in sorted(deletejokes_indexes, reverse = True):  
#     del data[ele] 
  
# with open ('./final_nosimjokes.json', "w") as f:
#     json.dump(data, f, indent = 4)