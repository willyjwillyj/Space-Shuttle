import requests
import os
from dotenv import load_dotenv

api_key = os.getenv("CHALLONGE_API_KEY")
headers = requests.utils.default_headers()
headers["User-Agent"] = "Space Shuttle"
async def get_participant_data(url_string):
    """
    Takes in url string and gets the data from challonge
    Returns in a list of 2-tuples
    0 - username
    1 - id
    """
    res = requests.get(f"https://api.challonge.com/v1/tournaments/galacticpgc-{url_string}/participants.json?api_key={api_key}",headers=headers)
    data = res.json()
    players = []
    for i in data:
        this_player = [i["participant"]["name"],i["participant"]["id"]]
        players.append(this_player)
    return players
async def get_match_data(url_string):
    """
    Takes in url string and gets the data from challonge
    Returns in a list of 4-tuples
    0 - id
    1 - player 1
    2 - player 2
    3 - state
    """
    res = requests.get(f"https://api.challonge.com/v1/tournaments/galacticpgc-{url_string}/matches.json?api_key={api_key}",headers=headers)
    data = res.json()
    matches = []
    for i in data:
        this_match = [i["match"]["id"],i["match"]["player1_id"],i["match"]["player2_id"],i["match"]["state"]]
        matches.append(this_match)
    print(matches)
    return matches

async def submit_score(url_string, match_id, scores, winner_id):
    print(f"https://api.challonge.com/v1/tournaments/galacticpgc-{url_string}/matches/{match_id}.json?api_key={api_key}&match[scores_csv]={scores}&match[winner_id]={winner_id}")
    requests.put(f"https://api.challonge.com/v1/tournaments/galacticpgc-{url_string}/matches/{match_id}.json?api_key={api_key}&match[scores_csv]={scores}&match[winner_id]={winner_id}",headers=headers)
