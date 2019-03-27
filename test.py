from flask import Flask, render_template, request, jsonify
import json
import requests
from pprint import pprint
from functools import wraps
from flask import  Response

def check_auth(username, password):
    return username == 'aak36' and password == 'heihei2'

def authenticate():
    return Response(
    'Could not verify your access level for that URL.\n'
    'You have to login with proper credentials', 401,
    {'WWW-Authenticate': 'Basic realm="Login Required"'})

def requires_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.authorization
        if not auth or not check_auth(auth.username, auth.password):
            return authenticate()
        return f(*args, **kwargs)
    return decorated



app = Flask(__name__)


api_url = 'https://api.punkapi.com/v2/'
beers_url = 'https://api.punkapi.com/v2/beers'
random_url = 'https://api.punkapi.com/v2/beers/random'
id_url = 'https://api.punkapi.com/v2/beers/{id}'

@app.route('/')
@requires_auth
def hello():
    return "<h1> Welcome to Punk API!</h1>"

@app.route('/name', methods=['GET'])
def names():
    response = requests.get(beers_url).json()
    names = {'name' : [], 'id' : []}
    for x in response:
        names['name'].append(x['name'])
        names['id'].append(x['id'])
    #return jsonify(names)
    return render_template('table2.html', result = response)

@app.route('/beers', methods=['GET'])
def beers():
    response = requests.get(beers_url).json()
    beers = {'name' : [], 'tagline' : [], 'ingredients' : [], 'description' : [], 'food_pairing' : []}
    for x in response:
        beers['name'].append(x['name'])
        beers['tagline'].append(x['tagline'])
        beers['ingredients'].append(x['ingredients'])
        beers['description'].append(x['description'])
        beers['food_pairing'].append(x['food_pairing'])
    #return jsonify(beers)
    return render_template('table.html', result = response)

@app.route('/beers/random' , methods=['GET'])
def random_list():
    response = requests.get(random_url).json()
    beers = {'name' : [], 'tagline' : [], 'first_brewed' : [], 'description' : [], 'food_pairing' : []}
    for x in response:
        beers['name'].append(x['name'])
        beers['tagline'].append(x['tagline'])
        beers['first_brewed'].append(x['first_brewed'])
        beers['description'].append(x['description'])
        beers['food_pairing'].append(x['food_pairing'])
    #return jsonify(beers)
    return render_template('table1.html', result = response)

@app.route('/beers/<id_name>' , methods=['GET'])
def beer_id(id_name):
    url = id_url.format(id=id_name)
    response = requests.get(url)
    dict_test = {'name' : [], 'tagline' : [], 'first_brewed' : [], 'description' : [], 'food_pairing' : [], 'id' : []}
    #beer_name = {'name' : [], 'tagline' : [], 'description' : [], 'food_pairing' : []}
    if response.status_code == 404:
        return "Error! Beer not found", 404
    elif response.status_code == 429:
        return "Error! Beer id not valid", 429
    new_response = response.json()

    #dict_test = {'name' : new_response['name']}
    #return jsonify(dict_test)

    for x in new_response:
        dict_test['name'].append(x['name'])
        dict_test['tagline'].append(x['tagline'])
        dict_test['first_brewed'].append(x['first_brewed'])
        dict_test['description'].append(x['description'])
        dict_test['food_pairing'].append(x['food_pairing'])
        dict_test['id'].append(x['id'])
    return jsonify(dict_test)

#    return render_template('html.html', html = response)


if __name__ == '__main__':
	app.run(port= 5000, debug=True)
