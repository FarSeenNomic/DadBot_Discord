import re
from random import shuffle
import discord
import pickle
import os
#permissions 201329664

bot = discord.Client()

names = ["somthing went wrong"]

optIN = {}
optOut = {}

@bot.event
async def on_ready():
    global names
    global optIN
    print('Bot ready!')
    print(bot.user.name)
    print('-------')
    if os.path.exists('names.p'):
        names = pickle.load(open("names.p", "rb"))
    else:
        names = ["DadBot"]*20

    if os.path.exists('optIN.p'):
        optIN = pickle.load(open("optIN.p", "rb"))
    else:
        optIN = {}

    if os.path.exists('optOut.p'):
        optOut = pickle.load(open("optOut.p", "rb"))
    else:
        optOut = {}


@bot.event
async def on_guild_join(guild):
    await guild.system_channel.send("Hi "+guild.name+", I'm DadBot!")


@bot.event
async def on_message(message):
    global names
    global optIN
    global optOut
    try:
        if message.author == message.guild.me:
            return

        if lower(message.content) == "optin":
            if not optIN.get(message.author.id, False):
                if not message.guild.me.top_role.permissions.manage_nicknames:
                    await message.channel.send("I cannot change nicknames, but I'll put you on the list.")
                elif message.author.top_role > message.guild.me.top_role:
                    await message.channel.send("You outrank me, but I'll put you on the list.")
                optIN[message.author.id] = True
                pickle.dump(optIN, open("optIN.p", "wb"))

                optOut[message.author.id] = message.author.display_name
                pickle.dump(optOut, open("optOut.p", "wb"))
            return

        if lower(message.content) == "optout":
            if optIN.get(message.author.id, False):
                optIN.pop(message.author.id)
                pickle.dump(optIN, open("optIN.p", "wb"))
                if optIN[message.author.id] != message.author.display_name:
                    await message.author.edit(nick=optOut[message.author.id], reason="DadBot")
            return

        word = re.search(r'\bi\'?m\s+(.*)', message.content, re.IGNORECASE)
        if word is None:
            return
        if len(word.group(1)) > 32:
            word = re.search(r'\bi\'?m\s+(\w+)', message.content, re.IGNORECASE)
        word = word.group(1)

        if lower(word) == lower("DadBot"):
            await message.channel.send("Wait, you're me?")
            return

        if lower(word) == lower("Dad"):
            await message.channel.send("Wait, you're me?")
            return

        shuffle(names)
        await message.channel.send("Hi "+word+", I'm " + names.pop() + "!")
        names.append(word)
        pickle.dump(names, open("names.p", "wb"))

        if optIN.get(message.author.id, False):
            if not message.guild.me.top_role.permissions.manage_nicknames:
                #await message.channel.send(
                #    "Somebody named "+message.guild.owner.display_name+" won't let me change names.")
                return
            if message.author.top_role > message.guild.me.top_role:
                #if message.author == message.guild.owner:
                #    await message.channel.send(
                #        "Somebody named "+message.author.display_name+
                #        " won't let me change their name.")
                #else:
                #    await message.channel.send(
                #        "Somebody named "+message.author.display_name+
                #        " won't let me change their name."
                #        " (It might be "+message.guild.owner.display_name+"'s fault)")
                return
            if len(word) > 32:
                word = word[:27] + "..."
            await message.author.edit(nick=word, reason="DadBot")

    except Exception as exc:
        print(repr(exc))
        await message.channel.send(
            "Something went wrong. It is probably "+message.author.display_name+"'s fault.")

bot.run(open("TOKEN", "r").read().rstrip())
