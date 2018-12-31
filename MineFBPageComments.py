import pandas as pd
import json
from pprint import pprint
import os
import requests
import logging

companyList = pd.read_csv('../../../../../../../../../Data Extract/Fortune 500 2017 - Fortune 500 - ExceptionsReprocessing-Batch9c.csv')

access_token="<your access token string>"

logger = logging.getLogger()

def constructUrl(contentType, variableStr):
   #contentType is either post, comment, or subcomment
   #variableStr is either the company name, post id (for comments), or comment id (for sub comments)
    if contentType == 'post':
        url = 'https://graph.facebook.com/v2.12/'+variableStr+'/feed?fields=message%2C+from%2C+created_time%2C+updated_time&limit=100&access_token='+access_token
    elif contentType == 'comment':
        url = 'https://graph.facebook.com/v2.12/'+variableStr+'/comments?fields=message%2C+created_time%2C+parent%2C+comment_count%2C+like_count&access_token='+access_token
    elif contentType == 'subComment':
        url = 'https://graph.facebook.com/v2.12/'+variableStr+'/comments?fields=message%2C+created_time%2C+parent%2C+comment_count%2C+like_count&access_token='+access_token

    return url

def graphApiRequest(url):
    requestResult = requests.get(url)
    return requestResult

def writeToFile(folderName, fileName, extractedData):
    if not os.path.exists(folderName):
        os.makedirs(folderName)
    f = open(folderName+fileName, "w+")
    #f = open(folderName + fileName, "a+")
    f.write(extractedData.text+"\n")
    f.close()
    return

def getNextPageUrl(folderName, fileName):
    # read file to get the next
    with open(folderName+fileName) as jsonFile:
        jsonData = json.load(jsonFile)

    try:
        nextPageUrl = jsonData["paging"]["next"]
    except KeyError:
        nextPageUrl = 'null'
    return nextPageUrl

# Step 1
def readJsonFile(fileLocationAndName):
    print("===== fileLocationAndName" + fileLocationAndName)
    #with open('../../Data Extract/88-Nike/1-CompanyPost/Nike_posts_page1.json') as json_file:
    with open(fileLocationAndName) as json_file:
        data = json.load(json_file)
        #print(data['data'][2]['message'])

        #companyPostId = data['data'][2]['id']

  
    return data

################ ACTIONS

companyFbName = companyList['FBPage'][0]

for i in range(companyList['FBPage'].size): # Loop through each company in the CSV file list
    #company_post_file_pagenum = 1
    companyFbName = companyList['FBPage'][i]

    # company_post_folder_name = '../../Data Extract/' + str(companyList['Rank'][i]) + '-' + companyFbName + '/1-CompanyPost/'
    # company_post_comment_folder_name = '../../Data Extract/' + str(companyList['Rank'][i]) + '-' + companyFbName + '/1-CompanyPostComment/'

    # DESKTOP LOCAL
    company_post_folder_name = '../../../../../../../../../Data Extract/' + str(
        companyList['Rank'][i]) + '-' + companyFbName + '/1-CompanyPost/'
    company_post_comment_folder_name = '../../../../../../../../../Data Extract/' + str(
        companyList['Rank'][i]) + '-' + companyFbName + '/1-CompanyPostComment/'
    # END - DESKTOP LOCAL

    company_post_json_files = os.listdir(company_post_folder_name)
    num_of_company_post_jsonfiles = len(company_post_json_files)

    for j in range(num_of_company_post_jsonfiles): # Loop through each JSON file (company post files))
        j+=1 # Offset zero array start
        #company_post_json_file = readJsonFile("../../../../../../../../../Data Extract/" + str(companyList['Rank'][i]) + "-" +
          #              companyFbName + "/1-CompanyPost/" + companyFbName + "_posts_page" + str(j) + ".json")

        # LOCAL DESKTOP ONLY
        company_post_json_file = readJsonFile(
            "../../../../../../../../../Data Extract/" + str(companyList['Rank'][i]) + "-" +
            companyFbName + "/1-CompanyPost/" + companyFbName + "_posts_page" + str(j) + ".json")
        # END - LOCAL DESKTOP ONLY

        # Check if there's data file. Sometimes there isn't. It will throw an exception
        try:
            dummy_for_exception = company_post_json_file['data'][2]['id']
        except Exception as e:
            print("EXCEPTION: " + str(e))

        index_of_company_post_in_range = True
        ctr_for_company_post_in_json = 1
        pageNum_for_comments_file = 1

        # The filename that will be created
        company_post_comment_filename = companyFbName + "_posts_comments_post" + str(j)

        while index_of_company_post_in_range: # Loop while there are company post elements in the Json file.
            try:  # Check/Catch message if it is null.
                company_post_comment_id = company_post_json_file['data'][ctr_for_company_post_in_json]['id']
                url = constructUrl("comment", company_post_comment_id)

                while url != 'null':
                    extractedData = graphApiRequest(url)

                    ### FOR VIEWING DURING EXECUTIION:
                    print("company_post_json_file: " + str(companyList['Rank'][i]) + "-" +
                        companyFbName + "/1-CompanyPost/" + companyFbName + "_posts_page" + str(j) + ".json" +
                          ", company_post_comment_folder_name: " + company_post_comment_folder_name + " - Page " + str(pageNum_for_comments_file))
                    #print("### ctr_for_company_post_in_json: " + str(ctr_for_company_post_in_json))

                    writeToFile(company_post_comment_folder_name, company_post_comment_filename+
                                "-"+company_post_comment_id+"_page"+str(pageNum_for_comments_file)+".json", extractedData)
                    nextPageUrl = getNextPageUrl(company_post_comment_folder_name, company_post_comment_filename+
                                "-"+company_post_comment_id+"_page"+str(pageNum_for_comments_file)+".json")
                    url = nextPageUrl
                    pageNum_for_comments_file += 1

                ctr_for_company_post_in_json += 1


            except Exception as e:
                str_e = str(e).replace("'", "") #remove single quotes for if condition string check.
                print("*** EXCEPTION:" + str_e)
                if str_e == "list index out of range":
                    index_of_company_post_in_range = False
                    print("*** Index is now out of range***")
                    ctr_for_company_post_in_json += 1
                elif str_e == "data":
                    #with open('../../Data Extract/Exceptions-Comments.txt', "a") as exceptionFile:
                     #   exceptionFile.write(',' + companyFbName + '- Exception: ' + str_e)

                    # LOCAL DESKTOP ONLY
                    with open('../../../../../../../../../Data Extract/Exceptions-Comments.txt', "a") as exceptionFile:
                        exceptionFile.write(',' + companyFbName + '- Exception: ' + str_e)
                    # END - LOCAL DESKTOP ONLY

                    index_of_company_post_in_range = False
                else:
                    #with open('../../Data Extract/Exceptions-Comments.txt', "a") as exceptionFile:
                     #   exceptionFile.write(',' + companyFbName + '- Exception: ' + str_e)

                    # LOCAL DESKTOP ONLY
                    with open('../../../../../../../../../Data Extract/Exceptions-Comments.txt', "a") as exceptionFile:
                        exceptionFile.write(',' + companyFbName + '- Exception: ' + str_e)
                    # END - LOCAL DESKTOP ONLY

                    index_of_company_post_in_range = False

            #ctr_for_company_post_in_json += 1
        #company_post_file_pagenum += 1

########### ACTIONS






