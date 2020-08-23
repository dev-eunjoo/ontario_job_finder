import requests
from bs4 import BeautifulSoup

LIMIT = 30

number = 1

def get_last_page(url):
    results = requests.get(url)
    soup = BeautifulSoup(results.text, "html.parser")
    pagination = soup.find("div", {"class": "pagination"})
    links = pagination.find_all('a')
    pages = []
    for link in links[:-1]:
        pages.append(int(link.string))

    max_page = pages[-1]
    return max_page

def extract_job(html, jobsUrl):
    title = html.find("h2", {"class":"title"}).find("a")["title"]
    company = html.find("span", {"class": "company"})

    if company:
        company_anchor = company.find("a")
        if company_anchor is not None:
            company = str(company_anchor.string)
        else:
            company = str(company.string)
        company = company.strip()
    else:
        company = None
    location = html.find("div", {"class": "recJobLoc"})["data-rc-loc"]
    job_id = html["data-jk"]

    return { 
        'title': title, 
        'company' : company, 
        'location': location, 
        'link': f"{jobsUrl}&vjk={job_id}"}

def extract_jobs(last_page, url):
    jobs = []
    for page in range(last_page):
        print(f"Scrapping page {page}")
        jobsUrl = f"{url}&start={(page-1)*10}"
        result = requests.get(f"{jobsUrl}")
        soup = BeautifulSoup(result.text, "html.parser")
        results = soup.find_all("div", {"class": "jobsearch-SerpJobCard"})
        for result in results:
            job = extract_job(result, jobsUrl)
            jobs.append(job)
    return jobs

def get_jobs(word):
    url = f"https://ca.indeed.com/jobs?q={word}&l=ontario&LIMIT={LIMIT}"
    last_page = get_last_page(url)
    jobs = extract_jobs(last_page, url)
    return jobs





