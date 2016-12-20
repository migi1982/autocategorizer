from sim_calculator import SimCalculator
from naive_bayes import NaiveBayes
import constants
import pickle
import sys
from collections import OrderedDict
import os

if __name__ == '__main__':
    sc = SimCalculator()
    bag_path = os.path.join(constants.PKL_DIR_NAME, constants.TFIDF_BAG_FILENAME)
    with open(bag_path, 'rb') as f:
        tfidf_bag = pickle.load(f)
    # with open('basic.json', mode='w', encoding='utf-8') as f:
    #     json.dump(tfidf_bag, f)

    nb_input = NaiveBayes()

    for query in sys.stdin:
        nb_input.word_count = {}  # 二回目以降のinputのための初期化
        nb_input.train(query, 'input')  # 標準入力で入れた文字列を'input'カテゴリとして学習
        results = OrderedDict()
        for category in tfidf_bag:
            # sim_simpson = sc.sim_simpson(nb_input.word_count['input'], tfidf_bag[category])
            # results[category] = sim_simpson
            sim_cos = sc.sim_cos(nb_input.word_count['input'], tfidf_bag[category])
            results[category] = sim_cos

        for result in results:
            print('カテゴリー「%s」との類似度は %f です' % (result, results[result]))

        # http://cointoss.hatenablog.com/entry/2013/10/16/123129 の通りやってもmaxのkey取れない(´・ω・`)
        best_score_before = 0.0
        best_category = ''
        for i, category in enumerate(results):
            if results[category] > best_score_before:
                best_category = category
                best_score_before = results[category]
        try:
            print('%s類似度の最も高いカテゴリーは「%s」で類似度は %f です%s' %
                  ('\033[94m', best_category, results[best_category], '\033[0m'))
        except KeyError:  # inputが空白のとき
            continue
