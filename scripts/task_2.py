# Get user's personal information
first_name = input("First Name: ")
last_name = input("Last Name: ")
date_of_birth = input("Date of Birth (Format: MM/DD/YYYY): ")
telephone_number = input("Telephone Number (Format: xxx-xxx-xxxx):")
print("Mailing Address: ")
street = input("Street number and name: ")
apt_num = input("APT No. (If not applicable enter NA): ")
city = input("City: ")
state = input("State: ")
zip_code = input("Zip Code (first 5 digit): ")
email = input("Email ID: ")

# Dictionary of common replacements for the alphabet -- TODO
common_replacements = {
    'a': ['@', '4', '^', '/\\', '/-\\', 'aye'],
    'b': ['8', '6', '13', '|3', '/3'],
    'c': ['<', '[', '(', '{'],
    'd': [')', '|)', '[)', '?', '|>', '|o'],
    'e': ['3', '&', '€', 'ë', '[-'],
    'f': ['|=', '/=', '|#', 'ph'],
    'g': ['6', '9', '&', 'C-', '(_+', 'gee'],
    'h': ['#', '}{', '|-|', ']-[', '[-]', ')-(', '(-)', '/-/'],
    'i': ['1', '!', '¡', '|', ']', 'eye'],
    'j': [']', '¿', '_|', '_/', '</', '(/'],
    'k': ['X', '|<', '|{', '|('],
    'l': ['|', '1', '£', '|_', '1_'],
    'm': ['|v|', '|\/|', '/\/\\', '(v)', '/|\\', '//.', '^^', 'em'],
    'n': ['|\|', '/\/', '[\]', '/V', '^/'],
    'o': ['0', '()', '[]', 'oh'],
    'p': ['|*', '|o', '|"', '|>', '9', '|7', '|^(o)'],
    'q': ['9', '0_', '()_', '(_,)', '<|'],
    'r': ['2', '/2', '12', 'I2', 'l2', '|^', '|?', 'lz'],
    's': ['5', '$', 'z', 'es'],
    't': ['7', '+', '-|-', '\'][\''],
    'u': ['|_|', '(_)', 'L|', 'v'],
    'v': ['\/', '^'],
    'w': ['VV', '\/\/', '\\\'', '\'//', '\|/', '\^/', '(n)'],
    'x': ['%', '*', '><', '}{', ')(', 'ecks'],
    'y': ['¥', 'J', '\'/', 'j'],
    'z': ['2', '7_', '~/_', '>_', '%'],
}

passwords = []
print("List of common passwords with the given information: ")
print(*passwords, sep = "\n")