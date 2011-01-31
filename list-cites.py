from sys import argv
from urllib import quote_plus
import urllib2
import re,sys

info_finder = re.compile('<h3.*?>(<span.*?>.*?</span>)?<a.*?>(.*?)<')
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

    headers = {'User-agent': 'Mozilla/5.0 (Windows; U; Windows NT 6.0; en-US) AppleWebKit/525.13 (KHTML, like Gecko) Chrome/0.2.149.29 Safari/525.13'};
    #headers = {'User-Agent': 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US;rv:1.9.0.4) Gecko/2008102920 Firefox/3.0.4'}

    req = urllib2.Request(page_url,None,headers)
    superline = ""
    for line in urllib2.urlopen(req):
        superline += line

    fh = open('tester.html','w')
    fh.write(superline)
    fh.close()

    matches = []
    titles = []
    t_point = 0
    info_finder
    for (ignore,match) in info_finder.findall(superline):
        titles.append(match.strip().replace('&hellip;','').strip())

    for match in cite_finder.findall(superline):
        if t_point < len(titles) and len(titles[t_point]) > 2:
            matches.append((titles[t_point],int(match)))
            t_point+=1

    return matches
    


#scholar_addr = "http://scholar.google.com/scholar?hl=en&btnG=Search"
scholar_addr = "http://scholar.google.co.uk/scholar?hl=en&btnG=Search&as_sdt=2000&as_ylo=&as_vis=0"

search_term = argv[1]
bibtex_loc = argv[2]

cite_pairs = doSearch(scholar_addr + "&q=" + quote_plus(search_term))

c_ref = ''
pairs = []
mtitlematch = {}
for line in open(bibtex_loc,'r'):
    if line.strip().startswith('@'):
        c_ref = line.strip()[line.strip().index('{')+1:-1]
    elif line.strip().lower().startswith('title'):
        l_line = line.strip().lower()
        title = l_line[l_line.index('{')+1:-2]
        while title.startswith('{'):
            title = title[1:]
        for mtitle in cite_pairs:
            if title.startswith(mtitle):                
                print "MATCH",title,"AND",mtitle
                mtitlematch[mtitle] = True
                done_already = False
                for p in pairs:
                    if p[2] == title:
                        done_already = True

                if not done_already:
                    pairs.append((c_ref,cite_pairs[mtitle],title))



def pair_sort(a,b):
    if a[1] > b[1]:
        return -1
    else:
        return 1

fh = open(argv[3],'w')
pairs.sort(pair_sort)
for pair in pairs[:min(5,len(pairs))]:
    print pair[0],"CITES:",pair[1]
    fh.write(pair[0] + "\n")
fh.close()

