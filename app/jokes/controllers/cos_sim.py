from nltk.tokenize import TreebankWordTokenizer
from . import *
import math


def inv_idx_trad(inverted_index):
    return {x['term']: [(x['joke_ids'][i], x['tfs'][i]) for i in range(len(
        x['joke_ids']))] for x in inverted_index}


def fast_cossim(query, inv_idx_terms, inverted_index):
    """
        Search the collection of documents for the given query
        Inputs: 
            query: list of tokens
            inv_idx_terms: dictionary mapping token to list of tuples where tuple = (joke_id, tfs)
            inverted_index: list of dictionaries for each token where dictionary maps
                - term
                - list of joke_ids
                - list of tfs
                - idf

        Output: list of tuples tuple = (joke, sim_score)
    """
    result = {}  # dictionary mapping doc_id to cosine similarity measure
    assert type(query) is list

    # make sure query is a string list!!
    q_set = set(query)

    q_norm = 0  # query norm
    # dictionary mapping term to list of tuple(joke_id, tf)
    idf = {}  # dictionary mapping term to idf

    for t_dict in inverted_index:
        if t_dict['term'] in q_set:
            if 'idf' in t_dict.keys():
                idf[t_dict['term']] = t_dict['idf']

    for q_word in q_set:
        if q_word in idf:
            tf_q = query.count(q_word)
            q_norm += (tf_q * idf[q_word])**2
            for tup in inv_idx_terms[q_word]:
                doc = tup[0]
                if doc not in result:
                    result[doc] = 0
                result[doc] += (tup[1] * (idf[q_word]**2) * tf_q)

    q_norm = math.sqrt(q_norm)
    for doc in result:
        print(doc)
        norm = Joke.query.filter_by(id=doc).first().norm
        result[doc] = result[doc] / (q_norm * float(norm))

    # result = sorted(result.items(), key=lambda x: (x[1], x[0]), reverse=True)
    return result