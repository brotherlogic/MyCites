from sys import argv
from urllib import quote_plus
import urllib2
import re

info_finder = re.compile('<h3 class="r"><a.*?>(.*?)<')
cite_finder = re.compile('Cited by (.*?)<')

def doSearch(search_url):

    results = extract_page(search_url)
    
    for i in range (10,100,10):
        results.extend(extract_page(search_url + "&start=" + `i`))

    res_map = {}
    for res in results:
        res_map[res[0].lower()] = res[1]

    return res_map

def extract_page(page_url):

    headers = {'User-Agent': 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US;rv:1.9.0.4) Gecko/2008102920 Firefox/3.0.4'}

    req = urllib2.Request(page_url,None,headers)
    superline = ""
    for line in urllib2.urlopen(req):
        superline += line

    matches = []
    titles = []
    t_point = 0
    info_finder
    for match in info_finder.findall(superline):
        titles.append(match.strip())

    for match in cite_finder.findall(superline):
        if t_point < len(titles):
            matches.append((titles[t_point],int(match)))
            t_point+=1
    
    return matches
    


scholar_addr = "http://scholar.google.com/scholar?hl=en&btnG=Search"

search_term = argv[1]
bibtex_loc = argv[2]

cite_pairs = doSearch(scholar_addr + "&q=" + quote_plus(search_term))

c_ref = ''
pairs = []
for line in open(bibtex_loc,'r'):
    if line.strip().startswith('@'):
        c_ref = line.strip()[line.strip().index('{')+1:-1]
    elif line.strip().lower().startswith('title'):
        l_line = line.strip().lower()
        title = l_line[l_line.index('{')+1:-2]
        if title in cite_pairs:
            #print title,c_ref,cite_pairs[title]

            done_already = False
            for p in pairs:
                if p[2] == title:
                    done_already = True

            if not done_already:
                pairs.append((c_ref,cite_pairs[title],title))


def pair_sort(a,b):
    if a[1] > b[1]:
        return -1
    else:
        return 1

pairs.sort(pair_sort)
for pair in pairs[:min(5,len(pairs))]:
    print pair[0]

