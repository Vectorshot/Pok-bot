import re
import json
from pathlib import Path
import sys
from database import ReplayDatabase
from collections import defaultdict
POKE = r"\|poke\|(?P<player>.+?)\|(?P<poke>.+?)\|"
USER_PLAYER = r"\|player\|(?P<player>.+?)\|(?P<username>.+?)\|.*?"
TURN =  r"\|turn\|(?P<turnNumber>.+?)"
SWITCH = r"\|(switch|drag)\|(?P<player>.+?)(a|b): (?P<nickname>.+?)\|(?P<pokename>.+)\|(?P<remainingHealth>.+)/(?P<totalHealth>.+)"
REPLACE = r"\|replace\|(?P<player>.+?)(a|b): (?P<nickname>.+?)\|(?P<pokename>.+?).+?"
MOVE = r"\|move\|(?P<player1>.+?)(a|b): (?P<poke1>.+?)\|(?P<move>.+?)\|(\[of\] )*(?P<player2>.+?)(a|b): (?P<poke2>.+)"
DAMAGE_MOVE = r"\|-damage\|(?P<player>.+?)(a|b): (?P<poke>.+?)\|(?P<remainingHealth>.+?)/(?P<totalHealth>.+)"
DAMAGE_FROM_FAINT_MOVE = r"\|-damage\|(?P<player>.+?)(a|b): (?P<poke>.+?)\|0 fnt\|\[from\] (?P<move>.+)"
DAMAGE_FROM_MOVE =  r"\|-damage\|(?P<player>.+?)(a|b): (?P<poke>.+?)\|(?P<remainingHealth>.+?)/(?P<totalHealth>.+?)\|\[from\] (?P<move>.+)"
DAMAGE_FAINT = r"\|-damage\|(?P<player>.+?)(a|b): (?P<poke>.+?)\|0 fnt"
DAMAGE_ITEM = r"\|-damage\|(?P<player>.+?)(a|b): (?P<poke>.+?)\|(?P<remainingHealth>.+?)/(?P<totalHealth>.+?)\|\[from\] item: (?P<item>.+)"
DAMAGE_ITEM_FAINT = r"\|-damage\|(?P<player>.+?)(a|b): (?P<poke>.+?)\|0 fnt\|\[from\] item :(?P<item>.+)"
WIN =  r"\|win\|(?P<player>.+)"

HEALTH =r"([a-zA-Z]+)(?P<health>[0-9]+).+?"
healthOne = {}
healthTwo ={}
nick_names ={}
team1 = []
team2 =[]
team1pokemon = []
team2pokemon = []
user1 = ''
user2 = ''
    
noOfTeam1Pokemon = 0 
noOfTeam2Pokemon = 0 
    
noOfFaintedPokemonForTeam1=0 
noOfFaintedPokemonForTeam2=0
turn = 1
ans = []
def handle_line(lines):
    global noOfTeam1Pokemon 
    global noOfTeam2Pokemon 
    global teamOneHealth
    global teamTwoHealth 
    global ans  
    global noOfFaintedPokemonForTeam1 
    global noOfFaintedPokemonForTeam2
    global turn
    print(lines)
    for line in lines:
        print(line)
        match = re.match(USER_PLAYER, line)
        if match:
            player = match.group("player")
            nickname = match.group("username")
            if("p1" in player):
                user1 = nickname
            else:
                user2 = nickname
            continue
        match = re.match(WIN,line)
        if match : 
            print('ee11')
            player = match.group("player")
            teamOneHealth = sum(healthOne.values())/len(healthOne.values())
            teamTwoHealth = sum(healthTwo.values())/len(healthTwo.values())
            team1.append([turn,noOfTeam1Pokemon,noOfFaintedPokemonForTeam1,teamOneHealth])
            team2.append([turn,noOfTeam2Pokemon,noOfFaintedPokemonForTeam2,teamTwoHealth])
            if("p1" in player):
                ans = [team1,team2]
                break
            else:
                ans =  [team2,team1]
            
            
            
        match = re.match(TURN, line)
        if(match): 
            teamOneHealth = sum(healthOne.values())/len(healthOne.values())
            teamTwoHealth = sum(healthTwo.values())/len(healthTwo.values())
            team1.append([turn,noOfTeam1Pokemon,noOfFaintedPokemonForTeam1,teamOneHealth])
            team2.append([turn,noOfTeam2Pokemon,noOfFaintedPokemonForTeam2,teamTwoHealth])
            turn +=1
            continue
        
        match = re.match(SWITCH, line)
        if match:
                nickname = match.group("nickname").split("-")[0]
                pokemon = match.group("pokename").split("-")[0].split(",")[0]
                player = match.group("player")
                totalHealth = match.group("totalHealth")
                remainingHealth = match.group("remainingHealth")
                
                if(totalHealth == remainingHealth):
                    if("p1" in player):
                        healthOne[nickname] = 100
                    else : 
                        healthTwo[nickname] = 100

                if(nickname != ''):
                    nick_names[nickname] = pokemon
                else : 
                    nick_names[pokemon] = pokemon

                if("p1" in player):
                    if(nickname not in team1pokemon):
                        noOfTeam1Pokemon += 1 
                        team1pokemon.append(nickname)
                else : 
                    if(nickname not in team2pokemon):
                        noOfTeam2Pokemon += 1 
                        team2pokemon.append(nickname)
                continue

        match = re.match(REPLACE, line) 
        if match:
                nickname = match.group("nickname").split("-")[0]
                pokemon = match.group("pokename").split("-")[0].split(",")[0]
                player = match.group("player")
                totalHealth = match.group("totalHealth")
                remainingHealth = match.group("remainingHealth")
                
                if("p1" in player):
                    healthOne[nickname] = 100
                else : 
                    healthTwo[nickname] = 100

                if(nickname != ''):
                    nick_names[nickname] = pokemon
                else : 
                    nick_names[pokemon] = pokemon

                if("p1" in player):
                    if(nickname not in team1pokemon):
                        noOfTeam1Pokemon += 1 
                        team1pokemon.append(nickname)
                else : 
                    if(nickname not in team2pokemon):
                        noOfTeam2Pokemon += 1 
                        team2pokemon.append(nickname)
                continue

        match = re.match(DAMAGE_ITEM_FAINT, line) 
        if match : 
                pokemon = match.group("poke").split("-")[0]
                nickname = nick_names[pokemon]
                player = match.group("player")
                if("p1" in player): 
                    healthOne[nickname] = 0
                    noOfFaintedPokemonForTeam1 +=1
                else : 
                    healthTwo[nickname] = 0 
                    noOfFaintedPokemonForTeam2 +=1
                continue
        else : 
                
                match = match = re.match(DAMAGE_ITEM, line) 
                if(match):
                    pokemon = match.group("poke").split("-")[0]
                    remainingHealth = match.group("remainingHealth").strip("(").strip(")").split(" ")
                    totalHealth = match.group("totalHealth").strip("(").strip(")").split(" ")
                    
                    if(len(remainingHealth)==2) : 
                        remainingHealth = remainingHealth[1].strip("(")
                    else : 
                        remainingHealth= remainingHealth[0].strip("(")
                    temp = re.compile("([0-9]+)([a-zA-Z]*)") 
                    totalHealth = re.match(temp,totalHealth[0]).groups()[0]
                     
                    percentageDamage =((int(totalHealth)-int(remainingHealth)) /int(totalHealth)) *100 
                    pokemon = match.group("poke").split("-")[0]
                    nickname = nick_names[pokemon]
                    player = match.group("player")
                    if("p1" in player): 
                        healthOne[nickname] = percentageDamage
                    else : 
                        healthTwo[nickname] = percentageDamage
                    continue
                else :
                          
                        match = match = re.match(DAMAGE_ITEM, line) 
                        if(match):
                            pokemon = match.group("poke").split("-")[0]
                            remainingHealth = match.group("remainingHealth").strip("(").strip(")").split(" ")
                            totalHealth = match.group("totalHealth").strip("(").strip(")").split(" ")
                            
                            if(len(remainingHealth)==2) : 
                                remainingHealth = remainingHealth[1].strip("(")
                            else : 
                                remainingHealth= remainingHealth[0].strip("(")
                            temp = re.compile("([0-9]+)([a-zA-Z]*)") 
                            totalHealth = re.match(temp,totalHealth[0]).groups()[0]
                            
                            percentageDamage =((int(totalHealth)-int(remainingHealth)) /int(totalHealth)) *100 
                            pokemon = match.group("poke").split("-")[0]
                            nickname = nick_names[pokemon]
                            player = match.group("player")
                            if("p1" in player): 
                                healthOne[nickname] = percentageDamage
                            else : 
                                healthTwo[nickname] = percentageDamage
                            continue
                        else :
                            
                            match = re.match(DAMAGE_FROM_FAINT_MOVE, line) 
                            if(match): 
                                pokemon = match.group("poke").split("-")[0]
                                nickname = nick_names[pokemon]
                                player = match.group("player")
                                if("p1" in player): 
                                    healthOne[nickname] = 0
                                    noOfFaintedPokemonForTeam1 +=1
                                else : 
                                    healthTwo[nickname] = 0 
                                    noOfFaintedPokemonForTeam2 +=1
                                continue
                            else :
                                
                                match = re.match(DAMAGE_FAINT, line) 
                                if match : 
                                    pokemon = match.group("poke").split("-")[0]
                                    nickname = nick_names[pokemon]
                                    player = match.group("player")
                                    if("p1" in player): 
                                        healthOne[nickname] = 0
                                        noOfFaintedPokemonForTeam1 +=1
                                    else : 
                                        healthTwo[nickname] = 0 
                                        noOfFaintedPokemonForTeam2 +=1
                                    continue
                                else : 
                                        
                                        match = match = re.match(DAMAGE_MOVE, line) 
                                        if(match):
                                            pokemon = match.group("poke").split("-")[0]
                                            remainingHealth = match.group("remainingHealth").strip("(").strip(")").split(" ")
                                            totalHealth = match.group("totalHealth").strip("(").strip(")").split(" ")
                                            
                                            if(len(remainingHealth)==2) : 
                                                remainingHealth = remainingHealth[1].strip("(")
                                            else : 
                                                remainingHealth= remainingHealth[0].strip("(")
                                            temp = re.compile("([0-9]+)([a-zA-Z]*)") 
                                            totalHealth = re.match(temp,totalHealth[0]).groups()[0]
                                            
                                            percentageDamage =((int(totalHealth)-int(remainingHealth)) /int(totalHealth)) *100 
                                            pokemon = match.group("poke").split("-")[0]
                                            nickname = nick_names[pokemon]
                                            player = match.group("player")
                                            if("p1" in player): 
                                                healthOne[nickname] = percentageDamage
                                            else : 
                                                healthTwo[nickname] = percentageDamage
     
                                            continue
    
    

         
if __name__ == "__main__":
    r = ReplayDatabase(sys.argv[0])
    names = r.select_all_replays()
    index = 0
    for username in names[:1]:
        directory = username
        print("ee")
        healthOne = {}
        healthTwo ={}
        nick_names ={}
        team1 = []
        team2 =[]
        team1pokemon = []
        team2pokemon = []
        user1 = ''
        user2 = ''
            
        noOfTeam1Pokemon = 0 
        noOfTeam2Pokemon = 0 
            
        noOfFaintedPokemonForTeam1=0 
        noOfFaintedPokemonForTeam2=0
        turn = 1
        ans = []
        for log in directory[2].split("\n"):
            
            index = index+1
            lines = log.split("\n")
            
            handle_line(lines)
            if(ans != []):
                with open("turns.csv", "w") as f:
                    win_team  = ans[0]
                    lose_team = ans[1]
                    for i in range(len(win_team)) : 
                        f.write(str(win_team[i]).strip("[]").replace(" ","")+",0")
                        f.write("\n")
                        f.write(str(lose_team[i]).strip("[]").replace(" ","")+",1")
                        f.write("\n")
                f.close()
            

           

        
   