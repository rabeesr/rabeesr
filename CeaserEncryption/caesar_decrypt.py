from caesar_encrypt import *
from problem4 import *


#read in and parse the common_words.txt file and create a list of common words
filename = 'common_words.txt'
t1 = process_file(filename)
list_of_common_words = t1[1]
maxKey = 1

#My approach to this was to start with a key of 1 and cycle all the way to 26. 
# The decryption key with the most words matched in the common words file is the key that is likely going to be used to decypt the message
s = 'mpwtpgp jzf nly lyo jzf lcp slwqhlj espcp'
empty_dict = {}
for i in range(1,27):
    counter = 0
    decrypted_string = caesar_decrypt(i, s)
    for word in decrypted_string.split():
        if word in list_of_common_words:
            counter += 1
    empty_dict[i] = counter

#check for which key has the greatest number of matches in the common words file.
for i in empty_dict:
    if empty_dict[i] > empty_dict[maxKey]:
        maxKey = i

#print final result
print('The decrypted phrase is likely:','"',caesar_decrypt(maxKey, s),'"',"with a key value of:",maxKey)