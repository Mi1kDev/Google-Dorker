import urllib.parse
import requests
import re
import os
from bs4 import BeautifulSoup

class Dorker:
    def __init__(self, query, num, **kwaargs):
        self.host = "https://www.google.com"
        self.baseUrl = "https://www.google.com/search?"
        self.query = query
        self.num = num
        self.finalUrl = None
        self.params = {
            "as_eqp": "Results must include this query in the same word order",
            "as_oq": "Results must include one or more words in this string.",
            "as_eq": "Results must NOT include these words.",
            "as_filetype": "Returns results that end in the given extension",
            "as_sitesearch": "Limits results to specified site.",
            "as_rq": "Finds sites related to your given url",
            "as_lq": "Finds sites that link to a given url",
        }
        self.foundUrls = []
        self.formatUrl(**kwaargs)

    def formatUrl(self, **kwaargs):
        params = {"q": self.query, "num": self.num}
        for key, value in kwaargs.items():
            if key in self.params:
                params[key] = value 
        params = urllib.parse.urlencode(params)
        self.finalUrl = self.baseUrl + params
    
    def paramList(self):
        for key, value in self.params.items():
            print("[+] {k}: {v}".format(k=key, v=value))
    
    def findResults(self):
        r = requests.get(self.finalUrl)
        soup = BeautifulSoup(r.content, "html.parser")
        results = []
        for link in soup.find_all("a", href=True):
            if not "http" in link["href"][0:4] and "search?q={q}".format(q=self.query.replace(" ", "+")) in link["href"]:
                results.append(self.host + link["href"])
        
        self.foundUrls = results
    
    def exportToTextFile(self):
        if len(self.foundUrls) <= 0:
            print("[!] Either no urls were found, or you have not run the find results function")
            return None
        else:
            self.createFolder("Text Files")
            with open(os.path.join("Text Files", self.query+".txt"), "w") as q:
                q.write("\n".join(self.foundUrls) + "\n")
    
    def createFolder(self, name):
        if not os.path.isdir(name):
            os.mkdir(name)
    
    def saveLinks(self):
        if len(self.foundUrls) <= 0:
            print("[!] Either no urls were found, or you have not run the find results function")
            return None
        else:
            i = 0
            for link in self.foundUrls:
                r = requests.get(link)
                if "content-disposition" in r.headers:  
                    headers = r.headers["content-disposition"]
                    filename = re.findall("filename=(.+)", headers)[0]
                    if filename is None:
                        filename = str(i)
                        i += 1
                else:
                    filename = str(i)
                    i += 1
                dirName = self.query+" Files"
                self.createFolder(dirName)
                with open(os.path.join(dirName, filename), "wb") as f:
                    f.write(r.content)