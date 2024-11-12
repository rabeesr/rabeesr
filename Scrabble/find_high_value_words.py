import re
import words
import itertools

# 1st pattern to detect from user
PATTERN1 = r'^[a-zA-Z]*$'
# 2nd pattern words seperated by spaces
PATTERN2 = r'([A-Za-z] )+[A-Za-z]*$'
# 3rd pattern words seperated by commas
PATTERN3 = r'([A-Za-z],)+[A-Za-z]*$'

# preprocess the scrabble word file and store in a list of valid words
def preprocess_scrabble_list():
    with open('./scrabble_list.txt', 'r') as word_list:
        scrabble_list = word_list.read().split()
    return scrabble_list

# preprocess user input and detect appropriate pattern using regex
def preprocess_user_input(user_input):
    array_of_letters = []
    # check to see which pattern the user input matches
    check_1 = re.match(PATTERN1, user_input)
    check_2 = re.match(PATTERN2, user_input)
    check_3 = re.match(PATTERN3, user_input)
    # if it doesn't match any of the 3 patterns, then raise an exception that can be caught in a try-except block
    if not(check_1 or check_2 or check_3):
        raise ValueError('Bad Input')
    #store the characters in an array based on input pattern 
    elif check_1:
        for char in user_input:
            array_of_letters.append(char)
    # empty spaces case
    elif check_2:
        for char in user_input:
            if char != ' ':
                array_of_letters.append(char)
    # commas
    elif check_3:
        for char in user_input:
            if char != ',':
                array_of_letters.append(char)
    return array_of_letters

# create permutations of any length based on the user input
def create_permutations(list_of_char, list_of_scrabble_words):
    word_dictionary = {}
    # cycle through array of possible lengths of words
    for i in range(0,len(list_of_char)-1):
        list_of_valid_words = []
        # create permutations of all the letters
        perm = list(itertools.permutations(list_of_char, i+2))
        # combine the letters into words and check to see if they are in the list of scrable words
        for tup in perm:
            word = ''
            for letter in tup:
                word += letter
            if str(word).upper() in list_of_scrabble_words:
                # append all valid words into the list of valid words
                list_of_valid_words.append(word)
            #store the list of valid words for each length of word
        word_dictionary[str(i+2) + ' Letter Words'] = list_of_valid_words
    return word_dictionary

# helper function to write the final results into a file
def wrt_to_file(filename, dictionary_of_words):
    x2 = open(filename, 'w')
    for a in dictionary_of_words:
        x2.write('\n' + a + '\n')
        if dictionary_of_words[a] != []:
            scored_list = words.calc_score_each_word(dictionary_of_words[a])
            words.sort_by_score(scored_list)
            for word in scored_list[0:16]:
               x2.write('    ' + word[0] + ' -> ' + str(word[1]) + '\n')
        else:
            x2.write('    NO WORDS')
    x2.close()

#main driver which calls the functions in the appropriate order to determine the scrabble words
def main():
    enter = input('>Enter each letter in your rack: ')
    try:
        lst_char = preprocess_user_input(enter)
    except:
        print('This is a bad input, please try with only letters, spaces, or commas.')
    else:
        scrabble_words = preprocess_scrabble_list()
        dic_words = create_permutations(lst_char, scrabble_words)
        print(dic_words)
        for len_word in dic_words:
            print(len_word)
            if dic_words[len_word] != []:
                scored_list = words.calc_score_each_word(dic_words[len_word])
                words.sort_by_score(scored_list)
                for word in scored_list:
                    print('    ' + word[0] + ' -> ' + str(word[1]))
            else:   
                print('    NO WORDS')

        wrt_to_file('./possible_scrabble_words', dic_words)

if __name__ == '__main__':
    main()