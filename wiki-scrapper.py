# wiki-scrapper.py
import flask
from flask import Flask, request
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)


@app.route("/")
def home_view():
    return "<h1>Welcome to the sports-wiki</h>"


@app.route('/search')
def search_wiki():
    # first let's check if parameters are included
    if request.args.get('org') is None or request.args.get('team') is None:
        err = {'Error': "Valid URL parameters org= team="}
        return err

    """Next, checking for MLB or FIFA"""

    # obtain team first
    team = request.args.get('team')
    if request.args.get('org').upper() == "MLB":
        team = get_team(team)
        if team is None:
            return not_found()
        response = requests.get(
            url="https://en.wikipedia.org/wiki/" + team
        )
    else:
        response = requests.get(
            url="https://en.wikipedia.org/wiki/" + team + "_at_the_FIFA_World_Cup"
        )

    if response.status_code == 404:  # not found status code
        return not_found()
    # function scrape will scrape only the summary of the wikipedia article
    resp = {'summary': scrape(response)}
    return resp


def get_team(team):
    """
    will try to obtain a MLB team from list
    team - any key words to a MLB team (ex. Giants or San Francisco or San Francisco Giants)
    returns MLB team name wikipedia will recognize
    """
    for t in mlb_teams:
        if team.lower() in t.lower():
            return t.replace(" ", "_")  # replacing spaces with "_" for wikipedia url search
    return None


def not_found():
    """
    Will return a json object indicating an error
    """
    err = {'Error': "Team not found"}
    return err


def scrape(response):
    """
    Will use beautifulsoup to scrape a wikipedia HTML content and only obtain the <p> tags in the summary
    response - should contain the HTML response from the wikipedia page
    returns the summary
    """
    soup = BeautifulSoup(response.content, 'html.parser')
    summary = ""
    amount = 0
    for tag in soup.find_all():
        if tag.name == "p" and amount < 3:
            summary += tag.get_text()
            amount += 1
        elif tag.name == "p" and amount >= 3:
            summary += tag.get_text()
        elif tag.name == "div" and amount >= 3:
            break
    return summary


# create a list containing every MLB team so that we can scrape the right article from Wikipedia
mlb_teams = ["Baltimore Orioles", "Boston Red Sox", "New York Yankees", "Tampa Bay Rays", "Toronto Blue Jays",
             "Chicago White Sox", "Cleveland Guardians", "Detroit Tigers", "Kansas City Royals", "Minnesota Twins",
             "Houston Astros", "Los Angeles Angels", "Oakland Athletics", "Seattle Mariners", "Texas Rangers (baseball)",
             "Atlanta Braves", "Miami Marlins", "New York Mets", "Philadelphia Phillies", "Washington Nationals",
             "Chicago Cubs", "Cincinnati Reds", "Milwaukee Brewers", "Pittsburgh Pirates", "St. Louis Cardinals",
             "Arizona Diamondbacks", "Colorado Rockies", "Los Angeles Dodgers", "San Diego Padres",
             "San Francisco Giants"]

if __name__ == '__main__':
    app.run()
