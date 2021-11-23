import camelot
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.pyplot import savefig
import io, json
from camelot import utils
import sys
import warnings
warnings.filterwarnings("ignore", category=UserWarning)

# file path global variable
file_path = ""

#get pdf dimensions
def startparser(path):
  file_path = sys.argv[1]

  print(file_path)
  layout, dim = utils.get_page_layout(file_path)

  # read all table
  completeTable = camelot.read_pdf(file_path, flavor="stream")

  # get first column coordinates (to get Y's)
  firstColumnCoordinates = completeTable[0].cols[0]
  firstColumnTable = camelot.read_pdf(file_path, flavor="stream", table_areas=[str(int(firstColumnCoordinates[0])) + "," + str(dim[1]) + "," + str(int(firstColumnCoordinates[1])) + ", 0"])
  yCoords = firstColumnTable[0].rows

  # get week day columns coordinates (to get X's)
  xCoords = []
  dates = completeTable[0].data[1][3:10]
  for i in range(3, 10):
    xCoords.append(completeTable[0].cols[i])
    table = camelot.read_pdf(file_path, flavor="stream", table_areas=[str(int(xCoords[i-3][0])) + "," + str(dim[1]) + "," + str(int(xCoords[i-3][1])) + ", 0"])

  def make_flat(table):
    flatten_table = []
    for i in range(0,len(table[0].data)):
      flatten_table.append(table[0].data[i][0])
    return flatten_table

  #  now we can cross the information to create sub tables
  fig = camelot.plot(completeTable[0], kind='text')

  # xCoords = xCoords[:1] # only for tests, the first four columns and last one are not important
  subTables = []
  total = (len(yCoords) - 1 - 4) * len(xCoords)
  count = 0
  for i in range(4, len(yCoords)-1):
    aux = []
    for j in range(len(xCoords)):
      try:
        count += 1
        print(str(int(count*100/total))+"%")
        tableCoordinate = [str(int(xCoords[j][0])) + ',' + str(int(yCoords[i][0])) + ',' + str(int(xCoords[j][1])) + ',' + str(int(yCoords[i][1]))]
        table = camelot.read_pdf(file_path, flavor="stream", table_areas=tableCoordinate)
        aux.append(make_flat(table))
      except:
        pass
    subTables.append(aux)

  day_names = ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"]

  # generate json
  week = []

  # get columns
  days = list(zip(*subTables))

  for i in range(0,7):
    week.append({
      "date": dates[i],
      "week_day": day_names[i],
      "breakfast": days[i][0:2],
      "lunch": days[i][2:6],
      "dinner": days[i][6:10],
    })

  with open('data.json', 'w', encoding="utf-8") as f:
    f.write(json.dumps(week, ensure_ascii=False, indent=2))

if __name__ == "__main__":
  if(len(sys.argv) < 2):
    sys.exit("Insira o caminho de um arquivo -> python parser.py [path].pdf")
  startparser(sys.argv[1])

