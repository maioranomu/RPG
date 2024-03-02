import time
import random
import os

def clear_screen():
    if os.name == 'posix':
        _ = os.system('clear')
    elif os.name == 'nt':
        _ = os.system('cls')

player = {
    "name": "",
    "level": 1,
    "maxhealth": 10,
    "health": 10,
    "minattack": 0,
    "maxattack": 3,
    "chancedrop1": random.randint(0, 3),
}

inventorylist = []
playerquipment = []

slime = {
    "name": "slime",
    "maxhealth": 5,
    "health": 5,
    "minattack": 0,
    "maxattack": 2,
    "exp": 3,
    "perc1/1": 1,
    "perc2/1": 3,
    "chancedrop1": random.randint(1, 3),
    "drop1": "goo"
}      

goblin = {
    "name": "goblin",
    "maxhealth": 7,
    "health": 7,
    "minattack": 0,
    "maxattack": 3,
    "exp": 5,
    "perc1/1": 1,
    "perc2/1": 7,
    "chancedrop1": random.randint(1, 7),
    "drop1": "dagger"
}


def itemdropchance(entity):
    if entity["chancedrop1"] == 1:
        print(f"You got {entity["drop1"]}!")
        inventorylist.append({entity["drop1"]})


def xpneededcalculator(level):
    return level * 10
player["xpneeded"] = xpneededcalculator(player["level"])

def currentexpe():
    global player
    global currentexp
    global currentexpdisplay
    currentexp = player["level"] * 10 - player["xpneeded"]
    currentexpdisplay = f"{currentexp}/{player["level"] * 10}"
    return currentexpdisplay
    
def inventory():
    print("\n")
    inventorylist.sort()
    for item in inventorylist:
        print(item)

def playerinfo():
    print(f"""
        Player Information:
        Name: {player["name"]}
        Level: {player["level"]}
        Attack: {player["minattack"]}-{player["maxattack"]}
        Max Health: {player["maxhealth"]}
        Health: {player["health"]}
        EXP: {currentexpe()}
    
    """)

def attack(attacker):
    damage = random.randint(attacker["minattack"], attacker["maxattack"])
    return damage

def resetentity(entity):
    entity["health"] = entity["maxhealth"]
    entity["chancedrop1"] = random.randint(entity["perc1/1"], entity["perc2/1"])

def askplayername():
    global player
    player["name"] = input("Name: ")
    print("\n")

def gotexp(xpgotten):
    global player
    for xp in range(xpgotten):
        player["xpneeded"] -= 1
        if player["xpneeded"] <= 0:
            player["level"] += 1
            print(f"Leveled Up! [{player["level"]}]")
            player["maxhealth"] += 3
            player["health"] += 3
            player["maxattack"] += 1
            player["xpneeded"] = xpneededcalculator(player["level"])

def battle(entity):
    global currentexp
    global player
    global playerdamage
    global entitydamage
    print(f"A battle against {entity["name"]} has begun!")

    
    while player["health"] > 0 and entity["health"] > 0:
        print("\n")
        print(f"{entity["name"].title()} HP: {entity["health"]}/{entity["maxhealth"]}")
        print(f"Player HP: {player["health"]}/{player["maxhealth"]}")
        input("")
        time.sleep(1)
        print("\n")
        
        playerdamage = attack(player)
        entity["health"] -= playerdamage
        
        if playerdamage == 0:
            print(f"You tried to attack, but failed.")
        
        elif entity["health"] > 0:
            print(f"You attacked the {entity["name"]}, dealing {playerdamage} damage. Leaving it at {entity["health"]}HP!") 
            
        elif entity["health"] <= 0:
            print(f"You defeated the {entity["name"]}. You have gained {entity["exp"]} experience points.") #KILLED THE ENTITY
            gotexp(entity["exp"])
            itemdropchance(entity)
            resetentity(entity)
            break
            
        entitydamage = attack(entity)
        player["health"] -= entitydamage
        
        if entitydamage == 0:
            print(f"The {entity["name"]} tried to attack, but failed.")
        
        elif player["health"] > 0:
            print(f"The {entity["name"]} attacked you, dealing {entitydamage} damage. Leaving you at {player["health"]}HP!")
            
        elif player["health"] <= 0:
            print(f"The {entity["name"]} attacked you, dealing {entitydamage} damage. Leaving you at {player["health"]}HP! GAME OVER!")
            resetentity(entity)
            break
        
        
        
##############################################################################################################################################################       
clear_screen()


if player["name"] == "":
    askplayername()
    
if player["name"].lower() == "dev":
    gotexp(100)
    inventorylist.append("LEGENDARY GOD GREATSWORD ULTRA++")
    inventorylist.append("LEGENDARY GOD GREATSWORD ULTRA++")
    
        
playerinfo()
inventory()

    
# while player["health"] > 0:
    
#     print(goblin["chancedrop1"])
#     battle(goblin)
#     print(slime["chancedrop1"])
#     battle(slime)

#     playerinfo()
#     inventory()




