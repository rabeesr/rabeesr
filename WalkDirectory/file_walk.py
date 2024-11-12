#The os.walk method will print all directories and subdirectories and is native python

import os
import sys

def print_sub_dir(path, spaces=''):
    #set the name of the root file, by finding the last slash
    name = path[path.rfind('/') +1 :]
    #add the appropriate number of spaces if the file is a child file
    print_friendly_name = spaces + name + '/'
    print(print_friendly_name)
    #try except block to recursively check file directory and print all child files
    try:
        #check each subdirectory or file under the parent file
        for dir in os.listdir(path):
            test_path = path + '/' + dir
            #if it is a directory i.e. folder, call function recursively
            if os.path.isdir(test_path):
                spaces2 = spaces + '   '
                print_sub_dir(test_path, spaces2)
            #if it is a file, then just print the file name with the appropriate number of spaces
            elif os.path.isfile(test_path):
                name2 = '   ' + spaces + dir
                print(f'{name2}')
        #catch exceptions in case the file cannot be opened or there is an error with checking its path
    except:
        print('Sorry Path not found. Please make sure the specified path exists')

def main():
    #path = '/Users/Rabees/Library/Mobile Documents/com~apple~CloudDocs/Development/ConceptsProgramming/assignment_4_rrafiq0'
    try:
        #print subdirectory for first argument after calling function
        print_sub_dir(sys.argv[1])
    except:
        #return this message if the subdirectory could not be found.
        print('Sorry Path not found. Please make sure the specified path exists. Use "./" to scan the current directory')

if __name__ == '__main__':
    main()


# Specify the directory path you want to start from