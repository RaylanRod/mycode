#!/usr/bin/env python3

def sing_99_bottles():
    for num in range(99, 0, -1):
        if num > 1:
            print(f"{num} bottles of beer on the wall, {num} bottles of beer.")
            if num > 2:
                print(f"Take one down and pass it around, {num-1} bottles of beer on the wall.\n")
            else:
                print("Take one down and pass it around, 1 bottle of beer on the wall.\n")
        else:
            print("1 bottle of beer on the wall, 1 bottle of beer.")
            print("Take one down and pass it around, no more bottles of beer on the wall.\n")

    print("No more bottles of beer on the wall, no more bottles of beer.")
    print("Go to the store and buy some more, 99 bottles of beer on the wall.")

if __name__ == "__main__": 
    sing_99_bottles()

