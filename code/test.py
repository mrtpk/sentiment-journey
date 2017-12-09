# from n_grams import NGramsSentiment
# gram_model = NGramsSentiment(verbose=True)
# gram_model.find_sentiment(sentence="Ankitha is shit")

'''
EDGE CASES:
this can't be good --> here (be) should be avoided
'''


# path = 'res\\rt-polaritydata\\rt-polarity-neg.txt'
# with open(path, encoding="utf-8") as file:
#     data = file.readlines()

# print(len(data) )

# from numpy import random as np_random

# l = [[1],[2],[3],[4],[5]]
# m = []
# print(l)
# for i in range(0, 3):
#     i = np_random.random_integers(low=0, high=len(l)-1)
#     m.append(l.pop(i))
# print(m)
# print(l)

def get_kgrams(sentence, k=1):
    '''
    return list of kgrams from a given sentence
    '''
    grams = list()
    for i in range(len(sentence)):
        grams.append(sentence[i:i+k])
        if i+k >= len(sentence):
            break
    return grams


# print(get_kgrams(['a','b','c','d','e'], k=1))
# print(get_kgrams(['a','b','c','d','e'], k=2))
# print(get_kgrams(['a','b','c','d','e'], k=3))
# print(get_kgrams(['a','b','c','d','e'], k=4))

# a = get_kgrams(['a','b','c','d','e'], k=1)
# a.extend(get_kgrams(['a','b','c','d','e'], k=2))
# a.extend(get_kgrams(['a','b','c','d','e'], k=3))
# a.extend(get_kgrams(['a','b','c','d','e'], k=4))

# for i in a:
#     print(' '.join(i))


# kgrams = list()
# for k in range(1, self.no_of_grams + 1):
#     kgrams.extend(self.get_kgrams(sentence, k))

# no_of_grams = 1
# a = []
# for k in range(no_of_grams, 0, -1):
#    a.extend(get_kgrams(['a','b','c','d','e'], k))

# print(a)

# a, b = [0,1]
# print(a, b)
a,b = 1, 1
a,b += 2, 2
print(a,b)