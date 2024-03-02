import time
import random
import os

def clear_screen():
    if os.name == 'posix':
        _ = os.system('clear')
    elif os.name == 'nt':
        _ = os.system('cls')



items = {
    "weapons": [
        {"name": "LEGENDARY GOD GREATSWORD ULTRA++", "type": "Sword", "mindamage": 100, "maxdamage": 200},
        {"name": "Dagger", "type": "Dagger", "mindamage": 3, "maxdamage": 5}
    ],
    "valuables": [
        {"name": "Goo", "value": 5}
    ],
    "armor": [
        {"name": "Basic Helmet", "type": "Helmet", "defense": 2}
    ]
}

player = {
    "name": "",
    "level": 1,
    "gold": 0,
    "maxhealth": 10,
    "health": 10,
    "defense": 0,
    "minattack": 0,
    "maxattack": 4,
    "chancedrop1": random.randint(0, 3),
}

inventorylist = []
playerequipment = []

slime = {
    "index": 1,
    "name": "Slime",
    "maxhealth": 5,
    "health": 5,
    "minattack": 0,
    "maxattack": 2,
    "exp": 3,
    "mingold": 0,
    "maxgold": 2,
    "perc1/1": 1,
    "perc2/1": 3,
    "chancedrop1": random.randint(1, 3),
    "drop1": items["valuables"][0]
}      

goblin = {
    "index": 2,
    "name": "Goblin",
    "maxhealth": 7,
    "health": 7,
    "minattack": 0,
    "maxattack": 3,
    "exp": 5,
    "mingold": 0,
    "maxgold": 6,
    "perc1/1": 1,
    "perc2/1": 7,
    "chancedrop1": random.randint(1, 7),
    "drop1": items["weapons"][1]
}

def choose_random_enemy(*args):
    return random.choice(args)


def itemdropchance(entity):
    if entity["chancedrop1"] == 1:
        print(f"You got {entity['drop1']}!")
        inventory(entity['drop1'])


def xpneededcalculator(level):
    return level * 10
player["xpneeded"] = xpneededcalculator(player["level"])

def playerequipped():
    global playerequipment
    playerequipment = list(playerequipment)
    playerequipment.sort(key=lambda x: x['name'] if isinstance(x, dict) else x)
    equipped_items = ""
    for item in playerequipment:
        status = ""
        for key, value in item.items():
            if key != 'name' and key != 'type':
                status += f"{key.capitalize()}: {value}, "
        status = status.rstrip(', ') if status else "No status information available"
        equipped_items += f"{item.get('name', '')}, Type: {item.get('type', '')}, Status: {status}\n"
    return equipped_items



def currentexpe():
    global player
    global currentexp
    global currentexpdisplay
    currentexp = player["level"] * 10 - player["xpneeded"]
    currentexpdisplay = f"{currentexp}/{player["level"] * 10}"
    return currentexpdisplay
    
def inventory(*args):
    global inventorylist
    if args and args[0] == "open":
        inventorylist = list(inventorylist)
        inventorylist.sort(key=lambda x: x['name'] if isinstance(x, dict) else x)
        for index, item in enumerate(inventorylist, start=1):
            if isinstance(item, dict):
                print(f"{index}. {item['name']}")
            else:
                print(f"{index}. {item}")

        if inventorylist:
            item_index = input("Enter the index of the item you want to equip (or press Enter to exit): ")
            if item_index.isdigit():
                item_index = int(item_index)
                if 1 <= item_index <= len(inventorylist):
                    return inventorylist[item_index - 1]['name']
                else:
                    print("Invalid item index.")
            elif not item_index.strip():
                return None
            else:
                print("Invalid input.")
    else:
        for arg in args:
            inventorylist.append(arg)


def equip_item(item_name):
    global player
    item_found = None
    for item in inventorylist:
        if isinstance(item, dict) and item.get('name') == item_name:
            item_found = item
            break
    
    if item_found:
        if item_name in [inv['name'] for inv in playerequipment]:
            print("Item is already equipped.")
        else:
            inventorylist.remove(item_found) 
            playerequipment.append(item_found)
            print(f"{item_name} equipped.")
    else:
        print("Item not found in inventory.")



def playerinfo():
    print(f"""
        Player Information:
        Name: {player["name"]}
        Level: {player["level"]}
        Attack: {player["minattack"]}-{player["maxattack"]}
        Max Health: {player["maxhealth"]}
        Health: {player["health"]}
        EXP: {currentexpe()}
        GOLD: {player["gold"]}
        
Items Equipped: 
{playerequipped()}
    
    """)

def attack(attacker):
    damage = random.randint(attacker["minattack"], attacker["maxattack"])
    return damage

def resetentity(entity):
    global entitygold
    entity["health"] = entity["maxhealth"]
    entity["chancedrop1"] = random.randint(entity["perc1/1"], entity["perc2/1"])
    entitygold = random.randint(entity["mingold"], entity["maxgold"])

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
    entitygold = random.randint(entity["mingold"], entity["maxgold"])
    print(f"A battle against {entity["name"]} has begun!")

    
    while player["health"] > 0 and entity["health"] > 0:
        print("\n")
        print(f"{entity["name"]} HP: {entity["health"]}/{entity["maxhealth"]}")
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
            player["gold"] += entitygold
            itemdropchance(entity)
            resetentity(entity)
            break
            
        entitydamage = attack(entity)
        entitydamage -= player["defense"]
        if entitydamage <= 0:
            entitydamage = 0
        player["health"] -= entitydamage
        
        if entitydamage == 0:
            print(f"The {entity["name"]} tried to attack, but failed.")
        
        elif player["health"] > 0:
            print(f"The {entity["name"]} attacked you, dealing {entitydamage} damage. Leaving you at {player["health"]}HP!")
            
        elif player["health"] <= 0:
            print(f"The {entity["name"]} attacked you, dealing {entitydamage} damage. Leaving you at {player["health"]}HP! GAME OVER!")
            resetentity(entity)
            break
        
def game():
    global inventorylist
    global inventory
    global player
    
    clear_screen()
    inventory(items["armor"][0])
    
    if player["name"] == "":
        askplayername()
        
    if player["name"].lower() == "dev":
        
        gotexp(10000)
        inventory(items["weapons"][0])
    
    while player["health"] > 0:
        
        actionlist = ["1", "2" ,"3" ,"4", "c"]
        action = input("What do you want to do? [1 FIGHT | 2 INVENTORY | 3 PLAYER INFO | 4 SAVE | C CLEAR] ").lower()
        print("\n")
        
        while action not in actionlist:
            action = input("What do you want to do? [1 FIGHT | 2 INVENTORY | 3 PLAYER INFO | 4 SAVE | C CLEAR] ").lower()
            print("\n")
            
        if action == "1":
            battle(choose_random_enemy(goblin, slime))
            
        elif action == "2":
            
            if len(inventorylist) == 0:
                print("You don't have anything in your inventory!")
                print("\n")  
                
            else:
                item_to_equip = inventory("open")  
                if item_to_equip:
                    equip_item(item_to_equip) 
                    print("\n")
            
        elif action == "3":
            
            playerinfo()
            print("\n")
            
        elif action == "4":
            print("Saving not impmented yet!") 
            
            
        elif action == "c":
            clear_screen()
            
  

game()
