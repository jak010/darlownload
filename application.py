import os

import yt_dlp

from darlim.collector import DarlimVideoCollector
from darlim.harvester import DarlimVideoDataHarvester
from ytb.api import YtbRequestor
from ytb.scrapper import YTBScrapper


class DarlimVideoDownloaderApplication:
    save_path = "./downloads"

    scrapper = YTBScrapper(target_url="https://www.youtube.com/@darlimchannel/videos")
    requestor = YtbRequestor(session=scrapper.session, header=scrapper.header)

    def __init__(self):

        if not os.path.isdir(self.save_path):
            os.mkdir(self.save_path)

        self.download_urls = DarlimVideoCollector(scrapper=self.scrapper, requestor=self.requestor).execute()

        self.download_options = {
            'outtmpl': './downloads/%(title)s.mp3',  # 다운로드 경로 및 파일명 설정
        }

    def execute(self):
        watch_urls = [f"https://www.youtube.com{download_url}" for download_url in self.download_urls]

        for watch_url in watch_urls:
            metadata = DarlimVideoDataHarvester(watch_url).execute()

            if "Cover" in metadata['title']:
                try:
                    with yt_dlp.YoutubeDL(self.download_options) as ydl:
                        ydl.download([watch_url])
                except Exception as e:
                    raise e


if __name__ == '__main__':
    DarlimVideoDownloaderApplication().execute()
