# coding=utf-8
import requests
from SPARQLWrapper import SPARQLWrapper, JSON
from flask import Flask, render_template, request, url_for
#from urllib import quote_plus
import freebase
import goslate
import wikipedia
from mstranslator import Translator



# Initialize the Flask application
app = Flask(__name__)

gs = goslate.Goslate()
# Define a route for the default URL, which loads the index
@app.route('/')
def index():
    return render_template('index.html')

# Define a route for the action of the index, for example '/engine/'
# We are also defining which type of requests this route is 
# accepting: POST requests in this case
@app.route('/engine/', methods=['POST'])
def engine():
    # Get question from user as text
    question =request.form['question']

    #translate question
    translator = Translator('emad_punk123456', 'R0go6LNQEj3CVh7nhyHw/DLenWLuQNjyjdhnZ0okRGE=')
    translated_question=translator.translate(question, lang_from='ar', lang_to='en')
    lower_q=translated_question.lower()
    #unicode_question=unicode(question, "utf-8")
    # Send question to api for question analysis and generate query
    # this Online App is An example For apply Quepy Model on DBpedia
    # We use it only as a quick demo but we have alot we need to do ..
    if translated_question !="":
       url = "http://quepy.machinalis.com/engine/get_query?question="+lower_q

    #gs.translate(text, 'de', 'en')
    # encoded_url = quote_plus(url.encode("utf-8"))
    #   Get sparql query as json
    r = requests.get(url)
    j = r.json()
    # Select only the sparql code
    query = (j['queries'][0]['query'])
    #print (query)
    # Send sparql-query to SPARQLWrapper Model to run it on dbpedia
    sparql = SPARQLWrapper("http://dbpedia.org/sparql")
    sparql.setQuery(query)
    sparql.setReturnFormat(JSON)
    # Get results as json
    results = sparql.query().convert()
    #convert question string to array
    q2=question.split(' ')
    #wiki_question = wikipedia.summary(question)
    # return json to answer page to view.
    return render_template('answer.html',query=query ,question=lower_q, results=results , q2=q2 , url=url )

# Run the app :)
if __name__ == '__main__':
  app.run(debug=True)

