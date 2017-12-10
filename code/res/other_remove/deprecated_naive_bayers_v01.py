import pickle
from tqdm import tqdm

from utilities.logger import Logger

class NaiveBayers():
    def __init__(self, verbose=True, training_cases=2500, testcases=500):
        self.verbose = verbose
        self.training_cases = training_cases
        self.testcases = testcases
        self.training = list()
        self.test = list()
        self.frequency = dict()
        self.stop_words =  self.get_stop_words()
        self.positive_words = 0
        self.negative_words = 0
        self.positive_sentence_count = 0
        self.negative_sentence_count = 0
        self.total_sentences = 0
        self.logger = Logger('NaiveBayers', 'NaiveBayers.log')
        self.filenames = ['res\\benchmark\\yelp_labelled.txt',
                          'res\\benchmark\\amazon_cells_labelled.txt',
                          'res\\benchmark\\imdb_labelled.txt']
    
    def _print(self, message):
        if self.verbose:
            print(message)

    def clean(self, sentence):
        ignore_characters = '''\t\n&"`~@#$%^*;+=<>//.,()[]{}:;!?'''
        sentence = self.replace_characters(sentence, ignore_characters)
        return sentence.lower().strip()
    
    def tokenise(self, sentence):
        sentence = self.clean(sentence)
        tokens = sentence.split(' ')
        filtered_tokens = list()
        for token in tokens:
            if len(token.strip()) != 0:
                filtered_tokens.append(token)
        return filtered_tokens

    def replace_characters(self, text, characters):
        for char in characters:
            text = text.replace(char, ' ')
        return text

    def get_data(self):
        data = list()
        for filename in self.filenames:
            self._print("Filename : " + filename)
            for datum in tqdm(self.load_data_from_file(filename)):
                sentence, label = datum.split('\t')
                label = int(label)
                sentence = self.clean(sentence)
                data.append([sentence, label])
        self.training = data[:self.training_cases]
        self.test = data[-self.testcases:]

    def load_data_from_file(self, filename, encoding="utf8"):
        with open(filename, encoding=encoding) as file:
            data = file.readlines()
        return data


    def get_kgrams(self, sentence, k=1):
        grams = list()
        for i in range(len(sentence)):
            grams.append(sentence[i:i+k])
            if i+k >= len(sentence):
                break
        return grams

    def train(self):
        # try:
        #     with open('frequency.pickle', "rb") as file:
        #         self.frequency = pickle.load(file)
        #     with open("count.pickle", "rb") as file:
        #         self.positive_words, self.negative_words = pickle.load(file)
        # except Exception as error:
        #     self.logger.debug("Frequency file not found")
        #     self.train_unigrams()
        self.find_frequency_unigrams()
        self.train_from_negative_sentences()
        self.train_from_positive_sentences()
        # print(self.positive_words)
        # print(self.negative_words)
        # print(len(self.frequency))
        self.find_probablility_unigrams()
        # print(len(self.probablility))
        self.logger.info("Training completed")
        self.logger.info("Number of positive sentences : " + str(self.positive_sentence_count))
        self.logger.info("Number of negative sentences : " + str(self.negative_sentence_count))


    def classify(self, sentence):
        sentence = self.preprocess(sentence)
        positive_probablity = self.positive_sentence_count / self.total_sentences
        negative_probablity = self.negative_sentence_count / self.total_sentences
        self.logger.debug("sentence : " + str(sentence) )
        self.logger.debug("words considered : ")
        for word in sentence:
            word = word[0]
            word_positive_probability, word_negative_probability = 1, 1
            if word in self.probablility:
                word_positive_probability, word_negative_probability = self.probablility[word]
                self.logger.debug("word : " + word +
                                 " word_positive_probability : " + str(word_positive_probability) +
                                  " word_negative_probability : " + str(word_negative_probability) )
            positive_probablity *= word_positive_probability
            negative_probablity *= word_negative_probability
        
        self.logger.debug("positive_probablity : " + str(positive_probablity) )
        self.logger.debug("negative_probablity : " + str(negative_probablity) )

        # if abs(positive_probablity - negative_probablity) < 0.0000000000000001:
        #     self.logger.debug("sentence is neutral")
        #     return ("neutral" , -1)
        if positive_probablity > negative_probablity:
            self.logger.debug("sentence is positive")
            return ("positive", 1)
        if negative_probablity > positive_probablity:
            self.logger.debug("sentence is negative")
            return ("negative", 0)

    def test_classifier(self):
        correct, wrong = 0, 0
        total = len(self.test)
        for sentence, actual_label in self.test:
            verdict, label = self.classify(sentence)
            if label == actual_label:
                correct += 1
            else:
                wrong += 1
        
        self.logger.info("correct : " + str(correct))
        self.logger.info("wrong : " + str(wrong))
        self.logger.info("total : " + str(total))
        self.logger.info("accuracy : " + str(int((correct/total)*100)))

    def get_stop_words(self):
        data = self.load_data_from_file('res\\eng_stop_words.txt')
        return set([datum.replace('\n', '') for datum in data])

    def remove_stop_words(self, sentence):
        filtered_words = list()
        for word in sentence:
            if word in self.stop_words:
                continue
            filtered_words.append(word) 
        return filtered_words


    def find_probablility_unigrams(self):
        self.probablility = dict()
        for word in self.frequency:
            positive_probablity = (self.frequency[word][0] + 1)/(self.positive_words + len(self.frequency))
            negative_probablity = (self.frequency[word][1] + 1)/(self.negative_words + len(self.frequency))
            self.probablility[word] = [positive_probablity, negative_probablity]

    def preprocess(self, sentence):
        sentence = self.tokenise(sentence)
        #sentence = self.remove_stop_words(sentence)
        sentence = self.get_kgrams(sentence, k=1)
        return sentence

    def train_from_negative_sentences(self):
        negative_files = ['res\\rt-polaritydata\\rt-polarity-neg.txt']
        for filename in negative_files:
            new_sentences = self.load_data_from_file(filename)

        for sentence in new_sentences:
            sentence = self.preprocess(sentence)
            self.negative_sentence_count += 1
            for word in sentence:
                word = word[0]
                if word not in self.frequency:
                    self.frequency[word] = [0, 0]
                self.frequency[word][1] += 1
                self.negative_words += 1

    def train_from_positive_sentences(self):
        positive_files = ['res\\rt-polaritydata\\rt-polarity-pos.txt']

        data = list()
        for filename in positive_files:
            new_sentences = self.load_data_from_file(filename)

        for sentence in new_sentences:
            sentence = self.preprocess(sentence)
            self.positive_sentence_count += 1
            for word in sentence:
                word = word[0]
                if word not in self.frequency:
                    self.frequency[word] = [0, 0]
                self.frequency[word][0] += 1
                self.positive_words += 1


    def find_frequency_unigrams(self):
        for sentence, label in self.training:
            self.total_sentences += 1
            sentence = self.preprocess(sentence)
            if label == 1:
                #positive sentence
                self.positive_sentence_count += 1
                for word in sentence:
                    word = word[0]
                    if word not in self.frequency:
                        self.frequency[word] = [0, 0]
                    self.frequency[word][0] += 1
                    self.positive_words += 1
            elif label == 0:
                #negative sentence
                self.negative_sentence_count += 1
                for word in sentence:
                    word = word[0]
                    if word not in self.frequency:
                        self.frequency[word] = [0, 0]
                    self.frequency[word][1] += 1
                    self.negative_words += 1
        #add pickle code here
        # with open("frequency.pickle", "wb") as file:
        #     pickle.dump(self.frequency, file)
        # with open("count.pickle", "wb") as file:
        #     pickle.dumb((self.positive_words, self.negative_words), file)


nb = NaiveBayers(verbose=False, training_cases=2999, testcases=1)
nb.get_data()
nb.train()
nb.test_classifier()
# print(nb.classify(sentence="This is not awesome"))
# print(nb.filter_out_stop_words())

'''
consider more words, consider negations in bigrams
'''
# while(True):
#     sentence = input("Give me a sentence : ")
#     print(nb.classify(sentence))
