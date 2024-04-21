#pip install discord.py
from discord.ext import commands
import discord

class leaderBoardUtility:
    REPLAY_FILE_TYPE  = ""
    CONFIG_FILE       = ""
    BOT_TOKEN         = ""
    CHANNEL_ID        = 0
    NEW_PLAYER_RATING = 0
    replayData        = []

    def __init__(self, CONFIG_FILE):
        self.CONFIG_FILE = CONFIG_FILE
        self.loadConfigFile()
        
    def loadConfigFile(self):
        file       = open(self.CONFIG_FILE, 'r')
        fileData   = file.readlines()
        file.close()
        
        BOT_TOKEN  = fileData[0].strip("\n").split("=")
        CHANNEL_ID = fileData[1].strip("\n").split("=")
        FILE_TYPE  = fileData[2].strip("\n").split("=")
        NEW_PLAYER_RATING = fileData[3].strip("\n").split("=")
        
        for data in fileData:
            data = data.strip("\n").split("=")
            if   data[0].strip(" ") == "BOT_TOKEN":
                self.BOT_TOKEN  = data[1].strip(" ")
            elif data[0].strip(" ") == "CHANNEL_ID":
                self.CHANNEL_ID  = int(data[1].strip(" "))
            elif data[0].strip(" ") == "REPLAY_FILE_TYPE":
                self.REPLAY_FILE_TYPE  = data[1].strip(" ")
            elif data[0].strip(" ") == "NEW_PLAYER_RATING":
                self.NEW_PLAYER_RATING  = data[1].strip(" ")

    def setReplayData(self, replayData):
        self.replayData = replayData


if __name__ == "__main__":
    CONFIG_FILE = "C:/Users/Newbi/Desktop/config.txt"
    utils = leaderBoardUtility(CONFIG_FILE)
    bot   = commands.Bot(command_prefix="!", intents=discord.Intents.all())
    @bot.event
    async def on_ready():
        channel = bot.get_channel(utils.CHANNEL_ID)
        await channel.send("Bot is ready!")

    @bot.event
    async def on_message(message):
        msg = str(message.content)
        if msg == "!submit":
            if len(message.attachments) > 0:
                for attachment in message.attachments:
                    if attachment.content_type == utils.REPLAY_FILE_TYPE:
                        print("success")
                        #utils.setReplayData( await attachment.read() )
                        await attachment.save("C:/Users/Newbi/Downloads/temp/" + attachment.filename)
            else:
                channel = bot.get_channel(utils.CHANNEL_ID)
                await channel.send("You didn't submit anything!")
        elif msg == "!exit":
            exit()



    bot.run(utils.BOT_TOKEN)