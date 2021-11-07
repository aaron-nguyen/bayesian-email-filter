import pandas as pd
import numpy as np
import json

'''
This is the word counter file.
It will:
            - Load/save dictionary of over 3000 words.
            - Count number of appearance for each word in ham and spam emails.
            - Output the probability of each words being spam/ham.
'''

class WordCounter:

    def __init__(self, file_available):
        super().__init__()
        self.number_of_spam = 0
        self.number_of_ham = 0
        if file_available == False:
            self.create_dictionary()        
        else:
            self.read_dictionary()

    def create_dictionary(self, path = 'dictionary.txt'):
        with open(path) as f:
            wordlist = f.readlines()
        
        self.word_list = ''.join(wordlist).strip().split('\n')

        word_dictionary = dict.fromkeys(self.word_list, 0)

        self.ham_word = word_dictionary.copy()
        self.spam_word = word_dictionary.copy()

        white = json.dumps(word_dictionary)

        # open file for writing, "w" 
        f = open("ham_word.json","w")
        f.write(white)

        f2 = open("spam_word.json","w")
        f2.write(white)

        # close file
        f.close()
        f2.close()

    def save_dict(self):
        ham = json.dumps(self.ham_word)
        spam = json.dumps(self.spam_word)

        # open file for writing, "w" 
        f1 = open("ham_word.json","w")
        f1.write(ham)

        f2 = open("spam_word.json","w")
        f2.write(spam)

        f = open("spamonham.txt","w")
        f.write(f"{self.number_of_spam}/{self.number_of_ham}")

        # close file
        f.close()
        f1.close()
        f2.close()

    def read_dictionary(self):
        with open("ham_word.json") as f:
            self.ham_word = json.load(f)
        with open("spam_word.json") as f:
            self.spam_word = json.load(f)
        with open("spamonham.txt") as f:
            lines = f.readlines()
        
        self.word_list = list(self.ham_word.keys())
        a, b = ''.join(lines).split('/')
        self.number_of_ham = int(b) 
        self.number_of_spam = int(a)

    def update_word(self, word, spam):
        if word in self.word_list:
            if spam:
                self.spam_word[word] += 1
            else:
                self.ham_word[word] += 1

    def update_email(self, spam):
        if spam:
            self.number_of_spam += 1
        else:
            self.number_of_ham += 1

    def get_ham_prob(self, word):
        if word in self.word_list:
            return (self.ham_word[word] + 1)/ (self.number_of_ham + 2)
        else:
            return -1

    def get_spam_prob(self, word):
        if word in self.word_list:
            return (self.spam_word[word] + 1)/ (self.number_of_spam + 2)
        else:
            return -1