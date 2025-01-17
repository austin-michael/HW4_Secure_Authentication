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
    ret_lst = []
    #  Special chars allowed in email !#$%&'*+-/=?^_`{|}~
    for char in ['!', '#', '$', '%', '&', '\'', '*', '+', '-', '/', '=', '?', '^', '_', '`', '{', '|', '}', '~']:
        ret_lst += temp_email.split(char)
    return ret_lst

def split_street_address(street):
    return street.split(' ')

def leetize_me_captain(password):
    ret_list = [password]
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

def capitalize_nth(s, n):
    return s[:n].lower() + s[n:].capitalize()

def caseChanger(password): #TODO update this so multiple characters will be capitalized at the same time
    ret_list = []
    low_pass = password.lower()
    ret_list.append(low_pass)
    ret_list.append(password.upper())
    i = 0
    while i < len(low_pass):
        ret_list.append(capitalize_nth(low_pass, i))
        i += 1
    return ret_list

def gen_file(first_name='', last_name='', date_of_birth='', telephone_number='', street='', apt_num='', city='', state='', zip_code='', email=''):
    possible_emails = remove_email_domain(email)
    first_six_tele = telephone_number[:7]
    first_six_tele = first_six_tele.replace('-','')
    possible_street_address = split_street_address(street)
    flName = first_name + last_name
    lfName = last_name + first_name
    fNameDOBYY = first_name + date_of_birth[-2:]
    lNameDOBYY = last_name + date_of_birth[-2:]
    fNameDOBYYYY = first_name + date_of_birth[-4:]
    lNameDOBYYYY = last_name + date_of_birth[-4:]

    charCaseChanger = [first_name, last_name, city, state]

    inputs = {
        'first_name': [first_name],
        'last_name': [last_name],
        'date_of_birth': [date_of_birth],
        'telephone_number': [telephone_number],
        'city': [city],
        'state': [state],
        'zip_code': [zip_code],
        'birth_year': [date_of_birth[-4:]],
        'shortened_birth_year': [date_of_birth[-2:]],
        'first_six_of_telephone': [first_six_tele],
        'telephone_number': [telephone_number[-4:]],
        'first_and_last': [flName],
        'last_and_first': [lfName],
        'first_name_and_shortened_birth_year': [fNameDOBYY],
        'last_name_and_shortened_birth_year': [lNameDOBYY],
        'first_name_and_birth_year': [fNameDOBYYYY],
        'last_name_and_shortened_birth_year': [lNameDOBYYYY],
    }
    if apt_num not in ['NA', 'N/A', 'na', 'n/a']:
        inputs['apartment_number'] = [apt_num]

    inputs['street_address'] = []
    for i, item in enumerate(possible_street_address):
        inputs['street_address'].append(item)

    inputs['email_address'] = []
    for i, item in enumerate(possible_emails):
        inputs['email_address'].append(item)

    passwords = {}
    for key, lst in inputs.items():
        passwords[key] = []
        for item in lst:
            passwords[key] += leetize_me_captain(item)
    for key, lst in inputs.items():
        passwords[key] = list(set(passwords[key]))
        passwords[key].sort()
    with open(args.o, 'w', newline='') as f:
        writer = csv.writer(f, delimiter=',')
        for key, lst in passwords.items():
            for pw in lst:
                writer.writerow([key.replace('_', ' '), pw])
                writer.writerow([key.replace('_', ' '), pw.lower()])
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

    passwords = gen_file(
        first_name=first_name,
        last_name=last_name,
        date_of_birth=date_of_birth,
        telephone_number=telephone_number,
        apt_num=apt_num,
        city=city,
        state=state,
        zip_code=zip_code,
        email=email
    )

    print("List of common passwords with the given information: ")
    print(*passwords, sep = "\n")
    print(caseChanger("password"))
