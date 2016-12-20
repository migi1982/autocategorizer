import MeCab
import constants
import os
import re
from web_page import WebPage


def split_to_words(text):
    # 入力: 'すべて自分のほうへ'
    # 出力: tuple(['すべて', '自分', 'の', 'ほう', 'へ'])
    tagger = MeCab.Tagger('mecabrc')  # 別のTaggerを使ってもいい
    mecab_result = tagger.parse(text)
    info_of_words = mecab_result.split('\n')
    words = []
    for info in info_of_words:
        # macabで分けると、文の最後に’’が、その手前に'EOS'が来る
        if info == 'EOS' or info == '':
            break
        info_elems = re.split(u',|\t', info)
        # 名刺、動詞、形容詞のみ用いる
        if info_elems[1] == '名詞' or info_elems[1] == '動詞' or info_elems[1] == '形容詞':
            if info_elems[2] != '数' and info_elems[2] != '非自立' and \
                    info_elems[2] != '接尾' and info_elems[7] != 'する':
                # 6番目に、無活用系の単語が入る。もし6番目が'*'だったら0番目を入れる
                if info_elems[7] == '*':
                    # info_elems[0] => 'ヴァンロッサム\t名詞'
                    words.append(info_elems[0])
                    continue
                words.append(info_elems[7])
    return words


def load_all_html_files():
    pages = []
    for category in constants.CATEGORIES:
        for word in category['words']:
            pages.extend(load_html_files_with_query(word))
    return pages


def load_html_files_with_query(query):
    pages = []
    for i in range(constants.NUM_OF_FETCHED_PAGES):
        with open('%s_%s.html' % (query, str(i)), 'r') as f:
            page = WebPage()
            page.html_body = f.read()
        pages.append(page)
    return pages


def load_html_files():
    # HTMLファイルがあるディレクトリにいる前提で使う
    pages = load_html_files_with_query(constants.QUERY)
    return pages


def go_to_fetched_pages_dir():
    if not os.path.exists(constants.FETCHED_PAGES_DIR_NAME):
        os.mkdir(constants.FETCHED_PAGES_DIR_NAME)
    os.chdir(constants.FETCHED_PAGES_DIR_NAME)


def go_to_docs_dir():
    if not os.path.exists(constants.DOCS_DIR_NAME):
        os.mkdir(constants.DOCS_DIR_NAME)
    os.chdir(constants.DOCS_DIR_NAME)


def go_to_pkl_dir():
    if not os.path.exists(constants.PKL_DIR_NAME):
        os.mkdir(constants.PKL_DIR_NAME)
    os.chdir(constants.PKL_DIR_NAME)


def go_to_parent_dir():
    os.chdir('../')
