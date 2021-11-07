import os
from emailreader import EmailReader
from wordcount import WordCounter

class BayesianAgent:

    def __init__(self):
        super().__init__()
        self.reader = EmailReader()
        
        if "ham_word.json" in os.listdir() and "spam_word.json" in os.listdir() and "spamonham.txt" in os.listdir():
            self.wordy = WordCounter(file_available=True)
        else:
            self.wordy = WordCounter(file_available=False)
            self.load_weight()

    def load_weight(self):
        # Load data from emails
        ham_vec = [self.word.text2vec(self.word.html_to_plain(self.word.load_email(is_spam=False, filename=name))) for name in self.word.ham_filenames]
        spam_vec = [self.word.text2vec(self.word.html_to_plain(self.word.load_email(is_spam=True, filename=name))) for name in self.word.spam_filenames]

        # Count appearance
        for ham in ham_vec:
            for word in ham:
                self.wordy.update_word(word, False)
            self.wordy.update_email(False)

        for spam in spam_vec:
            for word in spam:
                self.wordy.update_word(word, True)
            self.wordy.update_email(True)
        
        # Save updated data
        self.wordy.save_dict()


    def predict(self, text):

        vec = self.reader.text2vec(text)

        prob_spam = self.wordy.number_of_spam / (self.wordy.number_of_ham + self.wordy.number_of_spam)
        prob_ham = self.wordy.number_of_ham / (self.wordy.number_of_ham + self.wordy.number_of_spam)

        prob_word_spam = 1
        prob_word_ham = 1

        for v in vec:
            hammy = self.wordy.get_ham_prob(v)
            spammy = self.wordy.get_spam_prob(v)

            if hammy != -1 and spammy != -1:
                prob_word_ham *= hammy
                prob_word_spam *= spammy

        prob = (prob_spam * prob_word_spam) / ((prob_spam * prob_word_spam) + (prob_ham * prob_word_ham))

        print(prob) 
        if prob > 0.5:
            print("Spam")
        else: 
            print('Ham')
