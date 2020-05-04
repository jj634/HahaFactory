import json 

pg13_maturity = [
    'sex',
    'crap',
    'fuck',
    'shit',
    'kill',
    'die',
    'murder',
    'penis',
    'vagina',
    'drugs',
    'pussy',
    'marijuana',
    'cocaine',
    'heroine',
    'meth',
    'death',
    'keg',
    'killed',
    'masturbate',
    'hitler',
    'nazi',
    'swastika',
    'sex-change',
    'alcohol',
    'bar',
    'rum',
    'pub',
    'wine',
    'whiskey',
    'gin',
    'viagra',
    'condom',
    'gun',
    'pistol',
    'bullet',
    'whore',
    'porn',
    'budlight',
    'coors',
    'skank',
    'bitch',
    'budweiser',
    'sexy',
    'murderer',
    'ass',
    'lingerie',
    'knife',
    'hell',
    'horny',
    'handjobs',
    'handjob',
    
]

pg13_cats = [
    'Bar Jokes',
    'Sex'
]

with open('../inv_idx_cat.json') as f:
    inv_cat = json.load(f)

with open ('../inv_idx_free.json') as f: 
    inv_idx = json.load(f)

with open ('../final_sizes.json') as f: 
    data = json.load(f)

bad_jokes = []
for word in pg13_maturity: 
    if word in inv_idx: 
        jokes = [j[0] for j in inv_idx[word]]
        bad_jokes += jokes
for i in range(len(inv_cat)):
    if (inv_cat[i]['category']) in pg13_cats:
        bad_jokes += inv_cat[i]['joke_ids']

bad_jokes = list(set(bad_jokes))

for index in bad_jokes: 
    data[index-1]['maturity'] = 1

with open('../final_sizes.json', 'w') as f:
    json.dump(data, f, indent=4)

