import constants
import pickle
import os
import utils

if __name__ == '__main__':
    utils.go_to_pkl_dir()
    with open(constants.TFIDF_RESULT_PKL_FILENAME, 'rb') as f:
        x = pickle.load(f)
    with open(constants.TFIDF_VECTORIZER_PKL_FILENAME, 'rb') as f:
        vectorizer = pickle.load(f)

    bag = {}
    values_set = {}
    words = vectorizer.get_feature_names()
    categories = []
    for category in constants.CATEGORIES:
        for word in category['words']:
            categories.append(word)
    matrix = x.toarray()

    for (i, values) in enumerate(matrix):
        num = i // constants.NUM_OF_FETCHED_PAGES
        values_set.setdefault(num, {})
        for (j, value) in enumerate(values):
            values_set[num].setdefault(j, value)
            values_set[num][j] += value

    for (i, category) in enumerate(categories):
        bag.setdefault(category, {})
        for (j, word) in enumerate(words):
            if values_set[i][j] > 0:
                bag[category].setdefault(word, 0)
                bag[category][word] = values_set[i][j]

    bag_path = os.path.join('..', constants.PKL_DIR_NAME, constants.TFIDF_BAG_FILENAME)

    with open(bag_path, 'wb') as f:
        pickle.dump(bag, f)
