import re

sizes_dict = {
    'Short': (0, 50), 
    'Medium': (50, 105),
    'Long': (105, 100000)
}

def size_filter(jokes, sizes):
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
        sizes: list of sizes: 'One-Liner', 'Short', 'Medium', 'Long'
    Output:
        resulting dictionary from filtering length of joke text for each joke in input jokes
    """
    ret = []
    if('One-Liner' in sizes): 
        for joke_meta in jokes: 
            if int(joke_meta["size"]) <= 30: 
                text = joke_meta["text"]
                sentence_list = re.split(r"(?<![A-Z])[.!?]\s+(?=[A-Z\"])", text)

                if(len(sentence_list) <= 1):
                    ret.append(joke_meta)
    for size_val in sizes_dict:
        if size_val in sizes: 
            min_size = sizes_dict[size_val][0]
            max_size = sizes_dict[size_val][1]
            for joke_meta in jokes: 
                if int(joke_meta["size"]) <= max_size and int(joke_meta["size"]) >= min_size:
                    ret.append(joke_meta)
    return ret