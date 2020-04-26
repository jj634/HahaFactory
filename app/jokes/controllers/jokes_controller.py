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
            new_joke = Joke(text=data['text'], categories=data['categories'],
                            score=data['score'], maturity=data['maturity'])
            db.session.add(new_joke)
            db.session.commit()
            return {"message": "joke {new_joke.id} has been created successfully."}
        else:
            return {"error": "The request payload is not in JSON format"}

    elif request.method == 'GET':
        jokes = Joke.query.all()
        results = [
            {
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
    categories = request.args.getlist('category')
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

    search_params = {}
    search_params['key_words'] = query if query else ''
    search_params['min_score'] = min_score if min_score else ''
    search_params['categories'] = categories if categories else ''
    search_params['size'] = size

    parse_dict = pl.parsing_dict(cat_options)
    p_cats = []
    if query:
        query, p_cats, tok_typos, cat_typos = pl.parse(
            query, inv_idx, cat_options, parse_dict)
    else:
        query = []

    # dictionary key = joke_id, value = (joke_dict, jac_sim)
    results_jac = {}

    if categories or p_cats:
        categories_list = categories + p_cats
        categories_list = list(set(categories_list))

        cat_jokes = {}  # dictionary where key = category, value = array of doc_ids with that category
        for cat in categories_list:  # for every category
            # get the record where category is equal to cat
            if cat == '':
                continue
            doc_lst = Categories.query.filter_by(category=cat).first()
            cat_jokes[cat] = doc_lst.joke_ids

    # dictionary with key = joke_id and value = numerator
        numer_dict = jac.get_rel_jokes(cat_jokes)

        rel_jokes = {}  # dictionary where key = joke_id, value = joke
        for doc in numer_dict.keys():
            rel_jokes[doc] = Joke.query.filter_by(id=doc).first()

        results_cat = jac.jaccard_sim(categories_list, numer_dict, rel_jokes)

        for element in results_cat:
            doc_id = element[0]
            joke = rel_jokes[doc_id]
            sim_measure = (element[1])
            if doc_id not in results_jac:
                results_jac[doc_id] = ({"text": joke.text, "categories": joke.categories, "score": str(
                    joke.score), "maturity": joke.maturity}, sim_measure)

    # dictionary where key= joke_id, value = (joke_dict, cos_sim)
    results_cos = {}

    if query:
        # a list of (joke_id, cos_sim)
        results_query = cos.fast_cossim(query, inv_idx, inv_idx_free)
        for element in results_query:
            doc_id = element[0]
            joke = Joke.query.filter_by(id=doc_id).first()
            sim_measure = element[1]
            results_cos[doc_id] = ({"text": joke.text, "categories": joke.categories, "score": str(
                joke.score), "maturity": joke.maturity}, sim_measure)

    results = ressy.weight(results_jac, results_cos)

    final = None
    if min_score:
        final = ressy.adj_minscore(float(min_score), results)
    else:
        # translate results into list without weighting for min_score
        final = [(x[1][0], "Similarity: " + str(x[1][1]))
                 for x in results.items()]

    # sort results by decreasing sim
    final = sorted(final, key=lambda x: (x[1]), reverse=True)
    cat_options = sorted(cat_options)
    return {"jokes": final}

    # Joke.testFunct()


@jokes.route('/cat-options', methods=['GET'])
def cat_options():
    return {"categories": sorted([cat.category for cat in Categories.query.all()])}
