import urllib.parse
import requests
import re
import os
import datetime
from bs4 import BeautifulSoup

class Dorker:
    def __init__(self, query, num, **kwaargs):
        #initializes the class with its base attributes
        self.host = "https://www.google.com" #this is the url appended to the front of found links
        self.baseUrl = "https://www.google.com/search?" #this is the base search url from which the final url will extend
        self.query = query
        self.num = num
        self.finalUrl = None #the final url is set to None at first as we do not yet know what value it will be
        #these are all the optional paramters that can be used to help narrow down search results
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
        #creates the final url from which we will scrape links from during the initialization
        self.formatUrl(**kwaargs)
    
    #this function simply logs any errors found during the runtime of the program using this class
    def logError(self, errorMsg):
        if not os.path.isfile("Errors.log"):
            with open("Errors.log", "w") as e:
                e.write("[!] At {t} an error occurred. The error message is as follows.\n{e}\n".format(t=datetime.datetime.now(), e=errorMsg))
        else:
            with open("Errors.log", "a") as e:
                e.write("[!] At {t} an error occurred. The error message is as follows.\n{e}\n".format(t=datetime.datetime.now(), e=errorMsg))

    #this function will format the search url based on the given optional paramters and their values
    def formatUrl(self, **kwaargs):
        params = {"q": self.query, "num": self.num}
        for key, value in kwaargs.items():
            if key in self.params:
                params[key] = value 
        params = urllib.parse.urlencode(params)
        self.finalUrl = self.baseUrl + params
    
    #this function will simply list all the paramters and what they do
    def paramList(self):
        for key, value in self.params.items():
            print("[+] {k}: {v}".format(k=key, v=value))
    
    def findResults(self):
        try:
            #makes a request to the properly formatted url
            r = requests.get(self.finalUrl)
            #creates a BeautifulSoup object from the results
            soup = BeautifulSoup(r.content, "html.parser")
            results = []
            #finds all urls on the page
            for link in soup.find_all("a", href=True):
                #limits the urls that are appended to meaningful ones
                if not "http" in link["href"][0:4] and "search?q={q}".format(q=self.query.replace(" ", "+")) in link["href"]:
                    results.append(self.host + link["href"])
            
            self.foundUrls = results
        except Exception as e:
            self.logError(e)
    
    def exportToTextFile(self):
        if len(self.foundUrls) <= 0:
            print("[!] Either no urls were found, or you have not run the find results function")
            return None
        else:
            try:
                #creates a folder to save the text files if there is none
                self.createFolder("Text Files")
                #writes the found urls into the text file line by lines
                with open(os.path.join("Text Files", self.query+".txt"), "w") as q:
                    q.write("\n".join(self.foundUrls) + "\n")
            except Exception as e:
                self.logError(e)
    
    def createFolder(self, name):
        if not os.path.isdir(name):
            os.mkdir(name)
    
    def saveLinks(self):
        if len(self.foundUrls) <= 0:
            print("[!] Either no urls were found, or you have not run the find results function")
            return None
        else:
            try:
                i = 0
                #downloads from each link that was found and stores the data in a file
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
            except Exception as e:
                self.logError(e)