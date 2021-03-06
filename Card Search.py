import json
import requests

## WHAT ARE YOU SEARCHING

searchTerm = "Angel"


## GET NAME SEARCH RESULTS FROM SCRYFALL IN LIST FORM

api_url = "https://api.scryfall.com/cards/search?q="+searchTerm+"+legal%3Avintage"
response =  requests.get(api_url)
responseData = response.json()['data']

while response.json()['has_more']:
    nextPageUri = response.json()['next_page']
    responseNext = requests.get(nextPageUri)
    responseDataNext = responseNext.json()['data']
    responseData += responseDataNext
    response = responseNext

reqResults = []
for item in responseData:
    name = item['name']
    reqResults.append(item['name'])

reqCount = len(reqResults)
print(reqCount)


#READ LOCAL MTGJSON FILE AND FILTER INVALID ELEMENTS

#### place the path to your local mtg JSON file in the next line

with open(r"AtomicCards.json", "r", encoding='utf-8') as read_file:
    rawData = json.load(read_file)

rawCardData = dict(rawData['data'])
cardDict = {}

for c in list(rawCardData.keys()):
    try:
        if not rawCardData[c][0]['legalities']['vintage']:
            continue
    except KeyError:
        continue
    else:
        cardDict[c] = c

cardNames = list(cardDict.keys())



# SEARCH THROUGH MODIFIED LOCAL LIST

myResults = []
myCount = 0

for n in cardNames:
    if searchTerm.lower() in n.lower():
        myResults.append(n)
        myCount+=1

print(myCount)



# COMPARE THE SEARCH RESULTS

#### may need to switch the order depending on which is larger

for r in reqResults:
    if r not in myResults:
        print(r)


# TO VIEW SPECIFIC RAW CARD DATA

# print(rawCardData['#####Card Name Here#####'])
