import numpy as np
import nltk

def get_toks(jokes):
    result = set()

    for joke in jokes:
        result = result.union(set(joke['toks']))

    result = sorted(result)
    word_to_idx = {}
    for i in range(len(result)):
        word_to_idx[result[i]] = i

    return result, word_to_idx

def organize_data(jokes):
    scored = []
    unscored = []
    for joke in jokes:
        if joke['score'] == None:
            unscored.append(joke)
        else:
            scored.append(joke)
    scored = sorted(scored, key=lambda i:i['score'])
    return unscored, scored

def comp_prob_dict(jk_lst, cl_lst, tok_lst, tok_idx):
    funny_mtrx = np.zeros((len(tok_lst)+1, 2))
    notfunny_mtrx = np.zeros((len(tok_lst)+1, 2))

    for i in range(len(jk_lst)):
        lst = jk_lst[i]['toks']
        if cl_lst[i] == 1:
            for t in tok_lst:
                if t in lst:
                    funny_mtrx[tok_idx[t]][1] += 1
                else:
                    funny_mtrx[tok_idx[t]][0] += 1
            if len(lst) < 15:
                funny_mtrx[len(tok_lst)][1] += 1
            else:
                funny_mtrx[len(tok_lst)][0] += 1
        else:
            for t in tok_lst:
                if t in lst:
                    notfunny_mtrx[tok_idx[t]][1] += 1
                else:
                    notfunny_mtrx[tok_idx[t]][0] += 1
            if len(lst) < 15:
                notfunny_mtrx[len(tok_lst)][1] += 1
            else:
                notfunny_mtrx[len(tok_lst)][0] += 1
    result = {}
    num_funny = funny_mtrx[0][0] + funny_mtrx[0][1]
    num_notfunny = notfunny_mtrx[0][0] + notfunny_mtrx[0][1]
    for t in tok_lst:
        idx = tok_idx[t]
        one_funny = (funny_mtrx[idx][1]+1)/(num_funny + 2)
        zero_funny = (funny_mtrx[idx][0]+1)/(num_funny + 2)
        one_notfunny = (notfunny_mtrx[idx][1]+1)/(num_notfunny + 2)
        zero_notfunny = (notfunny_mtrx[idx][0]+1)/(num_notfunny + 2)
        result[t] = {'one_funny': one_funny, 'zero_funny': zero_funny, 'one_notfunny': one_notfunny, 'zero_notfunny': zero_notfunny}

    one_funny = (funny_mtrx[len(tok_lst)][1]+1)/(num_funny + 2)
    zero_funny = (funny_mtrx[len(tok_lst)][0]+1)/(num_funny + 2)
    one_notfunny = (notfunny_mtrx[len(tok_lst)][1]+1)/(num_notfunny + 2)
    zero_notfunny = (notfunny_mtrx[len(tok_lst)][0]+1)/(num_notfunny + 2)
    result['LENGTH'] = {'one_funny': one_funny, 'zero_funny': zero_funny, 'one_notfunny': one_notfunny, 'zero_notfunny': zero_notfunny}

    return result

def calc_pr(jk_toks, pr_dict, tok_lst, funny):
    acc = 1
    one = None
    zero = None
    if funny:
        one = 'one_funny'
        zero = 'zero_funny'
    else:
        one = 'one_notfunny'
        zero = 'zero_notfunny'
    for tok in tok_lst:
        if tok in jk_toks:
            acc *= pr_dict[tok][one]
        else:
            acc *= pr_dict[tok][zero]

    if len(jk_toks) < 15:
        acc *= pr_dict['LENGTH'][one]
    else:
        acc *= pr_dict['LENGTH'][zero]
    return acc

def test_ml(pr_dict, jk_lst, cl_lst, tk_lst, pr_funny, pr_notfunny):
    num_correct = 0
    total = 0
    for jk in range(len(jk_lst)):
        cat_fun = calc_pr(jk_lst[jk]['toks'], pr_dict, tk_lst, True) * pr_funny
        cat_notfun = calc_pr(jk_lst[jk]['toks'], pr_dict, tk_lst, False) * pr_notfunny
        # print(cat_fun)
        # print(cat_notfun)
        cat = 1 if cat_fun >= cat_notfun else 0
        if cl_lst[jk] == cat:
            num_correct += 1
        total += 1
    return num_correct/total

def get_features(jokes, tokenizer):
    """
    Returns a tuple of ([features], [word_to_idx]) where [features] is a set of
    features for the jokes and [word_to_idx] is a dictionary mapping a feature
    to a corresponding index that it will be in the doc-feature matrix.

    Features include the tokens, the POS composition of the joke, and the
    length of the joke. Using analysis.py the length of the funnier jokes
    seemed to be noticeably concentrated at the lower end compared to the not
    funny jokes.

    Inputs:
        jokes - list of strings where the string is a joke.
        tokenizer - a tokenizer
    """
    features = set()
    for joke in jokes:
        toks = tokenizer.tokenize(joke.lower())
        features = features.union(set(toks))
        tag_fd = nltk.pos_tag(toks)
        tag_fd = nltk.FreqDist(tag for (word, tag) in tag_fd)
        tag_fd = tag_fd.most_common()
        for t in tag_fd:
            features.add(t[0])
    features.add('len')
    
    features = sorted(features)
    word_to_idx= {}
    for i in range(len(features)):
        word_to_idx[features[i]] = i
    
    return features, word_to_idx

def create_mtrx(jokes, feas, fea_to_idx, tokenizer):
    """
    Returns an nxm matrix where n = number of jokes and m = number of features.

    Inputs:
        jokes - list of strings where a string is a joke
        feas - set of features
        fea_to_idx - dictionary mapping a feature to its corresponding index
        in the resulting matrix
        tokenizer - a tokenizer
    """
    result = np.zeros((len(jokes), len(feas)))
    for i in range(len(jokes)):
        joke_toks = tokenizer.tokenize(jokes[i].lower())
        joke_feas = nltk.pos_tag(joke_toks)
        joke_feas = nltk.FreqDist(tag for (word, tag) in joke_feas)
        joke_feas = joke_feas.most_common()
        for t in joke_toks:
            if t in fea_to_idx:
                result[i][fea_to_idx[t]] += 1
        for t in joke_feas:
            if t[0] in fea_to_idx:
                result[i][fea_to_idx[t[0]]] += t[1]
        # more weight on jokes less than 30 tokens
        if len(joke_toks) <=30:
          result[i][fea_to_idx['len']] = 15
    return np.asarray(result)    
