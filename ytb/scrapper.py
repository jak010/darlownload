import re
from functools import cached_property

import requests
from bs4 import BeautifulSoup
from fake_headers import Headers


class YTBScrapper:
    session = requests.session()
    header = Headers(browser="chrome", os='win').generate()

    def __init__(self, target_url: str):
        self.target_url: str = target_url

    @cached_property
    def soup(self) -> BeautifulSoup:
        resp = self.session.get(self.target_url, headers=self.header)
        if resp.status_code == 200:
            return BeautifulSoup(resp.text, "html.parser")

    @cached_property
    def get_ytb_initialdata(self):
        """ JavaScript의  ytInitialData 얻기 """
        _guess_exceed_number = 5000
        for x in self.soup.findAll("script"):
            if "ytInitialData" in x.text and len(x.text) > _guess_exceed_number:
                return x.text

    @cached_property
    def get_continuation_token(self):
        """ continuationCommand Token 얻기 """
        pattern = r'"continuationCommand"\s*:\s*{"token"\s*:\s*"[^"]{1000,}"'

        match = re.search(pattern, self.get_ytb_initialdata)

        continuation_token = match.group(0).split(":")[-1]
        return continuation_token.replace("\"", "")

    def convert_to_ytblink(self, text):
        return f"/watch?v={text}"
