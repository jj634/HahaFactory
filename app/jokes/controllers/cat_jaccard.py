def get_rel_jokes(inv_idx):
    """
    Returns: dictionary mapping the joke id to its numerator in jaccard sim

    Inputs:
        inv_idx: dictionary mapping category to list of jokes ids that contain
            that category.
    """
    result = {}
    for cat, ls_ids in inv_idx.items():
        for doc in ls_ids:
            if doc not in result.keys():
                result[doc] = 1
            else:
                result[doc] += 1
    return result 

def jaccard_sim(query, num_dict, jokes_meta):
    """
    Returns: a list of tuples where t[0] is the joke id and t[1] is
    the similarity measure.

    Inputs:
        query: list of categories represented as strings
        num_dict: dictionary that maps joke id to its numerator in jaccard
            similarity measure.
        jokes_meta: dictionary of jokes mapping the joke id to its metadata

    """
    result = {}
    for joke in jokes_meta: 
        joke_id = joke.id
        result[joke_id] = num_dict[joke_id]/(len(set(joke.categories).union(set(query))))
    return result   
