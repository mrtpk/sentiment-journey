from textblob import TextBlob

from utilities.logger import Logger
import json

from naive_bayes import NaiveBayes
from bag_of_words import BagOfWordSentiment

class Comparer():
    def __init__(self, no_of_testcases = 100, verbose=True, nb=None, bw=None):
        self.logger = Logger('Comparer', 'logs\\comparer.log', is_verbose=verbose)
        
        if nb is None:
            self.nb = NaiveBayes(verbose=False, test_set_count=no_of_testcases, no_of_grams=4)
            self.nb.ready()
        else:
            self.nb = nb
            self.nb.logger.is_verbose = False
        
        if bw is None:
            self.bw = BagOfWordSentiment(verbose=False, no_of_grams=4)
            self.bw.ready()
        else:
            self.bw = bw
            self.bw.logger.is_verbose = False

        self.no_of_testcases = no_of_testcases
        self.nb_correct, self.bw_correct, self.tb_correct = 0, 0, 0
        self.nb_wrong, self.bw_wrong, self.tb_wrong = 0, 0, 0
        self.nb_accuracy, self.bw_accuracy, self.tb_accuracy = 0, 0, 0

        self.counter = 0
        self.testcases = dict()

    def ready(self):

        self.positive_test_bag = self.nb.get_positive_test_bag()
        self.negative_test_bag = self.nb.get_negative_test_bag()

    def compare(self):
        '''
        compares sentiment analysis done through Naive Bayes and bag of words method
        with popular text processing library textblob.
        '''
        self.test_for_bag(self.positive_test_bag, 1)
        self.test_for_bag(self.negative_test_bag, 0)

        self.nb_accuracy = (self.nb_correct/len(self.testcases)) * 100
        self.bw_accuracy = (self.bw_correct/len(self.testcases)) * 100
        self.tb_accuracy = (self.tb_correct/len(self.testcases)) * 100

        self.logger.info("Naive Bayes classifier")
        self.logger.info("Correct classification : " + str(self.nb_correct))
        self.logger.info("Wrong classification : " + str(self.nb_wrong))
        self.logger.info("Accuracy classification : " + str(int(self.nb_accuracy)))

        self.logger.info("Bag of Words classifier")
        self.logger.info("Correct : " + str(self.bw_correct))
        self.logger.info("Wrong classification : " + str(self.bw_wrong))
        self.logger.info("Accuracy : " + str(int(self.bw_accuracy)))

        self.logger.info("textblob classifier")
        self.logger.info("Correct : " + str(self.tb_correct))
        self.logger.info("Wrong classification : " + str(self.tb_wrong))
        self.logger.info("Accuracy : " + str(int(self.tb_accuracy)))

        self.store_results()

    def store_results(self):
        with open('output\\comparison_data.json', 'w') as file_pointer:
            json.dump(self.testcases, file_pointer)

    def test_for_bag(self, bag, actual_result):
        for sentence in bag:
            sentence = ' '.join(sentence)
            nb_result = self.nb.classify(sentence)
            bw_result = self.bw.classify(sentence)
            tb_result = self.classify_using_textblob(sentence)
            self.counter += 1
            self.testcases[self.counter] = {
                "sentence" : sentence,
                "actual"   : actual_result,
                "nb_result": list(nb_result),
                "bw_result": list(bw_result),
                "tb_result": list(tb_result)
            }

            if nb_result[1] == actual_result:
                self.nb_correct += 1
            else:
                self.nb_wrong += 1

            if bw_result[1] == actual_result:
                self.bw_correct += 1
            else:
                self.bw_wrong += 1

            if tb_result[1] == actual_result:
                self.tb_correct += 1
            else:
                self.tb_wrong += 1

    def classify_using_textblob(self, sentence):
        '''
        classifies the sentence using textblob library
        '''
        text_blob = TextBlob(sentence)
        polarity = text_blob.sentiment[0]
        if polarity > 0:
            return ("positive", 1, polarity)
        if polarity < 0:
            return ("negative", 0, polarity)
        return ("neutral", -1, polarity)    
