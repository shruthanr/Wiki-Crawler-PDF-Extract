####################################################################################################################
# Extracts the content from all the pdfs in the Google Sheet. 
# Limits to 100 pages per document

# Output Format
# A json file named pdf_extract.json which is a list of objects with three fields: pdf-url, page-url and pdf-content
# pdf-content is a list of strings. Each string contains the content of one page. (Hence len(list) == No. of pages)
# Each page is stored as a separate string, assuming that having it this way  might be useful for further processing
#####################################################################################################################

import requests
from pdf2image import convert_from_bytes, convert_from_path
import pytesseract
from bs4 import BeautifulSoup
import json
import pandas as pd


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

results = []
for i in range(len(data)):
    print(f"Row {i+1}")
    results.append(get_content(data.iloc[i][0]))

out_file = open("pdf_extract.json", "w")
json.dump(results, out_file)
out_file.close()