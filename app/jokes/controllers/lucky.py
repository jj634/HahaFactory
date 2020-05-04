from . import *
from random import randint

N_JOKES = 5932

@jokes.route('/random', methods=['GET'])
def generate_random_joke():
    """
    Returns: A random joke
    TODO: should we populate form fields with the joke's info?
    TODO: should we select from preset keyword, category, maturity, length options?
    """
    
    joke_meta = Joke.query.filter_by(id=randint(1, N_JOKES)).first()

    joke_obj = {
        "text": joke_meta.text,
        "categories": joke_meta.categories,
        "score": str(joke_meta.score),
        "maturity": str(joke_meta.maturity),
        "size": str(joke_meta.size),
    }

    return {"jokes": joke_obj}