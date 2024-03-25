import re
from typing import List

from ytb.api import YtbRequestor
from ytb.scrapper import YTBScrapper


class DarlimVideoCollector:
    CHANNEL_ID = "UColC6Y1j99rqJE7TyE6TBrA"

    def __init__(self, scrapper: YTBScrapper, requestor: YtbRequestor):
        self.scrapper = scrapper
        self.requestor = requestor

    def get_urls_from_ytb_initialdata(self) -> List[str]:
        pattern = r'"videoId":"([\w-]+)"'

        urls = set()
        for url in set(re.findall(pattern, self.scrapper.get_ytb_initialdata)):
            urls.add(self.scrapper.convert_to_ytblink(url))

        return list(urls)

    def get_urls_from_continuation(self) -> List[str]:
        urls = self.requestor.browse_with_continuation_token(
            channel_id=self.CHANNEL_ID,
            continuation_token=self.scrapper.get_continuation_token
        )
        return urls

    def get_urls_without_continuation(self) -> List[str]:
        urls = self.requestor.browse_without_continuation_token(channel_id=self.CHANNEL_ID)
        return urls

    def execute(self):
        urls = []
        urls.extend(self.get_urls_from_ytb_initialdata())
        urls.extend(self.get_urls_from_continuation())
        urls.extend(self.get_urls_without_continuation())

        return list(set(urls))
