# -*- coding: utf-8 -*-
import urllib
import requests
import sys
import my_api_keys


class Bing(object):
    # 同じ階層にmy_api_keys.pyというファイルを作り、そこにBING_API_KEYを書き込んでおく。
    # my_api_keys.pyはgitignoreしておくこと。
    def __init__(self, api_key=my_api_keys.BING_API_KEY):
        self.api_key = api_key

    def web_search(self, query, num_of_results, keys=["Url"], skip=0):
        # keysには'ID','Title','Description','DisplayUrl','Url'が入りうる
        # 基本になるURL
        url = 'https://api.datamarket.azure.com/Bing/Search/Web?'
        # 一回で返ってくる最大数
        max_num = 50
        params = {
            "Query": "'{0}'".format(query),
            "Market": "'ja-JP'",
            "Adult": "'Off'"
        }
        # フォーマットはjsonで受け取る
        request_url = url + urllib.parse.urlencode(params) + "&$format=json"
        results = []

        # 最大数でAPIを叩く繰り返す回数
        repeat = int((num_of_results - skip) / max_num)
        remainder = (num_of_results - skip) % max_num

        # 最大数でAPIを叩くのを繰り返す
        for i in range(repeat):
            result = self._hit_api(request_url, max_num, max_num * i, keys)
            results.extend(result)
        # 残り
        if remainder:
            result = self._hit_api(request_url, remainder, max_num * repeat, keys)
            results.extend(result)

        return results

    def related_queries(self, query, keys=["Title"]):
        # keysには'ID','Title','BaseUrl'が入りうる
        # 基本になるURL
        url = 'https://api.datamarket.azure.com/Bing/Search/RelatedSearch?'
        params = {
            "Query": "'{0}'".format(query),
            "Market": "'ja-JP'",
            "Adult": "'Off'"
        }
        # フォーマットはjsonで受け取る
        request_url = url + urllib.parse.urlencode(params) + "&$format=json"
        results = self._hit_api(request_url, 50, 0, keys)
        return results

    def _hit_api(self, request_url, top, skip, keys):
        # APIを叩くための最終的なURL
        final_url = "{0}&$top={1}&$skip={2}".format(request_url, top, skip)
        response = requests.get(final_url,
                                auth=(self.api_key, self.api_key),
                                headers={'User-Agent': 'My API Robot'}).json()
        results = []
        # 返ってきたもののうち指定された情報を取得する
        for item in response["d"]["results"]:
            result = {}
            for key in keys:
                result[key] = item[key]
            results.append(result)
        return results


if __name__ == '__main__':
    # bing_api.pyを単独で使うと、入力した語で50件検索して結果を表示するツールになる
    for query in sys.stdin:
        bing = Bing()
        results = bing.web_search(query=query, num_of_results=50, keys=["Title", "Url"])
        print(results)
