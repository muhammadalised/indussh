import random
import re

import tensorflow as tf
import numpy as np
import nltk
from nltk.stem.lancaster import LancasterStemmer


class ChatBot:
    ERROR_THRESHOLD = 0.50

    def __init__(self, model, intents, training_data):
        self.stemmer = LancasterStemmer()
        self.intents = intents
        self.model = model

        # self.words = training_data['words']
        # self.documents = training_data['documents']
        # self.classes = training_data['classes']

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

    def generate_offer(self, min_price, original_price, user_price=None):

        # If the offer isn't made by the user then let the bot generate offer
        if user_price is None:
            # If user hasn't made any offer at all then bot will generate the offer b/w min price and original price
            if len(self.__user_offers) <= 0 and len(self.__bot_offers) <= 0:
                offer = self.compute_offer_price(min_price, original_price)
            else:  # The bot will generate the offer amount between minimum price and the last bot offer price
                offer = self.compute_offer_price(
                    min_price, self.__user_offers[-1])
            # keep track of offers made by the bot
            self.__bot_offers.append(offer)
        # If the user has made an offer then evaluate it accordingly
        elif user_price is not None:
            if (user_price > min_price) and (user_price <= original_price):
                self.__user_offers.append(user_price)
                # Return the user price as the offer
                return user_price
            elif user_price < min_price:  # if the user price is lesser even then the min price
                # Append the user offers to keep track of them
                self.__user_offers.append(user_price)
                offer = self.compute_offer_price(
                    min_price, self.__user_offers[-1])
                self.__bot_offers.append(offer)

        return offer

    def compute_offer_price(self, min_price, price):
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
