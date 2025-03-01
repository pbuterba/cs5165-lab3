"""
@package    lab3-docker
@brief      Script to perform the basic tasks of Project 3 - Docker

@date       2/28/2025
@updated    2/28/2025

@author     Preston Buterbaugh
"""
# Imports
import subprocess
import sys
from typing import List, Dict, Tuple, Union

# Constants
NUM_WORDS_TRACKED = 3


def main() -> int:
    """
    @brief  Main function
    @return (int)
        - 0 if returned successfully
        - 1 otherwise
    """
    # Open files
    if_file = open('/home/data/IF-1.txt', 'r')
    always_file = open('/home/data/AlwaysRememberUsThisWay-1.txt', 'r')

    # Count words
    if_word_frequencies = {}
    if_word_count = 0
    top_if_words = []
    always_word_frequencies = {}
    always_word_count = 0
    top_always_words = []
    total_word_count = 0

    # Count if words
    for line in if_file:
        words = line.split(' ')
        for word in words:
            word = sanitize(word.lower())
            if len(word) > 0:
                if_word_frequencies, if_word_count, top_if_words = count_word(word, if_word_frequencies, if_word_count, top_if_words)
                total_word_count = total_word_count + 1

    print('FILE SWITCH')

    # Count always words
    for line in always_file:
        words = line.split(' ')
        for word in words:
            word = sanitize(word.lower())

            if "'" in word:
                contraction_words = expand_contraction(word)
                if contraction_words is None:
                    print(f'WARNING! Uncaught contraction {word}')
                    always_word_frequencies, always_word_count, top_always_words = count_word(word, always_word_frequencies, always_word_count, top_always_words)
                    total_word_count = total_word_count + 1
                else:
                    always_word_frequencies, always_word_count, top_always_words = count_word(contraction_words[0], always_word_frequencies, always_word_count, top_always_words)
                    always_word_frequencies, always_word_count, top_always_words = count_word(contraction_words[1], always_word_frequencies, always_word_count, top_always_words)
                    total_word_count = total_word_count + 2
            elif len(word) > 0:
                always_word_frequencies, always_word_count, top_always_words = count_word(word, always_word_frequencies, always_word_count, top_always_words)
                total_word_count = total_word_count + 1

    # Close files
    if_file.close()
    always_file.close()

    # Get IP address
    ip_address = subprocess.check_output(['ip', 'addr', 'show'])

    # Write output
    out_file = open('/home/data/output/result.txt', 'w')

    # Write if file results
    out_file.write(f'IF-1.txt: {if_word_count} words\n    Most common words:')
    for i, word in enumerate(top_if_words):
        out_file.write(f'\n    {i + 1}. {word} ({if_word_frequencies[word]} occurrences)')

    # Write always file results
    out_file.write(f'\n\nAlwaysRememberUsThisWay-1.txt: {always_word_count} words\n    Most common words:')
    for i, word in enumerate(top_always_words):
        out_file.write(f'\n    {i + 1}. {word} ({always_word_frequencies[word]} occurrences)')

    # Write total count
    out_file.write(f'\n\nTotal word count (across both files): {total_word_count}')

    # Write IP Address
    out_file.write(f'\n\nContainer IP Address: {ip_address}')

    out_file.close()

    # Print output
    out_file = open('/home/data/output/result.txt', 'r')
    for line in out_file:
        print(line, end='')
    print()
    out_file.close()

    return 0


def sanitize(word: str) -> str:
    """
    @brief  Sanitizes a word to remove trailing commas and newlines
    @param  word (str): The word to sanitize
    @return (str) The sanitized word
    """
    starting_characters = ["'"]
    ending_characters = ["'", '\n', ',', ':', ';', '!']
    if len(word) == 0:
        return ''
    if word[0] in starting_characters:
        return sanitize(word[1:])
    if word[len(word) - 1] in ending_characters:
        return sanitize(word[0:len(word) - 1])
    return word


def count_word(word: str, word_frequencies: Dict, word_count: int, top_words: List) -> (Dict, int, List):
    """
    @brief  Counts a word and updates the corresponding word frequencies entry, total word count, and top words list
    @param  word             (str):  The word to count
    @param  word_frequencies (Dict): The existing word frequency dictionary
    @param  word_count       (int):  The current word count
    @param  top_words        (List): The current list of top words
    @return:
        - (Dict) The updated word frequency dictionary
        - (int)  The updated word count
        - (List) The updated list of top words
    """
    # Increment word count
    if word in word_frequencies.keys():
        word_frequencies[word] = word_frequencies[word] + 1
    else:
        word_frequencies[word] = 1

    # Check if now top word
    if len(top_words) < NUM_WORDS_TRACKED and word not in top_words:
        top_words.append(word)
    elif word not in top_words and word_frequencies[word] > word_frequencies[top_words[NUM_WORDS_TRACKED - 1]]:
        top_words[NUM_WORDS_TRACKED - 1] = word

    if word in top_words:
        top_words.sort(key=lambda top_word: word_frequencies[top_word], reverse=True)

    word_count = word_count + 1

    return word_frequencies, word_count, top_words


def expand_contraction(contraction: str) -> Union[Tuple[str, str], None]:
    """
    @brief  Expands a contraction into its component words
    @param  contraction (str): The contraction to expand
    @return
        - (str, str): The component words of the contraction
        - (None): If the contraction is not in the existing list of contractions
    """
    contractions = {
        "it's": ('it', 'is'),
        "couldn't": ('could', 'not'),
        "i'm": ('i', 'am'),
        "can't": ('can', 'not'),
        "won't": ('will', 'not'),
        "i'll": ('i', 'will'),
        "don't": ('do', 'not'),
        "you're": ('you', 'are'),
        "that's": ('that', 'is')
    }
    if contraction in contractions.keys():
        return contractions[contraction]
    else:
        return None


if __name__ == '__main__':
    sys.exit(main())
