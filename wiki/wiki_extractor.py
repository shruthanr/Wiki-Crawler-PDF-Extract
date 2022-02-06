import requests
import argparse
import wikipedia
import json

parser = argparse.ArgumentParser()
parser.add_argument("-k", "--keyword", help = "Keyword to search", default="Wikipedia")
parser.add_argument("-n", "--num_urls", help = "Number of results", default=5)
parser.add_argument("-o", "--output", help = "Name of output file", default="out.json")

args = parser.parse_args()


SEARCHPAGE = args.keyword
NUM_URLS = int(args.num_urls)
OUT_FILE = args.output


S = requests.Session()

URL = "https://en.wikipedia.org/w/api.php"


PARAMS = {
    "action": "query",
    "format": "json",
    "list": "search",
    "srsearch": SEARCHPAGE,
    "srlimit": NUM_URLS
}

R = S.get(url=URL, params=PARAMS)
DATA = R.json()

result_list = []
i = 1
for result in DATA['query']['search']:
    print(f"Processing result {i} of {NUM_URLS}")
    i += 1
    pageid = result['pageid']
    page = wikipedia.page(pageid=pageid)
    content = page.content[:page.content.find("\n")]
    result_list.append({
        "url" : page.url,
        "paragraph" : content
    })


out_file = open(OUT_FILE, "w")
json.dump(result_list, out_file)
out_file.close()


