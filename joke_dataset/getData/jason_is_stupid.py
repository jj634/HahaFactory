from lxml import html
from lxml.cssselect import CSSSelector
import requests
import json
import re

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
    # 2. get rid of \ (not actually tho do it manually)
    # 3. replace email protected with @
    p1 = " ".join(strgood.split("\n")[2:-2])
    p2 = "$@".join(re.split('<a class=\"__cf_email__\".*?<\/a>',p1))

    end = "".join(p2.split("</li><p></p> </ul>"))
    nobr = "\n".join(end.split("<br/>"))
    noli = "\n".join(nobr.split("</li>"))
    nop = "\n".join(noli.split("<p>"))
    noul = "".join(nop.split("<ul>"))
    nolid = "".join(noul.split("<li>"))
    nopd = "".join(nolid.split("</p>"))

    res['joke'] = nopd
    

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
    # not actually tho change this directory if you want to waste 20 mins of ur life
    with open('./test.json', 'w') as file: 
        json.dump(jokes, file, indent=4)
