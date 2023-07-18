#!/usr/bin/env python3

def main():
    count = 0
    with open("dracula.txt", "r") as dracula_content:
        with open("vampiretimex.txt", "w") as vampire_lines:
            for line in dracula_content:
                if "vampire" in line.lower():
                    count += 1
                    print(line)
                    vampire_lines.write(line)


    print(f"The word Vampire appeared {count} times")


if __name__ == "__main__":
    main()
