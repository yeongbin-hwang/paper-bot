conference_list = ["Usenix", "IEEE Symposium on Security and Privacy", "CCS", "NDSS", "Wisec"]
keyword_list = ["5G", "4G", "LTE", "SIM", "cellular", "Cellular", "phone", "Phone"]

NDSS_years = list(range(12, 23))
Usenix_years = list(range(12, 23))

class Conference:
  def __init__(self, year, season=""):
    self.year = year
    self.season = season

  def find_paper(self):
    return
    
  def find_ref_data(self, ref):
    return

class urlError(Exception):
  pass

class pdfError(Exception):
  pass