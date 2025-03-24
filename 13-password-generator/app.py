# import random

# # Password Generator
# print('Welcome to Password Generator')

# # characters
# chars = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890!@#$%^&*()_+{}|":<>?'
# # number of passwords
# number= input('Enter number of passwords: ')
# # convert number to integer
# number = int(number)

# # password length
# length = input('Enter password length: ')

# # convert length to integer
# length = int(length)

# print('\nHere are your passwords:')

# # generate passwords
# for pwd in range(number):
#     password = ''
#     # generate password
#     for c in range(length):
#         password += random.choice(chars)
#     print(password)

import random
from colorama import Fore, Style

# Initialize Colorama for Windows support
print(Fore.CYAN + Style.BRIGHT + "Welcome to Password Generator!\n" + Style.RESET_ALL)

# Character set for password generation
chars = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890!@#$%^&*()_+{}|":<>?'

try:
    # Taking user input in a colorized format
    number = int(input(Fore.GREEN + "Enter the number of passwords: " + Style.RESET_ALL))
    length = int(input(Fore.YELLOW + "Enter the password length: " + Style.RESET_ALL))

    # Ensure inputs are positive
    if number < 1 or length < 1:
        print(Fore.RED + "Error: Please enter positive numbers!" + Style.RESET_ALL)
    else:
        print("\n" + Fore.RED + "Here are your passwords:\n" + Style.RESET_ALL)
        
        # Generate passwords
        for _ in range(number):
            password = ''.join(random.choices(chars, k=length))
            print(Fore.YELLOW + password + Style.RESET_ALL)

except ValueError:
    print(Fore.RED + "Invalid input! Please enter numeric values." + Style.RESET_ALL)
