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
        {"name": "LEGENDARY GOD GREATSWORD ULTRA++", "type": "Weapon", "mindamage": 100, "maxdamage": 200},
        {"name": "Dagger", "type": "Weapon", "mindamage": 1, "maxdamage": 3},
        {"name": "Wooden Sword", "type": "Weapon", "mindamage": 3, "maxdamage": 5}
    ],
    "valuables": [
        {"name": "Goo", "value": 5}
    ],
    "armor": [
        {"name": "Basic Leather Helmet", "type": "Helmet", "defense": 1},
        {"name": "Iron Chest", "type": "Armor", "defense": 6}
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
        status = status.rstrip(', ') if status else "No stats information available"
        equipped_items += f"{item.get('name', '')}, Type: {item.get('type', '')}, Stats: {status}\n"
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
                if item.get('type') in ['Weapon', 'Armor']:
                    if item.get('type') == 'Weapon':
                        print(f"{index}. {item['name']}")
                    elif item.get('type') == 'Armor':
                        print(f"{index}. {item['name']}")
                else:
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
                clear_screen()
                return None
            else:
                print("Invalid input.")
    else:
        for arg in args:
            inventorylist.append(arg)
    time.sleep(1)
    clear_screen()

def equip_item(item_name):
    global player
    item_found = None
    for item in inventorylist:
        if isinstance(item, dict) and item.get('name') == item_name:
            item_found = item
            break
    
    if item_found:
        item_type = item_found.get('type')
    
        if item_type in ["Weapon", "Armor", "Helmet"]: 
            for equipped_item in playerequipment:
                if equipped_item.get('type') == item_type:
                    print(f"You already have a {item_type} equipped. Do you want to replace it?")
                    replace = input("Enter 'Y' to replace or any other key to cancel: ")
                    if replace.lower() == 'y':
                        if equipped_item in playerequipment:
                            inventorylist.append(equipped_item) 
                            playerequipment.remove(equipped_item)
                            if 'mindamage' in equipped_item:
                                player['minattack'] -= equipped_item['mindamage']
                            if 'maxdamage' in equipped_item:
                                player['maxattack'] -= equipped_item['maxdamage']
                            if 'defense' in equipped_item:
                                player['defense'] -= equipped_item['defense']
                            print(f"{equipped_item['name']} unequipped and added back to inventory.")
                            break
                        else:
                            print("You don't have any equipped items of that type.")
                            break
                    else:
                        print("Equipping canceled.")
                        return

            if item_found in inventorylist:
                inventorylist.remove(item_found)
            playerequipment.append(item_found)
            print(f"{item_name} equipped.")
            
            if 'mindamage' in item_found:
                player['minattack'] += item_found['mindamage']
            if 'maxdamage' in item_found:
                player['maxattack'] += item_found['maxdamage']
            if 'defense' in item_found:
                player['defense'] += item_found['defense']
        else:
            print("You cannot equip this item.")
            
    elif item_found and item_found.get('type') == "Valuables":
        print("You cannot equip valuables.")
        
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
        Defense: {player["defense"]}
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
    global world
    global worldlist
    global total_value
    devlist = ["mu", "dev"]
    world = "1"
    clear_screen()
    inventory(items["armor"][0])
    
    if player["name"] == "":
        askplayername()
        
    if player["name"].lower() in devlist:
        try:
            howmuchgold = int(input("How much gold you want? "))
        except ValueError:
            howmuchgold = 0
        player["gold"] += howmuchgold
        try:
            howmuchexp = int(input("How much xp you want? "))
        except ValueError:
            howmuchexp = 0
        gotexp(howmuchexp)
        
        itemsquestion = input("You want 2 copies of each item? [y]")
        if itemsquestion == "y":
            for category in items.values():
                for item in category:
                    for _ in range(2):  # Add two copies of each item
                        inventory(item)
            
            
        
    time.sleep(0.2)
    while True:
        
        actionlist = ["f", "i" ,"p" ,"s", "m", "save"]
        print("What do you want to do? [F-FIGHT | I-INVENTORY | P-PLAYER INFO | S-SHOP | M-MAP | SAVE-SAVE] ")
        action = input("\n").lower()
        time.sleep(0.2)
        clear_screen()
        
        while action not in actionlist:
            print("What do you want to do? [F-FIGHT | I-INVENTORY | P-PLAYER INFO | S-SHOP | M-MAP | SAVE-SAVE] ")
            action = input("\n").lower()
            time.sleep(0.2)
            clear_screen()
            
        if action == "f":
            
            if world == "1":
                print("You are at the slime island!")
                battle(slime)
                
            elif world == "2":
                print("You are at the cave!")
                battle(choose_random_enemy(slime, goblin))    
                
            time.sleep(1)
            clear_screen()
            
        elif action == "i":
            
            if len(inventorylist) == 0:
                print("You don't have anything in your inventory!")
                input("\n") 
                time.sleep(0.2)
                clear_screen()
                
            else:
                item_to_equip = inventory("open")  
                if item_to_equip:
                    equip_item(item_to_equip) 
                    print("\n")
                    time.sleep(0.2)
                    clear_screen()
            
        elif action == "p":
            
            playerinfo()
            input("\n")
            time.sleep(0.2)
            clear_screen()
            
        elif action == "s":
            print("[S-SELL | 1 LIFE POTION 25$ | 2 WOODEN SWORD 100$ | 3 IRON CHEST 500$]")
            buy = input("\n")
            time.sleep(0.2)
            clear_screen()
        
            if buy.lower() == "s":
                total_value = 0
                for item in inventorylist:
                    if item in items["valuables"]:
                        total_value += item["value"]
                player["gold"] += total_value
                print(f"You sold all valuables for {total_value} gold.")
                inventorylist = [item for item in inventorylist if item not in items["valuables"]]
            
            
            elif buy == "1":
                
                if player["gold"] >= 25:
                    player["gold"] -= 25
                    player["health"] += 10
                    
                    if player["health"] > player["maxhealth"]:
                        player["health"] = player["maxhealth"]
                        
                    print("Life potion used!")
                    
                else:
                    print("Not enough gold.")
                    
            elif buy == "2":
                
                if player["gold"] >= 100:
                    player["gold"] -= 100
                    inventory(items["weapons"][2])
                    print("Wooden sword bought!")
                    
                else:
                    print("Not enough gold.")
                    
            elif buy == "3":
                
                if player["gold"] >= 500:
                    player["gold"] -= 500
                    inventory(items["armor"][1])
                    print("Wooden sword bought!")
                    
                else:
                    print("Not enough gold.")        
            
            
        elif action == "m":
            
            if 0 < player["level"] <= 3:
                worldlist = ["1"]
                world = input("[1 - SLIME ISLE] ")
                while world not in worldlist:
                    world = input("[1 - SLIME ISLE] ")
                                
            elif 3 < player["level"] <= 5:
                worldlist = ["1", "2"]
                world = input("[1 - SLIME ISLE | 2 - CAVE] ")
                while world not in worldlist:
                    world = input("[1 - SLIME ISLE | 2 - CAVE] ")   
                                
            else:
                worldlist = ["1", "2"]
                world = input("[1 - SLIME ISLE | 2 - CAVE] ")
                while world not in worldlist:
                    world = input("[1 - SLIME ISLE | 2 - CAVE] ")  
                
            
            clear_screen()
            
        elif action == "save":
            print("Saving not impmented yet!")
            input("\n")
            time.sleep(0.2)
            clear_screen()    
            
  
game()
