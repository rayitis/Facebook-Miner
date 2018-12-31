import pandas as pd
import json
from pprint import pprint
import os
import requests

# Load company list
companyList = pd.read_csv('../../../../../../../../../Data Extract/Fortune 500 2017 - Fortune 500 - ExceptionsReprocessing-Batch9.csv')

def constructUrl(contentType, variableStr):
   #contentType is either post, comment, or subcomment
   #variableStr is either the company name, post id (for comments), or comment id (for sub comments)
    if contentType == 'post':
        url = 'https://graph.facebook.com/v2.12/'+variableStr+'/feed?fields=message%2C+from%2C+created_time%2C+updated_time&limit=100&access_token=<your access token string>'
    elif contentType == 'comment':
        url = 'https://graph.facebook.com/v2.12/15087023444_10156012418158445/comments?fields=message%2C+created_time%2C+parent%2C+comment_count%2C+like_count&access_token=<your access token string>'
    elif contentType == 'subComment':
        url = 'https://graph.facebook.com/v2.12/10156012418158445_630377377297948/comments?fields=message%2C+created_time%2C+parent%2C+comment_count%2C+like_count&access_token=<your access token string>'

    return url

def graphApiRequest(url):
    requestResult = requests.get(url)
    return requestResult

def writeToFile(folderName, fileName, extractedData):
    if not os.path.exists(folderName):
        os.makedirs(folderName)
    f = open(folderName+fileName, "w+")
    f.write(extractedData.text)
    f.close()
    return

def getNextPageUrl(folderName, fileName):
    # read file to get the next
    with open(folderName+fileName) as jsonFile:
        jsonData = json.load(jsonFile)
    #pprint(jsonData)
    #print(jsonData["data"][0]["message"])
    #print(jsonData["paging"]["next"])

    try:
        nextPageUrl = jsonData["paging"]["next"]
    except KeyError:
        nextPageUrl = 'null'
    return nextPageUrl

################ ACTIONS
companyFbName = companyList['FBPage'][0]

for i in range(companyList['FBPage'].size):
    pageNum = 0
    companyFbName = companyList['FBPage'][i]
    #companyNum += 1
    folderName = '../../../../../../../../../Data Extract/' + str(companyList['Rank'][i]) + '-' + companyFbName + '/1-CompanyPost/'
    url = constructUrl('post', companyFbName)

    while url != 'null':
        #print "We're on time %d" % (x)
        pageNum += 1
        fileName = companyFbName+"_posts_page"+str(pageNum)+".json"
        extractedData = graphApiRequest(url)
        writeToFile(folderName, fileName, extractedData)
        nextPageUrl = getNextPageUrl(folderName, fileName)
        url = nextPageUrl
        print(companyFbName + ' page '+ str(pageNum) + ': '+ url)
        if url == 'null' and pageNum == 1:
            with open('../../../../../../../../../Data Extract/Exceptions.txt', "a") as exceptionFile:
                exceptionFile.write(',' + companyFbName)

########### ACTIONS






