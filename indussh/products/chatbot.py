import random
import re

import tensorflow as tf
import numpy as np
import nltk
from nltk.stem.lancaster import LancasterStemmer


class Chatbot:
    ERROR_THRESHOLD = 0.50

    def __init__(self, model, intents, training_data):
        self.stemmer = LancasterStemmer()
        self.intents = intents
        self.model = model

        self.words = training_data['words']
        self.documents = training_data['documents']
        self.classes = training_data['classes']

        self.context = {}
        self.__bot_offers = []
        self.__user_offers = []

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

    def extract_amount(self, sentence):
        sentence = sentence.lower()
        # This regular expression will filter out amounts from the sentence like:
        # rs. 400 or rs400 rs 400
        amount = re.findall(r'rs\s?\.?([0-9]+\.?[0-9]+)', sentence)[0]
        return int(amount)

    def generate_offer(self, min_price, original_price, user_price):
        if (user_price > min_price) and (user_price <= original_price):
            print('Done Deal')
        elif user_price < min_price:
            # If it's the first user offer and bot hasn't offered yet then
            if len(self.__user_offers) == 1 and len(self.__bot_offers) == 0:
                offer = self.compute_offer(min_price, user_price)
            # If the bot has made any offers then compute the offer relative to the last offer
            elif len(self.__bot_offers) > 0:
                offer = self.compute_offer(min_price, self.__bot_offers[-1])
            elif len(self.__user_offers) > 1:
                offer = self.compute_offer(min_price, self.__user_offers[-1])

            return offer

    def compute_offer_price(min_price, price):
        # Compute an offer relative to previous offered price or user offer
        offer = random.randint(min_price, price)
        # Round the offer amount to the nearest 10
        offer = offer - (offer % 10)
        return offer

    def response(self, sentence, user_id, show_details=False):
        results = self.classify(sentence)
        # if we have a classification then find the matching intent tag
        if results:
            # loop as long as there are matches to process
            while results:
                for i in self.intents['intents']:
                    # find a tag matching the first result
                    if i['tag'] == results[0][0]:
                        # set context for this intent if necessary
                        if 'context_set' in i:
                            if show_details:
                                print('context:', i['context_set'])
                            self.context[user_id] = i['context_set']

                        # check if this intent is contextual and applies to this user's conversation
                        if not 'context_filter' in i or \
                                (user_id in self.context and 'context_filter' in i and i['context_filter'] == self.context[user_id]):
                            if show_details:
                                print('tag:', i['tag'])
                            # a random response from the intent
                            return print(random.choice(i['responses']))

                results.pop(0)
