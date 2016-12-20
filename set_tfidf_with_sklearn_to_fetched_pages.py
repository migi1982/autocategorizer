import utils
import constants
import pickle
import os
from sklearn.feature_extraction.text import TfidfVectorizer


def tfidf(pages):
    # analyzerは文字列を入れると文字列のlistが返る関数
    # vectorizer = TfidfVectorizer(analyzer=utils.stems, min_df=1, max_df=50)
    vectorizer = TfidfVectorizer(analyzer=utils.split_to_words)
    corpus = [page.html_body for page in pages]

    x = vectorizer.fit_transform(corpus)

    return x, vectorizer  # xはtfidf_resultとしてmainで受け取る

if __name__ == '__main__':
    utils.go_to_fetched_pages_dir()
    pages = utils.load_all_html_files()  # pagesはhtmlをフェッチしてtextにセットずみ

    tfidf_result, vectorizer = tfidf(pages)  # tfidf_resultはtfidf関数のx

    pkl_tfidf_result_path = os.path.join('..',
                                         constants.PKL_DIR_NAME,
                                         constants.TFIDF_RESULT_PKL_FILENAME)
    pkl_tfidf_vectorizer_path = os.path.join('..',
                                             constants.PKL_DIR_NAME,
                                             constants.TFIDF_VECTORIZER_PKL_FILENAME)

    with open(pkl_tfidf_result_path, 'wb') as f:
        pickle.dump(tfidf_result, f)
    with open(pkl_tfidf_vectorizer_path, 'wb') as f:
        pickle.dump(vectorizer, f)
