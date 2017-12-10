from utilities.logger import Logger
logger = Logger('n_grams', 'n_grams.log')

class NGramsSentiment():
    def __init__(self, verbose=True):
        self.verbose = verbose
        self.pronouns = self.load_pronouns()
        self.double_negations, self.double_negations_collection = self.load_double_negations()
        self.positive_words, self.positive_word_collection = self.load_positive_words()
        self.negative_words, self.negative_word_collection = self.load_negative_words()
        self.negations, self.negation_collection = self.load_neagtions()
        self.sentence = list()
        self.sentence_structure = list()

    def replace_characters(self, text, characters):
        for char in characters:
            text = text.replace(char, ' ')
        logger.debug("characters replaced. length : " + str(len(text)) + ". Text :" + text.strip())
        return text

    def clean(self, sentence):
        ignore_characters = '''\t\n&"`~@#$%^*;+=<>//.,()[]{}:;'''
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

    def remove_pronouns(self, sentence):
        new_sentence = []
        new_sentence_structure = []
        for word in sentence:
            if word in self.pronouns:
                new_sentence_structure.append(word+"(pronoun)")
                continue
            new_sentence_structure(word)
            new_sentence.append(word)
        return new_sentence, new_sentence_structure

    def get_kgrams(self, sentence, k=1):
        grams = list()
        for i in range(len(sentence)):
            grams.append(sentence[i:i+k])
            if i+k >= len(sentence):
                break
        return grams

    def get_lbigram(self, sentence, loc):
        if 0 <= loc-1 < len(sentence):
            return sentence[loc-1]
        return None

    def get_rbigram(self, sentence, loc):
        if 0 <= loc+1 < len(sentence):
            return sentence[loc+1]
        return None

    def find_sentiment(self, sentence):
        sentence = self.tokenise(sentence)
        self._print(sentence)
        sentence_str = ' '.join(sentence)
        self._print("sentence : " + sentence_str)
        analysis = list()
        #consumed
        #sentence = self.remove_pronouns(sentence)
        #check for double negations
        quadgrams = self.get_kgrams(sentence, k=4)

        for quadgram in quadgrams:
            pharse = ' '.join(quadgram)
            if self.is_double_negation(pharse):
                word = quadgram[-1]
                if self.is_positive(word):
                    analysis.append((pharse,'+'))
                    self._print("double negation of positive word, " + word + ". phrase : " + pharse)
                elif self.is_negative(word):
                    analysis.append((pharse,'-'))
                    self._print("double negation of negative word, " + word + ". phrase : " + pharse)
            
            if self.is_positive(pharse, perfect_match=True):
                analysis.append((pharse,'+'))
                self._print("positive quadgram : " + pharse)
            elif self.is_negative(pharse, perfect_match=True):
                analysis.append((pharse,'-'))
                self._print("negative quadgram : " + pharse)

        trigrams = self.get_kgrams(sentence, k=3)
        for trigram in trigrams:
            pharse = ' '.join(trigram)
            if self.is_double_negation(pharse):
                word = trigram[-1]
                if self.is_positive(word):
                    analysis.append((pharse,'+'))
                    self._print("double negation of positive word, " + word + ". phrase : " + pharse)
                elif self.is_negative(word):
                    analysis.append((pharse,'-'))
                    self._print("double negation of negative word, " + word + ". phrase : " + pharse)
            
            if self.is_positive(pharse, perfect_match=True):
                analysis.append((pharse,'+'))
                self._print("positive trigram : " + pharse)
            elif self.is_negative(pharse, perfect_match=True):
                analysis.append((pharse,'-'))
                self._print("negative trigram : " + pharse)

        bigrams = self.get_kgrams(sentence, k=2)
        for bigram in bigrams:
            pharse = ' '.join(bigram)
            if self.is_negation(pharse):
                word = bigram[-1]
                if self.is_positive(word):
                    analysis.append((pharse,'-'))
                    self._print("negation of positive word, " + word + ". phrase : " + pharse)
                elif self.is_negative(word):
                    analysis.append((pharse,'+'))
                    self._print("negation of negative word, " + word + ". phrase : " + pharse)
            if self.is_positive(pharse, perfect_match=True):
                analysis.append((pharse,'+'))
                self._print("positive bigram : " + pharse)
            elif self.is_negative(pharse, perfect_match=True):
                analysis.append((pharse,'-'))
                self._print("negative bigram : " + pharse)

        unigrams = self.get_kgrams(sentence, k=1)
        for unigram in unigrams:
            word = unigram[0]
            if self.is_positive(word):
                analysis.append((word,'+'))
                self._print("a positive word, " + word)
            elif self.is_negative(word):
                analysis.append((word,'-'))
                self._print("a negative word, " + word)

        #find the sentiment by counting positive and negative
        sentence_str = ' '.join(sentence)
        positive_count = 0
        negative_count = 0
        for phrase, sentiment in analysis:
            sentence_str = sentence_str.replace(phrase, sentiment)
      
        positive_count = sentence_str.count("+")
        negative_count = sentence_str.count("-")
        
        self._print("after analysis : " + sentence_str)
        if positive_count > negative_count:
            self._print("sentence sentiment is positive")
            return 'positive',1
        elif negative_count > positive_count:
            self._print("sentence sentiment is negative")
            return 'negative',0
        else:
            self._print("sentence sentiment is neutral")
            return 'neutral',-1 


    def is_double_negation(self, pharse):
        for double_negation in self.double_negations:
            if pharse.startswith(double_negation):
                return True
        for double_negation in self.double_negations_collection:
            if pharse.startswith(double_negation):
                return True
        return False

    def is_negation(self, pharse):
        for negation in self.negations:
            if pharse.startswith(negation):
                return True
        for negation in self.negations:
            if pharse.startswith(negation):
                return True
        return False

    def is_positive(self, word, perfect_match=False):
        if word in self.positive_words:
            return True
        if perfect_match is False:
            for positive_word in self.positive_word_collection:
                if word.startswith(positive_word):
                    return True
        return False

    def is_negative(self, word, perfect_match=False):
        if word in self.negative_words:
            return True
        if perfect_match is False:
            for negative_word in self.negative_word_collection:
                if word.startswith(negative_word):
                    return True
        return False
        # find the sentiment of emoticons if any
        # tokenise the sentences excluding ?(doubt) !(more strength)
        # what about - or _
#print(find_sentiment(sentence="I haven't done this"))

    def load_pronouns(self):
        filename = 'res\\pronouns.txt'
        with open(filename, encoding="utf8") as file:
            pronouns = file.readlines()
        return set([pronoun.replace('\n', '') for pronoun in pronouns])

    def load_positive_words(self):
        filename = 'res\\positive_words.txt'
        with open(filename, encoding="utf8") as file:
            positive_words = file.readlines()
        return self.get_words(positive_words)
    
    def load_negative_words(self):
        filename = 'res\\negative_words.txt'
        with open(filename, encoding="utf8") as file:
            negative_words = file.readlines()
        return self.get_words(negative_words)

    def load_double_negations(self):
        filename = 'res\\double_negation.txt'
        with open(filename, encoding="utf8") as file:
            double_negations = file.readlines()
        return self.get_words(double_negations)

    def load_neagtions(self):
        filename = 'res\\negation.txt'
        with open(filename, encoding="utf8") as file:
            negations = file.readlines()
        return self.get_words(negations)

    def get_words(self, input_words):
        words = set()
        multiple_words = list()
        for word in input_words:
            word = word.replace('\n', '').replace('(1)','').strip().lower()
            if '*' in word or '_' in word:
                word = word.replace('*','').replace('_', ' ')
                multiple_words.append(word.strip())
                continue
            words.add(word)
        return words, multiple_words

    def _print(self, message):
        if self.verbose:
            print(message)