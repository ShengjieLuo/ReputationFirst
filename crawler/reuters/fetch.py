import requests
from bs4 import BeautifulSoup
import re
import json
from newspaper import Article
import threading

class NewsParser(threading.Thread):

    def __init__(self,source):
        threading.Thread.__init__(self)
        self.source = source

    def _fetch_links(self,url):
        links = []
        r = requests.get(url)
        if r.status_code!=200:
            print(url+":Not Correct Response")
        soup = BeautifulSoup(r.text,"html.parser")
        for link in soup.find_all('a'):
            rawlink = link.get('href')
            if rawlink and re.match("(\S)+://www.reuters.com/article/(\S)+",rawlink):
                links.append(rawlink)
        return links

    def _fetch_data(self,link):
        datum = {}
        article = Article(link)
        try:
            article.download()
        except:
            print(link+": Cannot be download!")
            return datum
        try:       
            article.parse()
        except:
            print(link+": Cannot be parsed!")
            return datum            
        datum["authors"] = article.authors
        datum["date"]    = str(article.publish_date)
        datum["text"]    = str(article.text)
        datum["title"]   = str(article.title)
        return datum
    
    def parse(self,source):
        f = open("data_"+source.split("/")[-1],"w")
        links = self._fetch_links(source)
        count = 0
        for link in links:
            datum = self._fetch_data(link)
            if len(datum)==0:
                continue
            f.write(json.dumps(datum)+'\n')
            print("Fetch news from " + source + " : "+str(count)+"/"+str(len(links)))
            count += 1
        f.close()

    def run(self):
        self.parse(self.source)
             
def _get_targets():
    f = open("sourcelist")
    lines = f.readlines()
    f.close()
    result = []
    for line in lines:
        if line:
            result.append(line.strip())
    return result

def real_main():
    sources = _get_targets()
    threads = []
    for source in sources:
        threads.append(NewsParser(source))
    for t in threads:
        t.start()
    for t in threads:
        t.join()

if __name__=="__main__":
    real_main()
