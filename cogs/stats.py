import os
import discord
import requests
from datetime import datetime
from discord.ext import commands


class Rank(discord.ui.View):
    def __init__(self, index, events, number, author):
        super().__init__()
        self.index = index
        self.events = events
        self.number = number
        self.author = author

    @discord.ui.button(label='⬅️', style=discord.ButtonStyle.blurple)
    async def left(self, button: discord.ui.Button, interaction: discord.Interaction):
        self.index -= 1
        if self.index < 0:
           self.index += 1
           button.disabled = True
        else:
            for child in self.children:
                child.disabled = False
        embed = discord.Embed(title=f"Team {self.number.upper()} Rankings", timestamp=datetime.utcnow(), color=0x00FF00)
        embed.add_field(name="Tournament", value=self.events[self.index]['tournament'], inline=False)
        embed.add_field(name="Rank", value=self.events[self.index]["rank"], inline=True)
        embed.add_field(name="W-L-T", value=self.events[self.index]["wlt"], inline=True)
        embed.add_field(name="Win Points", value=self.events[self.index]["wp"], inline=True)
        embed.add_field(name="Autonomous Points", value=self.events[self.index]["ap"], inline=True)
        embed.add_field(name="Strength Points", value=self.events[self.index]["sp"], inline=True)   
        await interaction.message.edit(embed=embed, view=self)

    @discord.ui.button(label='➡️', style=discord.ButtonStyle.blurple)
    async def right(self, button: discord.ui.Button, interaction: discord.Interaction):
        self.index += 1
        if self.index > (len(self.events) - 1):
           self.index -= 1
           button.disabled = True
        else:
            for child in self.children:
                child.disabled = False
        embed = discord.Embed(title=f"Team {self.number.upper()} Rankings", timestamp=datetime.utcnow(), color=0x00FF00)
        embed.add_field(name="Tournament", value=self.events[self.index]['tournament'], inline=False)
        embed.add_field(name="Rank", value=self.events[self.index]["rank"], inline=True)
        embed.add_field(name="W-L-T", value=self.events[self.index]["wlt"], inline=True)
        embed.add_field(name="Win Points", value=self.events[self.index]["wp"], inline=True)
        embed.add_field(name="Autonomous Points", value=self.events[self.index]["ap"], inline=True)
        embed.add_field(name="Strength Points", value=self.events[self.index]["sp"], inline=True)   
        await interaction.message.edit(embed=embed, view=self)
    
    async def interaction_check(self, interaction: discord.Interaction) -> bool:
        if interaction.user == self.author:
            return True
        else:
            await interaction.response.send_message('This button isn\'t for you!', ephemeral=True)
            return False

class Skills(discord.ui.View):
    def __init__(self, index, events, number, author):
        super().__init__()
        self.index = index
        self.events = events
        self.number = number
        self.author = author

    @discord.ui.button(label='⬅️', style=discord.ButtonStyle.blurple)
    async def left(self, button: discord.ui.Button, interaction: discord.Interaction):
        self.index -= 1
        if self.index < 0:
           self.index += 1
           button.disabled = True
        else:
            for child in self.children:
                child.disabled = False
        embed = discord.Embed(title=f"Team {self.number.upper()} Skills", timestamp=datetime.utcnow(), color=0x00FF00)
        embed.add_field(name='Tournament', value=self.events[self.index]["tournament"], inline=False)
        embed.add_field(name='Type', value=(self.events[self.index]["type"]).capitalize(), inline=False)
        embed.add_field(name="Rank", value=self.events[self.index]["rank"], inline=True)
        embed.add_field(name="Score", value=self.events[self.index]["score"], inline=True)
        embed.add_field(name="Attempts", value=self.events[self.index]["attempts"], inline=True)
        await interaction.message.edit(embed=embed, view=self)

    @discord.ui.button(label='➡️', style=discord.ButtonStyle.blurple)
    async def right(self, button: discord.ui.Button, interaction: discord.Interaction):
        self.index += 1
        if self.index > (len(self.events) - 1):
           self.index -= 1
           button.disabled = True
        else:
            for child in self.children:
                child.disabled = False
        embed = discord.Embed(title=f"Team {self.number.upper()} Skills", timestamp=datetime.utcnow(), color=0x00FF00)
        embed.add_field(name='Tournament', value=self.events[self.index]["tournament"], inline=False)
        embed.add_field(name='Type', value=(self.events[self.index]["type"]).capitalize(), inline=False)
        embed.add_field(name="Rank", value=self.events[self.index]["rank"], inline=True)
        embed.add_field(name="Score", value=self.events[self.index]["score"], inline=True)
        embed.add_field(name="Attempts", value=self.events[self.index]["attempts"], inline=True)
        await interaction.message.edit(embed=embed, view=self)

    async def interaction_check(self, interaction: discord.Interaction) -> bool:
        if interaction.user == self.author:
            return True
        else:
            await interaction.response.send_message('This button isn\'t for you!', ephemeral=True)
            return False

class Stats(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.notfound = "Team not found!"
        self.endpoint = 'https://www.robotevents.com/api/v2/'
        self.auth = {"Authorization": f"Bearer {os.getenv('RETOKEN')}", "accept": "application/json"}

    @commands.command(name='team', help='Get team information!')
    async def team(self, ctx, number):
        info = (requests.get(self.endpoint + f'teams?number%5B%5D={number.upper()}&myTeams=false', headers=self.auth)).json()
        if info["data"] == []:
            return await ctx.send(self.notfound)
        embed = discord.Embed(title=f'Team {number.upper()}', timestamp=datetime.utcnow(), color=0x00FF00)
        embed.add_field(name='Team Name', value=info["data"][0]['team_name'], inline=True)
        embed.add_field(name='Grade', value=info["data"][-1]["grade"], inline=True)
        embed.add_field(name='Organization', value=info["data"][0]['organization'], inline=False)
        location = info["data"][0]['location']
        embed.add_field(name='Location', value=f"{location['city']}, {location['region']} {location['postcode']}", inline=True)
        await ctx.send(embed=embed)

    @commands.command(name='skills', help='Get a team\'s skills stats!')
    async def skills(self, ctx, number):
        team = (requests.get(self.endpoint + f'teams?number%5B%5D={number.upper()}&myTeams=false', headers=self.auth)).json()
        if team["data"] == []:
            return await ctx.send(self.notfound)
        else:
            num = team["data"][0]["id"]
        info = (requests.get(self.endpoint + f'teams/{num}/skills', headers=self.auth)).json()
        if info["data"] == []:
            return await ctx.send("This team has no skills stats!")
        events = []
        for event in info["data"]:
            events.append({"tournament": event["event"]["name"], "type": event["type"], "rank": event['rank'], "score": event["score"], "attempts": event["attempts"]})
        index = len(events) - 1
        embed = discord.Embed(title=f"Team {number.upper()} Skills", timestamp=datetime.utcnow(), color=0x00FF00)
        embed.add_field(name='Tournament', value=events[index]["tournament"], inline=False)
        embed.add_field(name='Type', value=(events[index]["type"]).capitalize(), inline=False)
        embed.add_field(name="Rank", value=events[index]["rank"], inline=True)
        embed.add_field(name="Score", value=events[index]["score"], inline=True)
        embed.add_field(name="Attempts", value=events[index]["attempts"], inline=True)
        arrows = Skills(index, events, number, ctx.author)
        await ctx.send(embed=embed, view=arrows)

    @commands.command(name='awards', help='Get a list of a team\'s awards!')
    async def awards(self, ctx, number):
        def find(lst: list, key):
            for i, dic in enumerate(lst):
                if dic["name"] == key:
                    return i
            return -1
        team = (requests.get(self.endpoint + f'teams?number%5B%5D={number.upper()}&myTeams=false', headers=self.auth)).json()
        if team["data"] == []:
            return await ctx.send(self.notfound)
        else:
            num = team["data"][0]["id"]
        info = (requests.get(self.endpoint + f'teams/{num}/awards', headers=self.auth)).json()
        if info["data"] == []:
            return await ctx.send("This team has no awards!")
        awards = []
        for award in info["data"]:
            ind = find(awards, award["event"]["name"])
            if ind != -1:
                awards[ind]["awards"] += f"\n{award['title']}"
            else:
                awards.append({"name": award["event"]["name"], "awards": award['title']})
        if len(awards) > 2:
            awards = awards[-2:]
        embed = discord.Embed(title=f"Team {number.upper()} Awards", timestamp=datetime.utcnow(), color=0x00FF00)
        for award in awards:
            embed.add_field(name=award["name"], value=award["awards"])
        await ctx.send(embed=embed)

    @commands.command(name='rank', help='Get a team\'s most recent ranking!')
    async def rank(self, ctx, number):
        team = (requests.get(self.endpoint + f'teams?number%5B%5D={number.upper()}&myTeams=false', headers=self.auth)).json()
        if team["data"] == []:
            return await ctx.send(self.notfound)
        else:
            num = team["data"][0]["id"]
        info = (requests.get(self.endpoint + f'teams/{num}/rankings', headers=self.auth)).json()
        if info["data"] == []:
            return await ctx.send("This team has no rankings!")
        embed = discord.Embed(title=f"Team {number.upper()} Rankings", timestamp=datetime.utcnow(), color=0x00FF00)
        events = []
        for event in info["data"]:
            events.append({"tournament": event["event"]["name"], "rank": event["rank"], "wlt": f"{event['wins']}-{event['losses']}-{event['ties']}", "wp": event["wp"], "ap": event["ap"], "sp": event["sp"]})
        events = events[::-1]
        index = len(events) - 1
        embed.add_field(name="Tournament", value=events[index]['tournament'], inline=False)
        embed.add_field(name="Rank", value=events[index]["rank"], inline=True)
        embed.add_field(name="W-L-T", value=events[index]["wlt"], inline=True)
        embed.add_field(name="Win Points", value=events[index]["wp"], inline=True)
        embed.add_field(name="Autonomous Points", value=events[index]["ap"], inline=True)
        embed.add_field(name="Strength Points", value=events[index]["sp"], inline=True)
        arrows = Rank(index, events, number, ctx.author)
        await ctx.send(embed=embed, view=arrows)

    async def cog_command_error(self, ctx, error):
        await ctx.send(f"**`ERROR in {os.path.basename(__file__)}:`** {type(error).__name__} - {error}")

def setup(bot):
    bot.add_cog(Stats(bot))