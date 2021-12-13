import requests
from bs4 import BeautifulSoup
from csv import writer
import os
import sys
import time

# extracting data from the web

user = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.93 Safari/537.36"}
header = ['Title', 'Description']

# Gets the list of jobs from the main page
def extractJobListPage(jobTitle, page):
    """"Takes the variable JobTitle (i.e Data Analyst) and page, returns html page of the requested page"""
    # replaces the white spaces with "+" 
    job = jobTitle.replace(" ", "+")
    url = f"https://www.indeed.com/jobs?q={job}&start={page*10}"
    result = requests.get(url, user)
    if (result.status_code != 200):
        #if the page is not accessable then it will just go onto next page
        print("This page was not accessable")
        # avoid getting errors
        pass
    else:
        page = BeautifulSoup(result.content, "html.parser")
        return page

# Extracts the link from the page
def extractLink(page):
    """Take the html page, returns all the job link in the page"""
    try:
        jobList = []
        # Find the div tag by the given id
        tableTag = page.find('table', id = 'resultsBody')
        divTag = tableTag.find('div', id = 'mosaic-provider-jobcards')
        # "href=True" will ensure that link in href is present 
        for link in divTag.find_all('a', class_ = 'tapItem', href=True):
            cleanLink = link.get('href')
            jobList.append("https://indeed.com"+ cleanLink)
        return jobList
    except:
        print(f"This error occured - {sys.exc_info()[0]}")
        pass
        

def extractPage(url):
    """Take an url and returns html of the page"""
    """Helper function for extractRequirement"""
    result = requests.get(url, user)
    if (result.status_code != 200):
        print("This page was not accessable")
        pass
    else:
        page = BeautifulSoup(result.content, "html.parser")
        return page

# CSV writer
def writerCSV(newData, fileName):
    """if the file does not exists then create one and add the newData into it"""
    """Helper function for extractRequirement"""
    """as this function is called again the loop then if the file exists the if statement will be false
    and use the code inside the else which will append the newData"""
    if (os.path.exists(fileName) == False):
        with open(fileName, 'w', encoding='utf-8', newline='') as f:
            writerFile = writer(f)
            # write the header
            writerFile.writerow(header)
            writerFile.writerow(newData)
            f.close()

    else:
        with open(fileName, 'a', encoding='utf-8', newline='') as f:
            # take the csv file and pass to the writer function
            writerFile = writer(f)
            # adds the new data
            writerFile.writerow(newData)
            f.close()
            
            
# gets the skill required for the job
def extractRequirement(jobList, fileName):
    """Takes a List of job links and file name for each job, store the description in the csv file"""
    if (jobList is not None):
        for n in jobList:
            jobPage = extractPage(n)
            # store the title of the job and separator argument adds space between the removed tag
            title = jobPage.find('title').get_text(separator=' ')
            # store the job description
            jobDes = jobPage.find('div', id = 'jobDescriptionText').get_text(separator=' ')
            temp = [title, jobDes]
            writerCSV(temp, fileName)
            # Added a delay to scrape whole page
            time.sleep(20)
    else:
        print("There was no link on this page")
        pass