from naive_bayes import NaiveBayes
from bag_of_words import BagOfWordSentiment
from comparer import Comparer

from utilities.menu import Menu


menu_options = [
    'classify using bag of words',
    'classify using Naive Bayes',
    'compare bag of words method, Naive Bayes and textblob',
    'test accuracy of bag of words method by randomly choosing test sentences of uniform distribution',
    'test accuracy of Naive Bayes classifier by randomly choosing test sentences of uniform distribution',
    'exit'
]

bw = BagOfWordSentiment(verbose=True, no_of_grams=4)
nb = NaiveBayes(verbose=True, test_set_count=100, no_of_grams=4)

def start():
    bw.ready()
    nb.ready()
    display_menu()

def display_menu():
    menu = Menu(title='Sentiment Analysis', options=menu_options)
    while(True):
        option = menu.get_single_choice()
        if menu_options[0] == option:
            classify_using_bag_of_words()
        elif menu_options[1] == option:
            classify_using_naive_bayes()
        elif menu_options[2] == option:
            compare_models()
        elif menu_options[3] == option:
            test_accuracy_bag_of_words()
        elif menu_options[4] == option:
            test_accuracy_naive_bayes()
        elif menu_options[5] == option:
            stop_program()

def classify_using_bag_of_words():
    while(True):
        print(">>>Analysis using bag of words")
        sentence = input(">>>Enter a sentence (press 'x' to exit) : ")
        if sentence.lower() == 'x':
            break
        print(">>>Result")
        print(">>>Sentence :", sentence )
        print(">>>Analysis:")
        print(">>>Result :", bw.classify(sentence))
        print("")

def classify_using_naive_bayes():
    while(True):
        print(">>>Analysis using Naive Bayes")
        sentence = input(">>>Enter a sentence (press 'x' to exit) : ")
        if sentence.lower() == 'x':
            break
        print(">>>Result")
        print(">>>Sentence :", sentence )
        print(">>>Analysis:")
        print(">>>Result :", nb.classify(sentence))
        print("")

def test_accuracy_bag_of_words():
    bw.no_of_testcases = int(input("Enter number of testcases. max(13562) : "))
    bw.find_accuracy()

def test_accuracy_naive_bayes():
    nb.find_accuracy()

def compare_models():
    c = Comparer(no_of_testcases=100, nb=nb, bw=bw)
    c.ready()
    c.compare()

def stop_program():
    exit(0)

start()