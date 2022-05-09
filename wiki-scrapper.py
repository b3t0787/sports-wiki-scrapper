# wiki-scrapper
import flask
from flask import Flask, request
import wikipedia
import json

app = Flask(__name__)


@app.route("/")
def home_view():
    return "<h1>Welcome to the sports-wiki</h>"


@app.route('/search')
def search_wiki():
    # first let's check if parameters are included
    if request.args.get('org') is None or request.args.get('team') is None:
        err = {'Error': "Valid URL parameters org= team="}
        err = json.dumps(err)
        resp = flask.Response(response=err, content_type='application/json', status=400)
        return resp

    # try to obtain page from wikipedia based on search from URL parameters
    try:
        wikiPage = wikipedia.page(request.args.get('org') + ' ' + request.args.get('team'))
        print(request.args.get('org') + ' ' + request.args.get('team'))
        text = wikiPage.summary  # get summary from article
        text = {'summary': text}  # make a dictionary with key 'summary'
        # to stop unicode encoding let's create json object manually and add switch and encode type
        text = json.dumps(text, ensure_ascii=False).encode('utf8')
        # response
        resp = flask.Response(response=text, content_type='application/json', status=200)
        return resp
    except wikipedia.exceptions.PageError:
        # error, return error with status 404
        err = {'Error': "Wikipedia article not found"}
        err = json.dumps(err)
        resp = flask.Response(response=err, content_type='application/json', status=404)
        return resp


if __name__ == '__main__':
    app.run()
