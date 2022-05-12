from ast import keyword
import requests
from bs4 import BeautifulSoup

year = 22
season = "summer"

keyword_list = ["5G", "4G", "LTE", "SIM", "cellular", "Cellular"]

class Usenix:
  def __init__(self, year, season):
    self.year = year
    self.season = season

  def find_paper(self):
    raw = requests.get("https://www.usenix.org/conference/usenixsecurity%d/%s-accepted-papers" % (year, season))
    html = BeautifulSoup(raw.text, "html.parser")

    fields = html.select_one("div.field.field-name-field-session-papers > div.field-items")
    #print(fields)
    #print(len(fields))
    titles = fields.select("h2.node-title")
    #print(titles)
    files = []
    for title in titles:
      if any(keyword in title.text for keyword in keyword_list):
        ref = title.find('a').attrs['href']
        #print(title.text.strip())
        #print(ref)
        file_name = title.text.strip()
        file_url = self.find_ref_data(ref)
        files.append({"name" : file_name, "url" : file_url})
    return files

  def find_ref_data(self, ref):
    raw = requests.get("https://www.usenix.org" + ref)
    html = BeautifulSoup(raw.text, "html.parser")

    file = html.select_one("div.field-name-field-presentation-pdf span.file")
    ref = file.find('a').attrs['href']
    
    return ref

if __name__ == "__main__":
  usenix = Usenix(year, season)
  files = usenix.find_paper()
  print(files)