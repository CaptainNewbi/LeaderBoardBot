#pip install discord.py
from discord.ext import commands
import discord
import leaderBoardUtility as lbu

if __name__=="__main__":
    # Initialize variables 
    lbUtils = lbu.leaderBoardUtility()

    # Set up and run the bot
    bot   = commands.Bot(command_prefix="!", intents=discord.Intents.all())

    @bot.event
    async def on_ready():
        channel = bot.get_channel(lbUtils.CHANNEL_ID)
        await channel.send("Bot is ready!")

    @bot.command()
    async def challenge(ctx, name):
        name = name[2:-1:1]     
        challenger = ctx.author
        riskTaker = bot.get_user( int(name) )
        lbUtils.createChallenge(int(challenger.id) , int(riskTaker.id))

    @bot.command()
    async def accept(ctx):
        riskTaker = ctx.author
        lbUtils.acceptChallenge(int(riskTaker.id))

    @bot.command()
    async def winner(ctx):
        winner = ctx.author
        lbUtils.reportWinner(int(winner.id))
        
    @bot.command()
    async def loser(ctx):
        loser = ctx.author
        lbUtils.reportLoser(int(loser.id))
        
#######################################################################################
# Code left for reference, download or read files from chat to parse for info
#######################################################################################
#    @bot.event
#    async def on_message(message):
#        msg = str(message.content)
#        if msg == "!submit":
#            if len(message.attachments) > 0:
#                for attachment in message.attachments:
#                    if attachment.content_type == lbUtils.REPLAY_FILE_TYPE:
#                        print("success")
#                        #lbUtils.setReplayData( await attachment.read() )
#                        await attachment.save("C:/Users/Newbi/Downloads/temp/" + attachment.filename)
#            else:
#                channel = bot.get_channel(lbUtils.CHANNEL_ID)
#                await channel.send("You didn't submit anything!")
#        elif msg == "!exit":
#            exit()

    bot.run(lbUtils.BOT_TOKEN)