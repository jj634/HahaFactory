from lxml import html
from lxml.cssselect import CSSSelector
import requests
import json
import re
import bs4

cat_regex = re.compile('(?<=Category: )(.*[A-z])')
scr_regex = re.compile("(?<=Rating: )(.*\d)")

NUM_JOKES = 3773

def extract_joke(id):
    res = {}

    url = 'http://stupidstuff.org/jokes/joke.htm?jokeid={}'
    response = requests.get(url.format(id))

    sel_joke = CSSSelector('.scroll td')
    sel_cat = CSSSelector('center+ .bkline td')

    html_elmnts = html.fromstring(response.content)

    soup = bs4.BeautifulSoup(response.content, "html5lib")

    scroll = soup.find(class_="scroll")
    good = scroll.find("td")
    strgood = str(good)

    # 1. replace \n with space
    # 2. get rid of \
    # 3. replace email protected with @
    content = strgood[strgood.index(">")+1:strgood.index("</td>")]


    p1 = " ".join(content.split("\n"))
    p2 = "$@".join(re.split('<a class=\"__cf_email__\".*?<\/a>',p1))

    # remove list starter and header

    full_text=p2
    ul_ind = p2.find("<ul>")
    # is a list
    if ul_ind != -1:
        acc = p2[:ul_ind]
        rest = p2[ul_ind+4:]

        rest_bulleted = " - ".join(rest.split("<li>"))
        rest_separated = "\n".join(rest_bulleted.split("</li>"))

        nould = "\n".join(rest_separated.split("</ul>"))

        full_text = acc+"\n"+nould



    full_text = "\n\n".join(full_text.split("<p>"))
    full_text = "".join(full_text.split("</p>"))
    full_text = "\n".join(full_text.split("<br/>"))


    # replacing weird \n's
    final = " ".join(re.split('\s*\\n\s*(?=[a-z])',full_text))
    final1 = "\n".join(re.split(' +\\n +|\\n +| +\\n',final))


    res['joke'] = final1.strip()
    

    for cat in sel_cat(html_elmnts):
        content = cat.text_content().strip()
        category = (cat_regex.search(content)).group(0)
        if (category == 'Miscellaneous'):
            res['categories'] = []
        else: 
            res['categories'] = [category]
        rating = (scr_regex.search(content)).group(0)
        res['score'] = float(rating)


    return res

jokes = []

try:
    for i in range(1, NUM_JOKES+1):
        jokes.append(extract_joke(i))

finally:
    with open('../json/raw/jasons_cool_json_2.json', 'w') as file:
        json.dump(jokes, file, indent=4)
