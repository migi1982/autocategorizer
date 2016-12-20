import requests
import cchardet
import re


class WebPage():
    def __init__(self, url=''):
        self.url = url

    def fetch_html(self):
        try:
            response = requests.get(self.url)
            self.set_html_body_with_cchardet(response)
        except requests.exceptions.ConnectionError:
            self.html_body = ''

    def set_html_body_with_cchardet(self, response):
        encoding_detected_by_cchardet = cchardet.detect(response.content)['encoding']
        response.encoding = encoding_detected_by_cchardet
        self.html_body = response.text

    def scrape_html(self):
        self._remove_html_breaks()
        self._remove_html_scripts()
        self._remove_html_styles()
        self._remove_html_tags()
        self._remove_html_url()
        self._remove_html_nbsp()

    def _remove_html_url(self):
        html_script_pattern = re.compile('https?:\/\/[\w/:%#\$&\?\(\)~\.=\+\-\;]+')
        self.html_body = html_script_pattern.sub(' ', self.html_body)

    def _remove_html_breaks(self):
        html_script_pattern = re.compile('\s')
        self.html_body = html_script_pattern.sub(' ', self.html_body)

    def _remove_html_scripts(self):
        html_script_pattern = re.compile('<script.*?</script>')
        self.html_body = html_script_pattern.sub('', self.html_body)

    def _remove_html_styles(self):
        html_style_pattern = re.compile('<style.*?</style>')
        self.html_body = html_style_pattern.sub('', self.html_body)

    def _remove_html_tags(self):
        html_tag_pattern = re.compile('<.*?>')
        self.html_body = html_tag_pattern.sub('', self.html_body)

    def _remove_html_nbsp(self):
        html_script_pattern = re.compile('\&nbsp;')
        self.html_body = html_script_pattern.sub(' ', self.html_body)
