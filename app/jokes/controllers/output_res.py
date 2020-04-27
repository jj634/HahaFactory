from . import *
import re

def weight(jac_res, cos_res, min_score):
    """
    Combine results from jaccard and cosine similarity
    Inputs:
        jac_res, cos_res: dictionary mapping joke_id to sim_score
        min_score: string
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

    for joke_id in jacky.union(cos_key):
        # to discuss - we are making 3 database calls for jaccard categories, this weighting, and metadata. that seems inefficient
        joke_meta = Joke.query.filter_by(id=joke_id).first()

        weighted_similarity = 0.20 * jac_res.get(joke_id, 0)
        weighted_similarity += 0.70 * cos_res.get(joke_id, 0)

        weighted_similarity += 0.20 * float(joke_meta.score)/5 if float(
            joke_meta.score) >= float(min_score) else 0.10 * float(joke_meta.score)/5

        results.append({
                        "text": joke_meta.text,
                        "categories": joke_meta.categories,
                        "score": str(joke_meta.score),
                        "maturity": joke_meta.maturity,
                        "size": str(joke_meta.size),
                        "similarity": str(weighted_similarity)
                    })
    return results

def size_filter(jokes, min_size, max_size):
    """
    Filters jokes based on given min_size and max_size.
    Inputs:
        jokes: list of dictionaries with following keys + values: 
            - "text": joke text
            - "categories": joke categories
            - "score": joke score
            - "maturity": joke maturiy
            - "size": joke size
            - "similarity": joke similarity score. 
        min_size: min size limit for joke_meta.text (length predefined in jokes_controller.py depending on input)
        max_size: max size limit for joke_meta.text (length predefined in jokes_controller.py depending on input)
    Output:
        resulting dictionary from filtering length of joke text for each joke in input jokes
    """
    ret = []
    if(min_size == -1): 
        for joke_meta in jokes: 
            if int(joke_meta["size"]) <= 30: 
                text = joke_meta["text"]
                sentence_list = re.split(r"(?<![A-Z])[.!?]\s+(?=[A-Z\"])", text)

                if(len(sentence_list) <= 1):
                    ret.append(joke_meta)
    else:
        for joke_meta in jokes: 
            if int(joke_meta["size"]) <= max_size and int(joke_meta["size"]) >= min_size:
                ret.append(joke_meta)
    return ret


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
