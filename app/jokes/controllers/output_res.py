from . import *

def weight(jac_res, cos_res, min_score, advanced):
    """
    Combine results from jaccard and cosine similarity
    Inputs:
        jac_res, cos_res: dictionary mapping joke_id to sim_score
        min_score: string [value between 0 and 0.5]
    Output:
        list of dictionaries with following keys + values: 
            - "text": joke text
            - "categories": joke categories
            - "score": joke score
            - "maturity": joke maturiy
            - "size": joke size
            - "similarity": joke similarity score. 
        Currently, 20% weight is given to Jaccard, 70% to Cosine Similarity, 20% to jokes > min_score and 10% to jokes < min_score.
        Note: if a joke is not in one of the input dictionaries, its sim_score for that measure is 0.
    """
    
    results = []
    jacky = set(jac_res.keys())  # haha get it? jac_key -> jacky
    cos_key = set(cos_res.keys())
    cos_weight = None
    jac_weight = None
    sc_weight = float(min_score) # this is relevance vs funny

    if (len(jacky) == 0 and len(cos_key) == 0):
        cos_weight = 0
        jac_weight = 0
    elif (len(jacky) == 0):
        cos_weight = 1
        jac_weight = 0
    elif (len(cos_key) == 0):
        cos_weight = 0
        jac_weight = 1
    else:
        if advanced:
            cos_weight = 0.6
            jac_weight = 0.4
        else:
            cos_weight = 0.7
            jac_weight = 0.3
    
    cos_weight *= (1.0 - sc_weight)
    jac_weight *= (1.0 - sc_weight)

    for joke_id in jacky.union(cos_key):
        # to discuss - we are making 3 database calls for jaccard categories, this weighting, and metadata. that seems inefficient
        joke_meta = Joke.query.filter_by(id=joke_id).first()

        cos_score = cos_weight * cos_res.get(joke_id, 0)
        jac_score = jac_weight * jac_res.get(joke_id, 0)
        sc_score = sc_weight * float(joke_meta.score)/5
        weighted_similarity = jac_score
        weighted_similarity += cos_score
        weighted_similarity += sc_score

        results.append({
                        "text": joke_meta.text,
                        "categories": joke_meta.categories,
                        "score": str(joke_meta.score),
                        "maturity": str(joke_meta.maturity),
                        "size": str(joke_meta.size),
                        "similarity": str(weighted_similarity),
                        "cos_score": str(cos_score),
                        "jac_score": str(jac_score),
                        "sc_score": str(sc_score)
                    })
    return results, cos_weight, jac_weight, sc_weight


def special_weighting(jokes, min_score):
    results = jokes
    if min_score:
        min_weight = min_score*2
        joke_weight = (1-min_weight)
        for i in range(len(jokes)):
            curr_rand = float(results[i]['rand'])
            curr_score = float(results[i]['score'])/5
            results[i]['rand'] = str(curr_rand*joke_weight + curr_score*min_weight)
    return jokes

def adj_minscore(min_score, results):
    """
    Combine results from jaccard and cosine similarity
    Inputs:
        min_score: a float from 0-5. high min_score means to value relevance more
        and joke.score less, low min_score means to value relevance less and
        joke.score more
        results: dictionary that matches joke_id to (joke_metadata,sim_score)
        joke_metadata is a dictionary containing keys: text, categories, score, maturity

    Output:
        The sim_score of each joke is weighted with jaccard (0-1), cosine (0-1),
        and joke.score (0-5, but normalized to 0-1) as follows:
         - if joke.score >= min_score: 0.67 * (jaccard + cosine) + 0.33 * joke.score
         - else, 0.67 * (jaccard + cosine) + 0.16 * joke.score
        This places higher value on jokes with score exceeding min_score.
    """

    final = []
    for joke_meta, joke_sim in results.values():
        # this case never happens, since all jokes are scored
        if joke_meta['score'] == 'None':
            final.append({
                "text": joke_meta["text"],
                "categories": joke_meta["categories"],
                "score": joke_meta["score"],
                "maturity": joke_meta["maturity"],
                "similarity": str(joke_sim*0.67)
            })
        else:
            joke_score = float(joke_meta['score'])
            if joke_score >= min_score:
                final.append({
                    "text": joke_meta["text"],
                    "categories": joke_meta["categories"],
                    "score": str(joke_meta["score"]),
                    "maturity": joke_meta["maturity"],
                    "similarity": str(joke_sim*0.67 + (0.33/5*joke_score))
                })
            else:
                final.append({
                    "text": joke_meta["text"],
                    "categories": joke_meta["categories"],
                    "score": str(joke_meta["score"]),
                    "maturity": joke_meta["maturity"],
                    "similarity": str(joke_sim*0.67 + (0.16/5*joke_score))
                })

    # used if no jac or cos joke outputs but min_score is provided
    # to discuss - is this necessary when they are provided?
    jokes = Joke.query.filter(Joke.score >= min_score).all()
    nonrelated_jokes = [{
        "text": joke.text,
        "categories": joke.categories,
        "score": str(joke.score),
        "maturity": joke.maturity,
        "similarity": str(0.16/5*float(joke.score))
    } for joke in jokes]

    final += nonrelated_jokes
    return final
