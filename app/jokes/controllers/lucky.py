from . import *
from random import randint


@jokes.route('/random', methods=['GET'])
def generate_random_joke(category):
    joke_lst = (Categories.query.filter_by(category = category).first()).joke_ids
    rand_joke_id = joke_lst[randint(0, len(joke_lst)-1)]
    joke = Joke.query.filter_by(id = rand_joke_id).first()
    joke_obj =  {'text': joke.text, 'categories': joke.categories, 'score': str(joke.score), 'maturity': str(joke.maturity), 'size': str(joke.size)}
    return {"joke": joke_obj}