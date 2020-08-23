import csv
def save_to_file(jobs, word, option):
    print("I am in ")
    file = open(f"{word}_jobs_in_ON_from_{option}.csv", "w", -1,"utf-8", newline='')
    writer = csv.writer(file)
    writer.writerow(['number', 'title', 'company', 'location', 'link'])
    i = 0
    while i < len(jobs):
       jobList = list(jobs[i].values())
       writer.writerow([i+1, jobs[i]['title'], jobs[i]['company'], jobs[i]['location'], jobs[i]['link']])
       i += 1
    return 
