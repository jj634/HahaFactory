import json

joke_list = {}
final = []
with open ('./final_sizes.json') as f:
    data = json.load(f)
    for joke in data:
        text = joke['text'].lower()
        if text not in joke_list.keys():
            joke_list[text] = len(final) 
            final.append(joke)
        else: 
            duplicate_index = joke_list[text]
            duplicate_score = final[duplicate_index]['score']
            duplicate_categories = final[duplicate_index]['categories']

            curr_score = joke['score']
            curr_categories = joke['categories']

            new_categories = list(set(duplicate_categories + curr_categories))
            new_score = (duplicate_score + curr_score) / 2

            final[duplicate_index]['categories'] = new_categories
            final[duplicate_index]['score'] = new_score
    f.close()

with open ('./final_sizes_nodups.json', "w") as f:
    json.dump(final, f, indent = 4)