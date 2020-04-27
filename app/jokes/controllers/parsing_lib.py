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
# can write a script to add plurals and ___ jokes but too lazy for now
diff_dict = {
    'love and romance': 'love & romance',
    'family and parent': 'family, parents',
    'pickup line': 'pick-up line',
    'family': 'family, parents',
    'parent': 'family, parents',
    'food': 'food jokes',
    'animal': 'animals',
    'bar': 'bar jokes',
    'blind': 'blind jokes',
    'blonde joke': 'blonde jokes',
    'computer': 'computers',
    'crazy joke': 'crazy jokes',
    'dad joke': 'dad jokes',
    'deep thought': 'deep thoughts',
    'ethnic joke': 'ethnic jokes',
    'food': 'food jokes',
    'heaven': 'heaven and hell',
    'hell': 'heaven and hell',
    'holiday': 'holidays',
    'insult': 'insults',
    'love': 'love & romance',
    'lawyer': 'lawyers',
    'light bulb': 'light bulbs',
    'office': 'office jokes',
    'one liner': 'one liners',
    'one-liner': 'one liners',
    'puns': 'pun',
    'sport': 'sports',
    'state joke': 'state jokes',
    'romance': 'love & romance',
    'police': 'police jokes'
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
    tmp = query
    # check for possible variations of category names
    for var in diff_dict:
        if var in tmp:
            while var in tmp:
                start = tmp.index(var)
                end = len(var) + start
                real_start = (
                    start <= 0) or tmp[start-1] == ' ' or tmp[start-1] == ','
                real_end = (end >= len(tmp)) or (
                    tmp[end] == ' ') or (tmp[end] == ',') or (tmp[end] == 's')
                tmp = tmp[:start] + tmp[end:]
                if real_start and real_end:
                    input_cats.append(diff_dict[var])
    for c in cats:
        if c in tmp:
            while c in tmp:
                start = tmp.index(c)
                end = len(c) + start
                real_start = (
                    start <= 0) or tmp[start-1] == ' ' or tmp[start-1] == ','
                real_end = end >= len(tmp) or (
                    tmp[end] == ' ' or tmp[end] == ',')
                tmp = tmp[:start] + tmp[end:]
                if real_start and real_end:
                    input_cats.append(c)
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
