from flask import Flask, render_template, request, redirect, send_file
from scrapper import get_jobs
from scrapper_workopolis import get_jobs_workopolis
from exporter import save_to_file

app = Flask("SuperScrapper")

db_indeed = {}  #fake DB
db_workpolis = {}
db_total = {}
db_value = " "

@app.route("/") 
def home():
    return render_template("main.html")

@app.route("/report")
def report():
    word = request.args.get('word')
    value = request.args.get('value')

    print(word)
    print(value)    

    if value == "option1":
        db_value = "option1"

        if word:
            word = word.lower()

            existingJobs = db_indeed.get(word)
            if existingJobs:
                jobs = existingJobs

            else:
                jobs = get_jobs(word)
                db_indeed[word] = jobs
        else:
            return redirect("/")
        return render_template(
        "report.html", 
        searchingBy=word, 
        resultNumber = len(jobs), jobs=jobs, 
        db_value=db_value  )
    elif value =="option2":
        db_value = "option2"
        if word:
            word = word.lower()
            existingJobs = db_workpolis.get(word)
            if existingJobs:
                jobs = existingJobs

            else:
                jobs = get_jobs_workopolis(word)
                db_workpolis[word] = jobs

        else:
            return redirect("/")        
        return render_template(
        "report.html", 
        searchingBy=word, 
        resultNumber = len(jobs), jobs=jobs, db_value=db_value  )
    else:
        db_value = "option3"
        if word:
            word = word.lower()
            existingJobs = db_total.get(word)
            if existingJobs:
                jobs = existingJobs

            else:
                jobs = get_jobs(word) + get_jobs_workopolis(word)
                db_total[word] = jobs
        else:
            return redirect("/")        
        return render_template(
        "report.html", 
        searchingBy=word, 
        resultNumber = len(jobs), jobs=jobs, db_value=db_value )        


@app.route("/download.csv")
def download():
    try:
        option = request.args.get('file')[:7]
        word = request.args.get('file')[8:]
        word = word.lower()

        print(option)
        print(word)

        if not word:
            raise Exception()
        jobs = {}
        if option == "option1":
            option = "indeed"
            jobs = db_indeed.get(word)   
        elif option == "option2":
            option = "workopolis"
            jobs = db_workpolis.get(word)   
        else:
            option = "indeed+workopolis"
            jobs = db_total.get(word)   
        if not jobs:
            raise Exception()

        save_to_file(jobs, word, option)
        return send_file(f"{word}_jobs_in_ON_from_{option}.csv", as_attachment=True, attachment_filename=f"{word}_jobs_in_ON_from_{option}.csv")
    except:
        return "error"


app.run(host="0.0.0.0")
