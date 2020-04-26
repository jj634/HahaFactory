from . import typo_lib as tl
from nltk.tokenize import TreebankWordTokenizer


def parsing_dict(categories):
    """
    Returns dicionary mapping the lowered from of a category to the real 
    category name. 
    """
    result = {}
    for cat in categories:
        result[cat.lower()] = cat
    return result


# possible variations of categories
diff_dict = {
    'love and romance': 'love & romance',
    'family and parents': 'family, parents',
    'pickup line': 'pick-up line',
    'pickup lines': 'pick-up line',
    'pick-up lines': 'pick-up line'
}

tokenizer = TreebankWordTokenizer()


def parse(query, inv_idx, cats, parse_dict):
    """
    Returns tuple of:
            'toks': list of toks for fast cosine
            'cats': list of categories for jaccard
            'typo_toks': Did you mean... for tokens
                                (typo, (crct, dist)) list where typo is what user inputted
                                and crct is the suggested term and dist is the edit distance
            'typo_cats': Did you mean... for categories
                                (typo, (crct, dist)) list where typo is what user inputted
                                and crct is the suggested term and dist is the edit distance

    Inputs:
            query: string
            inv_idx: inverse idx of the toks
            cats: lst of categories
            parse_dict: maps lowered cat names to real cat names
    """
    inv_idx = [k for k, v in inv_idx.items()]  # list of all tokens
    query = query.lower()
    cats = [c.lower() for c in cats]  # lower categories to match lowered query

    input_cats = []
    # first parse out categories
    for c in cats:
        if c in query:
            input_cats.append(c)
            start = query.index(c)
            end = len(c)
            query = query[:start] + ' ' + query[start + end:]
    # check for possible variations of category names
    for var in diff_dict:
        if var in query:
            input_cats.append(diff_dict[var])
            start = query.index(var)
            end = len(var)
            query = query[:start] + ' ' + query[start + end:]

    # list of categories for Jaccard
    input_cats = [parse_dict[c] for c in input_cats]

    # get toks
    toks = tokenizer.tokenize(query)
    new_toks = []
    typos = []

    # check if the tokens are valid (in the inv_idx), otherwise classified as typo
    for t in toks:
        if t not in inv_idx:
            typos.append(t)
        else:
            new_toks.append(t)

    # suggests a correction for every "typo" in query
    closest_toks = {}
    closest_cats = {}
    if typos:
        for t in typos:
            closest_toks[t] = tl.closest_word(t, inv_idx)
            closest_cats[t] = tl.closest_word(t, cats)

    return new_toks, input_cats, closest_toks.items(), closest_cats.items()
