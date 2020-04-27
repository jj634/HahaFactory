import json
from . import parsing_lib as pl
from . import cos_sim as cos
from . import cat_jaccard as jac
from . import output_res as ressy
from . import *
"""
{
  "text": "hi",
  "categories": [1,2,3],
  "score": 2,
  "maturity": 2
} 
"""


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
    inv_idx_free = json.load(f)

inv_idx = cos.inv_idx_trad(inv_idx_free)


@jokes.route('/search', methods=['GET'])
def search():
    cat_options = [cat.category for cat in Categories.query.all()]

    # query = request.args.get('search', default= '')
    query = request.args.get('search')
    min_score = request.args.get('score') or -1
    categories = request.args.getlist('categories')
    req_size = request.args.get('size') or ""
    print("original query ------")
    print(query)
    size = 1000000
    if req_size == "s":
        size = 10
    elif req_size == "m":
        size = 100
    elif req_size == "l":
        size = 1000
    elif req_size == "1":
        size = 0  # figure out later

    #----------- PARSING -----------#
    # maps lowered text to actual category names
    parse_dict = pl.parsing_dict(cat_options)
    p_cats = []
    tok_typos = None  # currently unused
    cat_typos = None  # currently unused
    if query:
        # next step: incorporate the thesaurus
        query, p_cats, tok_typos, cat_typos = pl.parse(query, inv_idx,
                                                       cat_options, parse_dict)
    else:
        query = []
    categories_list = categories + p_cats
    categories_list = categories
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
        results_cos = cos.fast_cossim(query, inv_idx, inv_idx_free)

    #--------------------- WEIGHTING & FORMATTING ---------------------#
    print("size is:")
    print(size)
    results = ressy.weight(results_jac, results_cos, min_score, size)

    #--------------------- SORTING ---------------------#
    # sort results by decreasing sim
    results = sorted(results, key=lambda x: (x["similarity"]), reverse=True)
    cat_options = sorted(cat_options)

    return {"jokes": results}


@jokes.route('/cat-options', methods=['GET'])
def cat_options():
    return {
        "categories": sorted([cat.category for cat in Categories.query.all()])
    }
