#!/usr/bin/env python3

""" This is an animal quizz for you to test your knowledge
on certain animals, characteristics would be given to the user and the user
would have to choose which animal it is"""


def main():
    # welcome banner
    print("WELCOME TO THE ANIMAL QUIZZ!")
    # Quizz instructions
    print("'Read the given characteristics of an animal and tell us which one is it!'")

    # would the player like to begin or quit the game?/ user input.
    user_choice = input("Press (a) to begin, (q) to quit: ")

    # if the user input is not on the list, print an invalid input message.
    # keeps looping until an answer on the list is given.
    while user_choice.lower() not in ["a", "q"]:
        print("Invalid input. Please enter (a) or (q).")
        user_choice = input("Press (a) to begin, (q) to quit: ")

    # if the user input is "q" then quit the quizz
    if user_choice.lower() == "q":
        print("You have chosen to quit the quizz.")
        quit()

    while True:
        # start the first quizz, assign the results to quit_quizz
        # if quit_quizz has a value of q than stop the application
        # otherwise move on to the next animal quizz
        quit_quizz = start_quizz("Elephant", "c", "C", 2)
        if quit_quizz == "q":
            quit()
        else:
            print("Next Animal:")
            print("_____________")
            start_quizz("Penguin", "d", "D", 2)
        try_again = input("Would you like to play again: y/N > ")   # Try again logic
        if try_again.upper().strip() == 'N':  # if the user input is N than quit the application
            break


# function to handle the quizzes and
# provide the application with the quizz information.
# this function will be called after the end of every quizz
# it will fetch for the characteristics and answers.
def start_quizz(animal, correct_answer, correct_message, max_attempts):
    attempts = 0

    # while the attempts count is less than the max attempts allowed
    # execute the block code, otherwise the quizz will not run.
    while attempts < max_attempts:
        print(f"Characteristics: {get_characteristics(animal)}")
        user_choice = input(f"Please choose the correct answer: {get_answers(animal)} ")

        if user_choice.lower() == "q":
            print("You have chosen to quit the quizz.")
            # return the user_choice, so we could have a value at quit_quizz
            return user_choice

        # if the user choice is equal to the correct answer
        # print "that is the correct answer", otherwise "Sorry that is the wrong answer"
        if user_choice.lower() == correct_answer:
            print(f"That is the Correct Answer")
            return
        elif attempts == max_attempts - 1:
            # after 2 attempts the correct answer will be revealed to the user
            print(f"Sorry, {user_choice} is the wrong answer! The correct answer is {correct_message}")
        else:
            print(f"Sorry, {user_choice} is the wrong answer!")
            print("    ")

        attempts += 1

    # blank line to create space after every animal or displayed output.
    print("             ")


# function that gets called to get the characteristics
def get_characteristics(animal):
    if animal == "Elephant":
        return "Largest land mammal, Has a long trunk, Large, floppy ears, Herbivorous diet"
    elif animal == "Penguin":
        return "Flightless bird, Black and white plumage, Excellent swimmer, " \
               "Lives in cold climates, especially Antarctica"
    else:
        return ""


# function to get the choices/ answers.
def get_answers(animal):
    if animal == "Elephant":
        choices = {"a": "Mammoth", "b": "Hippopotamus", 'c': "Elephant", 'd': "Walrus", 'q': "quit"}
        return choices
    elif animal == "Penguin":
        choices = {"a": "Common Murre", "b": "Atlantic Puffin", 'c': "Great Auk", 'd': "Penguins", 'q': "quit"}
        return choices


if __name__ == '__main__':
    main()
