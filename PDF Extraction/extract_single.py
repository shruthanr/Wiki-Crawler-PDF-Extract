####################################################################################################################
# Extracts the content of one pdf document
# Pass the url of the document directly (--url="...") or the row number in the Google Sheet (--row_num=10)

# Output Format
# A json file named outfile.json with three fields: pdf-url, page-url and pdf-content
# pdf-content is a list of strings. Each string contains the content of one page. (Hence len(list) == No. of pages)
# Each page is stored as a separate string, assuming that having it this way  might be useful for further processing
#####################################################################################################################

import requests
from pdf2image import convert_from_bytes, convert_from_path
import pytesseract
from bs4 import BeautifulSoup
import json
import pandas as pd
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("-u", "--url", help = "URL of the pdf")
parser.add_argument("-n", "--row_num", help = "Row number of pdf in the Google Sheet")

args = parser.parse_args()

if not (args.url or args.row_num):
    print("ERROR: Please pass in the url of the document or the row number of the document in the Google Sheet")
    exit()

if (args.url):
    url = args.url

if (args.row_num):
    row_num = int(args.row_num)
    data = pd.read_csv("Data Engineer Task.csv", header=None)
    if (row_num <= 0 or row_num > len(data)):
        print(f"ERROR: Row number out of bounds. Please enter a value between 1 and {len(data)}")
        exit()
    url = data.iloc[row_num-1][0]

results = []
def get_content(url):
    headers = requests.head(url).headers
    ## Type A
    if headers['Content-Type'] == "application/pdf":
        content = []
        res = requests.get(url)
        images = convert_from_bytes(res.content)
        
        for image_idx, image in enumerate(images):
            if (image_idx >= 100):
                break
            print(image_idx, end=" ")
            text = pytesseract.image_to_string(image, lang="hin")
            if (len(text) > 0):
                content.append(text)
        result = [{
            "page-url": url,
            "pdf-url" : url,
            "pdf-content": content 
        }]
    
    ## Type B
    else:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        links = soup.find_all('a')
        i = 0
        filenames = []
        s = set()
        for link in links:
            if ('.pdf' in link.get('href', []) and link.get('href') not in s):
                s.add(link.get('href'))
                i += 1
                print("Downloading file: ", i)

                # base link hardcoded based on observation from dataset
                current_link = "https://archive.org" + link.get('href')
                response = requests.get(current_link)

                currname = "pdf"+str(i)+".pdf"
                pdf = open(currname, 'wb')
                filenames.append((currname, current_link))
                pdf.write(response.content)
                pdf.close()
                print("File ", i, " downloaded")
        
        result = []
        for (filename, link) in filenames:
            images = convert_from_path("./" + filename)
            
            content = []
            
            for image_idx, image in enumerate(images):
                if (image_idx >= 100):
                    break
                print(image_idx, end=" ")
                text = pytesseract.image_to_string(image, lang="hin")
                content.append(text)
            result.append({
                "page-url": url,
                "pdf-url" : url,
                "pdf-content": content
            })
            
    return result

data = pd.read_csv("Data Engineer Task.csv", header=None)


result = (get_content(url))

out_file = open("outfile.json", "w")
json.dump(result, out_file)
out_file.close()