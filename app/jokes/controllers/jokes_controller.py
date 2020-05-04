import json
from . import parsing_lib as pl
from . import cos_sim as cos
from . import cat_jaccard as jac
from . import output_res as ressy
from . import sizing as siz
from . import lucky as lk
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

@jokes.route('/search', methods=['GET'])
def search():
    cat_options = sorted([cat.category for cat in Categories.query.all()])

    query = request.args.get('search') or []
    # input values are from [0, 0.5]. default to maximum relevance
    weighting = request.args.get('score') or 0 
    categories = request.args.getlist('categories')
    sizes = request.args.getlist('sizes')
    maturity = request.args.get('maturity') or ''
    typo = False

    print("original query ------")
    print(query)

    #----------- PARSING -----------#
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
                term = cat_suggest_tuple[0]
            elif cat_suggestion[1] < free_suggestion[1]: 
                term = cat_suggest_tuple[0]
            else: 
                term = free_suggestion[0]
            query.insert(index_typos[index], term)
    if query:
        query_string = " ".join(query)
        p_cats = pl.parse(query_string, cat_options, parse_dict)

    categories_list = categories + p_cats
    categories_list = list(set(categories_list))

    #--------------------- JACCARD ---------------------#
    # dictionary key = joke_id, value = (joke_dict, jac_sim)
    results_jac = {}
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

        # to discuss - this seems inefficient. do you have to filter one by one? theres prob a psql command
        rel_jokes_meta = {}  # dictionary where key = joke_id, value = joke
        for joke_id in numer_dict.keys():
            rel_jokes_meta[joke_id] = Joke.query.filter_by(id=joke_id).first()

        results_jac = jac.jaccard_sim(
            categories_list, numer_dict, rel_jokes_meta)

    #--------------------- COSINE ---------------------#
    # dictionary where key= joke_id, value = (joke_dict, cos_sim)
    results_cos = {}
    print("QUERY IS: ---------")
    print(query)
    if query:
        results_cos = cos.fast_cossim(query, inv_idx, idf_dict)
        print(results_cos)

    #--------------------- WEIGHTING & FORMATTING ---------------------#
    advanced = True if (categories or weighting or sizes or maturity) else False
    results, cos_score, jac_score, sc_score = ressy.weight(results_jac, results_cos, weighting, advanced)
    print("WEIGHTING IS: ---------")
    str_weighting = "Cosine: {}, Jaccard: {}, Score: {}".format(cos_score, jac_score, sc_score)
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
            print("MATURITY IS: ")
            print(jokes[0].maturity)
            results = [{
                "text": joke.text,
                "categories": joke.categories,
                "score": str(joke.score),
                "maturity": str(joke.maturity),
                "size": str(joke.size), 
                "similarity": str(joke.score/5)
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
                    'similarity': str(j.score/5)
                } for j in jokes if j.maturity == 1
            ]

    #--------------------- SORTING ---------------------#
    # sort results by decreasing sim
    results = sorted(results, key=lambda x: (x["similarity"]), reverse=True)

    typo_string = " ".join(query)
    if typo:
        print("TYPO EXISTS- New string below: -------------")
        print(typo_string)

    return {"jokes": results, "typo": typo, "typo_query" : typo_string, "cosine": cos_score, "jaccard": jac_score, "score": sc_score, "query" : query}


@jokes.route('/cat-options', methods=['GET'])
def cat_options():
    return {
        "categories": sorted([cat.category for cat in Categories.query.all()])
    }
