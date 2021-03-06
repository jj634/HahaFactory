import json
import prob_lib1 as pl
from nltk.tokenize import TreebankWordTokenizer
import numpy as np
import matplotlib.pyplot as plt
import nltk


with open('dataset_raw.json') as f:
    data = json.load(f)

unscored, scored = pl.organize_data(data)

funny_jokes = scored[len(scored)-500:] # label top 500 jokes as 'funny'
notfunny_jokes = scored[:750] # label bottom 750 jokes as 'not funny'

funny_classes = [1 for _ in funny_jokes] # use 1 for funny
notfunny_classes = [0 for _ in notfunny_jokes] # use 0 for not funny
all_jokes = np.array(funny_jokes + notfunny_jokes) #
all_classes = np.array(funny_classes + notfunny_classes)

funny_jokes = [i['joke'] for i in funny_jokes]
notfunny_jokes = [i['joke'] for i in notfunny_jokes]

tokenizer = TreebankWordTokenizer()

def get_toks(jokes):
    result = set()
    for joke in jokes:
        result = result.union(set(tokenizer.tokenize(joke.lower())))

    result = sorted(result)
    word_to_idx = {}
    for i in range(len(result)):
        word_to_idx[result[i]] = i
    return result, word_to_idx

def create_term_doc_mtrx(jokes):
    toks, tok_to_idx = get_toks(jokes)
    result = np.zeros((len(jokes), len(toks)))
    for i in range(len(jokes)):
        joke_toks = tokenizer.tokenize(jokes[i].lower())
        for t in joke_toks:
            if t in tok_to_idx:
                result[i][tok_to_idx[t]] += 1
    return np.asarray(result)

term_doc_mtrx_fun = create_term_doc_mtrx(funny_jokes)
term_doc_mtrx_notfun = create_term_doc_mtrx(notfunny_jokes)

def avg_leng(joke_mtrx):
    acc = []
    for i in range(len(joke_mtrx)):
        sum = np.sum(joke_mtrx[i])
        acc.append(np.sum(joke_mtrx[i]))

    acc = np.asarray(acc)
    print('max: ', np.max(acc))
    print('min: ', np.min(acc))
    print('avg: ', np.sum(acc)/len(acc))
    acc = [int(i) for i in acc]
    print('freq: ', np.bincount(acc).argmax())

def createScoreHistogram(mtrx):
    data = []
    for i in range(len(mtrx)):
        sum = np.sum(mtrx[i])
        data.append(np.sum(mtrx[i]))
    data = np.asarray(data)
    plt.hist(data, bins = 50)
    plt.ylabel('num')
    plt.xlabel('num tokens')
    plt.show()

def show_histograms():
    createScoreHistogram(term_doc_mtrx_fun)
    createScoreHistogram(term_doc_mtrx_notfun) # 40 good cut-off

def show_leng():
    avg_leng(term_doc_mtrx_fun)

def pos_analysis(jokes):
    pos_dict = {}
    for j in jokes:
        pos_lst = nltk.pos_tag(tokenizer.tokenize(j.lower()))
        tag_fd = nltk.FreqDist(tag for (word, tag) in pos_lst)
        tag_fd = tag_fd.most_common()
        for t in tag_fd:
            if t[0] not in pos_dict:
                pos_dict[t[0]] = []
            pos_dict[t[0]].append(t[1])
    return pos_dict

def show_pos(jokes):
    pos_dict = pos_analysis(jokes)
    for i in pos_dict:
        plt.hist(pos_dict[i], bins = 10)
        plt.ylabel('num')
        plt.xlabel('num ' + i)
        plt.show()

show_pos(funny_jokes)
        
