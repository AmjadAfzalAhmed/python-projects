import random
import string
from words import words

def get_valid_word(words):
    word = random.choice(words)
    while '-' in word or ' ' in word:
        word = random.choice(words)
    return word.upper()

def hangman():
    word = get_valid_word(words)
    word_letters = set(word)  # letters in the word
    alphabet = set(string.ascii_uppercase)
    used_letters = set()  # what the user has guessed already

    lives = 6
    # getting user input
    while len(word_letters) > 0 and lives > 0:
        print(f'\nYou have {lives} lives left.')
        print('You have used these letters:', ' '.join(used_letters))

        # Display the current guessed word (e.g., W - R D)
        word_list = [letter if letter in used_letters else '-' for letter in word]
        print('Current word:', ' '.join(word_list))

        user_input = input('Guess a letter: ').upper()
        if user_input in alphabet - used_letters:
            used_letters.add(user_input)
            if user_input in word_letters:
                word_letters.remove(user_input)
            else:
                lives -= 1
                print('Letter is not in the word.')

        elif user_input in used_letters:
            print('You have already used that letter. Please try again.')
        else:
            print('Invalid character. Please try again.')

    # player gets here when len(word_letters) == 0 OR when lives == 0
    if lives == 0:
        print('You died, sorry. The word was', word)
    else:
        print('You guessed the word', word, '!!')

if __name__ == '__main__':
    hangman()
