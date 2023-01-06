class HuntPlayer:
    def __init__(self,name="",kills=-1,deaths=-1,tokens=-1,score=-1):
        self.name=name
        self.kills=kills
        self.deaths=deaths
        self.tokens=tokens
        self.score=score
    def __str__(self):
        return self.name

    def updateStats(self,k,d,t):
        self.kills=k
        self.deaths=d
        self.tokens=t

    def updateScore(self,newScore):
        self.score=newScore

    #Return true or false depending on if the default values for stats are still set
    def checkStats(self):
        return not(self.kills == -1 or self.deaths or -1 or self.tokens == -1)

class HuntGame:
    def __init__(self,instance=False,
                gamemode="Classic",
                teams=[],players=[],
                ppKill=0,ppDeath=0,ppToken=0):
        #Current instance of the game running, True if running, False if not
        self.instance=instance
        #Gamemode of game
        self.gamemode=gamemode
        #teams is a list of teams, each team is a list of player names
        self.teams=teams
        #players is a list of HuntPlayer objects
        self.players=players

        #Set scoring for gamemode
        if(gamemode.lower()=="classic"):
            self.ppKill=10
            self.ppDeath=-5
            self.ppToken=30

        #"Slayer" gamemode, which gives more points to player kills, encouraging hunting down other teams
        elif(gamemode.lower()=="slayer"):
            self.ppKill=15
            self.ppDeath=-15
            self.ppToken=15

        elif(gamemode.lower()=="custom"):
            #placeholder for when I decide to make user-made custom gamemodes
            pass

    def __str__(self):
        rString=f"""Hunt Showdown Fantasy Game \n
                Gamemode: {self.gamemode}\n
                Players: {self.players}\n
                Points per Kill: {self.ppKill}\n
                Points per Death: {self.ppDeath}\n
                Points per Bounty Token: {self.ppToken}\n"""
        return rString

    def getPlayer(self,playerString):
        players=self.players
        for i in range(len(players)):
            if playerString==players[i].name:
                return players[i]
        print("Error getting player from playerString!")


    def teamString(self):
        teams=self.teams
        tString="The current teams are: \n"
        for i in range(len(teams)):
            tString=tString+"Team "+str(i+1)+": \n"
            for j in range(len(teams[i])):
                player=self.getPlayer(teams[i][j])
                if player.checkStats():
                    tString=tString+player.name+" - K:"+str(player.kills)+" / D:"+str(player.deaths)+" / T:"+str(player.tokens)+" / Score:"+str(player.score)+" \n"
                else:
                    tString=tString+player.name+" \n"
        return tString

    def calcPlayerScore(self,player):
        score=self.ppKill*player.kills+self.ppDeath*player.deaths+self.ppToken*player.tokens
        player.updateScore(score)
