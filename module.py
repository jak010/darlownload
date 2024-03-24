import re


def get_ytb_initialdata(soup):
    # 정상
    for x in soup.findAll("script"):
        if "ytInitialData" in x.text and len(x.text) > 5000:
            return x.text

def get_ytb_cgf(soup):
    # 정상
    for x in soup.findAll("script"):
        print(x)
        print("\n\n\n")
        # if "ytcfg.set" in x.text and len(x.text) > 5000:
        #     return x.text



def get_urls_from_initialdata(initialdata):
    pattern = r'"videoId":"([\w-]+)"'

    urls = set(re.findall(pattern, initialdata))

    return [x for x in set(urls)]
