from . import *

def weight(jac_res, cos_res, min_score, advanced, rel_jokes_meta):
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
        joke_meta = rel_jokes_meta[joke_id] # NEW: delete all database calls by using rel_jokes_meta

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