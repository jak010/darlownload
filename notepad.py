import requests
from bs4 import BeautifulSoup
from fake_headers import Headers

darlim_url = "https://www.youtube.com/@darlimchannel/videos"

r = requests.get(darlim_url)

soup = BeautifulSoup(r.content, "html.parser")

from module import get_urls_from_initialdata, get_ytb_initialdata, get_ytb_cgf

init_data = get_ytb_initialdata(soup)
# ytf_cfg = get_ytb_cgf(soup)
urls = get_urls_from_initialdata(init_data)

print(init_data)
# print(ytf_cfg)
