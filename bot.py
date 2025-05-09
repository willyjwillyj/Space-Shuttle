import discord
from discord import app_commands
import db_interactions as db
import tetrio as tetrio
import challonge_util as challonge
import requests
from discord.app_commands import checks 


import os
from dotenv import load_dotenv

#Setup intents
intents = discord.Intents.default()
intents.message_content = True
intents.members = True

#init client
client = discord.Client(intents=intents)
tree = app_commands.CommandTree(client)
server_id = 953645182975352886
logging_channel = 1358885334565257417


class TETRIOmodal(discord.ui.Modal, title="Register For TETR.IO"):
    name = discord.ui.TextInput(label='Enter Your TETR.IO Username')
    async def on_submit(self, itx: discord.Interaction):
        t_data = await tetrio.get_player_data(self.name.value)
        
        if t_data["success"] == False:
            if t_data["error"]["msg"] == "No such user! | Either you mistyped something, or the account no longer exists.":
                await itx.response.send_message("Registration Failed: No such user! | Either you mistyped something, or the account no longer exists.", ephemeral=True)
            else:
                await itx.response.send_message("Registration Failed: An unknown error occured. Please contact staff", ephemeral=True)
        elif t_data["data"]["tr"] == -1:
            await itx.response.send_message("Registration Failed: You must have a TR on TETR.IO to register for the tournament", ephemeral=True)
        else:
            username = await tetrio.get_player_id(self.name.value)
            message = await db.register_player(itx.user.id,itx.user.name,username,"TETR.IO",t_data["data"]["tr"])
            await itx.response.send_message(message, ephemeral=True)
            logging = client.get_channel(logging_channel)
            await logging.send(message)

class ZBmodal(discord.ui.Modal, title="Register For Zone Battle"):
    score = discord.ui.TextInput(label='Enter Your Zone Battle SR')
    async def on_submit(self, itx: discord.Interaction):
        message = await db.register_player(itx.user.id,itx.user.name,None,"Zone Battle",self.score.value)
        await itx.response.send_message(message, ephemeral=True)
        logging = client.get_channel(logging_channel)
        await logging.send(message)

class CSAmodal(discord.ui.Modal, title="Register For Classic Score Attack"):
    score = discord.ui.TextInput(label='Enter Your Classic Score Attack SR')
    async def on_submit(self, itx: discord.Interaction):
        message = await db.register_player(itx.user.id,itx.user.name,None,"Classic Score Attack",self.score.value)
        await itx.response.send_message(message, ephemeral=True)
        logging = client.get_channel(logging_channel)
        await logging.send(message)

class PPT2modal(discord.ui.Modal, title="Register For Puyo Puyo Tetris 2"):
    score = discord.ui.TextInput(label='Enter Your Puyo Puyo Tetris 2 Rating')
    async def on_submit(self, itx: discord.Interaction):
        message = await db.register_player(itx.user.id,itx.user.name,None,"Puyo Puyo Tetris 2",self.score.value)
        await itx.response.send_message(message, ephemeral=True)
        logging = client.get_channel(logging_channel)
        await logging.send(message)

class PPCmodal(discord.ui.Modal, title="Register For Puyo Puyo Champions"):
    score = discord.ui.TextInput(label='Enter Your Puyo Puyo Champions Rating')
    async def on_submit(self, itx: discord.Interaction):
        message = await db.register_player(itx.user.id,itx.user.name,None,"Puyo Puyo Champions",self.score.value)
        await itx.response.send_message(message, ephemeral=True)
        logging = client.get_channel(logging_channel)
        await logging.send(message)

class GCL_Regsiter(discord.ui.View):
    def __init__(self, *, timeout = None):
        super().__init__(timeout=timeout)

    @discord.ui.button(label="TETR.IO")
    async def reg_tetrio(self, itx: discord.Interaction, button: discord.ui.Button):
        if(await db.check_if_player_registered(itx.user.id,"TETR.IO")):
            message = await db.register_player(itx.user.id,itx.user.name,None,"TETR.IO")
            await itx.response.send_message(message, ephemeral=True)
            logging = client.get_channel(logging_channel)
            await logging.send(message)
        else:
            await itx.response.send_modal(TETRIOmodal())

    @discord.ui.button(label="Zone Battle")
    async def reg_zb(self, itx: discord.Interaction, button: discord.ui.Button):
        if(await db.check_if_player_registered(itx.user.id,"Zone Battle")):
            message = await db.register_player(itx.user.id,itx.user.name,None,"Zone Battle")
            await itx.response.send_message(message, ephemeral=True)
            logging = client.get_channel(logging_channel)
            await logging.send(message)
        else:
            await itx.response.send_modal(ZBmodal())

    @discord.ui.button(label="Classic Score Attack")
    async def reg_csa(self, itx: discord.Interaction, button: discord.ui.Button):
        if(await db.check_if_player_registered(itx.user.id,"Classic Score Attack")):
            message = await db.register_player(itx.user.id,itx.user.name,None,"Classic Score Attack")
            await itx.response.send_message(message, ephemeral=True)
            logging = client.get_channel(logging_channel)
            await logging.send(message)
        else:
            await itx.response.send_modal(CSAmodal())

    @discord.ui.button(label="Puyo Puyo Tetris 2")
    async def reg_ppt2(self, itx: discord.Interaction, button: discord.ui.Button):
        if(await db.check_if_player_registered(itx.user.id,"Puyo Puyo Tetris 2")):
            message = await db.register_player(itx.user.id,itx.user.name,None,"Puyo Puyo Tetris 2")
            await itx.response.send_message(message, ephemeral=True)
            logging = client.get_channel(logging_channel)
            await logging.send(message)
        else:
            await itx.response.send_modal(PPT2modal())

    @discord.ui.button(label="Puyo Puyo Champions")
    async def reg_ppc(self, itx: discord.Interaction, button: discord.ui.Button):
        if(await db.check_if_player_registered(itx.user.id,"Puyo Puyo Champions")):
            message = await db.register_player(itx.user.id,itx.user.name,None,"Puyo Puyo Champions")
            await itx.response.send_message(message, ephemeral=True)
            logging = client.get_channel(logging_channel)
            await logging.send(message)
        else:
            await itx.response.send_modal(PPCmodal())


@tree.command(
        name="open_registrations",
        description="Open registrations for GCL Tournaments",
        guild=discord.Object(id=server_id),
)
@checks.has_role("Big Galactic")
async def open_registration(itx : discord.Interaction):
    if(itx.user.id == 317475187391987713 or itx.user.id == 247221105515823104):
        view = GCL_Regsiter()
        await itx.response.send_message("Click the button for the game you would like to register for",view=view)
    else:
        await itx.response.send_message("You do not have permissions to use this command",ephemeral=True)

@tree.command(
        name="add_tournament",
        description="Add a tournament to the GCL database",
        guild=discord.Object(id=server_id),
)
@checks.has_role("Big Galactic")
async def add_tournament(itx : discord.Interaction,discord_channel_id:str,tournament_url:str,tournament:str,tournament_display_name:str):
    if(itx.user.id == 317475187391987713 or itx.user.id == 247221105515823104):
        message = await db.add_tournament_to_database(int(discord_channel_id),tournament_url,tournament,tournament_display_name)
        await itx.response.send_message(message)

@tree.command(
        name="remove_tournament",
        description="Remove tournament from the GCL database",
        guild=discord.Object(id=server_id),
)
@checks.has_role("Big Galactic")
async def remove_tournament(itx : discord.Interaction,tournament_display_name:str):
    if(itx.user.id == 317475187391987713 or itx.user.id == 247221105515823104):
        message = await db.remove_tournament_from_database(tournament_display_name)
        await itx.response.send_message(message)

@tree.command(
        name="list_tournaments",
        description="List tournaments in the GCL database",
        guild=discord.Object(id=server_id),
)
@checks.has_role("Big Galactic")
async def list_tournaments(itx : discord.Interaction):
    if(itx.user.id == 317475187391987713 or itx.user.id == 247221105515823104):
        message = await db.list_tournaments_in_database()
        await itx.response.send_message(message)

@tree.command(
        name="export_participants",
        description="Export registered participants",
        guild=discord.Object(id=server_id),
)
@checks.has_role("Big Galactic")
async def export_participants(itx : discord.Interaction):
    if(itx.user.id == 317475187391987713 or itx.user.id == 247221105515823104):
        await db.export_participants()
        await itx.response.send_message("Exported participants",file=discord.File("database.csv"))


@tree.command(
        name="refresh_players_from_challonge",
        description="refresh player IDs from challonge",
        guild=discord.Object(id=server_id),
)
@checks.has_role("Big Galactic")
async def refresh_from_challonge(itx : discord.Interaction):
    if(itx.user.id == 317475187391987713 or itx.user.id == 247221105515823104):
        data = await db.get_tournament_information()
        for i in data:
            this_data = await challonge.get_participant_data(i[0])
            print(this_data)
            for ii in this_data:
                print("met")
                await db.set_player_challonge_id(ii[0],i[1],ii[1])
        await itx.response.send_message("Finished")


@tree.command(
        name="refresh_matches",
        description="refresh matches challonge",
        guild=discord.Object(id=server_id),
)
@checks.has_role("Big Galactic")
async def refresh_matches(itx : discord.Interaction):
    if(itx.user.id == 317475187391987713 or itx.user.id == 247221105515823104):
        data = await db.get_tournament_information_for_matches()
        for i in data:
            this_data = await challonge.get_match_data(i[0])
            for ii in this_data:
                state = await db.get_state_of_match(ii[0])
                if (ii[3] == "open" and state is None):
                    textchannel = client.get_channel(i[2])
                    server = client.get_guild(953645182975352886)
                    p1 = await db.get_discord_info_from_challonge_info(ii[1])
                    p2 = await db.get_discord_info_from_challonge_info(ii[2])
                    p1 = p1[0]
                    p2 = p2[0]
                    this_thread = await textchannel.create_thread(name=f"{i[3]} -- {p1[1]} vs {p2[1]}", type=discord.ChannelType.private_thread, auto_archive_duration=10080)
                    
                    id1 = client.get_user(p1[0])
                    id2 = client.get_user(p2[0])
                    await this_thread.add_user(id1)
                    await this_thread.add_user(id2)

                    await db.add_thread_to_db(this_thread.id,ii[0],ii[3],ii[1],ii[2],i[0])
                if (ii[3] == "complete" and state == "open"):
                    print("met")
                    c_id = await db.get_channel_from_match(ii[0])
                    print(c_id)
                    textchannel = client.get_channel(c_id)
                    await textchannel.edit(archived=True, locked=True)
                    await db.end_state_of_match(ii[0])
                    pass #Close Thread and set state to complete
        await itx.response.send_message("Finished")

@tree.command(
        name="submit_score",
        description="Submit score for GCL",
        guild=discord.Object(id=server_id),
)
async def submit_score(itx : discord.Interaction,your_score:int,opponent_score:int):
    res = await db.get_match_info_from_match(itx.channel_id)
    tournament = await db.get_tournament_category_from_url(itx.channel_id)
    print(res)
    your_id = await db.get_challonge_id_from_discord_id_and_tournament(itx.user.id,tournament)
    opp_id = res[2] if res[1] == your_id else res[1]
    winner = your_id if your_score > opponent_score else opp_id if opponent_score > your_score else "tie"
    scores = f"{your_score}-{opponent_score}" if res[1] == your_id else f"{opponent_score}-{your_score}"


    your_name = await db.get_discord_info_from_challonge_info(your_id)
    your_name = your_name[0][1]
    opp_name = await db.get_discord_info_from_challonge_info(opp_id)
    opp_name = opp_name[0][1]
    if(res[4] == "open"):
        await challonge.submit_score(res[3],res[0],scores,winner)
        await itx.response.send_message(f"Submitted score of {your_name if your_id ==res[1] else opp_name} {scores} {your_name if your_id ==res[2] else opp_name}")
    else:
        await itx.response.send_message("This match has already been finalized. Please contact staff if you believe this is in error.")

@tree.command(
        name="refresh_seeding",
        description="Refresh TETR.IO Seeding",
        guild=discord.Object(id=server_id),
)
@checks.has_role("Big Galactic")
async def refresh_seeding(itx : discord.Interaction):
    if(itx.user.id == 317475187391987713 or itx.user.id == 247221105515823104):
        players = await db.get_tetrio_ids()
        msg = await itx.response.send_message("Working...")
        for i in players:
            data = await tetrio.get_player_data(i[0])
            await db.update_tetrio_tr(i[0],data["data"]["tr"])
        await itx.edit_original_response(content="Finished")

@tree.command(
        name="export_seeding",
        description="export seeding for GCL",
        guild=discord.Object(id=server_id),
)
@checks.has_role("Big Galactic")
async def export_seeding(itx : discord.Interaction,tournament:str):
    if(itx.user.id == 317475187391987713 or itx.user.id == 247221105515823104):
        await db.export_seeding(tournament)
        await itx.response.send_message("Exported participants",file=discord.File("seeding.csv"))

@tree.command(
        name="admin_execute_dql",
        description="ADMIN ONLY",
        guild=discord.Object(id=server_id),
)
@checks.has_role("Big Galactic")
async def execute_dql(itx : discord.Interaction,sql:str):
    if(itx.user.id == 317475187391987713 or itx.user.id == 247221105515823104):
        await db.execute_dql(sql)
        await itx.response.send_message("Executed DQL Query",file=discord.File("return.csv"))

@tree.command(
        name="admin_execute_dml",
        description="ADMIN ONLY",
        guild=discord.Object(id=server_id),
)
@checks.has_role("Big Galactic")
async def execute_dml(itx : discord.Interaction,sql:str):
    if(itx.user.id == 317475187391987713):
        await db.execute_dml(sql)
        await itx.response.send_message("Executed DML query")

@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')
    await tree.sync(guild=discord.Object(id=server_id))
    print("commands registered")
client.run(os.getenv("DISCORD_CLIENT_SECRET"))