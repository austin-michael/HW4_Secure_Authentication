import argparse
import csv

parser = argparse.ArgumentParser()
parser.add_argument('-f',
                    help='Password file used to generate password list',
                    type=str,
                    default='data/30-pwds.txt')
parser.add_argument('-o',
                    help='Output file name',
                    type=str,
                    default='./ELCP-2.txt')
args = parser.parse_args()

def remove_email_domain(email):
    temp_email = email.split('@')[0]
    return temp_email.split('_')

def split_street_address(street):
    return street.split(' ')

def leetize_me_captain(password):
    ret_list = []
    leetDict = {
        'a': ['A', '@', '4', '^', '/\\', '/-\\', 'aye'],
        'b': ['B', '8', '6', '13', '|3', '/3'],
        'c': ['C', '<', '[', '(', '{'],
        'd': ['D', ')', '|)', '[)', '?', '|>', '|o'],
        'e': ['E', '3', '&', '€', 'ë', '[-'],
        'f': ['F', '|=', '/=', '|#', 'ph'],
        'g': ['G', '6', '9', '&', 'C-', '(_+', 'gee'],
        'h': ['H', '#', '}{', '|-|', ']-[', '[-]', ')-(', '(-)', '/-/'],
        'i': ['I', '1', '!', '¡', '|', ']', 'eye'],
        'j': ['J', ']', '¿', '_|', '_/', '</', '(/'],
        'k': ['K', 'X', '|<', '|{', '|('],
        'l': ['L', '|', '1', '£', '|_', '1_'],
        'm': ['M', '|v|', '|\/|', '/\/\\', '(v)', '/|\\', '//.', '^^', 'em'],
        'n': ['N', '|\|', '/\/', '[\]', '/V', '^/'],
        'o': ['O', '0', '()', '[]', 'oh'],
        'p': ['P', '|*', '|o', '|"', '|>', '9', '|7', '|^(o)'],
        'q': ['Q', '9', '0_', '()_', '(_,)', '<|'],
        'r': ['R', '2', '/2', '12', 'I2', 'l2', '|^', '|?', 'lz'],
        's': ['S', '5', '$', 'z', 'es'],
        't': ['T', '7', '+', '-|-', '\'][\''],
        'u': ['U', '|_|', '(_)', 'L|', 'v'],
        'v': ['V', '\/', '^'],
        'w': ['W', 'VV', '\/\/', '\\\'', '\'//', '\|/', '\^/', '(n)'],
        'x': ['X', '%', '*', '><', '}{', ')(', 'ecks'],
        'y': ['Y', '¥', 'J', '\'/', 'j'],
        'z': ['Z', '2', '7_', '~/_', '>_', '%'],
    }

    low_pass = password.lower()
    #  Replace each character 1 by 1
    for i, char in enumerate(low_pass):
        tmp_pass = password
        if char in leetDict.keys():
            for replacement in leetDict[char]:
                ret_list.append('{}{}{}'.format(tmp_pass[:i], replacement, tmp_pass[i+1:]))
    #  TODO Replace all of same character
    for char in low_pass:
        if char in leetDict.keys():
            for replacement in leetDict[char]:
                tmp_pass = password
                ret_list.append(tmp_pass.replace(char, replacement))
                ret_list.append(tmp_pass.replace(char.upper(), replacement))
    ret_list.sort()
    return ret_list

def gen_file(first_name='', last_name='', date_of_birth='', telephone_number='', street='', apt_num='', city='', state='', zip_code='', email=''):
    inputs = []
    possible_emails = remove_email_domain(email)
    first_six_tele = telephone_number[:7]
    first_six_tele = first_six_tele.replace('-','')
    possible_street_address = split_street_address(street)

    if apt_num == "NA":
        inputs = [first_name, last_name, date_of_birth, telephone_number, state, zip_code, date_of_birth[-4:], date_of_birth[-2:], first_six_tele, telephone_number[-4:]]
    else:
        inputs = [first_name, last_name, date_of_birth, telephone_number, apt_num, city, state, zip_code, date_of_birth[-4:], date_of_birth[-2:], first_six_tele, telephone_number[-4:]]

    for item in possible_street_address:
        inputs.append(item)

    for item in possible_emails:
        inputs.append(item)

    passwords = []
    for item in inputs:
        passwords += leetize_me_captain(item)
        passwords.append(item)
    passwords = list(set(passwords))
    passwords.sort()
    with open(args.o, 'w', newline='') as f:
        writer = csv.writer(f, delimiter=' ')
        for pw in passwords:
            writer.writerow([pw])
    return passwords


if __name__ == '__main__':
    # Get user's personal information
    first_name = input("First Name: ")
    last_name = input("Last Name: ")
    date_of_birth = input("Date of Birth (Format: MM/DD/YYYY): ")
    telephone_number = input("Telephone Number (Format: xxx-xxx-xxxx):")
    street = input("Street number and name: ")
    apt_num = input("APT No. (If not applicable enter NA): ")
    city = input("City: ")
    state = input("State: ")
    zip_code = input("Zip Code (first 5 digit): ")
    email = input("Email ID: ")

    passwords = gen_file(first_name=first_name, last_name=last_name, date_of_birth=date_of_birth, telephone_number=telephone_number, apt_num=apt_num, city=city, state=state, zip_code=zip_code, first_six_tele=first_six_tele)

    print("List of common passwords with the given information: ")
    print(*passwords, sep = "\n")
