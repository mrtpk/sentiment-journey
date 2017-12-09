from utilities.logger import Logger

class NaiveBayers():
    def __init__(self, verbose=True, test_set_count=500, no_of_grams=1):
        self.logger = Logger('NaiveBayers', 'NaiveBayers.log')
        self.verbose = verbose
        self.counts = dict()
        self.positive_bag = []
        self.negative_bag = []

        self.positve_test_bag = []
        self.negative_test_bag = []

        self.counts["test set"] = test_set_count
        self.counts["positive phrases"] = 0
        self.counts["negative phrases"] = 0
        self.counts["total sentences"] = 0
        self.counts["positive sentences"] = 0
        self.counts["negative sentences"] = 0

        self.no_of_grams = no_of_grams

        self.phrase_occurrences = dict()
        self.phrase_probabilities = dict()

    def ready(self):
        self.load_data()
        self.create_test_set()
        self.fit()
        self.find_accuracy()
        self.logger.info("Naive Bayers classifier ready.")

    def classify(self, sentence):
        '''
        classifies a given sentence to positive or negative class
        '''
        positive_probablity, negative_probablity = self.find_conditional_probability(sentence)

        #TODO discuss with abhi about the edge cases
        if positive_probablity == 1 and negative_probablity == 1: #unable to classify a sentence
            self.logger.info("sentence - " + sentence + " - is neutral")
            return ("neutral", -1, positive_probablity)

        if positive_probablity == 1 and negative_probablity != 1:
            self.logger.info("sentence - " + sentence + " - is negative")
            return ("negative", 0, negative_probablity)        
        
        if positive_probablity != 1 and negative_probablity == 1:
            self.logger.info("sentence - " + sentence + " - is positive")
            return ("positive", 1, positive_probablity)

        if positive_probablity > negative_probablity:
            self.logger.info("sentence - " + sentence + " - is positive")
            return ("positive", 1, positive_probablity)

        if negative_probablity > positive_probablity:
            self.logger.info("sentence - " + sentence + " - is negative")
            return ("negative", 0, negative_probablity)

    def find_conditional_probability(self, sentence):
        '''
        finds the conditional probablity for a given sentence from phrase_probabilities
        '''
        sentence_str = sentence
        sentence = self.preprocess(sentence)

        sentence_positive_probablity = 1
        sentence_negative_probablity = 1

        positive_class_probability = self.counts["positive sentences"] / self.counts["total sentences"]
        negative_class_probability = self.counts["negative sentences"] / self.counts["total sentences"]
        
        sentence_positive_probablity *= positive_class_probability
        sentence_negative_probablity *= negative_class_probability

        kgrams = list()
        for k in range(self.no_of_grams, 0, -1):
            kgrams.extend(self.get_kgrams(sentence, k))
        
        for kgram in kgrams:
            phrase = ' '.join(kgram)
            sentence = ' '.join(sentence)
            if phrase in sentence and phrase in self.phrase_probabilities:
                phrase_positive_probability, phrase_negative_probability = self.phrase_probabilities[phrase]
                count = sentence.count(phrase)
                self.logger.debug(phrase + " " + str(phrase_positive_probability) + " " + str(phrase_negative_probability)  + " " + str(count))
                sentence_positive_probablity *= phrase_positive_probability ** count
                sentence_negative_probablity *= phrase_negative_probability ** count
                sentence = sentence.replace(phrase, ' ')
            sentence = self.preprocess(sentence)

        return sentence_positive_probablity, sentence_negative_probablity

    def fit(self):
        '''
        trains the model with sentences in positive and negative bags
        '''
        self.logger.info("training started")
        self.logger.info("total sentences : " + str(self.counts["total sentences"]))
        self.logger.info("positive sentences : " + str(self.counts["positive sentences"]))
        self.logger.info("negative sentences : " + str(self.counts["negative sentences"]))

        self.get_occurrences_from_bags()
        self.logger.info("calculated occurrences")
        self.logger.info("unique phrases : " + str(len(self.phrase_occurrences)))
        self.logger.info("phrases in positive class : " + str(self.counts["positive phrases"]))
        self.logger.info("phrases in negative class : " + str(self.counts["negative phrases"]))

        self.get_conditional_probabilities()
        self.logger.info("conditional probality for phrases calculated")
        self.logger.info("training completed")

    def get_conditional_probabilities(self):
        '''
        calculates the conditional probability for phrase|positive class and phrase|negative class
        '''
        total_unique_phrases = len(self.phrase_occurrences)
        for phrase in self.phrase_occurrences:
            positive_probablity = (self.phrase_occurrences[phrase][0] + 1)/(self.counts["positive phrases"] + total_unique_phrases)
            negative_probablity = (self.phrase_occurrences[phrase][1] + 1)/(self.counts["negative phrases"] + total_unique_phrases)
            self.phrase_probabilities[phrase] = [positive_probablity, negative_probablity]

    def get_occurrences_from_bags(self):
        '''
        calculates the occurrences of the phrases
        '''
        self.get_occurrences_from_positive_bag()
        self.get_occurrences_from_negative_bag()

    def get_occurrences_from_positive_bag(self):
        '''
        calculates the occurrences of unigram, bigram, trigram and quadgram from positive bag
        '''
        for sentence in self.positive_bag:
            kgrams = list()
            for k in range(1, self.no_of_grams + 1):
                kgrams.extend(self.get_kgrams(sentence, k))
            for kgram in kgrams:
                phrase = ' '.join(kgram)
                self.counts["positive phrases"] += 1
                if phrase not in self.phrase_occurrences:
                    self.phrase_occurrences[phrase] = [0, 0] #[word occurrence in positive class, word occurrence in negative class]
                self.phrase_occurrences[phrase][0] += 1
            
    def get_occurrences_from_negative_bag(self):
        '''
        calculates the occurrences of unigram, bigram, trigram and quadgram from negative bag
        '''
        for sentence in self.negative_bag:
            kgrams = list()
            for k in range(1, self.no_of_grams + 1):
                kgrams.extend(self.get_kgrams(sentence, k))
            for kgram in kgrams:
                phrase = ' '.join(kgram)
                self.counts["negative phrases"] += 1
                if phrase not in self.phrase_occurrences:
                    self.phrase_occurrences[phrase] = [0, 0]
                self.phrase_occurrences[phrase][1] += 1


    def get_kgrams(self, sentence, k=1):
        '''
        return list of kgrams from a given sentence
        '''
        grams = list()
        for i in range(len(sentence)):
            grams.append(sentence[i:i+k])
            if i+k >= len(sentence):
                break
        return grams

    def create_test_set(self):
        '''
        randomly selects test sentences from positive and negative bags and making a uniform distribution of test sentences
        '''
        from numpy import random as np_random
        count = self.counts["test set"] // 2
        while(count != 0):
            index = np_random.random_integers(low=0, high=len(self.positive_bag)-1)
            self.positve_test_bag.append(self.positive_bag.pop(index))
            index = np_random.random_integers(low=0, high=len(self.negative_bag)-1)
            self.negative_test_bag.append(self.negative_bag.pop(index))
            count -= 1
        
        self.logger.info("test sentences selected")
        self.logger.info("Total sentences for testing : " + str(len(self.positve_test_bag)+len(self.negative_test_bag)))
        self.logger.info("positive sentences for testing : " + str(len(self.positve_test_bag)))
        self.logger.info("negative sentences for testing : " + str(len(self.negative_test_bag)))
        
        self.counts["positive sentences"] = len(self.positive_bag)
        self.counts["negative sentences"] = len(self.negative_bag)
        self.counts["total sentences"] = len(self.positive_bag) + len(self.negative_bag)

 
    def load_data(self):
        '''
        loads the positive and negative sentences from filenames specified
        '''
        mixed_bag_paths = ['res\\dataset\\uci_dataset\\yelp_labelled.txt',
                           'res\\dataset\\uci_dataset\\amazon_cells_labelled.txt',
                           'res\\dataset\\uci_dataset\\imdb_labelled.txt']

        positive_bag_paths = ['res\\dataset\\polarity_dataset\\rt-polarity-pos.txt']
        negative_bag_paths = ['res\dataset\polarity_dataset\\rt-polarity-neg.txt']

        count_positive, count_negative = 0,0
        for filename in mixed_bag_paths:
            for mixed_data in self.load_data_from_file(filename):
                sentence, label = mixed_data.split('\t')
                label = int(label)
                sentence = self.preprocess(sentence)
                if label == 1: #if sentence is positive
                    self.positive_bag.append(sentence)
                    count_positive += 1
                else:
                    self.negative_bag.append(sentence)
                    count_negative += 1
        self.logger.debug("sentences from mixed bag imported")
        self.logger.debug("positive sentences : " + str(count_positive))
        self.logger.debug("negative sentences : " + str(count_negative))

        count_positive = 0
        for filename in positive_bag_paths:
            for sentence in self.load_data_from_file(filename):
                sentence = self.preprocess(sentence)
                self.positive_bag.append(sentence)
                count_positive += 1
        self.logger.debug("sentences from positive bag imported")
        self.logger.debug("positive sentences : " + str(count_positive))

        count_negative = 0
        for filename in negative_bag_paths:
            for sentence in self.load_data_from_file(filename):
                sentence = self.preprocess(sentence)
                self.negative_bag.append(sentence)   
                count_negative += 1             
        self.logger.debug("sentences from negative bag imported")
        self.logger.debug("negative sentences : " + str(count_negative))

        self.counts["positive sentences"] = len(self.positive_bag)
        self.counts["negative sentences"] = len(self.negative_bag)
        self.counts["total sentences"] = len(self.positive_bag) + len(self.negative_bag)

        self.logger.info("sentences imported")
        self.logger.info("Total sentences : " + str(self.counts["total sentences"]))
        self.logger.info("positive sentences : " + str(self.counts["positive sentences"]))
        self.logger.info("negative sentences : " + str(self.counts["negative sentences"]))

    
    def load_data_from_file(self, filename, encoding="utf8"):
        '''
        load the data as a list from the specified filename
        '''
        with open(filename, encoding=encoding) as file:
            data = file.readlines()
        return data

    def preprocess(self, sentence):
        '''
        preprocess the sentence and return as a list of words
        '''
        sentence = self.tokenise(sentence)
        #sentence = self.remove_stop_words(sentence)
        return sentence
    
    def tokenise(self, sentence):
        '''
        convert the sentence to list of words
        '''
        sentence = self.clean(sentence)
        tokens = sentence.split(' ')
        filtered_tokens = list()
        for token in tokens:
            if len(token.strip()) != 0:
                filtered_tokens.append(token.strip())
        return filtered_tokens

    def clean(self, sentence):
        '''
        clean sentence by removing the ignored characters
        '''
        ignore_characters = '''\t\n&"`~@#$%^*;+=<>//.,()[]{}:;!?'''
        sentence = self.replace_characters(sentence, ignore_characters)
        return sentence.lower().strip()
    
    def replace_characters(self, text, characters):
        '''
        replaces the specified characters in text with blank space
        '''
        for char in characters:
            text = text.replace(char, ' ')
        return text

    def test_for_fish_guitar(self):
        positive_sentences = ["fish smoked fish", "fish line", "fish haul smoked"]
        negative_sentences = ["guitar jazz line"]
        self.positive_bag = [sentence.split(" ") for sentence in positive_sentences]
        self.negative_bag = [sentence.split(" ") for sentence in negative_sentences]
        self.counts["total sentences"] = len(self.positive_bag) + len(self.negative_bag)
        self.counts["positive sentences"] = len(self.positive_bag)
        self.counts["negative sentences"] = len(self.negative_bag)

        self.get_occurrences_from_bags()
        self.get_conditional_probabilities()

        test_sentence = "line guitar jazz jazz"
        result = self.classify(sentence=test_sentence)
        self.logger.info(str(result))



    def find_accuracy(self):
        correct, wrong = 0, 0
        total = len(self.positve_test_bag) + len(self.negative_test_bag)
        
        _correct, _wrong = self.test_for_bag(self.positve_test_bag, actual_result=1)
        correct += _correct
        wrong += _wrong
        
        _correct, _wrong = self.test_for_bag(self.negative_test_bag, actual_result=0)
        correct += _correct
        wrong += _wrong

        self.accuracy = (correct/total) * 100
        self.info("total test sentences : " + str(total))
        self.info("correct output : " + str(correct))
        self.info("wrong output : " + str(wrong))
        self.info("accuracy (%) : " + str(int(self.accuracy)))
        
    def test_for_bag(self, bag, actual_result):
        correct, wrong = 0, 0

        for sentence in bag:
            result = self.classify(sentence=sentence)
            if result[1] == actual_result:
                correct += 1
            else:
                wrong += 1

        self.debug("total test sentences in bag : " + str(len(bag)))
        self.debug("correct output : " + str(correct))
        self.debug("wrong output : " + str(wrong))
        self.debug("accuracy (%) : " + str(int((correct/len(bag)) * 100)))
        return correct, wrong





nb = NaiveBayers(verbose=False, test_set_count=100, no_of_grams=4)
nb.ready()
#nb.test_for_fish_guitar()

while(True):
    sentence = input("Give me a sentence : ")
    print(nb.classify(sentence))
