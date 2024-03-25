import json
from typing import List

import requests


class YtbRequestor:

    def __init__(self, session=None, header=None):
        self.session: requests.Session = session
        self.header = header

    def browse_with_continuation_token(self, channel_id: str, continuation_token: str) -> List[str]:
        resp = self.session.post(
            "https://www.youtube.com/youtubei/v1/browse?prettyPrint=false",
            cookies=self.session.cookies.get_dict(),
            headers=self.header,
            data=json.dumps({
                "context": {"client": {"clientName": "WEB", "clientVersion": "2.20240322.01.00"}},
                "browseId": channel_id,
                "continuation": continuation_token
            })
        )
        if resp.status_code == 200:
            response_data = resp.json()

            # xxx: May be Entry ...
            continuation_items = response_data["onResponseReceivedActions"][0]["appendContinuationItemsAction"]["continuationItems"]

            urls = set()
            for x in range(len(continuation_items)):
                try:
                    urls.add(
                        continuation_items[x]["richItemRenderer"]["content"]["videoRenderer"]["navigationEndpoint"]["commandMetadata"][
                            "webCommandMetadata"]["url"]
                    )
                except Exception:
                    pass
            return list(urls)

    def browse_without_continuation_token(self, channel_id: str) -> List[str]:
        resp = self.session.post(
            "https://www.youtube.com/youtubei/v1/browse?prettyPrint=false",
            cookies=self.session.cookies.get_dict(),
            headers=self.header,
            data=json.dumps({
                "context": {"client": {"clientName": "WEB", "clientVersion": "2.20240322.01.00"}},
                "browseId": channel_id,
            })
        )
        if resp.status_code == 200:
            response_data = resp.json()

            urls = set()
            # May Entry ...
            for i in range(0, 5):
                for x in range(30):
                    try:
                        urls.add(
                            response_data['contents']['twoColumnBrowseResultsRenderer']['tabs'][0]['tabRenderer']['content']['sectionListRenderer']
                            ['contents'][i]['itemSectionRenderer']['contents'][0]['shelfRenderer']['content']['horizontalListRenderer']['items'][x]
                            ['gridVideoRenderer']['navigationEndpoint']['commandMetadata']['webCommandMetadata']['url']
                        )
                    except:
                        pass
            return list(urls)
