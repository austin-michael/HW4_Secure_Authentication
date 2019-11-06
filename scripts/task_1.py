#!/usr/bin/env python3
from itertools import product, permutations
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
                    default='./ELCP-1.txt')
args = parser.parse_args()

def smart_pass_permuations(password=None):
    final_list = [password]
    if password is not None and len(password) > 0:
        functions = {
            'a': repeat_pass,
            'b': reverse_pass,
            'c': quick_adjust_pass,
            'd': leetize_me_captain,
        }
        for fw, fx, fy, fz in permutations(functions.values()):
            pw_list = fw(password)
            tmp_list = []
            for func, pw in product([fx, fy, fz], pw_list):
                tmp_list += func(pw)
            final_list += tmp_list
        final_list = list(set(final_list))
        print(len(final_list))
        return final_list
        pass

def repeat_pass(password):
    ret_list = []
    ret_list.append('{}{}'.format(password, password))
    ret_list.append('{}{}{}'.format(password, password, password))
    return ret_list

def reverse_pass(password):
    return [password[::-1]]

def quick_adjust_pass(password):
    ret_list = []
    ret_list += capitalize_first(password)
    ret_list += permute_basic_chars(password)
    ret_list += permute_basic_chars(capitalize_first(password)[0])
    return ret_list

def capitalize_first(password):
    return [password.title()]

def permute_basic_chars(password):
    ret_list = []
    COMMON_CHARS = ['!', '?', '@', '#', '$', '%', '^', '&', '*', '(', ')']
    for n, c in product(range(10), COMMON_CHARS):
        ret_list.append('{}{}'.format(password, n))
        ret_list.append('{}{}'.format(password, c))
        ret_list.append('{}{}{}'.format(password, n, c))
        ret_list.append('{}{}{}'.format(password, c, n))
    return ret_list

def leetize_me_captain(password):
    ret_list = []
    leetDict = {
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


if __name__ == '__main__':
    password_list = []
    final_list = []
    if len(args.f) > 0:
        with open(args.f, newline='') as f:
            reader = csv.reader(f)
            for row in reader:
                password_list.append(row[0])
                final_list.append(row[0])
            f.close()
    for password in password_list:
        final_list += smart_pass_permuations(password=password)
    final_list.sort()
    with open(args.o, 'w', newline='') as f:
        writer = csv.writer(f, delimiter=' ')
        for pw in final_list:
            writer.writerow([pw])

    # from IPython import embed
    # embed()



"""
These top 30 passwords were obtained from wikipedia (https://en.wikipedia.org/wiki/List_of_the_most_common_passwords) using the top 25 lists from the last 8 years.
Most frequent passwords were obtained by frequency.

Number  Password        Total Instances     Percentage
1. 		123456 		    8                   3.9604
2. 		1234567 	    8                   3.9604
3. 		abc123 		    8                   3.9604
4. 		12345678 	    8                   3.9604
5. 		qwerty 		    8                   3.9604
6. 		password 	    8                   3.9604
7. 		football 	    7                   3.4653
8. 		monkey 		    7                   3.4653
9. 		12345 		    6                   2.9703
10. 	letmein 	    6                   2.9703
11. 	master 		    6                   2.9703
12. 	111111 		    6                   2.9703
13. 	dragon 		    6                   2.9703
14. 	123123 		    6                   2.9703
15. 	trustno1 	    5                   2.4752
16. 	sunshine 	    5                   2.4752
17. 	iloveyou 	    5                   2.4752
18. 	123456789 	    5                   2.4752
19. 	welcome 	    5                   2.4752
20. 	admin 		    4                   1.9802
21. 	princess 	    4                   1.9802
22. 	password1 	    4                   1.9802
23. 	passw0rd 	    4                   1.9802
24. 	1234 		    4                   1.9802
25. 	baseball 	    4                   1.9802
26. 	shadow 		    4                   1.9802
27. 	1234567890 	    3                   1.4851
28. 	michael 	    3                   1.4851
29. 	login 		    3                   1.4851
30. 	a 			    2                   0.9901 
"""
