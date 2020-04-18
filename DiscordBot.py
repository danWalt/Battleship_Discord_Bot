import discord
import settings
import bge

TOKEN = settings.DISCORD_TOKEN
GUILD = settings.DISCORD_GUILD


GAME_START = 'Let The Game Begin!'
INSTRUCTIONS1 = 'A game of battleships is about to begin'
INSTRUCTIONS2 = 'An 8X8 board with 3 ships on it will be created'
INSTRUCTIONS3 = "You'll have to select a row and a coloumn to shot at every " \
                "turn until you sink all 3 ships."
POSSIBLE_MOVES = []
UNKNOWN = 'The message you have sent is not a known order. Please try again.'


# @client.event
async def on_ready():
    print(f'{client.user.name} has connected to Discord!')


# @client.event
async def on_member_join(member):
    await member.create_dm()
    await member.dm_channel.send(
        f"Hi {member.name}, welcome to battle-ships server! Type 'play' to "
        f"start a game"
    )


# @client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content == '!play':
        author = message.author
        await author.create_dm()
        await author.dm_channel.send(GAME_START)
        await author.dm_channel.send(INSTRUCTIONS1)
        await author.dm_channel.send(INSTRUCTIONS2)
        await author.dm_channel.send(INSTRUCTIONS3)


# @client.event
async def game(message):
    if message.author == client.user:
        return
    author = message.author
    while not game.game_over:
        if message in POSSIBLE_MOVES:
            pass
        else:
            await author.dm_channel.send(UNKNOWN)


if __name__ == '__main__':
    client = discord.Client()

    game = bge.start_game()
    board = game.show_board(client)
    on_ready()
    on_member_join(member)
    on_message()


    client.run(TOKEN)
