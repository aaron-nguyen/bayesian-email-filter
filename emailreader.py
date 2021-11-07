import pandas as pd
import numpy as np
import os
import email
import email.policy
from bs4 import BeautifulSoup
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import string
import re

'''
This class will:
                    - Convert email from html to plain text
                    - Convert text to vector of distinct words 
'''

class EmailReader:

    def __init__(self, path = ''):
        super().__init__()
        self.path = path
        self.ham_filenames = [name for name in sorted(os.listdir('ham')) if len(name) > 20]
        self.spam_filenames = [name for name in sorted(os.listdir('spam')) if len(name) > 20]

    def load_email(self, filename, is_spam):
        directory = self.path + "spam" if is_spam else self.path + "ham"
        with open(os.path.join(directory, filename), "rb") as f:
            return email.parser.BytesParser(policy=email.policy.default).parse(f)
     
    def html_to_plain(self, email):
        try:
            soup = BeautifulSoup(email.get_content(), 'html.parser')
            return soup.text.replace('\n\n','')
        except:
            return "empty"

    def text2vec(self, text):
        res = re.sub(r'[^\w\s]', ' ', text.lower().strip().replace("\n", ''))
        res = res.translate(str.maketrans('', '', string.punctuation))
        res = ''.join([i for i in res if not i.isdigit()])
        stemmer = nltk.PorterStemmer()
        res = " ".join([stemmer.stem(i) for i in res.split()])
        
        word_tokens = word_tokenize(res)

        filtered_vector = []

        for w in word_tokens:
            if w not in filtered_vector:
                filtered_vector.append(w)

        return filtered_vector