import re
def points_for_letter(letter):
    """Return the points as an integer for a given letter according to Scrabble
    letter frequency tables.
    """  
    
    # Dictionary to look up the point value for each letter. In the dictionary,
    # the key is the letter and the value is the point value
    tile_score = {"a": 1, "c": 3, "b": 3, "e": 1, "d": 2, "g": 2,
                 "f": 4, "i": 1, "h": 4, "k": 5, "j": 8, "m": 3,
                 "l": 1, "o": 1, "n": 1, "q": 10, "p": 3, "s": 1,
                 "r": 1, "u": 1, "t": 1, "w": 4, "v": 4, "y": 4,
                 "x": 8, "z": 10}
    
    return tile_score[letter]

def preprocess_wordfile(filename):
    list_of_words = list()
    try:
        f1 = open(filename, 'r')
    except:
        print('Could not open the file. Please make sure the filename is correct and it is in the appropriate directory')
    else:
        #store each word in the list, remove new lines and split based on the pipe character
        for line in f1:
            l2 = line.strip('\n').split(' | ')
            #check for empty words or words with only spaces/empty characters
            if not(re.match(r'^[ +]', l2[0])) and l2[0] != '':
                list_of_words.append(l2[0])
        f1.close()
        list_of_words.sort()
    return list_of_words

def calc_score_each_word(list):
    list_of_word_score = []
    for x in list:
        word_score = 0
        #print(x)
        for c in x:
          #print(c)
          try:
            point = points_for_letter(c.lower())
            word_score = word_score + point
          except:
              continue
        list_of_word_score.append((x, word_score))
    return list_of_word_score

def sort_by_score(list):
    list.sort(key=lambda tup: tup[1], reverse = True)

def wrt_to_file(filename, list_of_words):
    x2 = open(filename, 'w')
    for word in list_of_words:
        x2.write(word[0] + ' -> ' + str(word[1]) + '\n')
    x2.close()

