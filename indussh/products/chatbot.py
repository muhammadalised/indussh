import pickle
import json
import random
import re

import tensorflow as tf
import numpy as np
import nltk
from nltk.stem.lancaster import LancasterStemmer


class Chatbot:
    ERROR_THRESHOLD = 0.65

    def __init__(self, model, intents, training_data):
        self.stemmer = LancasterStemmer()
        self.intents = intents
        self.model = model

        self.words = training_data['words']
        self.documents = training_data['documents']
        self.classes = training_data['classes']

    def process_sentence(self, sentence):
        # Tokenize the pattern
        sentence_words = nltk.word_tokenize(sentence)
        # Stem each word
        sentence_words = [self.stemmer.stem(
            word.lower()) for word in sentence_words]
        return sentence_words

    def bag_of_words(self, sentence, words, show_details=False):
        # Tokenize the pattern
        sentence_words = self.process_sentence(sentence)
        # Bag of words
        bag = [0]*len(words)
        for s in sentence_words:
            for i, w in enumerate(words):
                if w == s:
                    bag[i] = 1
                    if show_details:
                        print("found in bag: %s" % w)
        return (np.array(bag))

    def classify(self, sentence):
        # generate probabilities from the model
        p = self.bag_of_words(sentence, self.words)

        d = len(p)
        f = len(self.documents)-2
        a = np.zeros([f, d])
        tot = np.vstack((p, a))

        results = self.model.predict(tot)[0]

        # filter out predictions below a threshold
        results = [[i, r]
                   for i, r in enumerate(results) if r > self.ERROR_THRESHOLD]
        # sort by strength of probability
        results.sort(key=lambda x: x[1], reverse=True)
        return_list = []

        for r in results:
            return_list.append((self.classes[r[0]], r[1]))

        # return tuple of intent and probability
        return return_list

    def response(self):
        pass

    def extract_amount(self, sentence):
        sentence = sentence.lower()
        # This regular expression will filter out amounts from the sentence like:
        # rs. 400 or rs400 rs 400
        amount = re.findall(r'rs\s?\.?([0-9]+\.?[0-9]+)', sentence)[0]
        return int(amount)

    def track_user_offers(self, sentence):
        pass

    def track_bot_offers(self, sentence):
        pass

    def create_offer(self, min_price, original_price, bot_offer_count):
        pass
