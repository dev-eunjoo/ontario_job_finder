import requests
import math
from bs4 import BeautifulSoup

LIMIT = 30


def get_last_page(url):
    #links =[]
    result = requests.get(url)
    soup = BeautifulSoup(result.text, "html.parser")
    pages = soup.find("span", {"class": "ResultText-numTotal"}).get_text(strip=True)

    last_page = int(pages)/20
    if(last_page % 20 != 0):
        last_page = math.floor((last_page+1))
    
    print("last page: " , last_page-1)
    return int(last_page-1)

def extract_job(oneJob, jobsUrl):
    title = oneJob.find("h2")["title"]

    company = oneJob.find("div", {"class": "JobCard-company"}).get_text(strip=True)

    location = oneJob.find("span", {"class": "JobCard-location"}).get_text(strip=True).strip(" — ")

    job_id = oneJob["data-jobkey"]
    return {"title" : title, 
    'company': company, 
    'location': location, 
    'link':  f"{jobsUrl}&job={job_id}"}


def extract_jobs(last_page, url):
    jobs = []
    for page in range(last_page):
        print(f"Scrapping page {page}")
        jobsUrl = f"{url}&lg=en&pn={page+1}"
        result = requests.get(f"{jobsUrl}")
        soup = BeautifulSoup(result.text, "html.parser")
        results = soup.find_all("article", {"class": "JobCard"})

        for oneJob in results:
            job = extract_job(oneJob, jobsUrl)
            jobs.append(job)
    return jobs




def get_jobs_workopolis(word):
    url = f"https://www.workopolis.com/jobsearch/find-jobs?ak={word}&l=Ontario"
    last_page = get_last_page(url)
    jobs = extract_jobs(last_page, url)
    return jobs

