import os
class leaderBoardUtility():
    #######################################################################################
    # Member Variables
    #######################################################################################
    
    # Ladder related variables
    playerNames    = []
    playerIds      = []
    playerRatings  = []

    challenges     = []

    fileName       = "LeaderBoard.txt"
    
    winnerName     = ""
    loserName      = ""

    NEW_PLAYER_RATING = 0
    
    # Bot related variables
    REPLAY_FILE_TYPE  = ""
    BOT_TOKEN         = ""
    CHANNEL_ID        = 0
    NEW_PLAYER_RATING = 0
    
    #######################################################################################
    # Initialization Function
    #######################################################################################
    def __init__(self):        
        self.loadLeaderBoard()
        self.loadConfigFile()
        
    #######################################################################################
    # Load Configuration Data
    #######################################################################################
    def loadConfigFile(self):
        file       = open("./config.txt", 'r')
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
                
    #######################################################################################
    # Get the player's rating
    #######################################################################################
    def getPlayersRating(self, playerName):

        for i in range(len(self.playerRatings)):
            
            if playerName == self.playerNames[i]:

                return int(self.playerRatings[i]), i

        # If player not found, add new player and return default rating
        self.playerNames.append(playerName)
        self.playerRatings.append(self.NEW_PLAYER_RATING)
        return self.NEW_PLAYER_RATING, len(self.playerRatings)-1

    #######################################################################################
    # Find the expected probability to win the game based on rating
    #######################################################################################
    def expectedProbability(self, differenceInPlayerRating):
        SCALE_FACTOR  = 400.0
        EXPONENT_BASE = 10.0
    
        return (1.0 / ( 1.0 + pow(EXPONENT_BASE, differenceInPlayerRating/SCALE_FACTOR) ) )

    #######################################################################################
    # Update each players Rating
    #######################################################################################
    def updateRatings(self):
        # Kfactor normally is 32, but can change based on ratings if desired, example below
        # Players below 2100: K-factor of 32 used
        # Players between 2100 and 2400: K-factor of 24 used
        # Players above 2400: K-factor of 16 used.

        K_FACTOR     = 32.0
        WINNER_SCORE = 1.0
        LOSER_SCORE  = 0.0
        
        winnerRating, winnerIdx = self.getPlayersRating(self.winnerName)
        loserRating,  loserIdx  = self.getPlayersRating(self.loserName)
        
        expectedProbToWin       = self.expectedProbability( loserRating  - winnerRating )
        expectedProbToLose      = self.expectedProbability( winnerRating - loserRating )

        self.playerRatings[winnerIdx] = (winnerRating + round(K_FACTOR*( WINNER_SCORE - expectedProbToWin  ) ) )
        self.playerRatings[loserIdx]  = (loserRating  + round(K_FACTOR*( LOSER_SCORE  - expectedProbToLose ) ) )

    #######################################################################################
    # Load leaderboard from txt file
    #######################################################################################
    def loadLeaderBoard(self):
        # If file exists, read it
        if os.path.isfile(".\LeaderBoard.txt"):
            file     = open(".\LeaderBoard.txt", 'r')
            fileData = file.read()

            file.close()

            fileData = fileData.replace("\n", "")
            fileData = fileData.replace(" ", "")
            fileData = fileData.split(",")

            # Strip off the empty elements due to empty new lines in file
            while fileData[-1] == "":
                fileData = fileData[:-1]

            # If the file is not empty, populate member data
            for idx in range(0, len(fileData), 3):
                self.playerNames.append(fileData[idx])
                self.playerIds.append(int(fileData[idx+1]))
                self.playerRatings.append(int(fileData[idx+2]))
                
        # If the file does not exist, make one in default directory
        else:
            file = open("LeaderBoard.txt", "w")
            file.write("default, 0")
            file.close()

    #######################################################################################
    # Save leaderboard to text file
    #######################################################################################
    def saveLeaderBoard(self):
        data = ""
        for i in range(len(self.playerRatings)):
            if self.playerNames[i] != "default":
                data = data + self.playerNames[i] + "," + str(self.playerRatings[i]) + ",\n" 

        file = open(".\LeaderBoard.txt", 'w')
        file.write(data)
        file.close()
        return 0
        
    #######################################################################################
    # Create a challenge
    #######################################################################################
    def createChallenge(self, challengerId, riskTakerId):
        #  Challenger, riskerTaker, accepted, Challenger Reported, riskerTaker Reported
        
        challengeAccepted  = False
        
        challengerReported = False
        challengerResult   = "null"
        
        riskTakerReported  = False
        riskTakerResult    = "null"
        
        self.challenges.append([challengerId, riskTakerId, challengeAccepted, \
                                challengerReported, challengerResult,         \
                                riskTakerReported,  riskTakerResult])
     
    #######################################################################################
    # Accept a challenge
    #######################################################################################
    def acceptChallenge(self, riskTakerId):
        for openChallenges in self.challenges:
            if riskTakerId == openChallenges[1]:
                openChallenges[2] = True
        
    #######################################################################################
    # Report Winner
    #######################################################################################
    def reportWinner(self, winnerId):
        for openChallenges in self.challenges:
            if  ((winnerId == openChallenges[0]) and (openChallenges[2] == True)):
                openChallenges[3] = True
                openChallenges[4] = "Win"
            elif ((winnerId == openChallenges[1]) and (openChallenges[2] == True)):
                openChallenges[5] = True
                openChallenges[6] = "Win"
            if (openChallenges[3] == openChallenges[5]):
                print("Update Leaderboard")
                print("Delete Challenge")

    #######################################################################################
    # Report Loser
    #######################################################################################
    def reportLoser(self, loserId):
        for openChallenges in self.challenges:
            if   ((loserId == openChallenges[0]) and (openChallenges[2] == True)):
                openChallenges[3] = True
                openChallenges[4] = "Lost"
            elif ((loserId == openChallenges[1]) and (openChallenges[2] == True)):
                openChallenges[5] = True
                openChallenges[6] = "Lost"
            if (openChallenges[3] == openChallenges[5]):
                print("Update Leaderboard")
                print("Delete Challenge")

    #######################################################################################
    # TODO: Delete Challenge
    #######################################################################################

    #######################################################################################
    # TODO: Update Leaderboard
    #######################################################################################

    #######################################################################################
    # TODO: Return Leaderboard data to print to channel
    #######################################################################################
    
    #######################################################################################
    # TODO: Create the idea of leagues?
    #######################################################################################


    #######################################################################################
    # Update internal variables
    #######################################################################################
    def update(self, winnerName, loserName):
        self.winnerName = winnerName
        self.loserName  = loserName
        self.updateRatings()
        self.saveLeaderBoard()
