from . import *
from app.irsystem.models.helpers import *
from app.irsystem.models.helpers import NumpyEncoder as NumpyEncoder
from app.jokes import *
import app.irsystem.controllers.sim_lib as sl

project_name = "Haha Factory"
net_id = "Jason Jung: jj634, Suin Jung: sj575, Winice Hui: wh394, Cathy Xin: cyx5, Rachel Han: ryh25"

with open('./inv_idx_cat.json') as f:
    inv_idx_cat = json.load(f)
with open('./final.json') as f:
    data = json.load(f)

@irsystem.route('/', methods=['GET'])
def search():
    query = request.args.get('search')
    min_score = request.args.get('score')
    if query is not None:
        results = []
        categories = query.split(", ")
        jokes_cat = sl.jaccard_sim_json(categories, inv_idx_cat, data)
        for i in range(10):
            joke = jokes_cat[i][0]
            results.append(data[joke]['joke'] + ' ' + str(jokes_cat[i][1]))

    if not query and not min_score:
        results = []
        output_message = ''
    else:
        output_message = "Your search: " + query
    return render_template('search.html', name=project_name, netid=net_id, output_message=output_message, data=results)

@irsystem.route('/react', methods=['GET'])
def sendhome():
	return render_template('index.html')
