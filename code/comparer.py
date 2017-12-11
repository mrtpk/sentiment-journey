from textblob import TextBlob

from utilities.logger import Logger
import json

from naive_bayes import NaiveBayes
from bag_of_words import BagOfWordSentiment

class Comparer():
    def __init__(self, no_of_testcases = 100, verbose=True, nb=None, bw=None):
        self.logger = Logger('Comparer', 'logs\\comparer.log', is_verbose=verbose)
        self.load_html_structure()

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

        self.file_html = self.file_html.replace("@nb_right", str(self.nb_correct))
        self.file_html = self.file_html.replace("@bw_right", str(self.bw_correct))
        self.file_html = self.file_html.replace("@tb_right", str(self.tb_correct))
        self.file_html = self.file_html.replace("@nb_wrong", str(self.nb_wrong))
        self.file_html = self.file_html.replace("@bw_wrong", str(self.bw_wrong))
        self.file_html = self.file_html.replace("@tb_wrong", str(self.tb_wrong))
        self.file_html = self.file_html.replace("@nb_accuracy", str(int(self.nb_accuracy)))
        self.file_html = self.file_html.replace("@bw_accuracy", str(int(self.bw_accuracy)))
        self.file_html = self.file_html.replace("@tb_accuracy", str(int(self.tb_accuracy)))
        self.file_html = self.file_html.replace("@total_sentences", str(len(self.testcases)))

        self.testcases["nb_results"] = {
            "correct" : self.nb_correct,
            "wrong" : self.nb_wrong,
            "accuracy" : self.nb_accuracy
        }
        self.testcases["bw_results"] = {
            "correct" : self.bw_correct,
            "wrong" : self.bw_wrong,
            "accuracy" : self.bw_accuracy
        }
        self.testcases["tb_results"] = {
            "correct" : self.tb_correct,
            "wrong" : self.tb_wrong,
            "accuracy" : self.tb_accuracy
        }

        self.store_results()

    def store_results(self):
        with open('output\\comparison_data.json', 'w', encoding="utf-8") as file_pointer:
            json.dump(self.testcases, file_pointer)
        with open('output\\output.html', 'w', encoding="utf-8") as file_pointer:
            file_pointer.write(self.file_html)

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
            temp_html = self.html_structure
            temp_html = temp_html.replace("@sentence", str(sentence))
            temp_html = temp_html.replace("@actual_label", str(actual_result))
            temp_html = temp_html.replace("@nb_prediction", str(nb_result[1]))
            temp_html = temp_html.replace("@bw_prediction", str(bw_result[1]))
            temp_html = temp_html.replace("@tb_prediction", str(tb_result[1]))
            temp_html = temp_html.replace("@nb_label", str(nb_result[0]))
            temp_html = temp_html.replace("@bw_label", str(bw_result[0]))
            temp_html = temp_html.replace("@tb_label", str(tb_result[0]))
            temp_html = temp_html.replace("@nb_score", str(nb_result[2]))
            temp_html = temp_html.replace("@bw_score", str(bw_result[2]))
            temp_html = temp_html.replace("@tb_score", str(tb_result[2]))
            self.file_html = self.file_html + temp_html   

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

    def load_html_structure(self):
        '''
        stores the data from dictionary to html file
        '''
        with open('res\\table_structure.html', 'r') as myfile:
            self.html_structure = myfile.read()

        with open('res\\table_header.html', 'r') as myfile:
            self.file_html = myfile.read()
         