import math, json, sys, re
import requests
from bs4 import BeautifulSoup as bs

# (cloudcover, rain, snow)
weatherTypeLookup = {
  "helder": (0, 0, 0),
  # Clouds
  "lichtbewolkt": (0.25, 0, 0),
  "bewolkt": (0.25, 0, 0),
  "halfbewolkt": (0.5, 0, 0),
  "zwaarbewolkt": (0.75, 0, 0),
  "betrokken": (1, 0, 0),
  # Rain
  "motregen": (0.75, 0.25, 0),
  "lichte regen": (0.75, 0.5, 0),
  "regen en motregen": (0.75, 0.5, 0),
  "matige regen": (1, 0.75, 0),
  "regen": (1, 1, 0),
  # Snow
  "motsneeuw": (0.75, 0, 0.25),
  "lichte sneeuw": (0.75, 0, 0.5),
  "matige sneeuw": (1, 0, 0.75),
  "sneeuw": (1, 0, 1),
  # Misc
  "motregen of motsneeuw": (0.75, 0.25, 0.25),
  "mistbanken": (0.75, 0, 0),
  "mist": (1, 0, 0),
  "ijzel": (0, 0, 0),
  "nevel": (0.25, 0, 0),
  "heiig": (0.25, 0, 0)
}

cdLookup = ('N', 'O', 'Z', 'W')

def angle_avg(angles):
  return math.atan2(sum(map(math.sin, angles)), sum(map(math.cos, angles))) % (math.pi * 2)

# Cardinal direction name -> cd float
def cdn2cdf(cdn: str):
  if len(cdn) == 1:
    return (cdLookup.index(cdn) / 4) * math.pi * 2
  elif len(cdn) == 2:
    return angle_avg(map(cdn2cdf, cdn))
  elif len(cdn) == 3:
    cdns = [cdn[0], cdn[1:]]
    return angle_avg(list(map(cdn2cdf, cdns)))

def txt2f(txt: str):
  return float(txt.replace(',', '.'))


res = requests.get(sys.argv[1])
if res.status_code != 200:
  sys.exit("Status code " + res.status_code)

table = bs(res.text, 'html.parser').find('table')
if table == None:
  sys.exit("No table found, right page?")

rows = table.findAll('tr')
if len(rows) < 2: # Heading + units
  sys.exit("Table doesn't have the right heading, right table?")

# Check units
units = rows[1].findAll('td')
if list(map(lambda e: e.get_text(), units)) != ['\xa0', 'T (C)', 'U (%)', 'P (hPa)', 'Richting', 'Snelheid (km/h)', '\xa0']:
  sys.exit("Table heading doesn't have the right units, right table?")

data = {}

for row in rows[2:]:
  cols = row.findAll('td')
  colTxt = [e.get_text() for e in cols]
  if (len(cols) != 7):
    sys.exit("Table heading doesn't have the right units, right table?")
    sys.exit(1)
  city = str.strip(cols[0].get_text())
  rowData = {}
  rowData["cityCode"] = int(cols[0].find("city")["code"])
  if (colTxt[1] != '-'):
    rowData["t"] = txt2f(colTxt[1])
  if (colTxt[2] != '-'):
    rowData["rh"] = int(colTxt[2])
  if (colTxt[3] != '-'):
    rowData["pa"] = txt2f(colTxt[3])
  if (colTxt[4] != '-'):
    rowData["cdn"] = colTxt[4]
    rowData["cdf"] = round(cdn2cdf(colTxt[4]), 3)
  if (colTxt[5] != '-'):
    rowData["vkh"] = txt2f(colTxt[5])
  if (colTxt[6] != '-'):
    rowData["desc"] = colTxt[6]
    estCond = weatherTypeLookup[colTxt[6]]
    rowData["estc"] = estCond[0]
    rowData["estr"] = estCond[1]
    rowData["ests"] = estCond[2]

  data[city] = rowData

print(json.dumps(data))
