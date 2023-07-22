#!/usr/bin/env python3

import random
import time
import colorama
from colorama import Fore, Back, Style

from tabulate import tabulate

"""
Mutant Escape - A Text-Based Adventure Game

In Mutant Escape, you take on the role of Marcus, a man who went to visit his friend Steven near a mysterious military 
base. The base was conducting dangerous human experiments, creating mutants with disastrous consequences. 
The experiment went awry, and now the town is overrun by three types of mutants: Goblins, Skeletons, and Monsters.

One day, while hanging out with Steven, Marcus finds himself alone in the house when Steven is unable to return due to 
the mutant invasion. The mutants surround the house, leaving Marcus no choice but to find a way to escape. 
The only way out is through the Garden, guarded by a powerful Monster.

Your mission is to help Marcus navigate the haunted house, collect items, unlock doors, and defeat mutants in order 
to reach the Garden and face the final challenge. Choose your actions wisely, pick up valuable items, 
and use weapons strategically to survive the perilous journey.

Instructions:
- Use the commands 'go [direction]', 'get [item]', and 'attack [enemy]' to interact with the environment.
- Type 'm' or 'map' to view the map and plan your route.
- Defeat the mutants, collect clues, and solve puzzles to progress.
- Find the combination to the safe and use it to access valuable items.
- Keep an eye on your health and life count. If you lose all your lives, it's game over.
- Face the Garden Monster only if you have a powerful weapon.

May you be brave and resourceful in your quest to guide Marcus through the perilous Mutant Escape!

Author: [Raylan Rodriguez]
"""


# Game data for the rooms
rooms = {
    'Hall': {'south': 'Kitchen', 'east': 'Dining Room', 'item': 'silver key'},
    'Kitchen': {'north': 'Hall', 'south': 'Garage', 'item': 'machete', 'enemy': 'Goblin'},
    'Dining Room': {
        'west': 'Hall', 'south': 'Garden', 'north': 'Bedroom', 'east': 'Patio',
        'item': 'potion',
        'doors': {'east': {'locked': True, 'key': 'silver key'}, 'south': {'locked': True, 'key': 'garden key'}}
    },
    'Garden': {'north': 'Dining Room', 'enemy': 'Monster'},
    'Patio': {'west': 'Dining Room', 'item': 'garden key', 'south': 'Path Way To Shed'},
    'Bedroom': {'item': 'paper', 'combination': '4321', 'south': 'Dining Room',
                'east': 'Office', 'west': 'Bath Room', 'north': 'Bedroom 2'},
    'Shed': {
        'combination': '4321', 'north': 'Patio',
        'safe': {'locked': True, 'combination': '1234', 'item': 'bow and arrow'},
        'item': 'safe key'
    },
    'Path Way To Shed': {'enemy': 'Skeleton', 'south': 'Shed'},
    'Garage': {'north': 'Kitchen', 'item': 'baseball bat'},
    'Office': {'west': 'Bedroom', 'item': 'laptop'},
    'Bath Room': {'east': 'Bedroom', 'enemy': 'Goblin'},
    'Bedroom 2': {'south': 'Bedroom', 'item': 'charging cellphone'}
}

# Player inventory, which is initially empty
inventory = []

# Player health
player_health = 100
life = 3

# Dictionary of enemies
enemies = {
    'Goblin': {'health': 50, 'attack': 10},
    'Skeleton': {'health': 80, 'attack': 15},
    'Monster': {'health': 150, 'attack': 20}
}

items = {
    'bow and arrow': {'description': 'A powerful weapon that doubles your damage', 'damage_multiplier': 5.0},
    'machete': {'description': 'A sharp weapon that increases your damage', 'damage_multiplier': 2.5},
    'baseball bat': {'description': 'A sturdy weapon that slightly increases your damage', 'damage_multiplier': 1.5}
}

current_room = 'Hall'  # Player start location


def show_instructions():
    """Show the game instructions when called"""
    print('''
    RPG Game
    ========
    Commands:
      go [direction]
      get [item]
      attack [enemy]
      Direction Key: [north, south, east, west]
    ''')


def show_status():
    """Determine the current status of the player"""
    print('---------------------------')
    print('You are in the', Fore.BLUE + current_room + Style.RESET_ALL)
    print('Inventory:', inventory)
    print(f"Lives left: {life}")
    print("Type 'm' for Map")
    if 'item' in rooms[current_room] and 'item' not in inventory:
        print('You see a', Fore.YELLOW + rooms[current_room]['item'] + Style.RESET_ALL)
    if 'enemy' in rooms[current_room]:
        print('You are facing a', rooms[current_room]['enemy'])
    print("---------------------------")


def unlock_door(room, direction):
    """Unlock a door in the specified room in the given direction"""
    if 'doors' in rooms[room] and direction in rooms[room]['doors']:
        door = rooms[room]['doors'][direction]
        if door['locked'] and door['key'] in inventory:
            door['locked'] = False
            print('You unlocked the door with the', door['key'] + '.')
        elif door['locked']:
            print('The door is locked. You need a', door['key'] + ' to unlock it.')
        else:
            print('The door is already unlocked.')
    else:
        print('There is no door in that direction.')


def find_combination(room):
    """Find the combination for the safe in the specified room"""
    if 'safe' in rooms[room]:  # Check if there is a safe in the specified room
        if 'safe key' in inventory:  # Check if the player has the 'safe key' in their inventory
            # Ask the player to input the combination to the safe and check if it's correct
            print(f"The key has a tag that reads: {rooms[room]['safe']['combination']},"
                  f" could this be the combination?")
            while True:
                safe_code = input("Enter the combination to the safe: ")
                if safe_code == rooms[room]['safe']['combination']:
                    # If the combination is correct, add the bow and arrow to the inventory
                    print(f"The code: {safe_code} is correct.")
                    print(f"Congratulations! You have obtained a bow and arrow. "
                          f"This item will be added to your inventory.")
                    inventory.append("bow and arrow")
                    return safe_code
                else:
                    print('Wrong combination!!')
    else:
        print('There is no safe in this room.')  # Print a message if there is no safe in the specified room


def handle_combat(enemy):
    """Handle combat with the specified enemy"""
    global player_health, life
    enemy_health = enemies[enemy]['health']
    print('You are facing a', enemy + '! Get ready to fight!')
    print('===================')

    while enemy_health > 0 and player_health > 0:
        player_damage = player_attack()  # getting the player damage value for the fight
        enemy_health -= player_damage  # enemy health reducing
        print('You attacked the', enemy, 'for', player_damage, 'damage.')
        time.sleep(1)

        if enemy_health <= 0:
            print('You defeated the', enemy + '! Congratulations!')
            break

        enemy_damage = enemy_attack(enemy)
        player_health -= enemy_damage
        print('The', enemy, 'attacked you for', enemy_damage, 'damage.')
        time.sleep(1)  # adding a delay to the fight

        if player_health <= 0:
            print('The', enemy, 'defeated you!')
            life -= 1  # reduces the life
            game_over()  # checks to see if the game is over

    return enemy_health


def player_attack():
    """Calculate the damage dealt by the player"""

    base_attack = 10  # Player's basic attack power
    attack_modifier = random.uniform(0.7, 1.0)  # Randomly modifies attack power (70% to 100%)
    damage = int(base_attack * attack_modifier)  # Final damage calculation

    # Check if the player has special weapons in their inventory
    for weapon in items:
        if weapon in inventory:
            # If the player has a special weapon, increase the damage based on its multiplier
            damage *= items[weapon]['damage_multiplier']
            break  # Stop checking for other weapons, use the first one found

    return damage  # The total damage the player will deal with their attack


def enemy_attack(enemy):
    """Calculate the damage dealt by the enemy"""

    base_attack = enemies[enemy]['attack']  # Enemy's basic attack power
    attack_modifier = random.uniform(0.8, 1.0)  # Randomly modifies attack power (80% to 100%)
    damage = int(base_attack * attack_modifier)  # Final damage calculation

    return damage  # The total damage the enemy will deal with its attack


def game_over():
    global life

    if life <= 0:  # If the player has no lives left
        print("YOU HAVE 0 LIVES - GAME OVER!")  # Print game over message
        print("Please Try Again Later")  # Print a message asking the player to try again later
        exit()  # Exit the game
    else:  # If the player has lives left
        main()  # Restart the main game loop to continue playing


def print_map():
    """Print the map with room connections"""
    headers = ['Room', 'North', 'South', 'East', 'West']
    rows = []

    for room, connections in rooms.items():
        north = connections.get('north', '-')
        south = connections.get('south', '-')
        east = connections.get('east', '-')
        west = connections.get('west', '-')
        rows.append([room, north, south, east, west])

    print(tabulate(rows, headers=headers, tablefmt="grid"))


def main():
    """Main game loop"""
    global current_room, player_health, life

    current_room = 'Hall'  # Player start location
    player_health = 100  # Reset player health

    print_map()  # Prints the map to the console
    show_instructions()  # Show instructions to the player

    paper_picked_up = False
    retry_shed_combination = False
    shed_access = None

    while True:
        show_status()  # Display player's current status

        move = input('>')  # Prompt the player for their next move
        move = move.lower().split(" ", 1)  # Split the input into a command and an argument

        if move[0] in ['quit', 'q']:  # Check if the player wants to quit
            print("Thanks for playing! Goodbye.")
            quit()
        elif move[0].lower() in ['m', 'map']:
            print_map()

        if move[0] == 'go':  # If the player wants to move to a different room
            if move[1] in rooms[current_room]:  # Check if the direction is valid from the current room
                if 'doors' in rooms[current_room] and move[1] in rooms[current_room]['doors'] and \
                        rooms[current_room]['doors'][move[1]]['locked']:
                    print('The door in that direction is locked. You need to unlock it first.')
                    have_key = input("Do you have a key? Y/N: ")  # Ask if the player has a key to unlock the door
                    key_type = rooms[current_room]['doors'][move[1]]['key']
                    if have_key.lower() == "y" and key_type in inventory:
                        unlock_door(current_room, move[1])  # Call unlock_door function to unlock the door
                        current_room = rooms[current_room][move[1]]  # Move the player to the new room
                    else:
                        print("You need to find the key that opens this door")
                else:
                    current_room = rooms[current_room][move[1]]  # Move the player to the new room
            else:
                print('You can\'t go that way!')

        elif move[0] == 'get':  # If the player wants to pick up an item in the room
            if 'item' in rooms[current_room] and move[1].lower() == rooms[current_room]['item'].lower():
                inventory.append(move[1])  # Add the item to the player's inventory
                print('got ' + move[1])
                del rooms[current_room]['item']  # Remove the item from the room's items
            else:
                print('Can\'t get ' + move[1] + '!')  # Print a message if the item cannot be picked up

        elif move[0] == 'attack':  # If the player wants to attack an enemy
            if 'enemy' in rooms[current_room] and move[1] == rooms[current_room]['enemy']:
                enemy = rooms[current_room]['enemy']
                enemy_health = handle_combat(enemy)  # Handle combat with the enemy
                rooms[current_room]['enemy'] = enemy  # Update the enemy's health in the rooms dictionary
                if enemy_health <= 0:
                    del rooms[current_room]['enemy']  # Remove enemy if defeated
            else:
                print('There is no enemy to attack.')  # Print a message if there is no enemy to attack

        if 'enemy' in rooms[current_room]:  # If there is an enemy in the current room
            enemy = rooms[current_room]['enemy']
            enemy_health = handle_combat(enemy)  # Handle combat with the enemy
            del rooms[current_room]['enemy']
            if enemy == 'Monster' and enemy_health <= 0:
                print('You defeated the Monster and escaped the house... YOU WIN!')
                break

        # Check if the player is in the 'Bedroom' and there's an item to pick up
        if current_room == 'Bedroom' and 'item' in rooms['Bedroom']:
            if not paper_picked_up:  # Check if the player already picked up the paper
                print('You found a piece of paper with the combination to the shed!')
                combination = rooms['Bedroom']['combination']
                print('The combination to the shed is:', combination)
                paper_picked_up = True
            else:
                print('You already picked up the paper.')

        # Check if the player is in the 'Shed' and there's a combination to find
        if current_room == 'Shed' and 'combination' in rooms['Shed']:
            if retry_shed_combination:  # Check if the player previously failed to open the shed
                print("You failed to open the shed. You should try again or find the combination.")
                break

            if shed_access != rooms['Shed']['combination']:  # Check if the player provided the right combination
                shed_access = input("What is the combination to the Shed Door?  ")
                if shed_access == rooms['Shed']['combination']:
                    print("That is the correct code")
                    print("You found a safe in the shed!")
                    find_combination('Shed')  # Find the combination to the safe in the shed
                else:
                    print("That is the wrong combination!!")
                    try_again = input("Would you like to try again? or go find the combination? Type: try or go")
                    if try_again.lower() == 'go':
                        retry_shed_combination = True  # Player decided to go find the combination instead
                    else:
                        break
            else:
                find_combination('Shed')  # Find the combination to the safe in the shed

        if current_room == 'Shed' and 'bow and arrow' in inventory:
            print('You already found the bow and arrow in the shed.')

        # Check if the player is in the 'Shed' and there's an item to pick up
        if current_room == 'Shed' and 'item' in rooms['Shed']['safe'] and move[0] == 'get' \
                and move[1] == 'bow and arrow':
            if 'combination' not in rooms['Shed']['safe']:
                print('You need to find the combination to the safe first.')
            else:
                print('You found a bow and arrow in the safe!')
                inventory.append('bow and arrow')  # Add the bow and arrow to the player's inventory
                del rooms['Shed']['item']  # Remove the bow and arrow from the safe

        # Check if the player is in the 'Garden' and there's a Monster to face
        if current_room == 'Garden' and 'Monster' in rooms['Garden']:
            print('You are facing a Monster in the Garden!')
            print('You need a powerful weapon to defeat it.')

        # Check if the player is in the 'Garden' and there's a weapon to pick up
        if current_room == 'Garden' and 'item' in rooms['Garden'] and move[0] == 'get' and move[1] == 'weapon':
            if 'bow and arrow' not in inventory:
                print('You need a bow and arrow to defeat the Monster.')
            else:
                print('You picked up the bow and arrow and are ready to face the Monster.')
                del rooms['Garden']['item']  # Remove the weapon from the Garden's items
                rooms['Garden']['enemy'] = 'Monster'  # Add the Monster enemy to the Garden

        # Check if the player is in the 'Garden' and there's a Monster to face
        if current_room == 'Garden' and 'Monster' in rooms['Garden']:
            enemy = rooms['Garden']['enemy']
            enemy_health = handle_combat(enemy)  # Handle combat with the Monster
            del rooms['Garden']['enemy']
            if enemy == 'Monster' and enemy_health <= 0:
                print('You defeated the Monster and escaped the house... YOU WIN!')
                break

        # Check if the player decided to go find the combination for the shed instead of retrying
        if current_room == 'Shed' and retry_shed_combination:
            print('You decided to go find the combination instead.')
            break

    game_over()  # Call the game_over() function at the end of the game loop


if __name__ == "__main__":
    print(Fore.YELLOW + '''
      
Instructions for "Mutant Escape"

Objective:
Your goal is to help Marcus, the brave adventurer, escape from the haunted house infested with dangerous mutants. 
Explore the rooms, collect items, and defeat the mutants to find your way out.

How to Play:

Use the commands to navigate and interact with the environment:

go [direction]: Move to a different room (e.g., "go north").
get [item]: Pick up an item in the current room (e.g., "get machete").
attack [enemy]: Fight an enemy in the current room (e.g., "attack Goblin").
m or map: Display the map to help you navigate.
Explore the House:

Start your adventure in the "Hall."
Find useful items and weapons hidden in the rooms. Use them wisely to defeat the mutants.
Note that some doors may be locked, requiring specific keys to unlock them.
Battle the Mutants:

As you explore, you will encounter three types of mutants: Goblins, Skeletons, and Monsters.
Engage in combat by attacking them. Use powerful weapons to increase your chances of success.
Be strategic and keep an eye on your health. If your health reaches zero, you will lose a life.
Solving Puzzles:

Some rooms may have puzzles or challenges. Use your wits to find solutions and progress.
Find the Combination:

Keep an eye out for important clues and documents, like the combination to the safe.
Use the combination to access valuable items that will aid you in your journey.
Face the Garden Monster:

The Garden holds the final challenge – a powerful Monster. Make sure you have a strong weapon to face it.
Life and Game Over:

You have three lives. If you lose all your lives, it's game over.
If you defeat the Monster and escape the house, you win!
Remember: Every decision you make impacts your survival. Be cautious, observant, and resourceful to 
overcome the mutants and "Mutant Escape." Good luck, adventurer!
      ''' + Style.RESET_ALL)
    print()
    enter_game = input('PLAY NOW Y/N: ')
    if enter_game.lower() == 'y':
        main()  # Start the game by calling the main() function if this script is executed directly
    else:
        quit()  # Quits game application if the user does not want to play
