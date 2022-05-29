import sys
import ipaddress
from os.path import exists

args = {    'f' : '',
            'a' : '',
            's' : '',
            'c' : '',
            'i' : '',   }

# GET COMMAND LINE ARGUMENTS
def get_args():
    for arg in args:

        # input parameter format
        format = '-' + arg

        # get value of parameter
        if format in sys.argv:
            # index of argument
            index = sys.argv.index(format)
            # parsing value
            if index + 1 == len(sys.argv):
                continue
            if sys.argv[index + 1][1:] in args:
                continue
            else: args[arg] = sys.argv[index + 1]

    return args

# PRINT COMMAND LINE ARGUMENTS
def print_args(arguments):
    for arg in arguments:
        print('-'+arg,':',arguments[arg])

# CHECK IF ARGUMENTS HAVE VALUES
def check_args(arguments):
    for arg in arguments:

        if not arguments[arg]:
            print(arg, "has no value!")
            sys.exit()

        if arg == 'f' and not exists(arguments[arg]):
            print("file does not exist!")
            sys.exit()

        if arg == 'a':
            try: ipaddress.ip_address(arguments[arg])
            except ValueError:
                print("Not a valid IP address!")
                sys.exit()

        if arg == 's' and not arguments[arg].isnumeric():
            print(arg,": Not a valid Port!")
            sys.exit()

        if arg == 'c' and not arguments[arg].isnumeric():
            print(arg,": Not a valid Port!")
            sys.exit()

        if arg == 'i' and not arguments[arg].isalnum():
            print("Not a valid ID!")
            sys.exit()