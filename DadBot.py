import re
from random import shuffle
import discord
#permissions 201329664

bot = discord.Client()

@bot.event
async def on_ready():
    print('Bot ready!')
    print(bot.user.name)
    print('-------')

@bot.event
async def on_guild_join(guild):
    await guild.system_channel.send("Hi "+guild.name+", I'm DadBot!")

names = ["DadBot"]*20

@bot.event
async def on_message(message):
    try:
        if message.author == message.guild.me:
            return
        if not message.guild.me.top_role.permissions.manage_nicknames:
            await message.channel.send(
                "Some twat named "+message.guild.owner.display_name+" won't let me change names.")
            return
        if message.author.top_role > message.guild.me.top_role:
            if message.author == message.guild.owner:
                await message.channel.send(
                    "Some twat named "+message.author.display_name+
                    " won't let me change their name.")
            else:
                await message.channel.send(
                    "Some twat named "+message.author.display_name+
                    " won't let me change their name."
                    " (It might be "+message.guild.owner.display_name+"'s fault)")
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
        await message.author.edit(nick=word, reason="DadBot")

    except Exception as exc:
        print(repr(exc))
        await message.channel.send(
            "Something went wrong. It is probably "+message.author.display_name+"'s fault.")

bot.run(open("TOKEN", "r").read().rstrip())
