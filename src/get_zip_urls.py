import requests
from bs4 import BeautifulSoup
import os


class ZipLinks():

    def __init__(self):
        self.themes_url = 'https://theme.typora.io'

    def _request(self, url):
        req = requests.get(url)
        req.raise_for_status()
        resp = req.text
        return resp

    def get_theme_names(self, html_resp):
        soup = BeautifulSoup(html_resp, 'html.parser')
        link_wraps = soup.find('div', attrs={'id': 'content'}).find_all('a', class_='item-inner')
        rel_paths = {}
        for a_elem in link_wraps:
            theme_name = a_elem.find('div', class_='item-name').text
            rel_paths[theme_name] = a_elem.get('href')
        return rel_paths

    def get_archive_paths(self, themepath_dict):
        for name, path in themepath_dict.items():
            theme_url = self.themes_url + path
            page_resp = self._request(theme_url)
            soup = BeautifulSoup(page_resp, 'html.parser')
            buttons = soup.find_all('a', class_='btn')
            for button in buttons:
                if button.text == 'Download':
                    themepath_dict[name] = button.get('href')
                elif button.find('span'):
                    themepath_dict[name] = None

            if themepath_dict[name]:
                releases_paths = {}
                # Expunge Query String
                url_only = themepath_dict[name].split('?')[0]
                # Raw CSS or ZIP
                if len(url_only.split('.')[-1]) <= 3:
                    exec_str = 'cmd /c "http --download {0}"'.format(themepath_dict[name])
                    os.system(exec_str)
                else:
                    releases_paths[name] = themepath_dict[name]
        return releases_paths


if __name__=='__main__':
    f = ZipLinks()
    themes = f.get_theme_names(f._request(f.themes_url))
    tpd = f.get_archive_paths(themes)
    peint(tpd)

