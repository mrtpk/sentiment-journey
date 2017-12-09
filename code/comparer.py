from tqdm import tqdm
from textblob import TextBlob

def load_benchmark(filename):
    with open(filename, encoding="utf8") as file:
        data = file.readlines()
    return data

def compare(filenames):
    from n_grams import NGramsSentiment
    gram_model = NGramsSentiment(verbose=False)
    gram_model.find_sentiment(sentence="")
    avg_accuracy = 0
    
    for filename in filenames:
        print("Filename: ", filename)
        blob_correct, blob_wrong = 0,0
        correct, wrong, total = 0, 0, 0
        for benchmark in tqdm(load_benchmark(filename)):
            sentence, label = benchmark.split('\t')
            bench_label = int(label)
            test_label, test_value = gram_model.find_sentiment(sentence)
            blob = TextBlob(sentence)
            blob_sentimence = blob.sentiment.polarity
            if blob_sentimence > 0:
                blob_sentimence = 1
            elif blob_sentimence < 0:
                blob_sentimence = 0
            else:
                blob_sentimence = -1
            total += 1
            if bench_label == test_value:
                correct += 1
            else:
                wrong += 1
            if bench_label == blob_sentimence:
                blob_correct += 1
            else:
                blob_wrong += 1
        accuracy = (correct/total)*100
        avg_accuracy += accuracy
        print("Total :", total)
        print("Correct :", correct)
        print("wrong :", wrong)
        print("blob correct : ", blob_correct)
        print("blob wrong : ", blob_wrong)
        print("Blob Accuracy :", int((blob_correct/total)*100))
        print("Accuracy :", int((correct/total)*100))

    avg_accuracy = int(avg_accuracy/len(filenames))
    print("Average accuracy : " + str(avg_accuracy))

filenames = ['res\\benchmark\\yelp_labelled.txt',
             'res\\benchmark\\amazon_cells_labelled.txt',
             'res\\benchmark\\imdb_labelled.txt']
compare(filenames)