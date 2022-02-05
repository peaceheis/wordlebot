import random
from asyncio.tasks import _GatheringFuture 

import discord
import discord.ext.commands
from discord.ext.commands import core

GREEN_SQUARE = ":green_square:"
YELLOW_SQUARE = ":yellow_square:"
BLACK_SQUARE = ":black_large_square:"

CORRECT = (GREEN_SQUARE*5)

bot = discord.ext.commands.Bot(command_prefix='?', description="Wordle bot!")

bot.game_active = False
bot.word = ""
bot.current_user = None
bot.turn = 0

f = open("fixed.txt", "r")

words = list(set([word.removesuffix("\n") for word in f.readlines()]))

@bot.event
async def on_ready():
    print('We have logged in as {0.user}'.format(bot))

async def wordle_begin(message): 
    await message.channel.send(f'New Wordle game created by {message.author.mention}!')
    bot.word = words[random.randint(0, len(words) - 1)]
    await message.channel.send("Word chosen!")
    print(f"game started and word chosen: {bot.word}")

async def decode_guess(word, guess):
    if len(guess) != 5:
        return("Improper length!")

    bot.turn += 1

    word = [letter for letter in word]
    message = ""
    for i in range(5): 
        correct_letter = word[i]
        guess_letter = guess[i]
        print(guess_letter, correct_letter)
        if correct_letter == guess_letter: 
            message += GREEN_SQUARE
            word[i] = ""
        elif guess_letter in word: 
            message += YELLOW_SQUARE
            word[word.index(guess_letter)] = ""
        else: 
            message += BLACK_SQUARE

    if message == CORRECT: 
        bot.game_active = False
        turn = bot.turn
        bot.turn = 0
        return message + f"\nYou won with {turn}/6!"

    elif bot.turn >= 6: 
        bot.turn = 0
        return message + "\n6/6, Game over!"
    return message        


@bot.event
async def on_message(message: discord.message):
    if message.author == bot.user:
        return

    if bot.game_active: 
        if message.content.lower() in ["end game", "end", "bye", "kthxbye"]: 
            bot.turn = 0
            bot.game_active = False
            await message.channel.send(f"{message.author.mention} has ended game!")

        if message.content.startswith('$wordle'):
            await message.channel.send("Game active! Please wait.")
            return
        

        if bot.current_user == message.author:
            guess = message.content
            await message.channel.send(await decode_guess(bot.word, guess))
    else: 
        if not message.content.startswith('$wordle'):
            return
        bot.game_active = True
        bot.current_user = message.author
        await wordle_begin(message)






bot.run('TOKEN')