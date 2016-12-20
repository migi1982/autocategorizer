from bing_api import Bing
import os
import constants
from web_page import WebPage

if __name__ == '__main__':
    bing = Bing()
    if not os.path.exists(constants.FETCHED_PAGES_DIR_NAME):
        os.mkdir(constants.FETCHED_PAGES_DIR_NAME)
    os.chdir(constants.FETCHED_PAGES_DIR_NAME)
    for category in constants.CATEGORIES:
        for word in category['words']:
            print('%s: %s' % (category['category'], word))
            results = bing.web_search(query=word,
                                      num_of_results=constants.NUM_OF_FETCHED_PAGES,
                                      keys=['Url'])
            for i, result in enumerate(results):
                page = WebPage(result['Url'])
                page.fetch_html()
                page.scrape_html()
                f = open('%s_%s.html' % (word, str(i)), 'w')
                f.write(page.html_body)
                f.close()
