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
common_replacements = {'a': ['A', '@', '4'],
                       'b': ['B', '8'],
                       'c': ['C'],
                       'd': ['D'],
                       'e': ['E', '3'],
                       'f': ['F'],
                       'g': ['G', '9', '6'],
                       'h': ['H'],
                       'i': ['I', '1', '|', '!'],
                       'j': ['J'],
                       'k': ['K'],
                       'l': ['L'],
                       'm': ['M'],
                       'n': ['N'],
                       'o': ['O', '0'],
                       'p': ['P'],
                       'q': ['Q'],
                       'r': ['R'],
                       's': ['S', '$', '5'],
                       't': ['t', '7'],
                       'u': ['U'],
                       'v': ['V'],
                       'w': ['W'],
                       'x': ['X'],
                       'y': ['Y'],
                       'z': ['Z']}

passwords = []
print("List of common passwords with the given information: ")
print(*passwords, sep = "\n")