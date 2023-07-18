import random
from sys import exit
import time

# Game data
rooms = {
    'Hall': {
        'south': 'Kitchen',
        'east': 'Dining Room',
        'item': 'silver key'
    },
    'Kitchen': {
        'north': 'Hall',
        'item': 'machete',
        'enemy': 'Goblin'
    },
    'Dining Room': {
        'west': 'Hall',
        'south': 'Garden',
        'north': 'Bedroom',
        'east': 'Patio',
        'item': 'potion',
        'doors': {
            'east': {
                'locked': True,
                'key': 'silver key'
            },
            'south': {
                'locked': True,
                'key': 'garden key'
            }
        }
    },
    'Garden': {
        'north': 'Dining Room',
        'enemy': 'Monster'
    },
    'Patio': {
        'west': 'Dining Room',
        'item': 'garden key',
        'south': 'Path Way To Shed'
    },
    'Bedroom': {
        'item': 'paper',
        'combination': 'rr4590',
        'south': 'Dining Room'
    },
    'Shed': {
        'combination': 'rr4590',
        'north': 'patio',
        'safe': {
            'locked': True,
            'combination': 't555r5',
            'item': 'bow and arrow'
        },
        'item': 'safe key'
    },
    'Path Way To Shed': {
        'enemy': 'Skeleton',
        'south': 'Shed'
    }
}

# Player inventory, which is initially empty
inventory = []

# Player health
player_health = 100
life = 3

# Dictionary of enemies
enemies = {
    'Goblin': {
        'health': 50,
        'attack': 10
    },
    'Skeleton': {
        'health': 80,
        'attack': 15
    },
    'Monster': {
        'health': 150,
        'attack': 20
    }
}

items = {
    'bow and arrow': {
        'description': 'A powerful weapon that doubles your damage',
        'damage_multiplier': 2.3
    },
    'machete': {
        'description': 'A sharp weapon that increases your damage',
        'damage_multiplier': 1.80
    },
    'baseball bat': {
        'description': 'A sturdy weapon that slightly increases your damage',
        'damage_multiplier': 1.25
    }
}


def show_instructions():
    """Show the game instructions when called"""
    # Print a main menu and the commands
    print('''
    RPG Game
    ========
    Commands:
      go [direction]
      get [item]
      attack [enemy]
      Direction Key: [north,south,east,west]
    ''')


def show_status():
    """Determine the current status of the player"""
    # Print the player's current location
    print('---------------------------')
    print('You are in the ' + current_room)
    # Print what the player is carrying
    print('Inventory:', inventory)
    # print how many lives left
    print(f"lives left: {life}")
    # Check if there's an item in the room and print it
    if 'item' in rooms[current_room] and 'item' not in inventory:
        print('You see a ' + rooms[current_room]['item'])
    # Check if there's an enemy in the room and print it
    if 'enemy' in rooms[current_room]:
        print('You are facing a ' + rooms[current_room]['enemy'])
    print("---------------------------")


def unlock_door(room, direction):
    """Unlock a door in the specified room in the given direction"""
    if 'doors' in rooms[room] and direction in rooms[room]['doors']:
        door = rooms[room]['doors'][direction]
        if door['locked'] and door['key'] in inventory:
            door['locked'] = False
            print('You unlocked the door with the ' + door['key'] + '.')
        elif door['locked']:
            print('The door is locked. You need a ' + door['key'] + ' to unlock it.')
        else:
            print('The door is already unlocked.')
    else:
        print('There is no door in that direction.')


def find_combination(room):
    """Find the combination for the safe in the specified room"""
    if 'combination' and 'safe' in rooms[room]:
        if 'safe key' in inventory:
            input("Enter the combination to the safe: ")
            while True:
                safe_code = input()
                if safe_code == rooms[room]['safe']['combination']:
                    print(f"The {safe_code} to the safe is Correct")
                    return safe_code  # Correct combination entered, exit the loop
                else:
                    print('Wrong combination!!')
    elif 'combination' in rooms[room]:
        return rooms[room]['combination']
    else:
        print('There is no combination in this room.')


def handle_combat(enemy):
    """Handle combat with the specified enemy"""
    global player_health, enemy_health, life  # Declare player_health as global
    enemy_health = enemies[enemy]['health']
    print('You are facing a ' + enemy + '! Get ready to fight!')
    print('===================')

    while enemy_health > 0 and player_health > 0:
        # Player's turn
        player_damage = player_attack()
        enemy_health -= player_damage
        print('You attacked the ' + enemy + ' for ' + str(player_damage) + ' damage.')
        time.sleep(1)  # Add a delay of 1 second

        if enemy_health <= 0:
            print('You defeated the ' + enemy + '! Congratulations!')
            break

        # Enemy's turn
        enemy_damage = enemy_attack(enemy)
        player_health -= enemy_damage
        print('The ' + enemy + ' attacked you for ' + str(enemy_damage) + ' damage.')
        time.sleep(1)  # Add a delay of 1 second

        if player_health <= 0:
            print('The ' + enemy + ' defeated you!')
            life -= 1
            play_again()

    enemies[enemy]['health'] = enemy_health


# Function to calculate the damage dealt by the player
def player_attack():
    """Calculate the damage dealt by the player"""
    # Generate a random attack value between 70% and 100% of the player's base attack
    base_attack = 10
    attack_modifier = random.uniform(0.7, 1.0)
    damage = int(base_attack * attack_modifier)

    # Check if the player has any weapon in their inventory and apply the corresponding damage multiplier
    for weapon in items:
        if weapon in inventory:
            damage *= items[weapon]['damage_multiplier']
            break

    return damage


def enemy_attack(enemy):
    """Calculate the damage dealt by the enemy"""
    # Generate a random attack value between 80% and 100% of the enemy's base attack
    base_attack = enemies[enemy]['attack']
    attack_modifier = random.uniform(0.8, 1.0)
    damage = int(base_attack * attack_modifier)
    return damage


def play_again():
    if life == 0:
        print("YOU HAVE 0 LIFE - GAME OVER!")
        try_again = input("Do you want to play again? (yes/no): ")
        if try_again.lower() == 'yes':
            main()
        else:
            print("Thanks for playing! Goodbye.")
            quit()  # exit the application
    else:
        main()


def main():
    """Main game loop"""
    global current_room, player_health, enemy_health, life

    current_room = 'Hall'  # Player start location
    player_health = 100  # Reset player health

    show_instructions()  # Show instructions to the player

    # Flag to track if the paper has been picked up
    paper_picked_up = False

    while True:
        show_status()

        move = ''
        while move == '':
            move = input('>')

        move = move.lower().split(" ", 1)

        if move[0] in ['quit', 'q']:  # Check if the player wants to quit
            print("Thanks for playing! Goodbye.")
            quit()

        if move[0] == 'go':
            if move[1] in rooms[current_room]:
                if 'doors' in rooms[current_room] and move[1] in rooms[current_room]['doors'] and \
                        rooms[current_room]['doors'][move[1]]['locked']:
                    print('The door in that direction is locked. You need to unlock it first.')
                    have_key = input("Do you have a key? Y/N: ")
                    key_type = rooms[current_room]['doors'][move[1]]['key']
                    if have_key.lower() == "y" and key_type in inventory:
                        unlock_door(current_room, move[1])  # Call unlock_door function
                        current_room = rooms[current_room][move[1]]
                    else:
                        print("You need to find the key that opens this door")
                else:
                    current_room = rooms[current_room][move[1]]

            else:
                print('You can\'t go that way!')

        elif move[0] == 'get':
            if 'item' in rooms[current_room] and move[1].lower() == rooms[current_room]['item'].lower():
                inventory.append(move[1])
                print('got ' + move[1])
                del rooms[current_room]['item']
            else:
                print('Can\'t get ' + move[1] + '!')

        elif move[0] == 'attack':
            if 'enemy' in rooms[current_room] and move[1] == rooms[current_room]['enemy']:
                handle_combat(move[1])
            else:
                print('There is no enemy to attack.')

        if 'enemy' in rooms[current_room]:
            enemy = rooms[current_room]['enemy']
            handle_combat(enemy)
            del rooms[current_room]['enemy']
            if enemy == 'Monster' and enemy_health <= 0:
                print('You defeated the Monster and escaped the house... YOU WIN!')
                break

        if current_room == 'Bedroom' and 'item' in rooms['Bedroom']:
            if not paper_picked_up:
                print('You found a piece of paper with the combination to the shed!')
                combination = rooms['Bedroom']['combination']
                print('The combination to the shed is:', combination)
                paper_picked_up = True
            else:
                print('You already picked up the paper.')

        if current_room == 'Shed' and 'combination' in rooms['Shed']:
            safe_combination = rooms['Shed']['safe']['combination']  # Access the combination from the room's dictionary
            print(
                f"You found a safe in the shed!.. Your safe key has a tag that has the numbers "
                f"{safe_combination} try it")
            find_combination('Shed')

        if current_room == 'Shed' and 'bow and arrow' in inventory:
            print('You already found the bow and arrow in the shed.')

        if current_room == 'Shed' and 'item' in rooms['Shed']['safe'] and move[0] == 'get' and \
                move[1] == 'bow and arrow':
            if 'combination' not in rooms['Shed']['safe']:
                print('You need to find the combination to the safe first.')
            else:
                print('You found a bow and arrow in the safe!')
                inventory.append('bow and arrow')
                del rooms['Shed']['item']

        if current_room == 'Garden' and 'Monster' in rooms['Garden']:
            print('You are facing a Monster in the Garden!')
            print('You need a powerful weapon to defeat it.')

        if current_room == 'Garden' and 'item' in rooms['Garden'] and move[0] == 'get' and move[1] == 'weapon':
            if 'bow and arrow' not in inventory:
                print('You need a bow and arrow to defeat the Monster.')
            else:
                print('You picked up the bow and arrow and are ready to face the Monster.')
                del rooms['Garden']['item']
                rooms['Garden']['enemy'] = 'Monster'

        if current_room == 'Garden' and 'Monster' in rooms['Garden']:
            enemy = rooms['Garden']['enemy']
            handle_combat(enemy)
            del rooms['Garden']['enemy']
            if enemy == 'Monster' and enemy_health <= 0:
                print('You defeated the Monster and escaped the house... YOU WIN!')
                break

    play_again()


if __name__ == "__main__":
    main()
