import sqlite3
import pandas as pd

con = sqlite3.connect("registrations.db",autocommit=True)
cur = con.cursor()
cur.execute("CREATE TABLE IF NOT EXISTS registrations(discord_id BIGINT,discord_username VARCHAR(256),game_username VARCHAR(256),tournament VARCHAR(256),challonge_id BIGINT, rating FLOAT)")
cur.execute("CREATE TABLE IF NOT EXISTS threads(discord_id BIGINT, challonge_match_id BIGINT, state VARCHAR(32), challonge_player1_id BIGINT, challonge_player2_id BIGINT, tournament_url VARCHAR(64))")
cur.execute("CREATE TABLE IF NOT EXISTS tournaments(discord_channel BIGINT, tournament_url VARCHAR(64), tournament VARCHAR(64), tournament_name VARCHAR(128))")
res = cur.execute("SELECT * FROM registrations")

cur.close()


async def register_player(discord_id, discord_username, game_username, tournament, rating=None):
    cur = con.cursor()
    res = cur.execute("SELECT * FROM registrations WHERE discord_id = ? AND tournament = ?",(discord_id, tournament))
    data = res.fetchall()
    if len(data) == 0:
        cur.execute("INSERT INTO registrations VALUES(?, ?, ?, ?, ?, ?)", (discord_id, discord_username, game_username, tournament, None, rating))
        cur.close()
        return f"Successfully registered {discord_username} for {tournament} with rating {rating}"
    else:
        cur.execute("DELETE FROM registrations WHERE discord_id = ? AND tournament = ?",(discord_id, tournament))
        cur.close()
        return f"Successfully removed registration for {discord_username} for {tournament}"
    
async def check_if_player_registered(discord_id, tournament):
    cur = con.cursor()
    res = cur.execute("SELECT * FROM registrations WHERE discord_id = ? AND tournament = ?",(discord_id, tournament))
    data = res.fetchall()
    cur.close()
    if len(data) == 0:
        return False
    return True

async def add_tournament_to_database(discord_channel_id:int,tournament_url:str,tournament:str,tournament_display_name:str):
    cur = con.cursor()
    cur.execute("INSERT INTO tournaments VALUES(?, ?, ?, ?)",(discord_channel_id,tournament_url,tournament,tournament_display_name))
    cur.close()
    return f"Successfully added {tournament_display_name} to database under category {tournament} and url {tournament_url}.\nMatch threads will be created in <#{discord_channel_id}>"

async def remove_tournament_from_database(tournament_display_name:str):
    cur = con.cursor()
    cur.execute("DELETE FROM tournaments WHERE tournament_name = ?",(tournament_display_name,))
    cur.close()
    return f"Successfully deleted {tournament_display_name} from database"

async def list_tournaments_in_database():
    cur = con.cursor()
    res = cur.execute("SELECT tournament_name FROM tournaments")
    msg = res.fetchall()
    cur.close()
    return msg

async def get_tournament_information():
    cur = con.cursor()
    res = cur.execute("SELECT tournament_url, tournament FROM tournaments")
    msg = res.fetchall()
    cur.close()
    return msg

async def get_tournament_information_for_matches():
    cur = con.cursor()
    res = cur.execute("SELECT tournament_url, tournament, discord_channel, tournament_name FROM tournaments")
    msg = res.fetchall()
    cur.close()
    return msg
    
async def set_player_challonge_id(discord_username,tournament,challonge_id):
    cur = con.cursor()
    cur.execute("UPDATE registrations SET challonge_id = ? WHERE tournament = ? AND discord_username = ?",(challonge_id,tournament,discord_username))
    cur.close()

async def get_state_of_match(challonge_id):
    cur = con.cursor()
    print(challonge_id)
    res = cur.execute("SELECT state FROM threads WHERE challonge_match_id = ?",(challonge_id,))
    msg = res.fetchall()
    cur.close()
    if len(msg) == 0:
        return None
    return msg[0][0]

async def end_state_of_match(challonge_id):
    cur = con.cursor()
    cur.execute("UPDATE threads SET state = 'completed' WHERE challonge_match_id = ?",(challonge_id,))
    cur.close()
    
async def add_thread_to_db(discord_id, challonge_match_id, state, challonge_player1_id, challonge_player2_id, tournament_url):
    cur = con.cursor()
    cur.execute("INSERT INTO threads VALUES(?, ?, ?, ?, ?, ?)",(discord_id,challonge_match_id,state,challonge_player1_id,challonge_player2_id,tournament_url))
    cur.close()

async def get_discord_info_from_challonge_info(challonge_id):
    cur = con.cursor()
    res = cur.execute("SELECT discord_id, discord_username FROM registrations WHERE challonge_id = ?",(challonge_id,))
    msg = res.fetchall()
    cur.close()
    return msg

async def get_channel_from_match(challonge_id):
    cur = con.cursor()
    res = cur.execute("SELECT discord_id FROM threads WHERE challonge_match_id = ?",(challonge_id,))
    msg = res.fetchall()
    cur.close()
    return msg[0][0]

async def get_match_info_from_match(discord_id):
    cur = con.cursor()
    res = cur.execute("SELECT challonge_match_id, challonge_player1_id, challonge_player2_id, tournament_url, state FROM threads WHERE discord_id = ?",(discord_id,))
    msg = res.fetchall()
    cur.close()
    return msg[0]


async def get_tournament_category_from_url(thread_id):
    cur = con.cursor()
    res = cur.execute("SELECT tournament_url FROM threads WHERE discord_id = ?", (thread_id,))
    url_string = res.fetchall()[0][0]
    res = cur.execute("SELECT tournament FROM tournaments WHERE tournament_url = ?", (url_string,))
    msg = res.fetchall()
    cur.close()
    return msg[0][0]

async def get_challonge_id_from_discord_id_and_tournament(discord_id, tournament):
    cur = con.cursor()
    res = cur.execute("SELECT challonge_id from registrations WHERE discord_id = ? and tournament = ?",(discord_id,tournament))
    msg = res.fetchall()
    cur.close()
    return msg[0][0]

async def get_tetrio_ids():
    cur = con.cursor()
    res = cur.execute("SELECT game_username FROM registrations WHERE tournament = 'TETR.IO'")
    msg = res.fetchall()
    cur.close()
    return msg

async def update_tetrio_tr(game_username, rating):
    cur = con.cursor()
    res = cur.execute("UPDATE registrations SET rating = ? WHERE game_username = ?",(rating,game_username,))
    cur.close()

async def export_seeding(tournament):
    db_df = pd.read_sql_query(f"SELECT discord_username, rating FROM registrations WHERE tournament = '{tournament}' ORDER BY rating DESC", con)
    db_df.to_csv('seeding.csv', index=False)


async def export_participants():
    db_df = pd.read_sql_query("SELECT * FROM registrations", con)
    db_df.to_csv('database.csv', index=False)

async def get_player_counts():
    db_df = pd.read_sql_query("SELECT COUNT(discord_username) AS PlayerCount, tournament FROM registrations GROUP BY tournament ORDER BY PlayerCount", con)
    db_df.to_csv('player_counts.csv', index=False)

async def execute_dql(sql):
    db_df = pd.read_sql_query(sql, con)
    db_df.to_csv('return.csv', index=False)
    
async def execute_dml(sql):
    cur = con.cursor()
    res = cur.execute(sql)
    cur.close()