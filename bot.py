#!/usr/bin/env python3

# a simple discord bot

import discord
import asyncio
import re
import random

# read .env as a dictionary, with an = as the separator
dotenv = ""
with open('.env') as f:
    dotenv = dict(line.strip().split('=') for line in f)

# set token and prefix from dotenv
token = dotenv["TOKEN"]
prefix = dotenv["PREFIX"]

# create a discord client
client = discord.Client()

# on ready, print the bot's username
@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')

# on message, respond to the user
@client.event
async def on_message(message):
    # if the message is from the bot, ignore it
    if message.author == client.user:
        return

    channel = message.channel
    author = message.author
    content = message.content
    
    # if the message starts with the prefix and in the bots channel
    if message.content.startswith(prefix) and (channel.name == "bots" or channel.name == "bot-channel" or channel.name == "bot" or channel.name == "spam"):
        # get the command and arguments
        command = message.content[len(prefix):].split(' ')[0]
        args = message.content[len(prefix):].split(' ')[1:]

        if command == "oofs" or command == "oofcount":
            with open("oof.txt") as f:
                await channel.send("oof count: " + f.read())
        
        if command == "leaderboard":
            with open("oof_leaderboard.txt") as f:
                await channel.send(("oof leaderboard: \n**" + f.read().replace("\n", "\n**").replace(":", "** — ").replace("\n**\n", "") + "**").replace("****", ""))
        
    # if the message contains an "oof", add one to the oof counter file oof.txt
    if "oof" in message.content.lower() and not content.startswith(prefix):
        oofs = re.findall("oof", message.content.lower())
        if len(oofs) > 0:
            oofcount = 0
            with open("oof.txt", "r") as f:
                oofcount = int(f.read())
            oofcount += len(oofs)
            with open("oof.txt", "w") as f:
                f.write(str(oofcount))
            if channel.name == "bots" or channel.name == "bot-channel" or channel.name == "bot" or channel.name == "spam":
                if len(oofs) == 1:
                    await channel.send("+1 oof")
                else:
                    await channel.send("+" + str(len(oofs)) + " oofs")
        # update the oof leaderboard
        leaderboard = get_oof_leaderboard()
        try:
            leaderboard[author.name+"#"+author.discriminator] = int(leaderboard[author.name+"#"+author.discriminator]) + len(oofs)
        except KeyError:
            leaderboard[author.name+"#"+author.discriminator] = len(oofs)
        set_oof_leaderboard(leaderboard)
    
def get_oof_leaderboard():
    # returns oof leaderboard as dict
    with open("oof_leaderboard.txt") as f:
        return dict(line.strip().split(':') for line in f)

def set_oof_leaderboard(board):
    # sets oof leaderboard from dict
    with open("oof_leaderboard.txt", "w") as f:
        # make sure to sort by oofs
        for key, value in sorted(board.items(), key=lambda x: int(x[1]), reverse=True):
            f.write(key + ":" + str(value) + "\n")

# run the bot
client.run(token)