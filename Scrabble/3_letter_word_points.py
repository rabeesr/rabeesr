import words

def main():
    """Main driver for your program"""
    # preprocess 3_letter_words file and store in a list
    list_of_words = words.preprocess_wordfile('./3_letter_words.txt')
    # calculate the score for each word in thee list
    words_with_scores = words.calc_score_each_word(list_of_words)
    words.sort_by_score(words_with_scores)
    words.wrt_to_file('./scrabble_word_scores.txt', words_with_scores)


if __name__ == "__main__":
    main()

