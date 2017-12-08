from tqdm import tqdm

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
        correct, wrong, total = 0, 0, 0
        for benchmark in tqdm(load_benchmark(filename)):
            sentence, label = benchmark.split('\t')
            bench_label = int(label)
            test_label, test_value = gram_model.find_sentiment(sentence)
            total += 1
            if bench_label == test_value:
                correct += 1
            else:
                wrong += 1
        accuracy = (correct/total)*100
        avg_accuracy += accuracy
        print("Total :", total)
        print("Correct :", correct)
        print("wrong :", wrong)
        print("Accuracy :", int((correct/total)*100))

    avg_accuracy = int(avg_accuracy/len(filenames))
    print("Average accuracy : " + str(avg_accuracy))

filenames = ['res\\benchmark\\yelp_labelled.txt',
             'res\\benchmark\\amazon_cells_labelled.txt',
             'res\\benchmark\\imdb_labelled.txt']
compare(filenames)