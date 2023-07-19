#!/usr/bin/env python3

import requests

def main():
    pokenum= input("Pick a number between 1 and 151!\n>")
    pokeapi= requests.get("https://pokeapi.co/api/v2/pokemon/" + pokenum).json()
    
    img_url= pokeapi["sprites"]["front_default"]
    print(img_url)

    for move in pokeapi["moves"]:
        print(move["move"]["name"])

    count = 0
    for game_intance in pokeapi["game_indices"]:
        count += 1
    
    print("The amount of instances are: " + str(count))

main()

