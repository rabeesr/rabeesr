#this code was created in module 3 and is used to preprocess the common words file.
def process_file(filename): 
    """Read, sort and return a file""" 
    #open the file
    try:
        f1 = open(filename, 'r')
        #initialize variables
        sorted_items = []
        number_of_lines = 0
        #read all lines into a single string
        f2 = f1.read()
        #convert the string into a list of strings based on a single space while removing any excess whitespace
        sorted_items = f2.strip().split()
        #sort the string alphabetically
        sorted_items.sort()
        #the length of the list is the number of words
        number_of_lines = len(sorted_items)
        f1.close()
    # Return a tuple
        return(filename, sorted_items, number_of_lines)
    except:
        print('There was an error in the program. Please ensure that the filename exists in the current directory or specify the path of the file. If the file exists, ensure it is a text file')