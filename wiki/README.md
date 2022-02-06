# Wikipedia Extractor
A Python program to find N (user-defined) pages that are relevant to a keyword.

### Arguments
- `--keyword`: Keyword relevant to which pages are to be found. Default: Wikipedia
- `--num_urls`: Number of results to load. Default: 5
- `--output`: Name of output file. Default: out.json

### Example Run
`python3 wiki_extractor.py --keyword="NDTV" --num_urls=10 --output="out.json"`

### Requirements
- `requests` library - `pip install requests` 
- `wikipedia` library - `pip install wikipedia`
- `argparse` library - `pip install argparse`

### Approach
The Page IDs of the N most relevant Wikipedia pages are obtained by making an API call using the `requests` library to the `MediaWiki Action API` with Wikipedia as the endpoint. Then the wikipedia library is used to get the content of the respective pages.

NOTE: The wikipedia library also provides a Search function to search for pages given a keyword. However, this function fails for some keywords like `"NDTV"` and `"CNN"` (specifically for the most relevant link for these keywords). Hence it is not used here. 

