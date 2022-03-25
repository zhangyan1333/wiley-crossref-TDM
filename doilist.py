#wiley 311
#query item
import requests
def dois():
    crossrefAPI = "https://api.crossref.org/"
    memberID_url = "members/311"
    query_url = "/works?query="
    search_item = "(waste OR by-product OR byproduct) AND ('valorisation' OR 'valorization' OR 'conversion' OR 'recycling') "
    doi_url = crossrefAPI + memberID_url + query_url + search_item + '&rows=500'
    content = requests.get(doi_url)
    data = content.json()
    doilist = []
    for i in range(500):
        doi = data['message']['items'][i]['DOI']
        doilist.append(doi + '\n')
    with open('doilist.txt', 'w') as f:
        f.writelines(doilist)

    return doilist
    # cr = Crossref()
    # cr.members(ids = 311, works = True)
    # x = cr.works(query= 'byproduct')
    #不考虑用crossref这个函数了，一个request url请求就可以完成

doires = dois()

