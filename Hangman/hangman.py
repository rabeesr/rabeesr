from word_file_preprocessor import *
import random

#import and store the list of words from module 3 using the preprocessor that was created in module 3.
LIST_OF_WORDS = process_file('./common_words.txt')[1]
#create a function to randomly pick a word from the list
def pick_word(words:list):
    """Picks a random word from the supplied list"""
    i = random.randrange(0, len(words))
    return words[i]

def play_hangman(word:str):
    #track the number of wrong and right answers to know when to break out of the while loop
    wrong_answers = 0
    right_answers = 0
    #translate all characters in the word to upper case for comparison
    chars = [c.upper() for c in word]
    guess = []
    #create a string with the number of underscores representing the length of the string.
    for z in range(0,len(word)):
        guess.append('_')
    #commenting out the next two lines as they were only used for debugging
    #print(word)
    #print(chars)
    #if the user guesses incorrectly 5 times then exit out the while loop and let them know they lost
    while wrong_answers <= 4:
        #prompt user for input
        a = input('>>> Guess a letter? ').upper()
        temp_str = ''
        #check to ensure it is only a single character
        if len(a) > 1:
            print('Sorry, please enter a single character only. Try again!')
        #if a is found in the characters, then find the index and replace the underscore in guess, increment right answers by 1, 
        #and allow user to guess word. Break out of while loop if user successfully guesses the word
        elif a in chars:
            i = chars.index(a)
            right_answers +=1
            guess[i] = a.upper()
            for c in guess:
                temp_str = temp_str + c
            print(f'{a} is in the word {temp_str}')
            chars[i] = '_'
            if right_answers != len(word):
                b = input('Try and guess the word. ')
                if b.upper() == word.upper():
                    print(f'Congratulations!\nThe word was {word.upper()}')
                    break
        #if user guesses incorrectly increment wrong answers by 1 and return to the user.
        else:
            wrong_answers += 1
            print(f'{a} is not in the word.\n You have {5-wrong_answers} guesses remaining.')
        #if user guesses all the characters then they won, return the final word.
        if right_answers == len(word):
            print(f'Congratulations!\nThe word was {word.upper()}')
            break
    if wrong_answers == 5:
        print(f'Sorry - you lose!\nThe word was {word.upper()}')

#main program code to run the standalone program. 
def main():
    print("Let's Play Hangman ¯\_(ツ)_/¯")
    a = 'y'
    #keep playing until user does not enter y.
    while a.lower() == 'y':
        word = pick_word(LIST_OF_WORDS)
        play_hangman(word)
        a = input('Would you like to play again (y/n)? ')
    

if __name__ == '__main__':
    main()
