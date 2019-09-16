import re
from random import shuffle
import discord
import pickle
import os
#permissions 201329664

bot = discord.Client()

names = ["somthing went wrong"]

@bot.event
async def on_ready():
    global names
    print('Bot ready!')
    print(bot.user.name)
    print('-------')
    if os.path.exists('names.p'):
        names = pickle.load(open("names.p", "rb"))
    else:
        names = ["DadBot"]*20


@bot.event
async def on_guild_join(guild):
    await guild.system_channel.send("Hi "+guild.name+", I'm DadBot!")


@bot.event
async def on_message(message):
    global names
    try:
        if message.author == message.guild.me:
            return

        word = re.search(r'\bi\'?m\s+(.*)', message.content, re.IGNORECASE)
        if word is None:
            return
        if len(word.group(1)) > 32:
            word = re.search(r'\bi\'?m\s+(\w+)', message.content, re.IGNORECASE)
        word = word.group(1)
        if len(word) > 32:
            word = '<LONG DADJOKE>'

        shuffle(names)
        await message.channel.send("Hi "+word+", I'm " + names.pop() + "!")
        names.append(word)
        pickle.dump(names, open("names.p", "wb"))

        MAYCHANGENAMES = False

        if MAYCHANGENAMES:
            if not message.guild.me.top_role.permissions.manage_nicknames:
                await message.channel.send(
                    "Somebody named "+message.guild.owner.display_name+" won't let me change names.")
                return
            if message.author.top_role > message.guild.me.top_role:
                if message.author == message.guild.owner:
                    await message.channel.send(
                        "Somebody named "+message.author.display_name+
                        " won't let me change their name.")
                else:
                    await message.channel.send(
                        "Somebody named "+message.author.display_name+
                        " won't let me change their name."
                        " (It might be "+message.guild.owner.display_name+"'s fault)")
                return
            await message.author.edit(nick=word, reason="DadBot")

    except Exception as exc:
        print(repr(exc))
        await message.channel.send(
            "Something went wrong. It is probably "+message.author.display_name+"'s fault.")

bot.run(open("TOKEN", "r").read().rstrip())
