import random

def guess(x):
    random_number = random.randint(1, 10)

    guessed_number = 0

    while guessed_number != random_number:
        guessed_number = int(input("Guess a number between 1 and {x}: "))
        if guessed_number < random_number:
            print("Sorry, guess again as your guess is Too Low.")
        elif guessed_number > random_number:
            print("Sorry, guess again as your guess is Too High.")
    
    print(f"Yay! You have guessed the number {random_number} correctly.")


def computer_guess(x):
    low = 1
    high = x
    feedback = ''

    while feedback != 'c':
        if low != high:
            guessed_num = random.randint(low,high)
        else:
            guessed_num = low

        guessed_num = random.randint(low, high)
        feedback = input(f"Is {guessed_num} too high (H), too low (L), or correct (C)?? ").lower()

        if feedback == 'h':
            high = guessed_num -1
        elif feedback == 'l':
            low = guessed_num + 1

    print(f"Yay! The computer has guessed your number {guessed_num} correctly.")

guess(10)
computer_guess(10)
