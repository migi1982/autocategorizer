from sim_calculator import SimCalculator
from naive_bayes import NaiveBayes
import constants
import pickle
import utils
import csv
from collections import OrderedDict


if __name__ == '__main__':
    sc = SimCalculator()
    utils.go_to_pkl_dir()
    with open(constants.TFIDF_BAG_FILENAME, 'rb') as f:
        tfidf_bag = pickle.load(f)

    utils.go_to_parent_dir()
    utils.go_to_docs_dir()
    with open('topics.tsv', newline='') as f:
        result = ''
        reader = csv.reader(f, delimiter='\t')

        for row in reader:
            nb_input = NaiveBayes()
            nb_input.word_count = {}
            nb_input.train(row[1], 'input')
            results = OrderedDict()
            for category in tfidf_bag:
                try:
                    sim_cos = sc.sim_cos(nb_input.word_count['input'],
                                         tfidf_bag[category])
                    results[category] = sim_cos
                    # sim_simpson = sc.sim_simpson(nb_input.word_count['input'],
                    #                     tfidf_bag[category])
                    # results[category] = sim_simpson
                except KeyError:  # inputが空白のとき
                    continue

            sammary = OrderedDict()

            for group in results:
                for category in constants.CATEGORIES:
                    if group in category['words']:
                        sammary.setdefault(category['category'], 0)
                        sammary[category['category']] += results[group]
                        break

            best_score_before = 0.0
            best_category = ''
            for category in sammary:
                if sammary[category] > best_score_before:
                    best_category = category
                    best_score_before = sammary[category]
            try:
                for i, category in enumerate(constants.CATEGORIES):
                    if best_category is category['category']:
                        id = i
                result += '%s\t%s\n' % (row[0], id)
                # result += '%s\t%s\t%s\n' % (row[0], row[1], best_category)
                print('%s\t%s\t%s' % (row[0], best_category, row[1]))
            except KeyError:  # inputが空白のとき
                continue
        f = open('categorized_topics.txt', 'w')
        f.write(result)
        f.close()
