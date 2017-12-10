from utilities.logger import Logger

class NGramsSentiment():
    def __init__(self, no_of_grams=4, verbose=True, no_of_testcases=1000):
        self.verbose = verbose
        self.logger = Logger('n_grams', 'n_grams.log', is_verbose=self.verbose)

        self.no_of_grams= no_of_grams

        self.double_negations, self.double_negations_collection = set(), set()
        self.negations, self.negation_collection = set(), set()
        self.positive_words, self.positive_word_collection = set(), set()
        self.negative_words, self.negative_word_collection = set(), set()

        self.no_of_testcases = no_of_testcases
        self.positve_test_bag = list()
        self.negative_test_bag = list()

    def classify(self, sentence):
        '''
        classifies the sentence to positve or negative or neutral using bag of words method
        '''
        positive_score, negative_score = self.find_score(sentence)

        if positive_score > negative_score:
            self.logger.info("sentence - " + sentence + " - is positive")
            return ("positive", 1, positive_score)

        if positive_score < negative_score:
            self.logger.info("sentence - " + sentence + " - is negative")
            return ("negative", 0, negative_score)

        if positive_score == negative_score:
            self.logger.info("sentence - " + sentence + " - is neutral")
            return ("neutral", -1, positive_score)

    def find_score(self, sentence):
        '''
        finds positive and negative score for a given sentence
        '''
        positive_score, negative_score = 0, 0
        self.logger.info("sentence : " + sentence)
        sentence = self.tokenise(sentence)
        self.logger.info("tokenised sentence after cleaning : " + str(sentence))
        
        kgrams = list()
        for k in range(self.no_of_grams, 0, -1):
            kgrams.extend(self.get_kgrams(sentence, k))

        for kgram in kgrams: 
            phrase = ' '.join(kgram)
            sentence = ' '.join(sentence)

            if phrase in sentence:
                self.logger.info("considering phrase '"+phrase+"' from '"+sentence+"'")
                #check this phrase for double negation
                contains_double_negation, remaining_phrase = self.is_double_negation(phrase)
                if contains_double_negation:
                    if self.is_positive(remaining_phrase):
                        positive_score += 1
                        sentence = sentence.replace(phrase, ' ')
                        sentence = self.tokenise(sentence)
                        self.logger.info("double negation of positive phrase : " + phrase)
                        continue
                    if self.is_negative(remaining_phrase):
                        negative_score += 1
                        sentence = sentence.replace(phrase, ' ')
                        sentence = self.tokenise(sentence)
                        self.logger.info("double negation of negative phrase : " + phrase)
                        continue
                
                #check this phrase for negations
                contains_negation, remaining_phrase = self.is_negation(phrase)
                if contains_negation:
                    if self.is_positive(remaining_phrase):
                        negative_score += 1
                        sentence = sentence.replace(phrase, ' ')
                        sentence = self.tokenise(sentence)
                        self.logger.info("negation of positive phrase : " + phrase)
                        continue
                    if self.is_negative(remaining_phrase):
                        positive_score += 1
                        sentence = sentence.replace(phrase, ' ')
                        sentence = self.tokenise(sentence)
                        self.logger.info("negation of negative phrase : " + phrase)
                        continue

                #check for positive phrase
                if self.is_positive(phrase):
                    positive_score += 1
                    sentence = sentence.replace(phrase, ' ')
                    sentence = self.tokenise(sentence)
                    self.logger.info("positive phrase : " + phrase)
                    continue
                
                #check for negative phrase
                if self.is_negative(phrase):
                    negative_score += 1
                    sentence = sentence.replace(phrase, ' ')
                    sentence = self.tokenise(sentence)
                    self.logger.info("negative phrase : " + phrase)
                    continue


                self.logger.info("cannot deduce sentiment from phrase '" + phrase+"'")
            sentence = self.tokenise(sentence)



        return positive_score, negative_score                 
            

    def is_double_negation(self, phrase):
        '''
        checks whether a word is in bag of double negations
        '''
        for double_negation in self.double_negations:
            double_negation = double_negation + " "
            if phrase.startswith(double_negation):
                remaining_phrase = phrase.replace(double_negation, '')
                return True, remaining_phrase

        for double_negation in self.double_negations_collection:
            if phrase.startswith(double_negation):
                phrase_length = len(phrase.split(" "))
                double_negation_length = len(double_negation.split(" "))
                diff = phrase_length - double_negation_length
                
                if diff <= 0:
                    return False, phrase

                remaining_phrase = ' '.join(phrase.split(" ")[-diff:])
                return True, remaining_phrase
        return False, phrase

    def is_negation(self, phrase):
        '''
        checks whether a word is in bag of negations
        '''
        for negation in self.negations:
            negation = negation + " "
            if phrase.startswith(negation):
                remaining_phrase = phrase.replace(negation, '')
                return True, remaining_phrase

        for negation in self.negation_collection:
            if phrase.startswith(negation):
                phrase_length = len(phrase.split(" "))
                negation_length = len(negation.split(" "))
                diff = phrase_length - negation_length
                
                if diff <= 0:
                    return False, phrase

                remaining_phrase = ' '.join(phrase.split(" ")[-diff:])
                return True, remaining_phrase
        return False, phrase

    def is_positive(self, word):
        '''
        checks whether a word is in bag of positive words
        '''
        if word in self.positive_words:
            return True
        for positive_word in self.positive_word_collection:
            if word.startswith(positive_word):
                return True  
        return False

    def is_negative(self, word):
        '''
        checks whether a word is in bag of negative words
        '''
        if word in self.negative_words:
            return True
        for negative_word in self.negative_word_collection:
            if word.startswith(negative_word):
                return True  
        return False

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

    def load_data(self):
        '''
        loads the data necessary for analysis
        '''
        double_negation_files = ['res\\ngram_dataset\\double_negation.txt']
        negations_files = ['res\\ngram_dataset\\negation.txt']
        positive_word_files = ['res\\ngram_dataset\\positive_words.txt']
        negative_word_files = ['res\\ngram_dataset\\negative_words.txt']

        self.double_negations, self.double_negations_collection = self.get_words(self.load_data_from_files(double_negation_files))
        self.negations, self.negation_collection = self.get_words(self.load_data_from_files(negations_files))
        self.positive_words, self.positive_word_collection = self.get_words(self.load_data_from_files(positive_word_files))
        self.negative_words, self.negative_word_collection = self.get_words(self.load_data_from_files(negative_word_files))

        self.logger.info("words loaded")
        self.logger.info("double negations : " + str(len(self.double_negations)+len(self.double_negations_collection)))
        self.logger.info("negations : " + str(len(self.negations)+len(self.negation_collection)))
        self.logger.info("positive words : " + str(len(self.positive_words)+len(self.positive_word_collection)))
        self.logger.info("negative words : " + str(len(self.negative_words)+len(self.negative_word_collection)))

    def get_words(self, input_words):
        '''
        cleans the input words and group them into set of words and
        set of mulitple word set(words that have different forms)
        '''
        words = set()
        multiple_words = set()
        for word in input_words:
            word = word.replace('\n', '').replace('(1)','').replace("'",'')
            word = word.replace('_', ' ').replace('-', ' ').strip().lower()
            if '*' in word:
                word = word.replace('*','')
                multiple_words.add(word.strip())
                continue
            words.add(word)
        return words, multiple_words

    def tokenise(self, sentence):
        '''
        split the sentence into words
        '''
        sentence = self.clean(sentence)
        tokens = sentence.split(' ')
        filtered_tokens = list()
        for token in tokens:
            if len(token.strip()) != 0:
                filtered_tokens.append(token)
        return filtered_tokens

    def clean(self, sentence):
        '''
        clean the sentence by removing ignored characters
        '''
        ignore_characters = '''\t\n&"`~@#$%^*;+=<>//.,()[]{!}?:;_-'''
        sentence = sentence.lower().strip()
        sentence = self.remove_stop_words(sentence)
        sentence = self.replace_characters(sentence, ignore_characters)
        sentence = sentence.replace("'", '')
        return sentence.lower().strip()

    def remove_stop_words(self, sentence):
        stop_words = self.load_data_from_files(['res\\ngram_dataset\\refined_stop_words.txt'])
        sentence = sentence.split(" ")
        stop_word_set = set()
        for stop_word in stop_words:
                stop_word_set.add(stop_word.replace('\n','').replace('\t','').strip())
        new_sentence = list()
        for word in sentence:
                if word not in stop_word_set:
                    new_sentence.append(word)
        return ' '.join(new_sentence)

    def replace_characters(self, text, characters):
        '''
        replace the specified characters from text to blank spaces
        '''
        for char in characters:
            text = text.replace(char, ' ')
        return text

    def load_data_from_files(self, filenames, encoding="utf8"):
        '''
        load the data as a list from the specified filenames
        '''
        data = list()
        for filename in filenames:
            with open(filename, encoding=encoding) as file:
                data.extend(file.readlines())
        return data

    def find_accuracy(self):
        
        self.load_test_cases()
        self.create_test_set()

        correct, wrong = 0, 0
        total = len(self.positve_test_bag) + len(self.negative_test_bag)
        
        _correct, _wrong = self.test_for_bag(self.positve_test_bag, actual_result=1)
        correct += _correct
        wrong += _wrong
        
        _correct, _wrong = self.test_for_bag(self.negative_test_bag, actual_result=0)
        correct += _correct
        wrong += _wrong

        self.accuracy = (correct/total) * 100
        self.logger.info("total test sentences : " + str(total))
        self.logger.info("correct output : " + str(correct))
        self.logger.info("wrong output : " + str(wrong))
        self.logger.info("accuracy (%) : " + str(int(self.accuracy)))
        return (self.accuracy, total, correct, wrong)
        
    def test_for_bag(self, bag, actual_result):
        correct, wrong = 0, 0
        for sentence in bag:
            result = self.classify(sentence=sentence)
            if result[1] == actual_result:
                correct += 1
            else:
                wrong += 1

        self.logger.debug("total test sentences in bag : " + str(len(bag)))
        self.logger.debug("correct output : " + str(correct))
        self.logger.debug("wrong output : " + str(wrong))
        self.logger.debug("accuracy (%) : " + str(int((correct/len(bag)) * 100)))
        return correct, wrong

    def create_test_set(self):
        '''
        randomly selects test sentences from positive and negative bags and making a uniform distribution of test sentences
        '''
        from numpy import random as np_random
        count = self.no_of_testcases // 2
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
        
    def load_test_cases(self):
        '''
        loads the positive and negative sentences from filenames specified
        '''
        mixed_bag_paths = ['res\\dataset\\uci_dataset\\yelp_labelled.txt',
                           'res\\dataset\\uci_dataset\\amazon_cells_labelled.txt',
                           'res\\dataset\\uci_dataset\\imdb_labelled.txt']

        #followed training sets contain hard testcases
        positive_bag_paths = ['res\\dataset\\polarity_dataset\\rt-polarity-pos.txt']
        negative_bag_paths = ['res\dataset\polarity_dataset\\rt-polarity-neg.txt']
        #uncomment below two lines not to include difficult testcases
        # positive_bag_paths = []
        # negative_bag_paths = []

        self.positive_bag, self.negative_bag = list(), list()
        count_positive, count_negative = 0,0
        for filename in mixed_bag_paths:
            for mixed_data in self.load_data_from_files([filename]):
                sentence, label = mixed_data.split('\t')
                label = int(label)
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
            for sentence in self.load_data_from_files([filename]):
                self.positive_bag.append(sentence)
                count_positive += 1
        self.logger.debug("sentences from positive bag imported")
        self.logger.debug("positive sentences : " + str(count_positive))

        count_negative = 0
        for filename in negative_bag_paths:
            for sentence in self.load_data_from_files([filename]):
                self.negative_bag.append(sentence)   
                count_negative += 1             
        self.logger.debug("sentences from negative bag imported")
        self.logger.debug("negative sentences : " + str(count_negative))

        self.logger.debug("sentences imported")
        self.logger.debug("Total sentences : " + str(len(self.positive_bag) + len(self.negative_bag)))
        self.logger.debug("positive sentences : " + str(len(self.positive_bag)))
        self.logger.debug("negative sentences : " + str(len(self.negative_bag)))




ng = NGramsSentiment(verbose=True, no_of_testcases=2)
ng.load_data()
result = ng.classify(sentence='this is a few hell')
print(result)
# print(ng.find_accuracy())

    