""" IDEA 3 : With Request Session """
import json
from urllib import parse
from urllib.parse import quote
from bs4 import BeautifulSoup
import requests
from fake_headers import Headers
import re

fake_header = Headers(browser="chrome", os='win')
headers = fake_header.generate()

r = requests.session()

resp = r.get(
    url="https://www.youtube.com/@darlimchannel/videos",
    headers=headers
)
from module import get_urls_from_initialdata, get_ytb_initialdata, get_ytb_cgf

soup = BeautifulSoup(resp.content, "html.parser")

init_data = get_ytb_initialdata(soup)
# print(init_data)
# 정규 표현식 패턴
pattern = r'"continuationCommand"\s*:\s*{"token"\s*:\s*"[^"]{1000,}"'

# 정규 표현식 검사
match = re.search(pattern, init_data)

continuation_token = match.group(0).split(":")[-1]
continuation_token = continuation_token.replace("\"", "")

save_urls = set()

# 추가 데이터 요청 부분

resp2 = r.post(
    "https://www.youtube.com/youtubei/v1/browse?prettyPrint=false",
    cookies=resp.cookies.get_dict(),
    data=json.dumps({
        "context": {"client": {"clientName": "WEB", "clientVersion": "2.20240322.01.00"}},
        "browseId": "UColC6Y1j99rqJE7TyE6TBrA",

    })
)

d = resp2.json()
# print(d)
for i in range(1,3):
    for x in range(12):
        url = d["contents"]["twoColumnBrowseResultsRenderer"]["tabs"][0]["tabRenderer"]["content"]["sectionListRenderer"]["contents"][i][
            "itemSectionRenderer"]["contents"][0]["shelfRenderer"]["content"]["horizontalListRenderer"]["items"][x]["gridVideoRenderer"][
            "navigationEndpoint"]["commandMetadata"]["webCommandMetadata"]["url"]
        save_urls.add(url)

print(len(save_urls))
for x in save_urls:
    print(x)

# contiunation token controll
resp3 = r.post(
    "https://www.youtube.com/youtubei/v1/browse?prettyPrint=false",
    cookies=resp2.cookies.get_dict(),
    data=json.dumps({
        "context": {"client": {"clientName": "WEB", "clientVersion": "2.20240322.01.00"}},
        "browseId": "UColC6Y1j99rqJE7TyE6TBrA",
        "continuation": continuation_token
    })
)
d = resp3.json()

for x in range(30):
    url = d["onResponseReceivedActions"][0]["appendContinuationItemsAction"]["continuationItems"][x]["richItemRenderer"]["content"]["videoRenderer"][
        "navigationEndpoint"]["commandMetadata"]["webCommandMetadata"]["url"]
    save_urls.add(url)


print(len(save_urls))
for x in save_urls:
    print(x)