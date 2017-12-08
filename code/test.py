from n_grams import NGramsSentiment
gram_model = NGramsSentiment(verbose=True)
gram_model.find_sentiment(sentence="this can't good")

'''
EDGE CASES:
this can't be good --> here (be) should be avoided
'''