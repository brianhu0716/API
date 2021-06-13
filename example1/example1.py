# -*- coding: utf-8 -*-
"""
Created on Sun Jun 13 14:05:22 2021

website : https://programminghistorian.org/en/lessons/creating-apis-with-python-and-flask
@author: Patrick Smyth

"""
"""
review:
Function:
a) I am backend in this case, any request from url are is from frontend.
    It means that I hold the database and can return data whatever passed
    from url request.
b) in part2:
    I hold a database(list) named books, each element(dict) of it contains the 
    information about author, id, title, first sentence, and published of a book.
    when frontend use a url('/api/v1/resources/books/all') to GET all book,
    I will return exactly what frontend asks, which is books(reform as .json)
c) in part3:
    Now, this function is to traverse all book and return the "id" which included
    in url request from GET method, so in the first, function will examine if 
    the key: "id" is in url. If not, return error; else we will traverse every 
    id of book and add the qualified item to list then return it as format .json
d) Previous case are all about GET method. Now, the frontend pass a message ans wants 
    to add a book in my books, in this case, we first build a html called add 
    and ask frontend types all information I need. when backend fill the form
    and press "submit". the add.html will direct backend to url /api/v1/resources/books/add
    which shows backend the database after adding a book in it.
Method:
a) if methods = "POST", all methods related to the "request" needs to add suffix "form"
    ex : when I need to get the information passed from urls(GET) or body(POST),
    if methods = "GET": args = request.form.get("args")
    if methods = "POST": args = request.get("args")
b) To get information from body, we have two methods(take POST as example)
    (1) args = request.form.get("args")
    (2) args = request.form["args"]
    both (1) and (2) share the same result, but the difference between them is:
    (1) if args doesn't in the body, variable args will take null instead of 
        raising error, and the function will still return 
    (2) if "args" doesn't in the body, Error will be raised because of missing
        keyword: "args"
    
"""
import flask
from flask import request, jsonify, url_for, redirect

app = flask.Flask(__name__)


# Create some test data for our catalog in the form of a list of dictionaries.
books = [
    {'id': 0,
     'title': 'A Fire Upon the Deep',
     'author': 'Vernor Vinge',
     'first_sentence': 'The coldsleep itself was dreamless.',
     'year_published': '1992'},
    {'id': 1,
     'title': 'The Ones Who Walk Away From Omelas',
     'author': 'Ursula K. Le Guin',
     'first_sentence': 'With a clamor of bells that set the swallows soaring, the Festival of Summer came to the city Omelas, bright-towered by the sea.',
     'published': '1973'},
    {'id': 2,
     'title': 'Dhalgren',
     'author': 'Samuel R. Delany',
     'first_sentence': 'to wound the autumnal city.',
     'published': '1975'}
]


@app.route('/', methods=['GET'])
def home():
    return '''<h1>Distant Reading Archive</h1>
<p>A prototype API for distant reading of science fiction novels.</p>'''


# A route to return all of the available entries in our catalog.
# part2 
@app.route('/api/v1/resources/books/all', methods=['GET'])
def api_all():
    return jsonify(books)

# part3
@app.route('/api/v1/resources/books', methods=['GET'])
def api_id():
    # Check if an ID was provided as part of the URL.
    # If ID is provided, assign it to a variable.
    # If no ID is provided, display an error in the browser.
    if 'id' in request.args:
        id = int(request.args['id'])
    else:
        return "Error: No id field provided. Please specify an id."

    # Create an empty list for our results
    results = []

    # Loop through the data and match results that fit the requested ID.
    # IDs are unique, but other fields might return many results
    for book in books:
        if book['id'] == id:
            results.append(book)

    # Use the jsonify function from Flask to convert our list of
    # Python dictionaries to the JSON format.
    return jsonify(results)
    ''' url test case
    127.0.0.1:5000/api/v1/resources/books?id=0 
    127.0.0.1:5000/api/v1/resources/books?id=1 
    127.0.0.1:5000/api/v1/resources/books?id=2 
    127.0.0.1:5000/api/v1/resources/books?id=3
    '''
# part4
@app.route("/api/v1/resources/books/add", methods = ["GET"])
def add():
    if request.method == 'POST':
        ID = request.form.get('id')
        title = request.form.get("title")
        author = request.form.get("author")
        first_sentence = request.form.get("first_sentence")
        published = request.form.get("published")
        
        books.append(dict())
        books[-1]["id"] = ID
        books[-1]["title"] = title
        books[-1]["author"] = author
        books[-1]["first_sentence"] = first_sentence
        books[-1]["published"] = published
        
        return jsonify(books)
    
    else:
        ID = request.args.get('id')
        title = request.args.get("title")
        author = request.args.get("author")
        first_sentence = request.args.get("first_sentence")
        published = request.args.get("published")
        
        books.append(dict())
        books[-1]["id"] = ID
        books[-1]["title"] = title
        books[-1]["author"] = author
        books[-1]["first_sentence"] = first_sentence
        books[-1]["published"] = published
        return jsonify(books)
    
    
if __name__ == "__main__":
    
    app.run(debug = True)