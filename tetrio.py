import requests

async def get_player_data(usr:str):
    headers = requests.utils.default_headers()
    headers["User-Agent"] = "Space Shuttle"
    data = requests.get(f"https://ch.tetr.io/api/users/{usr.lower()}/summaries/league", headers=headers)
    return data.json()

async def get_player_id(usr:str):
    headers = requests.utils.default_headers()
    headers["User-Agent"] = "Space Shuttle"
    data = requests.get(f"https://ch.tetr.io/api/users/{usr.lower()}", headers=headers)
    item = data.json()
    return item["data"]["_id"]