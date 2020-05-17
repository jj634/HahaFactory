import json
from . import parsing_lib as pl
from . import cos_sim as cos
from . import cat_jaccard as jac
from . import output_res as ressy
from . import sizing as siz
from . import lucky as lk
from . import cache as che
import random
from . import *

@jokes.route('/jokes', methods=['GET', 'POST'])
def handle_jokes():
    if request.method == 'POST':
        if request.is_json:
            data = request.get_json()
            new_joke = Joke(text=data['text'],
                            categories=data['categories'],
                            score=data['score'],
                            maturity=data['maturity'])
            db.session.add(new_joke)
            db.session.commit()
            return {
                "message": "joke {new_joke.id} has been created successfully."
            }
        else:
            return {"error": "The request payload is not in JSON format"}

    elif request.method == 'GET':
        jokes = Joke.query.all()
        results = [{
            "text": joke.text,
            "categories": joke.categories,
            "score": str(joke.score),
            "maturity": joke.maturity,
        } for joke in jokes]

        return {"count": len(results), "jokes": results}


with open('./inv_idx_free.json') as f:
    inv_idx = json.load(f)

with open('./idf_dict.json') as f:
    idf_dict = json.load(f)

with open('./cache.json') as f:
    cache = json.load(f)

real_cache = {0: cache}

@jokes.route('/search', methods=['GET'])
def search():
    cat_options = sorted([cat.category for cat in Categories.query.all()])

    query = request.args.get('search') or []
    # input values are from [0, 0.5]. default to maximum relevance
    weighting = request.args.get('score') or 0 
    categories = request.args.getlist('categories')
    sizes = request.args.getlist('sizes')
    maturity = request.args.get('maturity')
    typo = False

    print("original query ------")
    print(query)

    cache_key = str(query)+str(categories)+str(weighting)+str(sizes)+str(maturity)

    if cache_key in real_cache[0]:
        return real_cache[0][cache_key]

    #----------- FIND TYPOS -----------#
    print("Finding Typo.....")
    # maps lowered text to actual category names
    parse_dict = pl.parsing_dict(cat_options)
    p_cats = []
    tok_typos = [] 
    cat_typos = []  
    index_typos = []
    
    if query:
        # next step: incorporate the thesaurus
        query, tok_typos, cat_typos, index_typos = pl.getTypos(query, inv_idx,
                                                       cat_options) 

    if(cat_typos != [] and tok_typos != []):
        typo = True
        for index in range(len(cat_typos)): 
            cat_suggestion = cat_typos[index][1]
            free_suggestion= tok_typos[index][1]

            if (cat_suggestion is None and free_suggestion is None):
                continue
            elif cat_suggestion is None: 
                term = free_suggestion[0]
            elif free_suggestion is None: 
                term = cat_suggestion[0]
            elif cat_suggestion[1] < free_suggestion[1]: 
                term = cat_suggestion[0]
            else: 
                term = free_suggestion[0]
            query.insert(index_typos[index], term)

     #----------- PARSING -----------#
    print("Parsing.....")
    if query:
        query_string = " ".join(query)
        p_cats = pl.parse(query_string, cat_options, parse_dict)

    categories_list = categories + p_cats
    categories_list = list(set(categories_list))


    #--------------------- JACCARD ---------------------#
    # dictionary key = joke_id, value = (joke_dict, jac_sim)
    results_jac = {}

    # NEW: accumulate all meta data so we don't do unnecessary database calls
    rel_jokes_meta = {} # dictionary where key = joke_id, value = joke

    print("CATEGORIES ARE: --------")
    print(categories_list)
    if categories_list:
        cat_jokes = {}  # dictionary where key = category, value = array of doc_ids with that category
        for cat in categories_list:  # for every category
            # get the record where category is equal to cat
            doc_lst = Categories.query.filter_by(category=cat).first()
            cat_jokes[cat] = doc_lst.joke_ids

        # dictionary with key = joke_id and value = numerator
        numer_dict = jac.get_rel_jokes(cat_jokes)

        rel_jokes = Joke.query.filter(Joke.id.in_(numer_dict.keys())).all()
        for joke_id in numer_dict.keys():
            rel_jokes_meta[joke_id] = Joke.query.filter_by(id=joke_id).first()

        results_jac = jac.jaccard_sim(
            categories_list, numer_dict, rel_jokes)

    #--------------------- COSINE ---------------------#
    # dictionary where key= joke_id, value = (joke_dict, cos_sim)
    results_cos = {}
    print("QUERY IS: ---------")
    print(query)
    if query:
        # NEW: add rel_jokes_meta as argument to fast_cossim
        results_cos, rel_jokes_meta = cos.fast_cossim(query, inv_idx, idf_dict, rel_jokes_meta)

    #--------------------- WEIGHTING & FORMATTING ---------------------#
    advanced = True if (categories or weighting or sizes or maturity) else False
    # NEW: add rel_jokes_meta as an argument to weight
    results, cos_weight, jac_weight, sc_weight = ressy.weight(results_jac, results_cos, weighting, advanced, rel_jokes_meta)
    print("WEIGHTING IS: ---------")
    str_weighting = "Cosine: {}, Jaccard: {}, Score: {}".format(cos_weight, jac_weight, sc_weight)
    print(str_weighting)

    #--------------------- LENGTH ------------------------------------#
    # At end, results is filtered based on length.
    print("Length IS: ---------")
    print(sizes)
    if sizes:
        if results: 
            results = siz.size_filter(results, sizes)
        else: 
            jokes = Joke.query.all()
            results = [{
                "text": joke.text,
                "categories": joke.categories,
                "score": str(joke.score),
                "maturity": str(joke.maturity),
                "size": str(joke.size), 
                "similarity": str(1),
                "rand": str(random.random())
            } for joke in jokes]
            results = siz.size_filter(results, sizes)

    #--------------------- MATURITY  ---------------------#
     # At end, results is filtered based on maturity. Retouch later.
    print("Maturity IS: ---------")
    print(maturity)
    if maturity:
        if results:
            if maturity == 'PG-13': 
                results = [joke for joke in results if joke['maturity'] == '1' ]
            if maturity == 'PG':
                results = [joke for joke in results if joke['maturity'] == "None"] 
        else:
            jokes = Joke.query.all()
            results = [
                {
                    'text': j.text,
                    'categories': j.categories,
                    'score': str(j.score),
                    'maturity': str(j.maturity),
                    'size': str(j.size),
                    'similarity': str(1),
                    'rand': str(random.random())
                } for j in jokes if j.maturity == 1
            ]

    #--------------------- SORTING ---------------------#
    # sort results by decreasing sim
    if (query or categories_list):
        results = sorted(results, key=lambda x: (x["similarity"]), reverse=True)
    else:
        results = ressy.special_weighting(results, float(weighting))
        results = sorted(results, key=lambda x: (x['rand']), reverse=True)

    #--------------------- CREATE NEW TYPO STRING FOR FRONTEND DISPLAY ---------------------#
    typo_string = " ".join(query)
    if typo:
        print("TYPO EXISTS- New string below: -------------")
        print(typo_string)

    real_cache[0][cache_key] = {"jokes": results, "typo": typo, "typo_query" : typo_string, "cosine": cos_weight, "jaccard": jac_weight, "score": sc_weight, "query" : query}

    if len(cache) > 100:
        tmp_cache = {}
        new_keys = list(real_cache[0].items())[50:]
        for i, j in new_keys:
            tmp_cache[i] = j
        real_cache[0] = tmp_cache

    with open('./cache.json', 'w') as f:
        json.dump(real_cache[0], f)

    return real_cache[0][cache_key]


@jokes.route('/cat-options', methods=['GET'])
def cat_options():
    return {
        "categories": sorted([cat.category for cat in Categories.query.all()])
    }
