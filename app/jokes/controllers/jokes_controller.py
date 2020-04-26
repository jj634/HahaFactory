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
    min_score = request.args.get('score')
    categories = request.args.getlist('categories')
    req_size = request.args.getlist('size') or ""

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
    categories_list = list(set(categories_list))


    #--------------------- JACCARD ---------------------#
    # dictionary key = joke_id, value = (joke_dict, jac_sim)
    results_jac = {}
    if categories_list:
        cat_jokes = {}  # dictionary where key = category, value = array of doc_ids with that category
        for cat in categories_list:  # for every category
            # get the record where category is equal to cat
            doc_lst = Categories.query.filter_by(category=cat).first()
            cat_jokes[cat] = doc_lst.joke_ids

        # dictionary with key = joke_id and value = numerator
        numer_dict = jac.get_rel_jokes(cat_jokes)

        rel_jokes = {}  # dictionary where key = joke_id, value = joke
        for joke_id in numer_dict.keys():
            rel_jokes[joke_id] = Joke.query.filter_by(id=joke_id).first()

        for joke_id, joke_sim in jac.jaccard_sim(categories_list, numer_dict,rel_jokes):
            joke_meta = rel_jokes[joke_id]
            if joke_id not in results_jac:
                results_jac[joke_id] = ({
                    "text": joke_meta.text,
                    "categories": joke_meta.categories,
                    "score": str(joke_meta.score),
                    "maturity": joke_meta.maturity
                }, joke_sim)

    
    #--------------------- COSINE ---------------------#
    # dictionary where key= joke_id, value = (joke_dict, cos_sim)
    results_cos = {}
    if query:
        # a list of (joke_id, cos_sim)
        for joke_id, joke_sim in cos.fast_cossim(query, inv_idx, inv_idx_free):
            joke_meta = Joke.query.filter_by(id=joke_id).first()
            results_cos[joke_id] = ({
                "text": joke_meta.text,
                "categories": joke_meta.categories,
                "score": str(joke_meta.score),
                "maturity": joke_meta.maturity
            }, joke_sim)
    
    
    #--------------------- WEIGHTING ---------------------#
    results = ressy.weight(results_jac, results_cos)

    final = None
    if min_score:
        final = ressy.adj_minscore(float(min_score), results)
    else:
        # translate results into list without weighting for min_score
        final = [{
            "text": joke_meta["text"],
            "categories": joke_meta["categories"],
            "score": joke_meta["score"],
            "maturity": joke_meta["maturity"],
            "similarity": str(joke_sim)
        } for joke_meta, joke_sim in results.values()]


    #--------------------- SORTING ---------------------#
    # sort results by decreasing sim
    final = sorted(final, key=lambda x: (x["similarity"]), reverse=True)
    cat_options = sorted(cat_options)
    return {"jokes": final}


@jokes.route('/cat-options', methods=['GET'])
def cat_options():
    return {
        "categories": sorted([cat.category for cat in Categories.query.all()])
    }
