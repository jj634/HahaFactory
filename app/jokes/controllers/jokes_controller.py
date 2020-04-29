import json
from . import parsing_lib as pl
from . import cos_sim as cos
from . import cat_jaccard as jac
from . import output_res as ressy
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


with open('./inv_idx_free_2.json') as f:
    inv_idx = json.load(f)

with open('./idf_dict.json') as f:
    idf_dict = json.load(f)

@jokes.route('/search', methods=['GET'])
def search():
    cat_options = [cat.category for cat in Categories.query.all()]

    query = request.args.get('search') or []
    min_score = request.args.get('score') or -1
    categories = request.args.getlist('categories')
    req_size = request.args.get('size') or ""
    typo = False

    print("original query ------")
    print(query)

    min_size = 0
    max_size = 1000000
    if req_size == "Short":
        min_size = 0
        max_size = 50
    elif req_size == "Medium":
        min_size = 50
        max_size = 105
    elif req_size == "Long":
        min_size = 105
        max_size = 1000000
    elif req_size == "One-Liner":
        min_size = -1
        max_size = -1

    #----------- PARSING -----------#
    # maps lowered text to actual category names
    parse_dict = pl.parsing_dict(cat_options)
    p_cats = []
    tok_typos = [] 
    cat_typos = []  
    index_typos = []
    
    if query:
        # next step: incorporate the thesaurus
        query, p_cats, tok_typos, cat_typos, index_typos = pl.parse(query, inv_idx,
                                                       cat_options, parse_dict)

    # Only checks typos currently if nothing in query matches tokens in inverted_index
    if(cat_typos != [] and tok_typos != []):
        typo = True
        for index in range(len(cat_typos)): 
            cat_suggestion = cat_typos[index][1]
            free_suggestion= tok_typos[index][1]

            if cat_suggestion[1] < free_suggestion[1]: 
                term = cat_suggest_tuple[0]
            else: 
                term = free_suggestion[0]
            query.insert(index_typos[index], term)
        if query:
            query_string = " ".join(query)
            query, p_cats , _, _, _ = pl.parse(query_string, inv_idx,
                                                       cat_options, parse_dict)
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

    #--------------------- WEIGHTING & FORMATTING ---------------------#
    results = ressy.weight(results_jac, results_cos, min_score)

    #--------------------- SCORING ------------------------------------#
    # Temporary: If there are no results from running jaccard + cosine, and a minimum score is provided, results normal min score filtered
    if not results and min_score != -1: 
        jokes = Joke.query.filter(Joke.score >= min_score).all()
        nonrelated_jokes = [{
            "text": joke.text,
            "categories": joke.categories,
            "score": str(joke.score),
            "maturity": joke.maturity,
            "size": str(joke.size),
            "similarity": str(0.16/5*float(joke.score))
        } for joke in jokes]
        results += nonrelated_jokes

    #--------------------- LENGTH ------------------------------------#
    # At end, results is filtered based on length.
    if req_size:
        if results: 
            results = ressy.size_filter(results, min_size, max_size)
        else: 
            jokes = Joke.query.all()
            results = [{
                "text": joke.text,
                "categories": joke.categories,
                "score": str(joke.score),
                "maturity": joke.maturity,
                "size": str(joke.size),
                "similarity": str(1.0)
            } for joke in jokes]
            results = ressy.size_filter(results, min_size, max_size)

    #--------------------- SORTING ---------------------#
    # sort results by decreasing sim
    results = sorted(results, key=lambda x: (x["similarity"]), reverse=True)
    cat_options = sorted(cat_options)

    typo_string = " ".join(query)
    if typo:
        print("TYPO EXISTS- New string below: -------------")
        print(typo_string)

    return {"jokes": results, "typo": typo, "typo_query" : typo_string}


@jokes.route('/cat-options', methods=['GET'])
def cat_options():
    return {
        "categories": sorted([cat.category for cat in Categories.query.all()])
    }
