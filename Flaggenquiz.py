import time
import discord
from discord import app_commands
from discord.ext import commands
from discord.ui import Button, View
from config import token, max_votes
import flaggenerator
from flaggenerator import country_gen
from importlib import reload
import datetime

global started
global id
global name
global skiped

bot = commands.Bot(command_prefix="!", intents = discord.Intents.all())
started = False # Variable die anzeigt ob der der Bot aktiv ist
name = [""] # name des Channels in dem der Bot läuft
id = [""] # id des Channels in dem der Bot läuft
flag_gen = country_gen()
skiped = False


@bot.event
async def on_ready():
    print("flaggenquiz ist Bereit")
    try:
        synced = await bot.tree.sync()
        print (f"synced {len(synced)} command(s)")
    except Exception as e:
        print(e)


#   Commands
@bot.tree.command(name="start", description="Starte das Flaggenquiz in diesem Channel")
async def start(interaction: discord.Interaction):
    channel_id = interaction.channel.id
    channel_name = interaction.channel.name
    global name
    global id
    name = channel_name
    id = channel_id
    global started
    if started == False:

        # button

        button = Button(label="Skip", style=discord.ButtonStyle.green, emoji="⏩")

        async def button_callback(interaction):
            await interaction.response.send_message(f"Das richtige Land währe `{flag_gen.country_name}` gewesen")
            global skiped
            skiped = True
            time.sleep(0.5)
            skiped = False

        button.callback = button_callback
        view = View()
        view.add_item(button)

        #Flaggenquiz 1. Nachricht

        await interaction.response.send_message(f"Flaggenquiz wurde in <#{channel_id}> gestartet!\n Aktuell nur in Englisch")
        started = True
        print(started)
        print(f"https://raw.githubusercontent.com/hampusborgos/country-flags/main/png1000px/{flag_gen.country.lower()}.png")
        channelname = bot.get_channel(id)
        embed = discord.Embed(title="Flaggenquiz")
        embed.set_footer(text=datetime.datetime.now())
        embed.set_image(url=f"https://raw.githubusercontent.com/hampusborgos/country-flags/main/png1000px/{flag_gen.country.lower()}.png")
        await channelname.send(embed=embed, view=view)


    else:
        await interaction.response.send_message(f"Flaggenquiz wurde bereits im channel <#{channel_id}> gestartet")

@bot.tree.command(name="stop", description="Stoppe das Flaggenquiz in diesem Channel")
async def stop(interaction: discord.Interaction):
    global started
    started = False
    channel_id = interaction.channel.id
    await interaction.response.send_message(f"Flaggenquiz wurde in <#{channel_id}> gestopt!")

@bot.event
async def on_message(message):
    if started == True:
        if flag_gen.country_name in message.content:

            # button

            button = Button(label="Skip", style=discord.ButtonStyle.green, emoji="⏩")

            async def button_callback(interaction):
                await interaction.response.send_message(f"Das richtige Land währe {flag_gen.country_name} gewesen")
                global skiped
                skiped = True
                time.sleep(0.5)
                skiped = False

            button.callback = button_callback
            view = View()
            view.add_item(button)

            # Flaggenquiz andere Nachrichten

            await message.add_reaction("👍")
            flag_gen.generate()
            print(f"https://raw.githubusercontent.com/hampusborgos/country-flags/main/png1000px/{flag_gen.country.lower()}.png")
            channelname = bot.get_channel(id)
            embed = discord.Embed(title="Flaggenquiz")
            embed.set_footer(text=datetime.datetime.now())
            embed.set_image(url=f"https://raw.githubusercontent.com/hampusborgos/country-flags/main/png1000px/{flag_gen.country.lower()}.png")
            await channelname.send(embed=embed, view=view)
            #print(country, country_name)
        else:
            if message.author == bot.user:
                return
            else:
                print(message.channel.id, id)
                if message.channel.id == id:
                    await message.add_reaction("👎")

bot.run(token)