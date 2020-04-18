import discord
from discord.ext.commands import Bot
from discord.ext import commands
import settings
import bge

GAME = bge.start_game()
TOKEN = settings.DISCORD_TOKEN
GUILD = settings.DISCORD_GUILD
BOARD = GAME.show_board()

Client = discord.Client()

bot_prefix = "^"

bot = commands.Bot(command_prefix=bot_prefix)

GAME_START = 'Let The Game Begin!'
INSTRUCTIONS1 = 'A game of battleships is about to begin'
INSTRUCTIONS2 = 'An 8X8 board with 3 ships on it will be created'
INSTRUCTIONS3 = "You'll have to select a row and a column to shot at every " \
                "turn until you sink all 3 ships."


@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')


@bot.event
async def on_member_join(member):
    await member.create_dm()
    await member.dm_channel.send(
        f"Hi {member.name}, welcome to battle-ships server! Type '^play' to "
        f"start a game"
    )


@bot.command()
async def start_game(ctx):
    author = ctx.message.author
    if author == bot.user:
        return

    await author.create_dm()
    await ctx.author.dm_channel.send(GAME_START)
    await ctx.author.dm_channel.send(INSTRUCTIONS1)
    await ctx.author.dm_channel.send(INSTRUCTIONS2)
    await ctx.author.dm_channel.send(INSTRUCTIONS3)
    for row in BOARD:
        await ctx.author.dm_channel.send(row)


@bot.command()
async def shoot(ctx, row: int, column: int):
    author = ctx.message.author
    if author == bot.user:
        return
    await ctx.author.dm_channel.send(GAME.shoot(row, column))
    for row in BOARD:
        await ctx.author.dm_channel.send(row)
    g_on = GAME.check_victory()
    if GAME.game_over:
        await ctx.author.dm_channel.send(g_on)
        await bot.close()
    else:
        await ctx.author.dm_channel.send(g_on)


@bot.command()
async def stats(ctx):
    author = ctx.message.author
    if author == bot.user:
        return
    stats = GAME.game_stats()
    for stat in stats:
        await ctx.author.dm_channel.send(stat)

@bot.command()
async def info(ctx):
    embed = discord.Embed(title="Battle Ships Bot",
                          description="a bot the lets you play the Battle "
                                      "Ships game in a DM channel in Discord",
                          color=0xeee657)

    # give info about you here
    embed.add_field(name="Daniel Walters", value="<Kishkashta>")

    # Shows the number of servers the bot is member of.
    embed.add_field(name="Server count", value=f"{len(bot.guilds)}")

    # give users a link to invite this bot to their server
    embed.add_field(name="Invite",
                    value="<https://discordapp.com/api/oauth2/authorize?client_id=700061008693166229&permissions=0&scope=bot>")

    await ctx.send(embed=embed)

bot.remove_command('help')

@bot.command()
async def help(ctx):
    embed = discord.Embed(title="Battle Ships Bot",
                          description="a bot the lets you play the Battle "
                                      "Ships game in a DM channel in Discord",
                          color=0xeee657)

    embed.add_field(name="^start_game", value="bot creates a dm channel and "
                                              "starts a battle ship game",
                    inline=False)
    embed.add_field(name="^shoot X Y", value="Bot shoots the given "
                                             "coordinates", inline=False)
    embed.add_field(name="^stats", value="Gives stats about current game, "
                                         "number of turns, hits and misses",
                    inline=False)
    embed.add_field(name="^info", value="Gives a little info about the bot",
                    inline=False)
    embed.add_field(name="^help", value="Gives this message", inline=False)

    await ctx.send(embed=embed)

# todo maybe add board printing in a seperate function
def board():
    pass


bot.run(TOKEN)