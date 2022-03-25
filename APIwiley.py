import io
import requests
import sys
from urllib.parse import quote_plus
#from habanero import Crossref

#key = 'your key'

def downloader(key):
    # Base URL of the Wiley API
    base_url = "https://api.wiley.com/onlinelibrary/tdm/v1/articles/"

    # Build request
    headers = {'Wiley-TDM-Client-Token': key}

    with open('doilist.txt') as f:
        # doilist = [line.strip() for line in f]
        for doi in f:
            doi = doi.strip()
            url = base_url + quote_plus(doi)
            r = requests.get(url, allow_redirects=True, headers=headers)
            if r.status_code != 200:
                if r.status_code == 403:
                    print("Download Failed (403): Unauthorized. Check that your API key is correct.")
                    #print("Download Failed (403): Unauthorized. Check that your API key is correct.", file=sys.stderr)
                elif r.status_code == 404:
                    print("Download Failed (404): DOI not found.")
                else:
                    print("Download Failed (http status {0})".format(r.status_code))
            else:
                    #name the pdf using DOI, replacing "/" with "_"
                    filename = doi.replace("/","_") + ".pdf"
                    print("downloaded", filename, file=sys.stderr)
                    with open(filename, "wb") as fp:
                        fp.write(r.content)

downloader(key)