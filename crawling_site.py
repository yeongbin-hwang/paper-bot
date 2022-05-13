from ast import keyword
import requests
from bs4 import BeautifulSoup
from basic_types import keyword_list, Conference, pdfError, urlError, Usenix_years, NDSS_years
import re

"""
Usenix
"""

class Usenix(Conference):
  def find_all_papers(self):
    papers = {}
    # get tech sessions
    papers["tech"] = self.find_tech_session()

    # get season papers
    seasons = ["spring", "summer", "fall"]
    for season in seasons:
      self.season = season
      papers[season] = self.find_paper()

    return papers

  # get files that contains the keyword in title.
  def get_files_bytitles(self, titles):
    files = []
    for title in titles:
      if any(keyword in title.text for keyword in keyword_list):
        ref = title.find('a').attrs['href']
        file_name = title.text.strip()
        try:
          file_url, authors = self.find_ref_data(ref)
          files.append({"name" : file_name, "authors": authors, "url" : file_url})
        except (urlError, pdfError):
          continue
    return files

  # find papers in tech session.
  def find_tech_session(self):
    raw = requests.get("https://www.usenix.org/conference/usenixsecurity%d/technical-sessions" % self.year)
    if(raw.status_code == 200):
      print("[Success] tech session, year: 20%d" % self.year)
    elif(raw.status_code == 404):
      print("[Error] tech session, year: 20%d" % self.year)
      return
    
    html = BeautifulSoup(raw.text, "html.parser")
    titles = html.select("h2.node-title.clearfix")

    return self.get_files_bytitles(titles)

  # find papers in season.
  def find_paper(self):
    raw = requests.get("https://www.usenix.org/conference/usenixsecurity%d/%s-accepted-papers" % (self.year, self.season))
    if(raw.status_code == 200):
      print("[Success] year: 20%d season: %s" % (self.year, self.season))
    elif(raw.status_code == 404):
      print("[Error] year: 20%d season: %s" % (self.year, self.season))
      return
    html = BeautifulSoup(raw.text, "html.parser")

    fields = html.select_one("div.field.field-name-field-session-papers > div.field-items")
    print(len(fields))
    titles = fields.select("h2.node-title")

    return self.get_files_bytitles(titles)

  def find_ref_data(self, ref):
    raw = requests.get("https://www.usenix.org" + ref)
    if(raw.status_code == 200):
      print("[Success] url : %s" % ref)
    elif(raw.status_code == 404):
      print("[Error] url : %s" % ref)
      raise urlError
    html = BeautifulSoup(raw.text, "html.parser")

    # ref
    file = html.select_one("div.field-name-field-presentation-pdf span.file")
    if(file == None):
      print("[Error] pdf don't exist : %s" % ref)
      raise pdfError
    file_ref = file.find('a').attrs['href']

    # author
    file = html.select_one("div.field-name-field-paper-people-text div.field-item")
    if(file == None):
      print("[Error] authors don't exist : %s" % ref)
      # todo: fix
      raise pdfError
    authors = file.text

    return file_ref, authors

"""
NDSS
"""
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
        try:
          file_url = self.find_ref_data(ref)
          files.append({"name" : file_name, "url" : file_url})
          continue
        except (urlError, pdfError):
          pass

        # for weird title
        ref_title = re.sub('[\,\:\?\+]', '', title.text.strip())
        ref_title = re.findall('\S+', ref_title)
        ref = "-".join(ref_title).lower()
        try:
          file_url = self.find_ref_data(ref)
          files.append({"name" : file_name, "url" : file_url})
        except (urlError, pdfError):
          continue
    return files

  def find_ref_data(self, ref):
    raw = requests.get("https://www.ndss-symposium.org/ndss-paper/" + ref)
    if(raw.status_code == 200):
      print("[Success] url : %s" % ref)
    elif(raw.status_code == 404):
      print("[Error] url : %s" % ref)
      raise urlError
    
    html = BeautifulSoup(raw.text, "html.parser")
    file = html.select_one("div.content")
    if(file == None):
      print("[Error] pdf don't exist : %s" % ref)
      raise pdfError
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
  year = 18
  #season = "fall"
  for year in [20]:
    usenix = Usenix(year, "fall")
    files = usenix.find_paper()
    #files = usenix.find_all_papers()
    print(files)
  # ndss = NDSS(year, season)
  # files = ndss.find_paper()
  # print(year)
  # print(files)