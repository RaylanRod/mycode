#!/usr/bin/env python3

def main():
    farms = [{"name": "NE Farm", "agriculture": ["sheep", "cows", "pigs", "chickens", "llamas", "cats"]},
         {"name": "W Farm", "agriculture": ["pigs", "chickens", "llamas"]},
         {"name": "SE Farm", "agriculture": ["chickens", "carrots", "celery"]}]

    for farm in farms:
        if farm["name"] == "NE Farm":
            animals = farm["agriculture"]

            for animal in animals:
                print(animal)

if __name__ == "__main__":
    main()
