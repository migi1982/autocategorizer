# girlschannel-autocategorizer

ナイーブベイズによるトピックの自動ジャンル分け

## 参考元

http://qiita.com/katryo/items/6a2266ffafb7efa9a46c

## mecabについての注意

[mecab-ipadic-NEologd](https://github.com/neologd/mecab-ipadic-neologd/blob/master/README.ja.md)を辞書として用いる

>mecab-ipadic-NEologd は、多数のWeb上の言語資源から得た新語を追加することでカスタマイズした MeCab 用のシステム辞書です。

`mecab`コマンドでこの辞書を使った自然言語解析がデフォルトでできるように予め設定しておく。

システム辞書の変更には`/usr/local/etc/mecabrc`を書き換える。

## 使い方

## 必要なパッケージ

```
pip install requests
pip install cchardet
pip install mecab-python3
pip install sklearn
pip install numpy
pip install scipy
```

### constants.py

NUM_OF_FETCHED_PAGESに教師に使うウェブページ数を入れる。
(ジャンル数×ページ数が取得するページの数になる)

### fetch_web_pages.py

ウェブページの取得。
この中でスクレイピングも行う。

### set_tfidf_with_sklearn_to_fetched_pages.py

取得したウェブページからtfidf値を計算。
結果を`tfidf_result.pkl`に、
ベクタライザを`tfidf_vectorizer.pkl`に保存。

### train_tfidf.py

tfidfを最終的にジャンル分類に使える形のワードバッグにして`tfidf_bag.pkl`に保存。


### calc_similarity_with_tfidf.py

自分で文章を打ってジャンル分けを試したい時はこちら。

### calc_category_from_topics.py

特定のテキストファイルの各行についてジャンル分けしたい時はこちら。
結果は`categorized_topics.txt`に保存。