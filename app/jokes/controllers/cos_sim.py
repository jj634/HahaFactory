from . import *
import math

def fast_cossim(query, inverted_index, idf, rel_jokes_meta):
    """
        Search the collection of documents for the given query
        Inputs: 
            query: list of tokens
            inverted_index: dictionary mapping word to list of tuples where tuple = (joke_id, tf)
            idf: dictionary mapping term to idf value

        Output: list of tuples tuple = (joke, sim_score)
    """
    result = {}  # dictionary mapping doc_id to cosine similarity measure
    jokes = []
    acc_joke_meta = rel_jokes_meta
    assert type(query) is list

    # make sure query is a string list!!
    q_set = set(query)

    q_norm = 0  # query norm

    for q_word in q_set:
        if q_word in idf:
            tf_q = query.count(q_word)
            q_norm += (tf_q * idf[q_word])**2
            for tup in inverted_index[q_word]:
                doc = tup[0]
                if doc not in result:
                    result[doc] = 0
                result[doc] += (tup[1] * (idf[q_word]**2) * tf_q)

    q_norm = math.sqrt(q_norm)
    for doc in result:
        if doc not in acc_joke_meta:
            acc_joke_meta[doc] = Joke.query.filter_by(id=doc).first()
        norm = acc_joke_meta[doc].norm
        result[doc] = result[doc] / (q_norm * float(norm))

    return result, acc_joke_meta