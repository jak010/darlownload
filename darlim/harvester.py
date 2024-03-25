import requests
from bs4 import BeautifulSoup


class DarlimVideoDataHarvester:

    def __init__(self, video_url):
        self.video_url = video_url

    def execute(self):
        r = requests.get(self.video_url)
        if r.status_code == 200:
            soup = BeautifulSoup(r.content, "html.parser")
            return {
                "title": soup.find("meta", property="og:title")['content'],
                "datepublished": soup.find("meta", {"itemprop": "datePublished"})['content']
            }
