from ast import keyword
import requests
from bs4 import BeautifulSoup
from basic_types import keyword_list, Conference
import re

class Usenix(Conference):
  def find_paper(self):
    raw = requests.get("https://www.usenix.org/conference/usenixsecurity%d/%s-accepted-papers" % (self.year, self.season))
    html = BeautifulSoup(raw.text, "html.parser")

    fields = html.select_one("div.field.field-name-field-session-papers > div.field-items")
    #print(fields)
    print(len(fields))
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
  
class NDSS(Conference):
  def find_paper(self):
    raw = requests.get("https://www.ndss-symposium.org/ndss20%d/accepted-papers/" % (self.year))
    html = BeautifulSoup(raw.text, "html.parser")

    titles = html.select("div.content p > strong")
    #print(fields)
    #print(len(fields))
    files = []
    for title in titles:
      if any(keyword in title.text for keyword in keyword_list):
        # remove weird char
        ref_title = re.sub('[^a-zA-Z0-9_\.\s-]+',  '', title.text.strip())
        ref_title = re.findall('[\w]+', ref_title)
        ref = "-".join(ref_title).lower()
        file_name = title.text.strip()
        file_url = self.find_ref_data(ref)

        # for weird title
        if(file_url == None or file_url == []):
          ref_title = re.sub('[\,\:\?\+]', '', title.text.strip())
          ref_title = re.findall('\S+', ref_title)
          ref = "-".join(ref_title).lower()
          file_url = self.find_ref_data(ref)

        files.append({"name" : file_name, "url" : file_url})
    return files

  def find_ref_data(self, ref):
    raw = requests.get("https://www.ndss-symposium.org/ndss-paper/" + ref)
    html = BeautifulSoup(raw.text, "html.parser")

    file = html.select_one("div.content")
    print(file)
    ref = file.find('a').attrs['href']
    return ref

class SnP(Conference):
  def find_paper(self):
    return
class CCS(Conference):
  def find_paper(self):
    return

class Wisec(Conference):
  def find_paper(self):
    return

class Mobycom(Conference):
  def find_paper(self):
    return

if __name__ == "__main__":
  year = 21
  season = "fall"
  """
  usenix = Usenix(year, season)
  files = usenix.find_paper()
  """
  ndss = NDSS(year, season)
  files = ndss.find_paper()
  print(files)